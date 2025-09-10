#!/usr/bin/env python3
"""
Enhanced AI-Powered OpenShift Troubleshooter v2.0
Features:
- Granular error categorization with severity levels
- AI-driven root cause analysis with fix suggestions  
- Pod resource consumption analysis
- Cluster-wide health correlation
- Step-by-step remediation guidance
- Log anomaly detection
- Visual timeline and event flowchart
"""

import streamlit as st
import subprocess
import json
import requests
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Enhanced AI OpenShift Troubleshooter v2.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Configuration
GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Severity levels and categories
SEVERITY_LEVELS = {
    "CRITICAL": {"color": "#c9190b", "icon": "🔴", "priority": 1},
    "WARNING": {"color": "#f0ab00", "icon": "🟡", "priority": 2},
    "INFO": {"color": "#0066cc", "icon": "🔵", "priority": 3},
    "SUCCESS": {"color": "#3e8635", "icon": "🟢", "priority": 4}
}

ERROR_CATEGORIES = {
    "RESOURCE": {"name": "Resource Issues", "icon": "💾", "patterns": ["insufficient", "resource", "memory", "cpu", "disk"]},
    "NETWORK": {"name": "Network Issues", "icon": "🌐", "patterns": ["network", "dns", "connection", "timeout", "unreachable"]},
    "STORAGE": {"name": "Storage Issues", "icon": "💿", "patterns": ["volume", "mount", "pvc", "storage", "disk"]},
    "IMAGE": {"name": "Image Issues", "icon": "📦", "patterns": ["image", "pull", "registry", "manifest"]},
    "PERMISSION": {"name": "Permission Issues", "icon": "🔐", "patterns": ["permission", "forbidden", "unauthorized", "rbac"]},
    "CONFIG": {"name": "Configuration Issues", "icon": "⚙️", "patterns": ["config", "environment", "secret", "configmap"]},
    "INIT": {"name": "Initialization Issues", "icon": "🔄", "patterns": ["init", "startup", "readiness", "liveness"]},
    "SCHEDULING": {"name": "Scheduling Issues", "icon": "📅", "patterns": ["schedule", "node", "affinity", "taint", "toleration"]}
}

# Enhanced CSS with severity colors and better visualization
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0066cc, #004080);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #0066cc;
    }
    
    .severity-critical {
        background-color: #fdf2f2 !important;
        color: #721c24 !important;
        border-left: 4px solid #c9190b;
        border: 1px solid #c9190b;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .severity-warning {
        background-color: #fdf8e7 !important;
        color: #795600 !important;
        border-left: 4px solid #f0ab00;
        border: 1px solid #f0ab00;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .severity-info {
        background-color: #f0f8ff !important;
        color: #151515 !important;
        border-left: 4px solid #0066cc;
        border: 1px solid #0066cc;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .severity-success {
        background-color: #f3faf3 !important;
        color: #1e4f18 !important;
        border-left: 4px solid #3e8635;
        border: 1px solid #3e8635;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .resource-metrics {
        background-color: #f8f9fa !important;
        color: #151515 !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #d2d2d2;
        margin: 1rem 0;
    }
    
    .remediation-step {
        background-color: #e8f4fd !important;
        color: #151515 !important;
        padding: 0.75rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 0.5rem 0;
        border: 1px solid #0066cc;
    }
    
    .timeline-item {
        background-color: #ffffff !important;
        color: #151515 !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #d2d2d2;
        margin: 0.5rem 0;
        position: relative;
        padding-left: 3rem;
    }
    
    .timeline-item::before {
        content: "●";
        position: absolute;
        left: 1rem;
        top: 1rem;
        color: #0066cc;
        font-size: 1.2rem;
    }
    
    .cluster-health {
        background-color: #f5f5f5 !important;
        color: #151515 !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #d2d2d2;
        margin: 1rem 0;
    }
    
    .anomaly-alert {
        background-color: #fff4e6 !important;
        color: #8c4400 !important;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f0ab00;
        border: 1px solid #f0ab00;
        margin: 1rem 0;
    }
    
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #d2d2d2;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0066cc;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
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

def categorize_error(error_text: str) -> Tuple[str, str]:
    """Categorize error and determine severity"""
    error_lower = error_text.lower()
    
    # Determine category
    category = "CONFIG"  # default
    for cat_key, cat_info in ERROR_CATEGORIES.items():
        if any(pattern in error_lower for pattern in cat_info["patterns"]):
            category = cat_key
            break
    
    # Determine severity based on keywords and patterns
    if any(word in error_lower for word in ["failed", "error", "crash", "critical", "fatal", "emergency"]):
        severity = "CRITICAL"
    elif any(word in error_lower for word in ["warning", "warn", "deprecated", "retry", "backoff"]):
        severity = "WARNING"
    elif any(word in error_lower for word in ["success", "completed", "ready", "healthy"]):
        severity = "SUCCESS"
    else:
        severity = "INFO"
    
    return category, severity

def analyze_resource_consumption(namespace: str, pod: str) -> Dict:
    """Analyze pod resource consumption"""
    try:
        # Get pod resource requests and limits
        cmd = f"oc get pod {pod} -n {namespace} -o json"
        returncode, stdout, stderr = run_command(cmd)
        
        if returncode != 0:
            return {"error": f"Failed to get pod info: {stderr}"}
        
        pod_data = json.loads(stdout)
        
        # Extract resource information
        containers = pod_data.get("spec", {}).get("containers", [])
        resource_info = {
            "requests": {"cpu": "0", "memory": "0"},
            "limits": {"cpu": "0", "memory": "0"},
            "containers": len(containers)
        }
        
        for container in containers:
            resources = container.get("resources", {})
            requests = resources.get("requests", {})
            limits = resources.get("limits", {})
            
            # Aggregate requests and limits
            if "cpu" in requests:
                resource_info["requests"]["cpu"] = requests["cpu"]
            if "memory" in requests:
                resource_info["requests"]["memory"] = requests["memory"]
            if "cpu" in limits:
                resource_info["limits"]["cpu"] = limits["cpu"]
            if "memory" in limits:
                resource_info["limits"]["memory"] = limits["memory"]
        
        # Get current resource usage (if available)
        cmd = f"oc adm top pod {pod} -n {namespace} --no-headers 2>/dev/null || echo 'N/A N/A'"
        returncode, stdout, stderr = run_command(cmd)
        
        usage_parts = stdout.strip().split()
        resource_info["current"] = {
            "cpu": usage_parts[1] if len(usage_parts) > 1 and usage_parts[1] != "N/A" else "N/A",
            "memory": usage_parts[2] if len(usage_parts) > 2 and usage_parts[2] != "N/A" else "N/A"
        }
        
        return resource_info
        
    except Exception as e:
        return {"error": f"Resource analysis failed: {str(e)}"}

def get_cluster_health(namespace: str) -> Dict:
    """Get cluster-wide health information"""
    try:
        health_info = {}
        
        # Get node status
        cmd = "oc get nodes --no-headers | wc -l"
        returncode, stdout, stderr = run_command(cmd)
        health_info["total_nodes"] = stdout.strip() if returncode == 0 else "N/A"
        
        cmd = "oc get nodes --no-headers | grep -c Ready"
        returncode, stdout, stderr = run_command(cmd)
        health_info["ready_nodes"] = stdout.strip() if returncode == 0 else "N/A"
        
        # Get namespace pod status
        cmd = f"oc get pods -n {namespace} --no-headers | wc -l"
        returncode, stdout, stderr = run_command(cmd)
        health_info["total_pods"] = stdout.strip() if returncode == 0 else "N/A"
        
        cmd = f"oc get pods -n {namespace} --no-headers | grep -c Running"
        returncode, stdout, stderr = run_command(cmd)
        health_info["running_pods"] = stdout.strip() if returncode == 0 else "N/A"
        
        # Get recent events
        cmd = f"oc get events -n {namespace} --sort-by='.lastTimestamp' | tail -5"
        returncode, stdout, stderr = run_command(cmd)
        health_info["recent_events"] = stdout if returncode == 0 else "No recent events"
        
        return health_info
        
    except Exception as e:
        return {"error": f"Cluster health check failed: {str(e)}"}

def detect_log_anomalies(logs: str) -> List[Dict]:
    """Detect anomalies in logs"""
    anomalies = []
    
    # Pattern-based anomaly detection
    patterns = {
        "excessive_restarts": {
            "pattern": r"restart.*(\d+)",
            "threshold": 5,
            "description": "Excessive container restarts detected"
        },
        "repeated_errors": {
            "pattern": r"(error|failed|exception)",
            "threshold": 10,
            "description": "High frequency of errors in logs"
        },
        "timeout_issues": {
            "pattern": r"timeout|timed out",
            "threshold": 3,
            "description": "Multiple timeout issues detected"
        },
        "network_retries": {
            "pattern": r"retry|retrying",
            "threshold": 5,
            "description": "Excessive network retries detected"
        }
    }
    
    for anomaly_type, config in patterns.items():
        matches = re.findall(config["pattern"], logs, re.IGNORECASE)
        if len(matches) >= config["threshold"]:
            anomalies.append({
                "type": anomaly_type,
                "count": len(matches),
                "description": config["description"],
                "severity": "WARNING" if len(matches) < config["threshold"] * 2 else "CRITICAL"
            })
    
    return anomalies

def get_enhanced_ai_analysis(pod_info: str, resource_info: Dict, cluster_health: Dict, anomalies: List[Dict], namespace: str, pod: str) -> str:
    """Get enhanced AI analysis with all the new features"""
    
    # Prepare comprehensive context for AI
    context = f"""
    ENHANCED KUBERNETES TROUBLESHOOTING ANALYSIS
    
    Pod: {namespace}/{pod}
    
    RESOURCE ANALYSIS:
    {json.dumps(resource_info, indent=2)}
    
    CLUSTER HEALTH:
    {json.dumps(cluster_health, indent=2)}
    
    DETECTED ANOMALIES:
    {json.dumps(anomalies, indent=2)}
    
    POD INFORMATION AND LOGS:
    {pod_info}
    
    Please provide a comprehensive analysis including:
    1. SEVERITY CLASSIFICATION (CRITICAL/WARNING/INFO/SUCCESS)
    2. ROOT CAUSE ANALYSIS with specific technical details
    3. STEP-BY-STEP REMEDIATION GUIDE with exact commands
    4. RESOURCE OPTIMIZATION RECOMMENDATIONS
    5. PREVENTIVE MEASURES for similar issues
    6. CLUSTER-WIDE IMPACT ASSESSMENT
    7. TIMELINE of events leading to the issue
    
    Format your response with clear sections and actionable insights.
    """
    
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
                    "content": "You are an expert Kubernetes and OpenShift troubleshooter with deep knowledge of container orchestration, resource management, and observability. Provide detailed, actionable insights with specific technical solutions."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.1
        }
        
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"AI Analysis Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"AI Analysis failed: {str(e)}"

def create_timeline_visualization(events: str) -> List[Dict]:
    """Create timeline from events"""
    timeline = []
    
    # Parse events and create timeline items
    lines = events.split('\n')
    for line in lines[1:]:  # Skip header
        if line.strip():
            parts = line.split()
            if len(parts) >= 6:
                timeline.append({
                    "time": parts[0],
                    "type": parts[1],
                    "reason": parts[2],
                    "object": parts[3],
                    "message": " ".join(parts[4:])
                })
    
    return timeline

# Main Streamlit App
def main():
    st.markdown('<div class="main-header"><h1>🤖 Enhanced AI OpenShift Troubleshooter v2.0</h1><p>Advanced Analysis • Resource Monitoring • Anomaly Detection • Step-by-Step Remediation</p></div>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Get available clusters
        clusters = ["current-cluster"]  # Simplified for demo
        selected_cluster = st.selectbox("🌐 Select Cluster", clusters)
        
        # Get namespaces
        cmd = "oc get namespaces --no-headers | awk '{print $1}' | head -20"
        returncode, stdout, stderr = run_command(cmd)
        namespaces = stdout.strip().split('\n') if returncode == 0 else ["default"]
        
        selected_namespace = st.selectbox("📁 Select Namespace", namespaces)
        
        if selected_namespace:
            # Get pods
            cmd = f"oc get pods -n {selected_namespace} --no-headers | awk '{{print $1}}'"
            returncode, stdout, stderr = run_command(cmd)
            pods = stdout.strip().split('\n') if returncode == 0 and stdout.strip() else []
            
            if pods:
                selected_pod = st.selectbox("🔍 Select Pod", pods)
            else:
                st.warning("No pods found in this namespace")
                selected_pod = None
        else:
            selected_pod = None
    
    # Main analysis section
    if selected_pod and selected_namespace:
        if st.button("🚀 Run Enhanced Analysis", type="primary"):
            with st.spinner("Running enhanced analysis..."):
                
                # Step 1: Basic pod analysis
                st.info("📊 Gathering pod information...")
                cmd = f"oc describe pod {selected_pod} -n {selected_namespace}"
                returncode, stdout, stderr = run_command(cmd)
                pod_info = stdout if returncode == 0 else f"Error: {stderr}"
                
                # Step 2: Resource analysis
                st.info("💾 Analyzing resource consumption...")
                resource_info = analyze_resource_consumption(selected_namespace, selected_pod)
                
                # Step 3: Cluster health
                st.info("🏥 Checking cluster health...")
                cluster_health = get_cluster_health(selected_namespace)
                
                # Step 4: Get logs for anomaly detection
                st.info("🔍 Detecting log anomalies...")
                cmd = f"oc logs {selected_pod} -n {selected_namespace} --tail=100 2>/dev/null || echo 'No logs available'"
                returncode, logs, stderr = run_command(cmd)
                anomalies = detect_log_anomalies(logs)
                
                # Step 5: AI Analysis
                st.info("🤖 Running AI analysis...")
                ai_analysis = get_enhanced_ai_analysis(pod_info, resource_info, cluster_health, anomalies, selected_namespace, selected_pod)
            
            st.success("✅ Enhanced analysis complete!")
            
            # Display results in tabs
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🎯 AI Analysis", "📊 Resources", "🏥 Cluster Health", "⚠️ Anomalies", "📅 Timeline", "🔧 Remediation"])
            
            with tab1:
                st.markdown(f"""
                <div class="severity-info">
                    <h3>🧠 Enhanced AI Analysis</h3>
                    <p><strong>Pod:</strong> {selected_namespace}/{selected_pod}</p>
                    <p><strong>Analysis Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(ai_analysis)
            
            with tab2:
                st.header("📊 Resource Analysis")
                
                if "error" not in resource_info:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{resource_info['containers']}</div>
                            <div class="metric-label">Containers</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        cpu_current = resource_info.get('current', {}).get('cpu', 'N/A')
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{cpu_current}</div>
                            <div class="metric-label">CPU Usage</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        memory_current = resource_info.get('current', {}).get('memory', 'N/A')
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{memory_current}</div>
                            <div class="metric-label">Memory Usage</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="resource-metrics">
                        <h4>Resource Requests & Limits</h4>
                        <p><strong>CPU Request:</strong> {resource_info['requests']['cpu']}</p>
                        <p><strong>CPU Limit:</strong> {resource_info['limits']['cpu']}</p>
                        <p><strong>Memory Request:</strong> {resource_info['requests']['memory']}</p>
                        <p><strong>Memory Limit:</strong> {resource_info['limits']['memory']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(resource_info["error"])
            
            with tab3:
                st.header("🏥 Cluster Health")
                
                if "error" not in cluster_health:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Nodes", cluster_health.get('total_nodes', 'N/A'))
                    with col2:
                        st.metric("Ready Nodes", cluster_health.get('ready_nodes', 'N/A'))
                    with col3:
                        st.metric("Total Pods", cluster_health.get('total_pods', 'N/A'))
                    with col4:
                        st.metric("Running Pods", cluster_health.get('running_pods', 'N/A'))
                    
                    st.markdown(f"""
                    <div class="cluster-health">
                        <h4>Recent Events</h4>
                        <pre>{cluster_health.get('recent_events', 'No events')}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(cluster_health["error"])
            
            with tab4:
                st.header("⚠️ Anomaly Detection")
                
                if anomalies:
                    for anomaly in anomalies:
                        severity_class = f"severity-{anomaly['severity'].lower()}"
                        icon = SEVERITY_LEVELS[anomaly['severity']]['icon']
                        
                        st.markdown(f"""
                        <div class="{severity_class}">
                            <h4>{icon} {anomaly['description']}</h4>
                            <p><strong>Type:</strong> {anomaly['type']}</p>
                            <p><strong>Count:</strong> {anomaly['count']}</p>
                            <p><strong>Severity:</strong> {anomaly['severity']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("🟢 No anomalies detected in the logs")
            
            with tab5:
                st.header("📅 Event Timeline")
                
                # Get events
                cmd = f"oc get events -n {selected_namespace} --field-selector involvedObject.name={selected_pod} --sort-by='.lastTimestamp'"
                returncode, events, stderr = run_command(cmd)
                
                if returncode == 0 and events.strip():
                    timeline = create_timeline_visualization(events)
                    
                    for item in timeline[-10:]:  # Show last 10 events
                        st.markdown(f"""
                        <div class="timeline-item">
                            <strong>{item.get('time', 'N/A')}</strong> - {item.get('type', 'N/A')}
                            <br><strong>Reason:</strong> {item.get('reason', 'N/A')}
                            <br><strong>Message:</strong> {item.get('message', 'N/A')}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No events found for this pod")
            
            with tab6:
                st.header("🔧 Remediation Steps")
                
                # Extract common remediation patterns
                if "CrashLoopBackOff" in pod_info:
                    st.markdown("""
                    <div class="remediation-step">
                        <h4>🔄 CrashLoopBackOff Remediation</h4>
                        <ol>
                            <li>Check container logs: <code>oc logs {pod} -n {namespace} --previous</code></li>
                            <li>Verify image and command configuration</li>
                            <li>Check resource limits and requests</li>
                            <li>Validate environment variables and secrets</li>
                        </ol>
                    </div>
                    """.format(pod=selected_pod, namespace=selected_namespace), unsafe_allow_html=True)
                
                if "ImagePullBackOff" in pod_info:
                    st.markdown("""
                    <div class="remediation-step">
                        <h4>📦 ImagePullBackOff Remediation</h4>
                        <ol>
                            <li>Verify image name and tag</li>
                            <li>Check registry credentials: <code>oc get secrets</code></li>
                            <li>Test image pull manually: <code>podman pull [image]</code></li>
                            <li>Check network connectivity to registry</li>
                        </ol>
                    </div>
                    """, unsafe_allow_html=True)
                
                if "Pending" in pod_info:
                    st.markdown("""
                    <div class="remediation-step">
                        <h4>📅 Pending Pod Remediation</h4>
                        <ol>
                            <li>Check node resources: <code>oc describe nodes</code></li>
                            <li>Verify PVC status: <code>oc get pvc -n {namespace}</code></li>
                            <li>Check node selectors and taints</li>
                            <li>Review resource requests vs available capacity</li>
                        </ol>
                    </div>
                    """.format(namespace=selected_namespace), unsafe_allow_html=True)
                
                # Always show general remediation
                st.markdown("""
                <div class="remediation-step">
                    <h4>🛠️ General Troubleshooting Steps</h4>
                    <ol>
                        <li>Get detailed pod information: <code>oc describe pod {pod} -n {namespace}</code></li>
                        <li>Check recent events: <code>oc get events -n {namespace} --sort-by='.lastTimestamp'</code></li>
                        <li>Review pod logs: <code>oc logs {pod} -n {namespace} -f</code></li>
                        <li>Check resource quotas: <code>oc get resourcequota -n {namespace}</code></li>
                        <li>Validate RBAC permissions: <code>oc auth can-i --list --as=system:serviceaccount:{namespace}:default</code></li>
                    </ol>
                </div>
                """.format(pod=selected_pod, namespace=selected_namespace), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
