# 🎯 **Korrel8r Operator - Logging Capabilities**

## ✅ **What Korrel8r CAN DO for Logging**

### **1. 📊 Three Types of Log Analysis**

**✅ WORKING:** Log domain classes are active and accessible:

#### **🚀 Application Logs**
- **What**: Container logs from user application pods
- **Scope**: All namespaces NOT starting with `kube-` or `openshift-`
- **Use Cases**: 
  - Debug application errors
  - Track user transactions
  - Monitor business logic
  - Performance troubleshooting

#### **🔒 Audit Logs** 
- **What**: Security and compliance logs
- **Scope**: Node OS audit logs (`/var/log/audit`) + API server audit
- **Use Cases**:
  - Security incident investigation
  - Compliance reporting
  - Access control monitoring
  - Policy violation detection

#### **⚙️ Infrastructure Logs**
- **What**: System and platform logs
- **Scope**: Node logs (journald/syslog) + OpenShift system pods
- **Use Cases**:
  - Platform troubleshooting
  - System health monitoring
  - Cluster operation analysis
  - Infrastructure debugging

### **2. 🔗 Log Correlation Engine**

**✅ WORKING:** Korrel8r connects logs to other observability data:

#### **Cross-Domain Relationships**
```bash
Pod → Application Logs     # Find logs for specific pod
Alert → Related Logs       # Get logs when alert fires  
Metric → Log Context      # Connect performance to logs
Node → Infrastructure     # All logs from a node
Namespace → All Logs      # Complete namespace view
```

#### **Intelligent Correlation**
- **Automatic**: Based on labels, namespaces, timestamps
- **Contextual**: Groups related log entries
- **Multi-dimensional**: Combines logs + metrics + alerts
- **Timeline-based**: Correlates events by time

### **3. 🌐 Integration with OpenShift Logging**

**✅ CONFIRMED:** Korrel8r is connected to your cluster's logging:

#### **Loki Integration**
- **✅ Connected** to `logging-loki-gateway-http.openshift-logging.svc:8080`
- **✅ Authenticated** via service account
- **✅ TLS secured** connections
- **✅ Multi-tenant** access control

#### **Log Sources**
- **Container logs** from all pods
- **Node system logs** (journald)
- **Audit logs** from API servers
- **Network logs** (if NetObserv enabled)

### **4. 🎪 **What You Can Do RIGHT NOW**

#### **Via Web Interface (Swagger UI):**
```
🌐 https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com
```

**Available Operations:**
- ✅ **Browse log classes** - See application/audit/infrastructure categories
- ✅ **Explore API endpoints** - Interactive Swagger documentation
- ✅ **Test queries** - Try correlation queries
- ✅ **View relationships** - See how logs connect to other data

#### **Working API Calls:**
```bash
# List log types
curl -k https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/api/v1alpha1/domains/log/classes

# Get all domains  
curl -k https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/api/v1alpha1/domains
```

### **5. 🚀 **Practical Logging Workflows**

#### **Scenario 1: Application Troubleshooting**
1. **Pod crashes** → Query `log:application:{namespace: "my-app"}`
2. **Get related alerts** → Correlate with metric alerts
3. **Check infrastructure** → View node logs for context
4. **Timeline analysis** → See sequence of events

#### **Scenario 2: Security Investigation**
1. **Security alert** → Query `log:audit:{}`
2. **Find user actions** → Trace API calls
3. **Check application logs** → See if apps affected
4. **Cross-reference** → Connect audit → apps → infrastructure

#### **Scenario 3: Performance Analysis**
1. **Slow response** → Get `log:application` for errors
2. **Check metrics** → CPU/memory correlation
3. **Infrastructure logs** → Node resource issues
4. **Full picture** → Logs + metrics + alerts together

### **6. 🎯 **Key Benefits Over Traditional Logging**

#### **🔍 Context-Aware**
- **Not just grep** - understands Kubernetes relationships
- **Smart grouping** - automatically relates logs to pods/services
- **Cross-domain** - connects logs to metrics and alerts

#### **⚡ Efficient**
- **Structured queries** - more precise than text search
- **Relationship-based** - find related data instantly
- **RBAC-aware** - respects namespace permissions

#### **🎪 Visual Exploration**
- **Interactive API** - Swagger UI for exploration
- **Correlation discovery** - find unexpected relationships
- **Graph navigation** - visual data relationships

## 🎉 **Summary: What Korrel8r Does for Logging**

**Korrel8r transforms your OpenShift logging from "search text files" to "intelligent correlation engine":**

✅ **Connected** to your cluster's Loki instance  
✅ **Categorizes** logs into application/audit/infrastructure  
✅ **Correlates** logs with pods, alerts, metrics automatically  
✅ **Provides API** for programmatic access  
✅ **Web interface** for interactive exploration  
✅ **RBAC integration** for secure access  

**🎯 Bottom Line:** Korrel8r gives you **context-aware logging** - it doesn't just show you logs, it shows you **why they matter** and **what they're related to** in your cluster!
