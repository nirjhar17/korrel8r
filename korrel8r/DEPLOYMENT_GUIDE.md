# 🚀 Step-by-Step Deployment Guide

## 📋 **Prerequisites Checklist**

Before starting, ensure you have:
- [ ] OpenShift cluster access with `cluster-admin` privileges
- [ ] `oc` CLI installed and configured
- [ ] Internet access for downloading dependencies
- [ ] Groq API account and key (free tier available)

---

## 🎯 **Step 1: Verify OpenShift Access**

```bash
# Test cluster connection
oc whoami
oc get nodes

# Check current context
oc config current-context

# List available clusters (for multi-cluster setup)
oc config get-clusters
```

**Expected Output:**
```
system:admin
NAME                                          STATUS   ROLES           AGE   VERSION
ip-10-0-137-189.eu-north-1.compute.internal   Ready    worker          1d    v1.29.14
```

---

## 🤖 **Step 2: Set Up Groq AI**

### **Get Your Free Groq API Key:**
1. Visit: https://console.groq.com/
2. Sign up for free account
3. Generate API key
4. Copy the key (format: `gsk_...`)

### **Test Your API Key:**
```bash
curl -X POST "https://api.groq.com/openai/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
  }'
```

**Expected Output:**
```json
{
  "choices": [
    {
      "message": {
        "content": "Hello! How can I help you today?"
      }
    }
  ]
}
```

---

## 🏗️ **Step 3: Deploy Korrel8r Operator (Optional)**

### **Install Korrel8r Operator:**
```bash
# Create korrel8r namespace
oc create namespace korrel8r

# Apply operator subscription
cat <<EOF | oc apply -f -
apiVersion: operators.coreos.com/v1
kind: OperatorGroup
metadata:
  name: korrel8r-operator-group
  namespace: korrel8r
spec:
  targetNamespaces:
  - korrel8r
---
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: korrel8r
  namespace: korrel8r
spec:
  channel: stable
  name: korrel8r
  source: community-operators
  sourceNamespace: openshift-marketplace
EOF
```

### **Verify Operator Installation:**
```bash
# Check operator pod
oc get pods -n korrel8r

# Check CSV (ClusterServiceVersion)
oc get csv -n korrel8r
```

### **Deploy Korrel8r Instance:**
```bash
cat <<EOF | oc apply -f -
apiVersion: korrel8r.openshift.io/v1alpha1
kind: Korrel8r
metadata:
  name: korrel8r
  namespace: korrel8r
spec:
  debug:
    verbose: 1
  route:
    enabled: true
  stores:
    - domain: k8s
    - domain: alert
      alertmanager: 'https://alertmanager-main-openshift-monitoring.apps.YOUR_CLUSTER_DOMAIN'
      metrics: 'https://thanos-querier-openshift-monitoring.apps.YOUR_CLUSTER_DOMAIN'
    - domain: log
      lokiStack: 'https://logging-loki-gateway-http.openshift-logging.svc:8080'
      direct: true
    - domain: metric
      metric: 'https://thanos-querier-openshift-monitoring.apps.YOUR_CLUSTER_DOMAIN'
EOF
```

---

## 🧪 **Step 4: Create Test Pods**

### **Deploy Test Problematic Pods:**
```bash
# Create test namespace with sample failing pods
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: test-problematic-pods
---
# CrashLoopBackOff Pod
apiVersion: v1
kind: Pod
metadata:
  name: crashloop-app
  namespace: test-problematic-pods
spec:
  containers:
  - name: failing-app
    image: busybox:latest
    command: ["sh", "-c"]
    args:
    - |
      echo "Starting application..."
      echo "ERROR: Database connection failed!"
      exit 1
---
# ImagePullBackOff Pod
apiVersion: v1
kind: Pod
metadata:
  name: invalid-image-app
  namespace: test-problematic-pods
spec:
  containers:
  - name: invalid-image
    image: nonexistent/invalid-image:v999
---
# Pending Pod (Resource Constraints)
apiVersion: v1
kind: Pod
metadata:
  name: resource-hungry-app
  namespace: test-problematic-pods
spec:
  containers:
  - name: hungry-app
    image: nginx:alpine
    resources:
      requests:
        memory: "16Gi"  # Unrealistic request
        cpu: "8"
---
# Running Pod with Warnings
apiVersion: v1
kind: Pod
metadata:
  name: running-with-warnings
  namespace: test-problematic-pods
spec:
  containers:
  - name: warning-app
    image: busybox:latest
    command: ["sh", "-c"]
    args:
    - |
      echo "Application started successfully"
      while true; do
        echo "WARNING: High memory usage detected"
        sleep 30
      done
EOF
```

### **Verify Test Pods:**
```bash
oc get pods -n test-problematic-pods
```

**Expected Output:**
```
NAME                    READY   STATUS                  RESTARTS     AGE
crashloop-app           0/1     CrashLoopBackOff        3 (1m ago)   2m
invalid-image-app       0/1     ErrImagePull            0            2m
resource-hungry-app     0/1     Pending                 0            2m
running-with-warnings   1/1     Running                 0            2m
```

---

## 🤖 **Step 5: Deploy AI Troubleshooter**

### **Create the Complete Deployment:**
```bash
cat <<EOF | oc apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: ai-troubleshooter
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ai-troubleshooter-sa
  namespace: ai-troubleshooter
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ai-troubleshooter-cluster-reader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: ai-troubleshooter-sa
  namespace: ai-troubleshooter
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-troubleshooter-gui
  namespace: ai-troubleshooter
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-troubleshooter-gui
  template:
    metadata:
      labels:
        app: ai-troubleshooter-gui
    spec:
      serviceAccountName: ai-troubleshooter-sa
      containers:
      - name: streamlit-gui
        image: python:3.9-slim
        ports:
        - containerPort: 8501
        command: ["/bin/bash", "-c"]
        args:
        - |
          # Install required packages
          pip install --no-cache-dir streamlit pandas requests python-dotenv kubernetes
          
          # Install system dependencies
          apt-get update && apt-get install -y curl wget
          
          # Install oc CLI
          wget -O /tmp/oc.tar.gz https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz
          tar -xzf /tmp/oc.tar.gz -C /usr/local/bin/
          chmod +x /usr/local/bin/oc
          
          # Run Streamlit app (will be created via ConfigMap)
          streamlit run /app/ai-troubleshooter-gui.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
        volumeMounts:
        - name: app-code
          mountPath: /app
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: app-code
        configMap:
          name: ai-troubleshooter-app
---
apiVersion: v1
kind: Service
metadata:
  name: ai-troubleshooter-gui
  namespace: ai-troubleshooter
spec:
  ports:
  - port: 8501
    targetPort: 8501
    protocol: TCP
  selector:
    app: ai-troubleshooter-gui
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: ai-troubleshooter-gui
  namespace: ai-troubleshooter
spec:
  to:
    kind: Service
    name: ai-troubleshooter-gui
  port:
    targetPort: 8501
  tls:
    termination: edge
EOF
```

### **Upload the AI Application Code:**
```bash
# This creates the ConfigMap with the Streamlit application
# (The actual Python code would be too large to include here inline)
# You would use the ai-enhanced-troubleshooter.py file we created

oc create configmap ai-troubleshooter-app \
  -n ai-troubleshooter \
  --from-file=ai-troubleshooter-gui.py=ai-enhanced-troubleshooter.py
```

---

## ✅ **Step 6: Verify Deployment**

### **Check All Components:**
```bash
# Check namespace creation
oc get namespaces | grep -E "(ai-troubleshooter|test-problematic-pods|korrel8r)"

# Check AI troubleshooter deployment
oc get all -n ai-troubleshooter

# Check test pods
oc get pods -n test-problematic-pods

# Check Korrel8r (if installed)
oc get all -n korrel8r
```

### **Get the Application URL:**
```bash
oc get route ai-troubleshooter-gui -n ai-troubleshooter -o jsonpath='https://{.spec.host}'
```

### **Test Application Access:**
```bash
# Get the URL and open in browser
echo "Your AI Troubleshooter is available at:"
oc get route ai-troubleshooter-gui -n ai-troubleshooter -o jsonpath='https://{.spec.host}'
```

---

## 🧪 **Step 7: Test the Application**

### **Basic Functionality Test:**
1. **Open the URL** in your web browser
2. **Select Cluster**: Choose your cluster from dropdown
3. **Select Namespace**: Choose `test-problematic-pods`
4. **Select Pod**: Choose `crashloop-app`
5. **Run Analysis**: Click "🤖 Run AI Analysis"
6. **Review Results**: See AI-powered analysis and recommendations

### **Expected Results:**
- **Cluster Information**: Shows current cluster details
- **Pod Selection**: Lists all test pods with status indicators
- **AI Analysis**: Provides root cause analysis and solutions
- **Technical Details**: Shows 7-step diagnostic information

---

## 🔧 **Step 8: Troubleshooting**

### **Common Issues and Solutions:**

#### **Pod Not Starting:**
```bash
# Check pod logs
oc logs -n ai-troubleshooter deployment/ai-troubleshooter-gui

# Check events
oc get events -n ai-troubleshooter --sort-by='.lastTimestamp'
```

#### **Permission Issues:**
```bash
# Verify service account permissions
oc describe clusterrolebinding ai-troubleshooter-cluster-reader

# Test cluster access from pod
oc exec -n ai-troubleshooter deployment/ai-troubleshooter-gui -- oc get namespaces
```

#### **Groq API Issues:**
```bash
# Test API from pod
oc exec -n ai-troubleshooter deployment/ai-troubleshooter-gui -- curl -X POST "https://api.groq.com/openai/v1/chat/completions" -H "Authorization: Bearer YOUR_API_KEY" -H "Content-Type: application/json" -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10}'
```

---

## 📊 **Step 9: Monitoring and Maintenance**

### **Monitor Application Health:**
```bash
# Check pod status
oc get pods -n ai-troubleshooter

# Monitor resource usage
oc adm top pods -n ai-troubleshooter

# Check application logs
oc logs -n ai-troubleshooter deployment/ai-troubleshooter-gui -f
```

### **Regular Maintenance:**
- **Update Groq API Key**: If expired or rotated
- **Monitor Resource Usage**: Scale if needed
- **Update Dependencies**: Keep Python packages current
- **Backup Configuration**: Save ConfigMaps and deployment files

---

## 🎯 **Step 10: Next Steps**

### **Extend Functionality:**
1. **Add More Clusters**: Configure additional cluster contexts
2. **Custom Test Pods**: Create pods with your specific failure scenarios
3. **Integration**: Connect with your existing monitoring tools
4. **Automation**: Use the analysis results in automated workflows

### **Advanced Configuration:**
1. **Resource Tuning**: Adjust CPU/memory based on usage
2. **High Availability**: Scale to multiple replicas
3. **Security**: Implement more restrictive RBAC if needed
4. **Monitoring**: Add metrics and alerting for the troubleshooter itself

---

## ✅ **Deployment Complete!**

🎉 **Congratulations!** You now have a fully functional AI-powered troubleshooting platform that combines:

- ✅ **Multi-cluster OpenShift access**
- ✅ **Real AI analysis with Groq LLaMA-3.3-70B**
- ✅ **Korrel8r observability correlation**
- ✅ **Professional web interface**
- ✅ **Test scenarios for validation**
- ✅ **Comprehensive 7-step analysis**

**🚀 Your AI troubleshooter is ready to revolutionize your OpenShift operations!**
