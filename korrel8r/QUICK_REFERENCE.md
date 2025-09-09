# 🚀 Quick Reference Guide

## 📱 **Application Access**
```
🌐 URL: https://ai-troubleshooter-gui-ai-troubleshooter.apps.rosa.loki123.orwi.p3.openshiftapps.com
```

---

## 🎯 **Quick Commands**

### **Check Status**
```bash
# Application status
oc get pods -n ai-troubleshooter

# Get application URL
oc get route ai-troubleshooter-gui -n ai-troubleshooter

# Test pods status
oc get pods -n test-problematic-pods

# Korrel8r status
oc get pods -n korrel8r
```

### **Restart Application**
```bash
# Restart the troubleshooter
oc rollout restart deployment/ai-troubleshooter-gui -n ai-troubleshooter

# Check rollout status
oc rollout status deployment/ai-troubleshooter-gui -n ai-troubleshooter
```

### **View Logs**
```bash
# Application logs
oc logs -n ai-troubleshooter deployment/ai-troubleshooter-gui -f

# Recent events
oc get events -n ai-troubleshooter --sort-by='.lastTimestamp'
```

---

## 🧪 **Test Scenarios**

### **Available Test Pods**
| Pod Name | Expected Status | Problem Type |
|----------|----------------|--------------|
| `crashloop-app` | 🔴 CrashLoopBackOff | App crashes |
| `invalid-image-app` | 🔴 ErrImagePull | Invalid image |
| `resource-hungry-app` | 🟡 Pending | Resource limits |
| `running-with-warnings` | 🟢 Running | Warnings in logs |

### **Test Workflow**
1. Select `test-problematic-pods` namespace
2. Choose any test pod
3. Click "🤖 Run AI Analysis"
4. Review AI recommendations

---

## 🤖 **AI Analysis Features**

### **What You Get**
- **🔍 Root Cause Analysis**: Primary issue identification
- **📊 Impact Assessment**: Criticality evaluation
- **⚡ Step-by-Step Solutions**: Actionable remediation
- **🛡️ Prevention Strategies**: Future issue prevention
- **📋 Technical Details**: 7-step diagnostic data

### **Analysis Steps**
1. **Pod Information** - Specs and configuration
2. **Pod Events** - Historical events and changes
3. **Pod Status** - Current state and conditions
4. **Storage Check** - PVC and volume analysis
5. **Node Availability** - Cluster resource status
6. **Korrel8r Integration** - Log domain correlation
7. **Vector Status** - Log collection health

---

## 🌐 **Multi-Cluster Features**

### **Cluster Management**
- **🏗️ Cluster Selection**: Dynamic cluster switching
- **📊 Context Display**: Server, user, and status info
- **🔄 Seamless Switching**: One-click context changes
- **🎯 Auto-Discovery**: Automatic cluster detection

### **Usage**
1. Select cluster from dropdown
2. Click "Switch to [cluster]" if needed
3. Choose namespace (auto-refreshed per cluster)
4. Select pod and analyze

---

## 🔧 **Configuration**

### **Key Settings**
```bash
# Groq AI Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_ENDPOINT=https://api.groq.com/openai/v1/chat/completions
GROQ_MODEL=llama-3.3-70b-versatile
```

### **Permissions Required**
- **cluster-admin** role for comprehensive analysis
- **Service Account**: `ai-troubleshooter-sa`
- **Namespace**: `ai-troubleshooter`

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **No Pods Listed**
```bash
# Check permissions
oc auth can-i get pods --as=system:serviceaccount:ai-troubleshooter:ai-troubleshooter-sa

# Verify cluster connection
oc get namespaces
```

#### **AI Analysis Fails**
```bash
# Test Groq API
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}'
```

#### **Application Won't Load**
```bash
# Check pod status
oc get pods -n ai-troubleshooter

# Check route
oc get route ai-troubleshooter-gui -n ai-troubleshooter

# View logs
oc logs -n ai-troubleshooter deployment/ai-troubleshooter-gui --tail=50
```

---

## 📊 **Performance**

### **Expected Performance**
- **Analysis Time**: 20-30 seconds per pod
- **Memory Usage**: 512MB-1GB during analysis
- **Concurrent Users**: Multiple sessions supported
- **Scalability**: 1000+ pods per namespace

### **Resource Monitoring**
```bash
# Check resource usage
oc adm top pods -n ai-troubleshooter

# Monitor over time
watch oc adm top pods -n ai-troubleshooter
```

---

## 🎯 **Best Practices**

### **Usage Tips**
1. **Start with Test Pods**: Use `test-problematic-pods` to learn the interface
2. **Review All Tabs**: Check both AI analysis and technical details
3. **Multi-Cluster**: Switch clusters to analyze different environments
4. **Save Results**: Copy important AI recommendations for documentation

### **Operational Guidelines**
1. **Regular Monitoring**: Check application health weekly
2. **API Key Rotation**: Update Groq API key as needed
3. **Resource Scaling**: Monitor and adjust resources based on usage
4. **Security Reviews**: Periodically review RBAC permissions

---

## 🔗 **Important Links**

- **Application**: https://ai-troubleshooter-gui-ai-troubleshooter.apps.rosa.loki123.orwi.p3.openshiftapps.com
- **Groq Console**: https://console.groq.com/
- **Korrel8r Docs**: https://korrel8r.github.io/korrel8r/
- **OpenShift Docs**: https://docs.openshift.com/

---

## 📞 **Support Checklist**

Before seeking help, verify:
- [ ] Application pod is running
- [ ] Route is accessible
- [ ] Groq API key is valid
- [ ] Service account has permissions
- [ ] Test pods are available
- [ ] Cluster connection is working

---

**🎉 You're all set! Happy troubleshooting with AI power!**
