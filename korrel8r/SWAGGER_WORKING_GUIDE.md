# 🎯 KORREL8R SWAGGER - WORKING SOLUTION

## ✅ **ISSUE RESOLVED!**

**Problem**: You were trying the root URL which returns 404  
**Solution**: Use the **full Swagger path**

## 🌐 **CORRECT SWAGGER URL:**
```
https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/swagger/index.html
```

## 🎪 **WHAT YOU'LL SEE IN SWAGGER:**

### **1. Interactive API Documentation**
- **REST API v1alpha1** for Korrel8r correlation engine
- **Try it out** buttons for each endpoint
- **Live testing** with your cluster data
- **JSON responses** with real results

### **2. Available Endpoints:**
- **`/api/v1alpha1/domains`** - List all available domains
- **`/api/v1alpha1/domains/log/classes`** - Show log categories
- **`/api/v1alpha1/objects`** - Query objects (when working)
- **`/api/v1alpha1/neighbours`** - Find correlations (when working)

## 🔧 **WORKING FEATURES RIGHT NOW:**

### **✅ Domains Available:**
- **alert** - Connected to AlertManager
- **k8s** - Kubernetes resources (permission issues)
- **log** - Connected to Loki (3 categories)
- **metric** - Connected to Prometheus/Thanos
- **mock** - Test data
- **netflow** - Network flows
- **trace** - Distributed tracing

### **✅ Log Categories Working:**
- **application**: Your apps (openshift-ai-analyzer, korrel8r, etc.)
- **audit**: Security and compliance logs
- **infrastructure**: OpenShift system logs

## 📋 **COMMAND LINE ALTERNATIVES:**

While you explore Swagger, you can also test directly:

```bash
# List domains
curl -k -s https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/api/v1alpha1/domains | jq -r '.[].name'

# Check log categories
curl -k -s https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/api/v1alpha1/domains/log/classes

# Use AI troubleshooter
./quick-troubleshooter.sh openshift-ai-analyzer cluster-selector-analyzer
```

## 🎯 **WHAT TO DO IN SWAGGER:**

1. **Open the correct URL** above
2. **Expand `/api/v1alpha1/domains`** section
3. **Click "Try it out"** button
4. **Click "Execute"** to see all domains
5. **Expand `/api/v1alpha1/domains/log/classes`** 
6. **Test log categories** the same way
7. **Explore other endpoints** as available

## 🚀 **EXPECTED RESULTS:**

**Domains Query** will show:
```json
[
  {"name": "alert", "stores": [...]},
  {"name": "log", "stores": [...]},
  {"name": "metric", "stores": [...]}
]
```

**Log Classes Query** will show:
```json
{
  "application": "Container logs from pods...",
  "audit": "Audit logs from the node OS...",
  "infrastructure": "Node logs and container logs..."
}
```

## 🎪 **BOTTOM LINE:**

**The Swagger interface IS working** - you just needed the full `/swagger/index.html` path!

**Now you can explore all Korrel8r capabilities interactively through the web interface.** 🎉
