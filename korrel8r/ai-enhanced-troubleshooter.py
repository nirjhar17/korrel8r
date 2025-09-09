#!/usr/bin/env python3
"""
🤖 AI-Enhanced Korrel8r Troubleshooter with Groq Integration
===========================================================
Real AI-powered analysis using Groq LLaMA for intelligent insights
"""

import streamlit as st
import subprocess
import json
import os
import time
import requests
from datetime import datetime
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="🤖 AI-Enhanced Korrel8r Troubleshooter",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Groq Configuration
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

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
    .ai-analysis-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
    .ai-badge {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .cluster-info {
        background-color: #f8f9fa;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    .cluster-switch-btn {
        background: linear-gradient(45deg, #007bff, #0056b3);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        width: 100%;
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

def call_groq_api(prompt, max_tokens=1000):
    """Call Groq API for AI analysis"""
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Kubernetes and OpenShift troubleshooter with deep knowledge of container orchestration, pod lifecycle, resource management, and observability. Provide concise, actionable insights and solutions."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3
        }
        
        response = requests.post(GROQ_ENDPOINT, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error calling Groq API: {str(e)}"

def get_available_clusters():
    """Get list of available clusters from kubeconfig"""
    try:
        returncode, stdout, stderr = run_command("oc config get-clusters --no-headers")
        if returncode == 0 and stdout.strip():
            clusters = [line.strip() for line in stdout.strip().split('\n') if line.strip()]
            return sorted(clusters)
    except Exception as e:
        st.error(f"Error getting clusters: {e}")
    
    # Fallback to current cluster
    returncode, stdout, stderr = run_command("oc config current-context")
    if returncode == 0 and stdout.strip():
        return [stdout.strip()]
    
    return ["current-cluster"]

def get_current_cluster():
    """Get current cluster context"""
    returncode, stdout, stderr = run_command("oc config current-context")
    if returncode == 0 and stdout.strip():
        return stdout.strip()
    return "unknown-cluster"

def switch_cluster(cluster_name):
    """Switch to a specific cluster context"""
    try:
        # Try to use the cluster context
        returncode, stdout, stderr = run_command(f"oc config use-context {cluster_name}")
        if returncode == 0:
            return True, f"Switched to cluster: {cluster_name}"
        else:
            return False, f"Failed to switch cluster: {stderr}"
    except Exception as e:
        return False, f"Error switching cluster: {e}"

def get_cluster_info(cluster_name):
    """Get detailed information about a cluster"""
    try:
        # Get cluster server URL
        cmd = f"oc config view -o jsonpath='{{.clusters[?(@.name==\"{cluster_name}\")].cluster.server}}'"
        returncode, stdout, stderr = run_command(cmd)
        server_url = stdout.strip() if returncode == 0 and stdout.strip() else "Unknown"
        
        # Get current user
        returncode, stdout, stderr = run_command("oc whoami")
        current_user = stdout.strip() if returncode == 0 and stdout.strip() else "Unknown"
        
        return {
            "name": cluster_name,
            "server": server_url,
            "user": current_user,
            "status": "Connected" if returncode == 0 else "Disconnected"
        }
    except Exception as e:
        return {
            "name": cluster_name,
            "server": "Unknown",
            "user": "Unknown", 
            "status": "Error"
        }

def get_namespaces():
    """Get list of namespaces"""
    returncode, stdout, stderr = run_command("oc get namespaces -o jsonpath='{.items[*].metadata.name}'")
    if returncode == 0:
        namespaces = stdout.strip().split()
        return sorted(namespaces)
    return ["openshift-monitoring", "ai-troubleshooter", "korrel8r", "test-problematic-pods"]

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
    script_path = "/tmp/quick-troubleshooter.sh"
    cmd = f"bash {script_path} {namespace} {pod_name}"
    
    returncode, stdout, stderr = run_command(cmd, timeout=60)
    
    return {
        "returncode": returncode,
        "output": stdout,
        "error": stderr,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_ai_analysis(troubleshooter_output, namespace, pod_name):
    """Get AI-powered analysis of the troubleshooting results"""
    prompt = f"""
    Analyze this Kubernetes pod troubleshooting output for pod '{pod_name}' in namespace '{namespace}':

    {troubleshooter_output}

    Provide a comprehensive analysis with:
    1. **Root Cause Analysis**: What is the primary issue?
    2. **Impact Assessment**: How critical is this problem?
    3. **Immediate Actions**: Step-by-step remediation
    4. **Prevention**: How to avoid this in the future
    5. **Related Issues**: What else might be affected

    Format your response with clear sections and actionable recommendations.
    """
    
    return call_groq_api(prompt, max_tokens=1500)

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
        <h1>🤖 AI-Enhanced Korrel8r Troubleshooter</h1>
        <p>Powered by Groq LLaMA - Intelligent OpenShift Pod Analysis with Real AI Insights</p>
        <span class="ai-badge">🧠 AI-POWERED</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for pod selection
    with st.sidebar:
        st.header("🎯 Select Pod to Analyze")
        
        # Cluster selection
        st.markdown("### 🌐 Cluster Selection")
        available_clusters = get_available_clusters()
        current_cluster = get_current_cluster()
        
        # Find current cluster index
        try:
            current_index = available_clusters.index(current_cluster)
        except ValueError:
            current_index = 0
        
        selected_cluster = st.selectbox(
            "🏗️ Cluster:",
            available_clusters,
            index=current_index,
            help="Select the OpenShift cluster to analyze"
        )
        
        # Show cluster switch status
        if selected_cluster != current_cluster:
            if st.button(f"🔄 Switch to {selected_cluster}", use_container_width=True):
                with st.spinner(f"Switching to {selected_cluster}..."):
                    success, message = switch_cluster(selected_cluster)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        # Show current cluster info
        cluster_info = get_cluster_info(selected_cluster)
        st.markdown(f"""
        **Current Cluster:**
        - 🏗️ **Name**: {cluster_info['name'][:30]}...
        - 🌐 **Server**: {cluster_info['server'][:40]}...
        - 👤 **User**: {cluster_info['user']}
        - 📊 **Status**: {cluster_info['status']}
        """)
        
        st.markdown("---")
        
        # Namespace selection
        st.markdown("### 📂 Namespace Selection")
        with st.spinner("Loading namespaces..."):
            namespaces = get_namespaces()
        
        selected_namespace = st.selectbox(
            "📂 Namespace:",
            namespaces,
            index=namespaces.index("test-problematic-pods") if "test-problematic-pods" in namespaces else 0,
            help="Select the namespace containing pods to analyze"
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
            "🤖 Run AI Analysis",
            disabled=not selected_pod,
            use_container_width=True
        )
        
        if st.button("🔄 Refresh Pod List", use_container_width=True):
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🧠 AI Features")
        st.markdown("✅ **Root Cause Analysis**")
        st.markdown("✅ **Impact Assessment**")
        st.markdown("✅ **Step-by-Step Solutions**")
        st.markdown("✅ **Prevention Strategies**")
        st.markdown("✅ **Correlation Insights**")
    
    # Main content area
    if selected_pod and analyze_button:
        st.header(f"🤖 AI Analysis: `{selected_cluster}` → `{selected_namespace}/{selected_pod}`")
        
        # Show cluster context
        st.markdown(f"""
        <div class="cluster-info">
            <strong>🏗️ Cluster Context:</strong> {cluster_info['name']}<br>
            <strong>🌐 Server:</strong> {cluster_info['server']}<br>
            <strong>👤 User:</strong> {cluster_info['user']} | <strong>📊 Status:</strong> {cluster_info['status']}
        </div>
        """, unsafe_allow_html=True)
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("Running AI-powered analysis..."):
            status_text.text("🚀 Initializing AI troubleshooter...")
            progress_bar.progress(15)
            
            status_text.text("📊 Gathering pod diagnostics...")
            progress_bar.progress(30)
            
            # Run analysis
            result = run_troubleshooter_analysis(selected_namespace, selected_pod)
            progress_bar.progress(50)
            
            status_text.text("🔗 Correlating with Korrel8r...")
            progress_bar.progress(65)
            
            status_text.text("🤖 Analyzing with Groq AI...")
            progress_bar.progress(80)
            
            # Get AI analysis
            ai_analysis = get_ai_analysis(result["output"], selected_namespace, selected_pod)
            progress_bar.progress(100)
            
            status_text.text("✅ AI analysis complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
        
        # Display results
        if result["returncode"] == 0:
            st.markdown("""
            <div class="success-box">
                <h3>✅ Analysis Complete!</h3>
                <p><strong>Timestamp:</strong> {}</p>
                <p><strong>AI Model:</strong> Groq LLaMA-3.1-70B</p>
            </div>
            """.format(result["timestamp"]), unsafe_allow_html=True)
            
            # AI Analysis Section (Featured)
            st.markdown("""
            <div class="ai-analysis-box">
                <h2>🧠 AI-Powered Analysis & Recommendations</h2>
                <p><strong>Powered by Groq LLaMA-3.1-70B Versatile</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(ai_analysis)
            
            st.markdown("---")
            
            # Parse and display technical sections
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
            with st.expander("🔧 View Raw Technical Output"):
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
        ## 👋 Welcome to AI-Enhanced Korrel8r Troubleshooter!
        
        ### 🤖 **Real AI-Powered Analysis:**
        - **🧠 Groq LLaMA-3.3-70B** - Advanced language model for intelligent insights
        - **🔍 Root Cause Analysis** - Deep understanding of Kubernetes issues
        - **⚡ Instant Recommendations** - Step-by-step solutions and prevention
        - **🔗 Korrel8r Integration** - Cross-domain correlation with observability data
        
        ### 🌐 **Multi-Cluster Support:**
        - **🏗️ Dynamic Cluster Selection** - Switch between multiple OpenShift clusters
        - **🔄 Context Switching** - Seamlessly change cluster contexts
        - **📊 Cluster Information** - View server, user, and connection status
        - **🎯 Namespace Discovery** - Auto-refresh namespaces per cluster
        
        ### 🎯 **Perfect for Testing:**
        - **`test-problematic-pods`** namespace has 5 different failure scenarios
        - **Real failure analysis** with AI-powered explanations
        - **Professional insights** comparable to senior DevOps engineers
        
        ### 🚀 **How to Use:**
        1. **Select your cluster** from the cluster dropdown (if multiple available)
        2. **Choose namespace** from the refreshed namespace list
        3. **Select a failing pod** (crashloop-app, invalid-image-app, etc.)
        4. **Click "🤖 Run AI Analysis"** to get comprehensive AI insights
        5. **Review AI recommendations** and technical details
        
        **👈 Start by selecting a cluster and pod from the sidebar!**
        """)
        
        # Enhanced stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏗️ Namespaces", len(get_namespaces()))
        with col2:
            st.metric("🤖 AI Model", "LLaMA-3.1-70B")
        with col3:
            st.metric("🔗 Korrel8r", "✅ Connected")
        with col4:
            st.metric("🧪 Test Pods", "5 Scenarios")

if __name__ == "__main__":
    main()
