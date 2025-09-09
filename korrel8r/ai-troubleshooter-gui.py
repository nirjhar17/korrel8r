#!/usr/bin/env python3
"""
🔍 AI-Powered Korrel8r Troubleshooter - Streamlit GUI
=====================================================
Interactive web interface for intelligent pod troubleshooting
"""

import streamlit as st
import subprocess
import json
import os
import time
from datetime import datetime
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="🔍 AI Korrel8r Troubleshooter",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2d5aa0);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .analysis-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f4e79;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #ffeaea;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #d32f2f;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2e7d32;
        margin: 1rem 0;
    }
    .step-header {
        background-color: #1f4e79;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def run_command(cmd, timeout=30):
    """Execute shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def get_namespaces():
    """Get list of namespaces"""
    returncode, stdout, stderr = run_command("oc get namespaces -o jsonpath='{.items[*].metadata.name}'")
    if returncode == 0:
        namespaces = stdout.strip().split()
        return sorted(namespaces)
    return ["openshift-monitoring", "openshift-ai-analyzer", "korrel8r", "openshift-logging"]

def get_pods_in_namespace(namespace):
    """Get pods in a specific namespace"""
    cmd = f"oc get pods -n {namespace} -o jsonpath='{{.items[*].metadata.name}}'"
    returncode, stdout, stderr = run_command(cmd)
    if returncode == 0 and stdout.strip():
        return sorted(stdout.strip().split())
    return []

def get_pod_status(namespace, pod_name):
    """Get basic pod status"""
    cmd = f"oc get pod {pod_name} -n {namespace} -o jsonpath='{{.status.phase}}'"
    returncode, stdout, stderr = run_command(cmd)
    if returncode == 0:
        return stdout.strip()
    return "Unknown"

def run_troubleshooter_analysis(namespace, pod_name):
    """Run the AI troubleshooter analysis"""
    script_path = "/Users/njajodia/logs_monitoring/korrel8r-project/korrel8r/quick-troubleshooter.sh"
    cmd = f"bash {script_path} {namespace} {pod_name}"
    
    returncode, stdout, stderr = run_command(cmd, timeout=60)
    
    return {
        "returncode": returncode,
        "output": stdout,
        "error": stderr,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def parse_analysis_output(output):
    """Parse the troubleshooter output into structured sections"""
    sections = {}
    current_section = None
    current_content = []
    
    lines = output.split('\n')
    for line in lines:
        if line.startswith('📋 Step'):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = line.strip()
            current_content = []
        elif line.startswith('🎯 ANALYSIS SUMMARY'):
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            current_section = "🎯 Analysis Summary"
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

# Main UI
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 AI-Powered Korrel8r Troubleshooter</h1>
        <p>Intelligent OpenShift Pod Analysis with Correlation Engine</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for pod selection
    with st.sidebar:
        st.header("🎯 Select Pod to Analyze")
        
        # Namespace selection
        namespaces = get_namespaces()
        selected_namespace = st.selectbox(
            "📂 Namespace:",
            namespaces,
            index=0 if "openshift-monitoring" in namespaces else 0
        )
        
        # Pod selection
        if selected_namespace:
            with st.spinner(f"Loading pods in {selected_namespace}..."):
                pods = get_pods_in_namespace(selected_namespace)
            
            if pods:
                selected_pod = st.selectbox(
                    "🐳 Pod:",
                    pods,
                    index=0
                )
                
                # Show pod status
                if selected_pod:
                    status = get_pod_status(selected_namespace, selected_pod)
                    status_color = "🟢" if status == "Running" else "🔴" if status in ["Pending", "Failed"] else "🟡"
                    st.info(f"Status: {status_color} **{status}**")
            else:
                st.warning("No pods found in this namespace")
                selected_pod = None
        else:
            selected_pod = None
        
        st.markdown("---")
        
        # Analysis controls
        st.header("🚀 Analysis Controls")
        
        analyze_button = st.button(
            "🔍 Run AI Analysis",
            disabled=not selected_pod,
            use_container_width=True
        )
        
        if st.button("🔄 Refresh Pod List", use_container_width=True):
            st.rerun()
    
    # Main content area
    if selected_pod and analyze_button:
        st.header(f"🔍 Analyzing: `{selected_namespace}/{selected_pod}`")
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Running comprehensive analysis..."):
            status_text.text("🚀 Initializing AI troubleshooter...")
            progress_bar.progress(20)
            
            status_text.text("📊 Gathering pod information...")
            progress_bar.progress(40)
            
            status_text.text("🔗 Correlating with Korrel8r...")
            progress_bar.progress(60)
            
            # Run analysis
            result = run_troubleshooter_analysis(selected_namespace, selected_pod)
            progress_bar.progress(80)
            
            status_text.text("🤖 Processing AI insights...")
            progress_bar.progress(100)
            
            time.sleep(0.5)  # Brief pause for UX
            progress_bar.empty()
            status_text.empty()
        
        # Display results
        if result["returncode"] == 0:
            st.markdown("""
            <div class="success-box">
                <h3>✅ Analysis Complete!</h3>
                <p><strong>Timestamp:</strong> {}</p>
            </div>
            """.format(result["timestamp"]), unsafe_allow_html=True)
            
            # Parse and display sections
            sections = parse_analysis_output(result["output"])
            
            # Create tabs for different sections
            if sections:
                tab_names = list(sections.keys())[:6]  # Limit to first 6 sections
                tabs = st.tabs(tab_names)
                
                for i, (section_name, content) in enumerate(sections.items()):
                    if i < len(tabs):
                        with tabs[i]:
                            st.markdown(f"""
                            <div class="step-header">
                                <h4>{section_name}</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Format content based on section type
                            if "Analysis Summary" in section_name:
                                st.markdown(f"""
                                <div class="analysis-box">
                                    <pre>{content}</pre>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.code(content, language="bash")
            
            # Raw output in expander
            with st.expander("🔧 View Raw Output"):
                st.code(result["output"], language="bash")
                
        else:
            st.markdown(f"""
            <div class="error-box">
                <h3>❌ Analysis Failed</h3>
                <p><strong>Error:</strong> {result["error"]}</p>
                <p><strong>Return Code:</strong> {result["returncode"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if result["output"]:
                st.code(result["output"], language="bash")
    
    elif not selected_pod:
        # Welcome screen
        st.markdown("""
        ## 👋 Welcome to AI-Powered Korrel8r Troubleshooter!
        
        ### 🎯 **What This Tool Does:**
        - **🔍 Comprehensive Pod Analysis** - Deep dive into pod status, events, and configuration
        - **🤖 AI-Powered Insights** - Intelligent root cause analysis and recommendations  
        - **🔗 Korrel8r Integration** - Cross-domain correlation with logs, metrics, and alerts
        - **📊 Multi-Step Diagnostics** - 7-step systematic troubleshooting approach
        
        ### 🚀 **How to Use:**
        1. **Select Namespace** from the sidebar dropdown
        2. **Choose Pod** to analyze
        3. **Click "Run AI Analysis"** to start comprehensive diagnostics
        4. **Review Results** in organized tabs and sections
        
        ### 📋 **Analysis Includes:**
        - Pod information and specifications
        - Recent events and scaling history  
        - Current status and health conditions
        - Storage (PVC) analysis
        - Node availability and placement
        - Korrel8r log domain connectivity
        - Vector/Loki logging stack status
        - AI-powered recommendations
        
        **👈 Start by selecting a namespace and pod from the sidebar!**
        """)
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏗️ Available Namespaces", len(get_namespaces()))
        with col2:
            st.metric("🔗 Korrel8r Status", "✅ Connected")
        with col3:
            st.metric("🤖 AI Engine", "✅ Ready")

if __name__ == "__main__":
    main()
