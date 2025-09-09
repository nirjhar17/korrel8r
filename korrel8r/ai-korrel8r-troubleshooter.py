#!/usr/bin/env python3
"""
AI-Powered Korrel8r Troubleshooter
Combines Korrel8r's correlation engine with AI analysis for intelligent pod troubleshooting
"""

import requests
import json
import subprocess
import sys
from datetime import datetime
import urllib3

# Disable SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AIKorrel8rTroubleshooter:
    def __init__(self, korrel8r_url, groq_api_key=None):
        self.korrel8r_url = korrel8r_url
        self.groq_api_key = groq_api_key
        self.session = requests.Session()
        self.session.verify = False  # For self-signed certs
        
    def get_pod_info(self, namespace, pod_name):
        """Get detailed pod information using oc describe"""
        try:
            cmd = ["oc", "describe", "pod", pod_name, "-n", namespace]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
        except Exception as e:
            return f"Error getting pod info: {str(e)}"
    
    def get_pod_logs(self, namespace, pod_name, container=None):
        """Get pod logs"""
        try:
            cmd = ["oc", "logs", f"{pod_name}", "-n", namespace]
            if container:
                cmd.extend(["-c", container])
            cmd.extend(["--tail=50"])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
        except Exception as e:
            return f"Error getting logs: {str(e)}"
    
    def get_events(self, namespace, pod_name):
        """Get events related to the pod"""
        try:
            cmd = ["oc", "get", "events", "-n", namespace, "--field-selector", f"involvedObject.name={pod_name}", "--sort-by='.lastTimestamp'"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
        except Exception as e:
            return f"Error getting events: {str(e)}"
    
    def get_node_info(self, node_name):
        """Get node information"""
        try:
            cmd = ["oc", "describe", "node", node_name]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
        except Exception as e:
            return f"Error getting node info: {str(e)}"
    
    def korrel8r_query(self, query):
        """Query Korrel8r API"""
        try:
            # Try different API endpoints
            endpoints = [
                f"{self.korrel8r_url}/api/v1alpha1/objects",
                f"{self.korrel8r_url}/api/v1alpha1/neighbours"
            ]
            
            for endpoint in endpoints:
                try:
                    params = {"query": query}
                    response = self.session.get(endpoint, params=params, timeout=10)
                    if response.status_code == 200:
                        return response.json()
                except:
                    continue
                    
            return {"error": "Korrel8r API not accessible"}
        except Exception as e:
            return {"error": f"Korrel8r query failed: {str(e)}"}
    
    def ai_analyze(self, problem_data):
        """Analyze the problem using AI (Groq)"""
        if not self.groq_api_key:
            return "AI analysis not available - no API key provided"
        
        try:
            prompt = f"""
You are a Kubernetes troubleshooting expert. Analyze this pod problem and provide:

1. **Root Cause Analysis**
2. **Recommended Solutions** (step-by-step)
3. **Prevention Strategies**
4. **Related Resource Checks**

Problem Data:
{problem_data}

Provide a clear, actionable response focused on fixing the issue.
"""
            
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.1-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 1500
            }
            
            response = requests.post(
                "https://api.groq.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"AI analysis failed: {response.status_code}"
                
        except Exception as e:
            return f"AI analysis error: {str(e)}"
    
    def troubleshoot_pod(self, namespace, pod_name):
        """Complete troubleshooting workflow"""
        print(f"🔍 AI-Powered Korrel8r Troubleshooting: {namespace}/{pod_name}")
        print("=" * 60)
        
        # 1. Gather basic pod information
        print("\n📋 Step 1: Gathering Pod Information...")
        pod_info = self.get_pod_info(namespace, pod_name)
        
        # 2. Get events
        print("\n📋 Step 2: Checking Events...")
        events = self.get_events(namespace, pod_name)
        
        # 3. Try to get logs
        print("\n📋 Step 3: Retrieving Logs...")
        logs = self.get_pod_logs(namespace, pod_name)
        
        # 4. Korrel8r correlation
        print("\n📋 Step 4: Korrel8r Correlation Analysis...")
        korrel8r_query = f"k8s:Pod.v1:{{namespace: {namespace}, name: {pod_name}}}"
        correlation_data = self.korrel8r_query(korrel8r_query)
        
        # 5. Compile data for AI analysis
        problem_data = f"""
POD INFORMATION:
{pod_info}

EVENTS:
{events}

LOGS:
{logs}

KORREL8R CORRELATION:
{json.dumps(correlation_data, indent=2)}
"""
        
        # 6. AI Analysis
        print("\n🤖 Step 5: AI Analysis...")
        ai_analysis = self.ai_analyze(problem_data)
        
        # 7. Generate report
        print("\n" + "=" * 60)
        print("🎯 TROUBLESHOOTING REPORT")
        print("=" * 60)
        print(ai_analysis)
        
        return {
            "pod_info": pod_info,
            "events": events,
            "logs": logs,
            "correlation": correlation_data,
            "ai_analysis": ai_analysis
        }

def main():
    # Configuration
    KORREL8R_URL = "https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com"
    
    # Try to get Groq API key from environment or config
    try:
        with open("/Users/njajodia/logs_monitoring/k8s-anomaly-detection/.env", "r") as f:
            for line in f:
                if line.startswith("GROQ_API_KEY="):
                    GROQ_API_KEY = line.split("=", 1)[1].strip()
                    break
            else:
                GROQ_API_KEY = None
    except:
        GROQ_API_KEY = None
    
    # Initialize troubleshooter
    troubleshooter = AIKorrel8rTroubleshooter(KORREL8R_URL, GROQ_API_KEY)
    
    # Example: Troubleshoot the pending Prometheus pod
    if len(sys.argv) >= 3:
        namespace = sys.argv[1]
        pod_name = sys.argv[2]
    else:
        # Default to the broken pod we found
        namespace = "openshift-monitoring"
        pod_name = "prometheus-k8s-0"
    
    print(f"🚀 Starting AI-Powered Korrel8r Troubleshooting...")
    print(f"Target: {namespace}/{pod_name}")
    
    result = troubleshooter.troubleshoot_pod(namespace, pod_name)
    
    print("\n✅ Troubleshooting Complete!")
    print(f"📊 Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
