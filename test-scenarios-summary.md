# 🧪 Test Scenarios for AI Analysis in Default Namespace

## Available Test Pods for Vector Database Analysis

### 1. **crash-loop-pod** - CrashLoopBackOff
- **Status**: `CrashLoopBackOff` with 4+ restarts
- **Issue**: Container exits with code 1 after 5 seconds
- **Expected AI Analysis**: Should find `KubePodCrashLooping` rule with high similarity
- **Test Focus**: Crash loop detection and restart policies

### 2. **init-fail-pod** - Init Container Failure  
- **Status**: `Init:CrashLoopBackOff` with 4+ restarts
- **Issue**: Init container fails with exit code 1
- **Expected AI Analysis**: Should identify init container issues and blocking main container
- **Test Focus**: Init container failure patterns

### 3. **invalid-image-pod** - Image Pull Failure
- **Status**: `ImagePullBackOff`
- **Issue**: References nonexistent image `nonexistent-registry.com/fake/image:latest`
- **Expected AI Analysis**: Should identify image availability issues
- **Test Focus**: Registry and image pull problems

### 4. **missing-volume-pod** - Volume Mount Failure
- **Status**: `Pending` 
- **Issue**: References nonexistent PVC `does-not-exist-pvc`
- **Expected AI Analysis**: Should identify storage/volume mounting issues
- **Test Focus**: Storage and PVC problems

### 5. **configmap-fail-pod** - ConfigMap Mount Failure
- **Status**: `ContainerCreating` (stuck)
- **Issue**: References nonexistent ConfigMap `nonexistent-configmap`
- **Expected AI Analysis**: Should identify configuration mounting issues
- **Test Focus**: ConfigMap availability problems

### 6. **secret-fail-pod** - Secret Mount Failure  
- **Status**: `ContainerCreating` (stuck)
- **Issue**: References nonexistent Secret `nonexistent-secret`
- **Expected AI Analysis**: Should identify secret mounting issues
- **Test Focus**: Secret availability problems

### 7. **probe-failure-xxx** - Readiness/Liveness Probe Failure
- **Status**: `Running` but not `Ready` (0/1)
- **Issue**: HTTP probes fail on nonexistent endpoints
- **Expected AI Analysis**: Should identify probe configuration issues
- **Test Focus**: Health check and probe failures

### 8. **resource-limited-pod** - Resource Constraints
- **Status**: `Running` (1/1) but potentially under stress
- **Issue**: Attempts to allocate 200MB with 50MB limit
- **Expected AI Analysis**: Should identify resource constraint issues
- **Test Focus**: Memory limits and resource management

## 🎯 Testing Strategy

### Test Each Scenario Against:
1. **v2.0** - Generic analysis without rules
2. **v3.0** - All 208 rules (context overload)  
3. **v3.1** - Semantic search with relevant rules

### Expected Improvements in v3.1:
- **Specific Rule Matching**: Find relevant PrometheusRules for each issue type
- **Similarity Scoring**: High scores for matching issues
- **Timeline Predictions**: Alert firing timelines from rules
- **Actionable Commands**: Specific troubleshooting steps
- **Root Cause Analysis**: Rule-based problem identification

### Key Rules Expected to Match:
- `KubePodCrashLooping` → crash-loop-pod, init-fail-pod
- `KubePodNotReady` → probe-failure pods
- `KubeContainerWaiting` → image pull and volume issues
- `KubePodRestartingTooMuch` → multiple restart scenarios
- Resource-related rules → resource-limited-pod

## 🔧 Quick Test Commands

```bash
# Check all pod statuses
oc get pods -n default

# Test specific pod analysis in v3.1
# Navigate to: https://ai-troubleshooter-gui-route-v31-ai-troubleshooter-v31.apps.rosa.loki123.orwi.p3.openshiftapps.com
# Select: Namespace: default
# Select: Pod: [any of the above pods]
# Click: Start Full Semantic Analysis
```

## 🎯 Success Metrics

### v3.1 Should Demonstrate:
✅ **Precision**: Relevant rules found with high similarity scores  
✅ **Conciseness**: Admin-focused 4-point analysis format  
✅ **Actionability**: Specific commands and next steps  
✅ **Intelligence**: Rule-based insights vs generic troubleshooting  
✅ **Variety**: Different rule types for different failure patterns  

### Comparison Points:
- **Rule Relevance**: v3.1 finds specific vs v2.0 generic
- **Analysis Depth**: v3.1 rule-based vs v2.0 surface-level  
- **Actionability**: v3.1 specific commands vs v2.0 general advice
- **Context Awareness**: v3.1 production thresholds vs v2.0 assumptions





