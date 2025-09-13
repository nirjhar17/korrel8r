# AI OpenShift Troubleshooter - Project Status

## ✅ **Working Deployments (Active)**

### **v2.0 - Basic AI Troubleshooter**
- **Namespace:** `ai-troubleshooter-v2`
- **Status:** ✅ Running (15h uptime)
- **Route:** https://ai-troubleshooter-gui-v2-ai-troubleshooter-v2.apps.rosa.loki123.orwi.p3.openshiftapps.com
- **Features:** Generic Kubernetes knowledge, pattern matching, verbose analysis

### **v3.1 - Vector Database RAG Implementation**
- **Namespace:** `ai-troubleshooter-v31`
- **Status:** ✅ Running (3h24m uptime)
- **Route:** https://ai-troubleshooter-gui-route-v31-ai-troubleshooter-v31.apps.rosa.loki123.orwi.p3.openshiftapps.com
- **Features:** 
  - ChromaDB vector database
  - Google AI Studio embeddings
  - PrometheusRule semantic search
  - Production rule intelligence

### **v3.2 - Admin-Focused Implementation**
- **Namespace:** `ai-troubleshooter-v32-admin`
- **Status:** ⚠️ Deployment files ready (not currently deployed)
- **Features:** Concise, actionable output format

## 🧪 **Test Environment**

### **Test Pod**
- **Name:** `crash-loop-test`
- **Namespace:** `default`
- **Status:** CrashLoopBackOff (50 restarts)
- **Purpose:** Demo scenario for crash loop analysis

## 📁 **Project Files (Kept)**

### **Core Implementations**
- `v2-complete.yaml` - Working v2.0 deployment
- `v3.1-vector-database.yaml` - Working v3.1 RAG deployment
- `v3.2-hybrid-implementation.py` - v3.2 Python code
- `v3.2-admin-focused-deployment.yaml` - v3.2 deployment

### **Documentation**
- `demo-showcase.md` - Demo scenarios and comparison
- `v3.2-admin-focused-prompt.md` - System prompt documentation
- `v3.2-hybrid-system-prompt.md` - Hybrid system prompt
- `test-scenarios-summary.md` - Test scenarios
- `QUICK_START.md` - Quick start guide
- `README_OpenShift_AI.md` - Project documentation

### **Utilities**
- `extract_prometheus_rules.py` - PrometheusRule extraction utility
- `export-feature.py` - Export functionality for Streamlit
- `export-script.py` - Command-line export script
- `config.env.example` - Configuration template
- `Dockerfile` - Docker configuration

## 🗑️ **Cleaned Up Files (Removed)**

- 60+ test files and duplicates
- Temporary deployment files
- Broken implementations
- Development artifacts

## 🚀 **Quick Access**

### **Demo Routes**
- **v2.0:** https://ai-troubleshooter-gui-v2-ai-troubleshooter-v2.apps.rosa.loki123.orwi.p3.openshiftapps.com
- **v3.1 (RAG):** https://ai-troubleshooter-gui-route-v31-ai-troubleshooter-v31.apps.rosa.loki123.orwi.p3.openshiftapps.com

### **Test Pod**
```bash
oc get pods -n default | grep crash-loop-test
```

### **Health Check**
```bash
oc get pods --all-namespaces | grep troubleshooter | grep Running
```

## 📊 **Architecture Summary**

| Version | Status | Intelligence | Output Format | Production Rules |
|---------|--------|--------------|---------------|------------------|
| v2.0 | ✅ Active | Generic AI | Verbose | ❌ None |
| v3.1 | ✅ Active | RAG + Vector DB | Detailed | ✅ Integrated |
| v3.2 | 📁 Ready | RAG + Admin-focused | Concise | ✅ Integrated |

## 🎯 **Next Steps**

1. **For Demo:** Use v3.1 route with crash-loop-test pod
2. **For v3.2:** Deploy when ready for admin-focused testing
3. **For Maintenance:** Run health checks weekly
4. **For New Project:** Use different namespaces to avoid conflicts

---
*Last Updated: September 13, 2025*
*Project Status: Active and Ready for Demo*


