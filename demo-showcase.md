# AI Troubleshooter Demo Showcase

## **Demo Scenarios for Comparison**

### **Scenario 1: Pod Crash Loop**
```bash
# Create test pod
oc run crash-loop-test --image=registry.access.redhat.com/ubi8/ubi-minimal:latest \
  --restart=Always \
  --command -- /bin/sh -c "echo 'Starting application...'; sleep 5; echo 'Application crashed!'; exit 1"
```

**Expected v2.0 Output**: 500+ words of technical analysis
**Expected v3.2 Output**: 4-line actionable summary

### **Scenario 2: Memory Issues**
```bash
# Create memory-intensive pod
oc run memory-test --image=registry.access.redhat.com/ubi8/ubi-minimal:latest \
  --limits=memory=100Mi \
  --command -- /bin/sh -c "while true; do dd if=/dev/zero of=/tmp/memory bs=1M count=200; sleep 10; done"
```

### **Scenario 3: Image Pull Issues**
```bash
# Create pod with invalid image
oc run image-pull-test --image=invalid-registry/invalid-image:latest
```

## **Demo Script**

### **Step 1: Show v3.1 Current Output**
1. Access: https://ai-troubleshooter-gui-route-v31-ai-troubleshooter-v31.apps.rosa.loki123.orwi.p3.openshiftapps.com
2. Select `default` namespace
3. Select problematic pod
4. Show verbose analysis

### **Step 2: Deploy v3.2 Admin-Focused**
```bash
# Deploy v3.2 with admin-focused output
oc apply -f v3.2-admin-focused-deployment.yaml
```

### **Step 3: Side-by-Side Comparison**
1. Open both versions in different tabs
2. Test same pod issue
3. Show difference in output format

## **Key Metrics to Highlight**

| Metric | v2.0 | v3.2 |
|--------|------|------|
| **Output Length** | 500+ words | <50 words |
| **Time to Action** | 2-3 minutes reading | 10 seconds |
| **Specificity** | Generic advice | Production-validated |
| **Actionability** | Multiple options | Direct commands |

## **Demo Talking Points**

1. **"v2.0 gives you a textbook"** - Long explanations, generic advice
2. **"v3.2 gives you a senior engineer"** - Immediate actions, production context
3. **"v3.2 knows your setup"** - Uses your actual alerting rules
4. **"v3.2 saves time"** - From minutes to seconds for actionable insights


