#!/usr/bin/env python3
"""
Enhanced AI-Powered OpenShift Troubleshooter v3.2 - HYBRID IMPLEMENTATION
Combines v2.0's technical depth with v3.1's vector database intelligence
Features:
- Senior SRE-level technical analysis
- Production alerting rule integration
- Comprehensive deep-dive troubleshooting
- Vector database semantic search
- Same look and feel as v2.0 with enhanced intelligence
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
import os

# Page configuration
st.set_page_config(
    page_title="AI OpenShift Troubleshooter v3.2 (Hybrid)",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Vector Database Setup
@st.cache_resource
def initialize_vector_database():
    """Initialize ChromaDB and Google AI Studio"""
    try:
        import chromadb
        import google.generativeai as genai
        
        # Configure Google AI Studio
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Initialize ChromaDB (persistent storage in mounted volume)
        db_path = "/app/vector-db-storage/prometheus_rules_db"
        os.makedirs(db_path, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=db_path)
        
        # Create or get collection
        try:
            collection = chroma_client.get_collection("prometheus-rules")
            count = collection.count()
            st.success(f"✅ Loaded existing PrometheusRule vector database with {count} embeddings")
        except Exception as e:
            st.warning(f"⚠️ Could not load existing collection: {e}")
            collection = chroma_client.create_collection(
                name="prometheus-rules",
                metadata={"description": "OpenShift PrometheusRule embeddings for semantic search"}
            )
            st.info("📊 Created new PrometheusRule vector database")
        
        return genai, collection, True
        
    except ImportError as e:
        st.error(f"❌ Missing dependencies: {e}")
        return None, None, False
    except Exception as e:
        st.error(f"❌ Vector database initialization error: {e}")
        return None, None, False

# Load vector database
genai, vector_collection, vector_db_ready = initialize_vector_database()

def load_and_embed_prometheus_rules():
    """Load PrometheusRules and create embeddings"""
    if not vector_db_ready:
        return [], False
    
    try:
        # Check if collection already has data
        count = vector_collection.count()
        if count > 0:
            st.info(f"📊 Found {count} existing PrometheusRule embeddings")
            return [], True
        
        # Extract PrometheusRules
        with st.spinner("🔍 Extracting PrometheusRules from cluster..."):
            result = subprocess.run(['oc', 'get', 'prometheusrule', '--all-namespaces', '-o', 'json'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                st.error("❌ Failed to extract PrometheusRules from cluster")
                return [], False
            
            rules_data = json.loads(result.stdout)
            alerting_rules = []
            
            # Process rules
            for item in rules_data.get('items', []):
                namespace = item['metadata']['namespace']
                rule_name = item['metadata']['name']
                
                spec = item.get('spec', {})
                for group in spec.get('groups', []):
                    for rule in group.get('rules', []):
                        if 'alert' in rule:
                            alerting_rules.append({
                                'alert_name': rule['alert'],
                                'namespace': namespace,
                                'rule_resource': rule_name,
                                'expr': rule['expr'].strip(),
                                'for_duration': rule.get('for', '0s'),
                                'severity': rule.get('labels', {}).get('severity', 'unknown'),
                                'description': rule.get('annotations', {}).get('description', ''),
                                'summary': rule.get('annotations', {}).get('summary', ''),
                                'runbook_url': rule.get('annotations', {}).get('runbook_url', '')
                            })
        
        if not alerting_rules:
            st.warning("⚠️ No PrometheusRules found to embed")
            return [], False
        
        st.success(f"✅ Extracted {len(alerting_rules)} PrometheusRules")
        
        # Create embeddings
        with st.spinner(f"🧠 Creating embeddings for {len(alerting_rules)} PrometheusRules..."):
            def create_rule_text(rule):
                """Create comprehensive text for embedding"""
                text_parts = [
                    f"Alert: {rule.get('alert_name', '')}",
                    f"Severity: {rule.get('severity', '')}",
                    f"Description: {rule.get('description', '')}",
                    f"Summary: {rule.get('summary', '')}",
                    f"Expression: {rule.get('expr', '')}",
                    f"Duration: {rule.get('for_duration', '')}",
                    f"Namespace: {rule.get('namespace', '')}"
                ]
                return " | ".join([part for part in text_parts if part.split(": ", 1)[1]])
            
            # Generate embeddings in batches
            rule_texts = [create_rule_text(rule) for rule in alerting_rules]
            rule_embeddings = []
            
            batch_size = 5  # Smaller batches to avoid rate limits
            progress_bar = st.progress(0)
            
            for i in range(0, len(rule_texts), batch_size):
                batch = rule_texts[i:i+batch_size]
                try:
                    result = genai.embed_content(
                        model="models/text-embedding-004",
                        content=batch
                    )
                    
                    # Handle different response formats
                    if isinstance(result['embedding'], list):
                        if len(batch) == 1:
                            rule_embeddings.append(result['embedding'])
                        else:
                            rule_embeddings.extend(result['embedding'])
                    else:
                        rule_embeddings.append(result['embedding'])
                    
                    # Update progress
                    progress = min(i + batch_size, len(rule_texts)) / len(rule_texts)
                    progress_bar.progress(progress)
                    
                    # Small delay to respect rate limits
                    time.sleep(0.5)
                    
                except Exception as e:
                    st.warning(f"⚠️ Embedding error for batch {i//batch_size + 1}: {e}")
                    # Create dummy embeddings as fallback
                    dummy_embedding = [0.0] * 768
                    rule_embeddings.extend([dummy_embedding] * len(batch))
            
            progress_bar.progress(1.0)
        
        # Store in ChromaDB
        with st.spinner("💾 Storing embeddings in vector database..."):
            rule_ids = [f"rule_{i}" for i in range(len(alerting_rules))]
            rule_metadatas = [
                {
                    "alert_name": rule.get('alert_name', ''),
                    "severity": rule.get('severity', 'unknown'),
                    "namespace": rule.get('namespace', ''),
                    "for_duration": rule.get('for_duration', ''),
                    "runbook_url": rule.get('runbook_url', ''),
                    "expr": rule.get('expr', '')[:500],  # Truncate long expressions
                    "description": rule.get('description', '')[:200]  # Truncate long descriptions
                }
                for rule in alerting_rules
            ]
            
            # Add to collection
            vector_collection.add(
                embeddings=rule_embeddings,
                documents=rule_texts,
                metadatas=rule_metadatas,
                ids=rule_ids
            )
        
        st.success(f"🎯 Successfully embedded and stored {len(alerting_rules)} PrometheusRules")
        return alerting_rules, True
        
    except Exception as e:
        st.error(f"❌ Error loading/embedding PrometheusRules: {e}")
        return [], False

def semantic_search_rules(query: str, issue_context: Dict, n_results: int = 5):
    """Perform semantic search for relevant PrometheusRules"""
    if not vector_db_ready:
        st.error("❌ Vector database not ready for semantic search")
        return []
    
    if not vector_collection:
        st.error("❌ Vector collection not available")
        return []
    
    try:
        # Check if collection has data
        count = vector_collection.count()
        if count == 0:
            st.error("❌ No embeddings found in vector database")
            return []
        
        st.info(f"🔍 Searching {count} embeddings for relevant rules...")
        
        # Enhanced query with context for better crash loop detection
        enhanced_query_parts = [f"Issue: {query}"]
        
        if issue_context.get('pod_status'):
            enhanced_query_parts.append(f"Pod Status: {issue_context['pod_status']}")
        if issue_context.get('container_state'):
            state = issue_context['container_state']
            enhanced_query_parts.append(f"Container State: {state}")
            # Add specific terms for better matching
            if "CrashLoopBackOff" in state:
                enhanced_query_parts.extend(["crash loop", "crashing", "restart loop", "pod crash", "container restart"])
        if issue_context.get('namespace'):
            enhanced_query_parts.append(f"Namespace: {issue_context['namespace']}")
        if issue_context.get('restart_count', 0) > 0:
            restart_count = issue_context['restart_count']
            enhanced_query_parts.append(f"Restart Count: {restart_count}")
            if restart_count > 3:
                enhanced_query_parts.extend(["high restart count", "frequent restarts", "restart threshold"])
        if issue_context.get('error_patterns'):
            enhanced_query_parts.append(f"Error Patterns: {issue_context['error_patterns']}")
        
        enhanced_query = " | ".join(enhanced_query_parts)
        
        # Generate query embedding
        query_result = genai.embed_content(
            model="models/text-embedding-004",
            content=enhanced_query
        )
        query_embedding = query_result['embedding']
        
        # Perform semantic search
        results = vector_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        relevant_rules = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0], 
            results['distances'][0]
        )):
            similarity_score = max(0, 1 - distance)  # Convert distance to similarity
            relevant_rules.append({
                'rank': i + 1,
                'alert_name': metadata['alert_name'],
                'severity': metadata['severity'],
                'namespace': metadata['namespace'],
                'for_duration': metadata['for_duration'],
                'runbook_url': metadata['runbook_url'],
                'expr': metadata['expr'],
                'description': metadata['description'],
                'similarity_score': similarity_score,
                'document': doc
            })
        
        return relevant_rules
        
    except Exception as e:
        st.error(f"❌ Semantic search error: {e}")
        return []

def analyze_with_hybrid_intelligence(pod_issue: str, pod_context: Dict, relevant_rules: List[Dict]) -> str:
    """V3.2 Hybrid Analysis - Combines v2 technical depth with v3 vector intelligence"""
    
    if not relevant_rules:
        return "❌ No relevant PrometheusRules found for hybrid analysis"
    
    # Build focused context from semantic search results
    rules_context = "# PRODUCTION ALERTING RULES CONTEXT\n\n"
    rules_context += f"Found {len(relevant_rules)} most relevant production rules:\n\n"
    
    for rule in relevant_rules:
        rules_context += f"""
## {rule['alert_name']} ({rule['severity'].upper()} severity) - Similarity: {rule['similarity_score']:.3f}
- **Condition**: `{rule['expr']}`
- **Duration**: {rule['for_duration']}
- **Namespace Scope**: {rule['namespace']}
- **Description**: {rule['description']}"""
        if rule['runbook_url']:
            rules_context += f"\n- **Runbook**: {rule['runbook_url']}"
        rules_context += "\n"
    
    # V3.2 Admin-Focused System Prompt - Concise and Actionable
    system_prompt = f"""You are a senior OpenShift SRE providing immediate, actionable troubleshooting guidance. Your response must be concise and admin-focused.

{rules_context}

RESPONSE FORMAT (STRICT):
```
🚨 **ISSUE**: [One-line summary]
📊 **RULE**: [Best matching alert rule name and brief condition]
⚡ **ACTIONS**: [3-5 immediate commands to run]
🔧 **FIX**: [Specific resolution steps]
```

KEY REQUIREMENTS:
1. **Maximum 200 words total**
2. **Lead with immediate diagnostic commands**
3. **Show only the BEST matching production rule**
4. **Focus on "what to do NOW" not "what rules apply"**
5. **Use specific `oc` commands**
6. **No verbose explanations or multiple rule comparisons**

PRODUCTION RULE INTEGRATION:
- Reference the most relevant PrometheusRule from the vector database
- Show only: rule name, severity, and brief condition
- Use rule context to validate your recommendations
- Don't explain multiple rules - pick the best one

EXAMPLE GOOD RESPONSE:
```
🚨 **ISSUE**: Pod crash-loop-test in CrashLoopBackOff with 16 restarts
📊 **RULE**: KubePodCrashLooping (WARNING) - triggers after 5min crash loop
⚡ **ACTIONS**: 
  oc logs crash-loop-test -c crasher --previous
  oc describe pod crash-loop-test
  oc get events --field-selector involvedObject.name=crash-loop-test
🔧 **FIX**: Container command has intentional `exit 1`. Remove exit statement or change restartPolicy to Never
```

WHAT NOT TO INCLUDE:
- ❌ Verbose "Key Observations" sections
- ❌ Multiple rule comparisons
- ❌ Long explanations of why rules apply
- ❌ "Production-Grade Recommendations" sections
- ❌ "Operational Context" paragraphs
- ❌ Example commands in separate sections

WHAT TO INCLUDE:
- ✅ Immediate diagnostic commands
- ✅ Specific fix instructions
- ✅ One best matching rule
- ✅ Concise, actionable format
"""
    
    # Concise user prompt for admin-focused analysis
    user_prompt = f"""
Analyze this OpenShift pod issue and provide immediate actionable guidance:

**Pod Issue**: {pod_issue}

**Technical Context**:
{json.dumps(pod_context, indent=2)}

Provide concise, admin-focused analysis following the exact format specified. Focus on immediate actions and specific fixes.
"""
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 4000
        }
        
        response = requests.post(GROQ_ENDPOINT, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            
            # Add hybrid intelligence metadata
            analysis += f"""

---
**🎯 Hybrid Analysis Enhanced with Production Intelligence**
- **Vector Database**: {len(relevant_rules)} relevant rules found
- **Top Similarity**: {relevant_rules[0]['similarity_score']:.3f} ({relevant_rules[0]['alert_name']})
- **Rule Coverage**: {', '.join(set(r['severity'] for r in relevant_rules))} severity levels
- **Operational Context**: Production alerting rules + Senior SRE technical analysis
"""
            
            return analysis
        else:
            return f"❌ Groq Analysis Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Hybrid Analysis Error: {str(e)}"

def run_command(command: str) -> Tuple[str, str, int]:
    """Execute shell command and return output, error, and return code"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1

# Enhanced CSS for v3.2 hybrid
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white !important;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid #3b82f6;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.2);
    }
    
    .hybrid-badge {
        background: linear-gradient(90deg, #10b981, #3b82f6);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .technical-analysis {
        background-color: #f0f9ff !important;
        color: #0c4a6e !important;
        border-left: 6px solid #3b82f6;
        border: 1px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
        font-family: 'Courier New', monospace;
    }
    
    .rule-match {
        background: linear-gradient(90deg, #f59e0b, #f97316);
        color: white !important;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 AI OpenShift Troubleshooter v3.2</h1>
    <p>Hybrid Intelligence: Senior SRE Analysis + Production Rule Intelligence</p>
    <div class="hybrid-badge">
        🧠 Technical Deep Dive + Vector Database + Production Rules
    </div>
</div>
""", unsafe_allow_html=True)

# Configuration status
st.write("✅ Configuration loaded successfully!")
st.write(f"🔑 Groq API Key: {bool(GROQ_API_KEY)}")
st.write(f"🔑 Google AI Studio Key: {bool(GOOGLE_API_KEY)}")
st.write(f"🗄️ Vector Database: {'✅ Ready' if vector_db_ready else '❌ Not Available'}")

# Initialize vector database and load rules
if vector_db_ready:
    st.info("🔄 Initializing hybrid intelligence system...")
    rules_data, embedding_success = load_and_embed_prometheus_rules()
    
    if vector_collection:
        rule_count = vector_collection.count()
        if rule_count > 0:
            st.success(f"✅ Hybrid intelligence ready with {rule_count} production rules")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Production Rules", f"{rule_count} rules")
            with col2:
                st.metric("🎯 Analysis Type", "Hybrid SRE")
            with col3:
                st.metric("🗄️ Intelligence", "Vector + Technical")
            with col4:
                st.metric("🔍 Search Type", "Semantic Enhanced")
        else:
            st.warning("⚠️ Vector database is empty - no embeddings found")
    else:
        st.error("❌ Vector collection not available")
else:
    st.error("❌ Vector database not ready - check API keys and dependencies")

# Sidebar for namespace and pod selection
st.sidebar.markdown("## 🔧 Hybrid Analysis Configuration")

# Get available namespaces
namespaces_output, _, _ = run_command("oc get namespaces --no-headers")
namespaces = [line.split()[0] for line in namespaces_output.strip().split('\n') if line.strip()]

selected_namespace = st.sidebar.selectbox(
    "📁 Select Namespace:",
    options=namespaces,
    index=namespaces.index("default") if "default" in namespaces else 0
)

# Get pods in selected namespace
if selected_namespace:
    pods_output, _, _ = run_command(f"oc get pods -n {selected_namespace} --no-headers")
    pods = []
    if pods_output.strip():
        for line in pods_output.strip().split('\n'):
            if line.strip():
                pod_name = line.split()[0]
                pods.append(pod_name)
    
    selected_pod = st.sidebar.selectbox(
        "🐳 Select Pod:",
        options=pods if pods else ["No pods found"],
        disabled=not pods
    )

# Analysis configuration
st.sidebar.markdown("### 🎛️ Hybrid Analysis Options")
include_logs = st.sidebar.checkbox("📝 Include Recent Logs", value=True)
include_events = st.sidebar.checkbox("📋 Include Pod Events", value=True)
similarity_threshold = st.sidebar.slider("🎯 Similarity Threshold", 0.0, 1.0, 0.3, 0.05)
max_rules = st.sidebar.selectbox("📊 Max Rules to Retrieve", [3, 5, 7, 10], index=1)

# Main analysis section
if st.sidebar.button("🚀 Start Hybrid Deep Analysis", type="primary"):
    if not selected_pod or selected_pod == "No pods found":
        st.error("❌ Please select a valid pod to analyze")
    elif not GROQ_API_KEY:
        st.error("❌ Please configure GROQ_API_KEY environment variable")
    elif not vector_db_ready:
        st.error("❌ Vector database not available")
    elif vector_collection.count() == 0:
        st.error("❌ No PrometheusRule embeddings found. Please initialize the vector database.")
    else:
        with st.spinner("🎯 Performing hybrid deep analysis with production intelligence..."):
            
            # Collect comprehensive data
            context_data = {
                "namespace": selected_namespace,
                "pod": selected_pod,
                "timestamp": datetime.now().isoformat()
            }
            
            # Get pod details
            pod_info, _, _ = run_command(f"oc get pod {selected_pod} -n {selected_namespace} -o json")
            pod_data = {}
            if pod_info:
                try:
                    pod_data = json.loads(pod_info)
                    context_data["pod_details"] = pod_data
                    
                    # Extract key information for semantic search
                    status = pod_data.get('status', {})
                    context_data["pod_status"] = status.get('phase', '')
                    
                    container_statuses = status.get('containerStatuses', [])
                    for container in container_statuses:
                        state = container.get('state', {})
                        if 'waiting' in state:
                            context_data["container_state"] = state['waiting'].get('reason', '')
                        context_data["restart_count"] = container.get('restartCount', 0)
                        
                except Exception as e:
                    st.warning(f"⚠️ Could not parse pod JSON: {e}")
            
            # Get pod events if requested
            if include_events:
                events_output, _, _ = run_command(f"oc get events -n {selected_namespace} --field-selector involvedObject.name={selected_pod} --sort-by='.lastTimestamp'")
                context_data["events"] = events_output
                context_data["error_patterns"] = events_output.lower()
            
            # Get recent logs if requested
            if include_logs:
                logs_output, _, _ = run_command(f"oc logs {selected_pod} -n {selected_namespace} --tail=50")
                context_data["recent_logs"] = logs_output
            
            # Build enhanced semantic search query for crash loops
            search_query_parts = [f"Pod {selected_pod} in namespace {selected_namespace}"]
            
            if context_data.get("container_state"):
                state = context_data['container_state']
                search_query_parts.append(f"container state {state}")
                # Add specific terms for better matching
                if "CrashLoopBackOff" in state:
                    search_query_parts.extend(["crash loop", "crashing", "restart loop", "pod crash"])
                elif "ImagePullBackOff" in state:
                    search_query_parts.extend(["image pull", "registry", "image not found"])
                elif "ContainerCreating" in state:
                    search_query_parts.extend(["container creation", "volume mount", "config mount"])
                    
            if context_data.get("restart_count", 0) > 0:
                restart_count = context_data['restart_count']
                search_query_parts.append(f"{restart_count} restarts")
                if restart_count > 3:
                    search_query_parts.extend(["high restart count", "frequent restarts", "restart threshold"])
                    
            if context_data.get("pod_status"):
                search_query_parts.append(f"pod status {context_data['pod_status']}")
            
            search_query = " ".join(search_query_parts)
            
            # Perform semantic search
            st.info("🔍 Performing semantic search for relevant production rules...")
            relevant_rules = semantic_search_rules(search_query, context_data, n_results=max_rules)
            
            if not relevant_rules:
                st.error("❌ No relevant PrometheusRules found")
            else:
                # Filter by similarity threshold
                filtered_rules = [r for r in relevant_rules if r['similarity_score'] >= similarity_threshold]
                
                if not filtered_rules:
                    st.warning(f"⚠️ No rules above similarity threshold {similarity_threshold}")
                    st.info("Using top 3 rules as fallback...")
                    filtered_rules = relevant_rules[:3]
                
                # Perform hybrid analysis
                st.info("🤖 Performing hybrid analysis with Senior SRE intelligence...")
                ai_analysis = analyze_with_hybrid_intelligence(search_query, context_data, filtered_rules)
                
                # Display results in tabs (same look and feel as v2)
                analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4, analysis_tab5, analysis_tab6, analysis_tab7 = st.tabs([
                    "🎯 Hybrid AI Analysis",
                    "📊 Production Rules",
                    "📋 Pod Information", 
                    "📋 Pod Events",
                    "📋 Pod Status",
                    "💾 Storage Check",
                    "🔗 Correlation"
                ])
                
                with analysis_tab1:
                    st.markdown("### 🎯 Hybrid Deep Analysis")
                    st.markdown('<div class="hybrid-badge">🧠 Senior SRE Technical Analysis + Production Rule Intelligence</div>', unsafe_allow_html=True)
                    
                    if ai_analysis.startswith("❌"):
                        st.error(ai_analysis)
                    else:
                        st.markdown(f'<div class="technical-analysis">{ai_analysis}</div>', unsafe_allow_html=True)
                
                with analysis_tab2:
                    st.markdown("### 📊 Production Alerting Rules")
                    st.markdown(f"**Found:** {len(filtered_rules)} rules above {similarity_threshold} similarity threshold")
                    
                    for rule in filtered_rules:
                        # Color code similarity score
                        if rule['similarity_score'] >= 0.8:
                            score_class = "rule-match"
                            score_emoji = "🔥"
                        elif rule['similarity_score'] >= 0.6:
                            score_class = "rule-match"
                            score_emoji = "✅"
                        else:
                            score_class = "rule-match"
                            score_emoji = "⚠️"
                        
                        st.markdown(f"""
                        <div class="technical-analysis">
                        <h5>🚨 {rule['alert_name']} ({rule['severity'].upper()})</h5>
                        <div class="{score_class}">{score_emoji} Similarity: {rule['similarity_score']:.3f}</div>
                        <p><strong>Condition:</strong> <code>{rule['expr']}</code></p>
                        <p><strong>Duration:</strong> {rule['for_duration']}</p>
                        <p><strong>Namespace:</strong> {rule['namespace']}</p>
                        <p><strong>Description:</strong> {rule['description']}</p>
                        {f'<p><strong>Runbook:</strong> <a href="{rule["runbook_url"]}" target="_blank">View Runbook</a></p>' if rule['runbook_url'] else ''}
                        </div>
                        """, unsafe_allow_html=True)
                
                with analysis_tab3:
                    st.markdown("### 📋 Pod Information")
                    pod_describe_output, _, _ = run_command(f"oc describe pod {selected_pod} -n {selected_namespace}")
                    st.text(pod_describe_output)
                
                with analysis_tab4:
                    st.markdown("### 📋 Pod Events")
                    if include_events and "events" in context_data:
                        st.text(context_data["events"])
                    else:
                        events_output, _, _ = run_command(f"oc get events -n {selected_namespace} --field-selector involvedObject.name={selected_pod}")
                        st.text(events_output)
                
                with analysis_tab5:
                    st.markdown("### 📋 Pod Status")
                    pod_status_output, _, _ = run_command(f"oc get pod {selected_pod} -n {selected_namespace} -o wide")
                    st.text(pod_status_output)
                
                with analysis_tab6:
                    st.markdown("### 💾 Storage Check (PVC Issues)")
                    pvc_output, _, _ = run_command(f"oc get pvc -n {selected_namespace}")
                    st.text(pvc_output)
                
                with analysis_tab7:
                    st.markdown("### 🔗 Correlation Analysis")
                    st.info("🔄 Korrel8r correlation available in other versions")

# Cluster Health Overview
st.markdown("---")
st.markdown("## 🏥 Cluster Health Overview")

col1, col2, col3 = st.columns(3)

with col1:
    nodes_output, _, _ = run_command("oc get nodes --no-headers")
    node_count = len([line for line in nodes_output.strip().split('\n') if line.strip()])
    ready_nodes = len([line for line in nodes_output.strip().split('\n') if 'Ready' in line])
    st.metric("Cluster Nodes", f"{ready_nodes}/{node_count} Ready")

with col2:
    pods_output, _, _ = run_command("oc get pods --all-namespaces --no-headers")
    total_pods = len([line for line in pods_output.strip().split('\n') if line.strip()])
    running_pods = len([line for line in pods_output.strip().split('\n') if 'Running' in line])
    st.metric("Total Pods", f"{running_pods}/{total_pods} Running")

with col3:
    namespaces_output, _, _ = run_command("oc get namespaces --no-headers")
    namespace_count = len([line for line in namespaces_output.strip().split('\n') if line.strip()])
    st.metric("Namespaces", namespace_count)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🎯 AI OpenShift Troubleshooter v3.2 - Hybrid Intelligence | 
    Senior SRE Analysis + Production Rule Intelligence + Vector Database</p>
</div>
""", unsafe_allow_html=True)



