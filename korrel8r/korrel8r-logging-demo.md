# 📋 Korrel8r Logging Capabilities - What It Can Do

## 🎯 **Core Logging Features**

### **1. Log Domain Classes**
Korrel8r provides **3 main log classes**:

- **📱 `application`**: Container logs from pods in user namespaces (non-kube*, non-openshift*)
- **🔍 `audit`**: Audit logs from node OS (/var/log/audit) and cluster API servers  
- **⚙️ `infrastructure`**: Node logs (journald/syslog) + container logs from system namespaces

### **2. Log Correlation Engine**
**What makes Korrel8r powerful for logging:**

#### **🔗 Cross-Domain Correlation**
- **Pod → Logs**: Find all logs for a specific pod
- **Logs → Alerts**: Correlate log errors with active alerts
- **Logs → Metrics**: Connect log patterns to performance metrics
- **Namespace → Logs**: Get all logs from a namespace
- **Node → Logs**: View all logs from a specific node

#### **📊 Relationship Discovery**
- **Automatic**: Finds related logs based on labels, namespaces, pods
- **Rule-based**: Uses predefined correlation rules
- **Temporal**: Correlates logs with events happening at same time
- **Contextual**: Groups related logs by application, service, component

### **3. Log Query Capabilities**

#### **Query Syntax Examples:**
```bash
# Get application logs from a namespace
log:application:{namespace: "my-app"}

# Get infrastructure logs from system components
log:infrastructure:{namespace: "openshift-logging"}

# Get audit logs for security analysis
log:audit:{}

# Correlate pod with its logs
k8s:Pod.v1:{name: "my-pod"} → log:application
```

### **4. Integration with OpenShift Logging Stack**

#### **✅ Built-in Loki Integration**
- **Direct connection** to OpenShift's Loki instance
- **LokiStack support** for log queries
- **Authentication** via service account tokens
- **TLS/SSL** secure connections

#### **🔄 Log Forwarding Support**
- Works with **ClusterLogForwarder**
- Supports **external Loki** instances
- **Multi-tenant** log access
- **RBAC-aware** log filtering

### **5. Practical Use Cases**

#### **🚨 Troubleshooting Workflows**
1. **Alert fired** → Find related logs → Identify root cause
2. **Pod crash** → Get logs → Find error patterns → Check metrics
3. **Performance issue** → Correlate logs with metrics → Find bottlenecks
4. **Security incident** → Audit logs → Application logs → Network logs

#### **📈 Operational Intelligence**
- **Log aggregation** across multiple services
- **Pattern recognition** in log data
- **Correlation analysis** with metrics and alerts
- **Timeline reconstruction** of incidents

### **6. API Endpoints for Logging**

#### **REST API Access:**
```bash
# List log classes
GET /api/v1alpha1/domains/log/classes

# Query logs
GET /api/v1alpha1/objects?query=log:application:{namespace:"my-app"}

# Find log correlations
GET /api/v1alpha1/neighbours?query=log:application:{namespace:"my-app"}

# Get correlation rules
GET /api/v1alpha1/rules
```

### **7. What Korrel8r Does Better Than Traditional Logging**

#### **🎯 Context-Aware Logging**
- **Not just text search** - understands Kubernetes context
- **Relationship-based** - connects logs to pods, services, nodes
- **Multi-domain** - correlates with alerts, metrics, traces

#### **🔍 Smart Discovery**
- **Automatic correlation** - finds related data without manual queries
- **Rule-based logic** - uses predefined patterns for common scenarios
- **Graph-based navigation** - explore relationships visually

#### **⚡ Efficient Querying**
- **Structured queries** - more precise than text search
- **Cross-reference** - jump between logs, metrics, alerts instantly
- **Filtered results** - RBAC-aware, namespace-scoped

## 🎪 **Demo Commands You Can Try**

### Via Web UI (Swagger):
```
https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com
```

### Via API:
```bash
# List all log classes
curl -k https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/api/v1alpha1/domains/log/classes

# Get correlation rules
curl -k https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com/api/v1alpha1/rules
```

## 🚀 **Bottom Line**

**Korrel8r transforms logging from "search in text files" to "intelligent correlation engine"** - it doesn't just store logs, it **connects the dots** between logs, metrics, alerts, and Kubernetes resources to give you the full picture of what's happening in your cluster.
