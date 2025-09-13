# 🚀 Quick Start Guide - OpenShift AI Log Analyzer

## 📋 **What You Need**

### **1. OpenShift Cluster**
- OpenShift cluster with logging enabled
- `oc` CLI installed and configured
- Cluster admin permissions

### **2. API Keys (Required)**
- **Groq API Key**: Get from https://console.groq.com (FREE)
- **Slack Webhook** (optional): For alerts

### **3. 5 Minutes Setup Time**

## ⚡ **Super Quick Setup**

### **Step 1: Get Groq API Key (2 minutes)**
1. Go to https://console.groq.com
2. Sign up (free account)
3. Create an API key
4. Copy the key (starts with `gsk_`)

### **Step 2: Configure (1 minute)**
```bash
# Copy the example config
cp config.env.example .env

# Edit .env file with your API key
nano .env
```

**Minimum required in .env:**
```bash
GROQ_API_KEY=gsk_your_actual_key_here
USE_GROQ=true
```

### **Step 3: Deploy (2 minutes)**
```bash
# Run the automated setup
python setup_openshift_ai.py
```

**That's it!** 🎉

## 🔍 **What Happens Next**

1. **System deploys** to your OpenShift cluster
2. **Log forwarding** is configured automatically
3. **AI starts analyzing** your OpenShift logs
4. **Dashboard becomes available** via OpenShift route
5. **Problems are highlighted** automatically
6. **Click any problem** for AI solutions

## 📊 **Access Your Dashboard**

After deployment, you'll get a URL like:
```
https://ai-log-analyzer-route-openshift-ai-analyzer.apps.your-cluster.com
```

## 🎯 **What You'll See**

### **Dashboard View:**
- 🚨 **Critical Issues** (red) - Node failures, operator crashes
- ⚠️ **High Priority** (orange) - Network issues, storage problems  
- 🔶 **Medium Priority** (yellow) - Application errors
- ℹ️ **Low Priority** (green) - Warnings

### **AI Solutions:**
Click any problem to get:
- Root cause analysis
- Step-by-step fixes
- OpenShift commands to run
- Prevention tips

## 🚨 **Troubleshooting**

### **If deployment fails:**
```bash
# Check cluster connection
oc whoami

# Check if you have admin permissions
oc auth can-i create deployments --all-namespaces
```

### **If no logs appear:**
```bash
# Check log forwarding
oc get clusterlogforwarder -n openshift-logging

# Check AI analyzer logs
oc logs -n openshift-ai-analyzer deployment/ai-log-analyzer
```

### **If AI analysis doesn't work:**
- Verify Groq API key in `.env` file
- Check API key has credits (Groq gives free credits)
- Review network connectivity

## 💡 **Pro Tips**

1. **Start with critical issues** - they need immediate attention
2. **Use AI solutions** - click problems for intelligent fixes
3. **Set up Slack alerts** - get notified of new problems
4. **Monitor trends** - dashboard shows problem patterns

## 🆘 **Need Help?**

1. Check the logs: `oc logs -n openshift-ai-analyzer deployment/ai-log-analyzer`
2. Review the full README: `README_OpenShift_AI.md`
3. Verify your configuration in `.env` file

---

**Ready to get AI-powered OpenShift insights? Let's go!** 🚀

