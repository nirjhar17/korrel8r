#!/bin/bash

echo "🧹 Cleaning up project files..."

# Files to KEEP (working versions)
KEEP_FILES=(
    "v2-complete.yaml"                    # Working v2 deployment
    "v3.1-vector-database.yaml"          # Working v3.1 deployment  
    "v3.2-hybrid-implementation.py"      # v3.2 implementation
    "v3.2-admin-focused-deployment.yaml" # v3.2 deployment
    "extract_prometheus_rules.py"        # Utility script
    "demo-showcase.md"                   # Demo documentation
    "v3.2-admin-focused-prompt.md"       # System prompt documentation
    "v3.2-hybrid-system-prompt.md"       # System prompt documentation
    "test-scenarios-summary.md"          # Test scenarios
    "export-feature.py"                  # Export functionality
    "export-script.py"                   # Export script
    "config.env.example"                 # Configuration example
    "Dockerfile"                         # Docker configuration
    "QUICK_START.md"                     # Quick start guide
    "README_OpenShift_AI.md"             # Documentation
)

# Files to REMOVE (test files and duplicates)
REMOVE_FILES=(
    # Test and temporary files
    "ai-enhanced-troubleshooter-v3-complete.py"
    "ai-enhanced-troubleshooter-v3-mcp-integrated.py"
    "ai-enhanced-troubleshooter-v3-with-rules.py"
    "ai-enhanced-troubleshooter-v3.1-vector.py"
    "ai-troubleshooter-v3-complete-working.yaml"
    "ai-troubleshooter-v3-final-deployment.yaml"
    "v2-exact-code.py"
    "v3-clean.py"
    "v3-enhanced-with-rules.yaml"
    "v3-exact-deployment.yaml"
    "v3-mcp-configmap.yaml"
    "v3-simple.yaml"
    "v3-with-mcp.py"
    "v3.1-full-vector-implementation.py"
    "v3.1-indentation-fix.py"
    "v3.1-vector-simple.yaml"
    "v3.1-working.yaml"
    "v3.2-admin-focused-fixed.yaml"
    "v3.2-admin-focused-simple.yaml"
    "v3.2-admin-patch.yaml"
    "v31-configmap.yaml"
    "v32-configmap.yaml"
    "vector-db-implementation-plan.py"
    "vector-db-persistence-fix.md"
    
    # Deployment test files
    "admin-dashboard.yaml"
    "anyuid-deployment.yaml"
    "anyuid-safe-deployment.yaml"
    "cluster-selector-dashboard.yaml"
    "comprehensive-dashboard.yaml"
    "final-deployment.yaml"
    "fixed-groq-deployment.yaml"
    "fixed-k8s-client-analyzer.yaml"
    "fixed-scanner-dashboard.yaml"
    "fixed-streamlit-deployment.yaml"
    "fixed-syntax-deployment.yaml"
    "flask-deployment.yaml"
    "image-deployment.yaml"
    "inline-deployment.yaml"
    "inline-streamlit-deployment.yaml"
    "k8s-mcp-server-deployment.yaml"
    "npm-k8s-mcp-deployment.yaml"
    "official-k8s-mcp-deployment.yaml"
    "openshift-deployment.yaml"
    "real-logs-analyzer.yaml"
    "simple-deployment.yaml"
    "simple-test-deployment.yaml"
    "simple-web-app.py"
    "simple_test.py"
    "smart-rule-filtering.py"
    "test-namespace-deployment.yaml"
    "working-deployment.yaml"
    "working-groq-deployment.yaml"
    "working-logging-solution.py"
    
    # Other test files
    "enhanced-ai-analysis-fix.py"
    "openshift-alerting.py"
    "openshift-knowledge-base.json"
    "openshift-log-forwarder.yaml"
    "setup_openshift_ai.py"
    "korrel8r-web.log"
    "kubernetes-mcp-server/"
)

echo "📁 Files to keep:"
for file in "${KEEP_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    fi
done

echo ""
echo "🗑️  Files to remove:"
for file in "${REMOVE_FILES[@]}"; do
    if [ -f "$file" ] || [ -d "$file" ]; then
        echo "  ❌ $file"
        rm -rf "$file"
    fi
done

echo ""
echo "📝 Adding files to git..."
git add "${KEEP_FILES[@]}"
git add requirements.txt

echo ""
echo "📋 Creating commit..."
git commit -m "feat: AI OpenShift Troubleshooter v2 & v3 implementations

- v2.0: Basic AI troubleshooting with generic Kubernetes knowledge
- v3.1: Vector database integration with PrometheusRule intelligence  
- v3.2: Admin-focused output with production rule context
- Added demo scenarios and export functionality
- Cleaned up test files and duplicates

Working deployments:
- v2: ai-troubleshooter-v2 namespace
- v3.1: ai-troubleshooter-v31 namespace (vector database)
- v3.2: ai-troubleshooter-v32-admin namespace (admin-focused)

Demo route: https://ai-troubleshooter-gui-route-v31-ai-troubleshooter-v31.apps.rosa.loki123.orwi.p3.openshiftapps.com"

echo ""
echo "🚀 Pushing to remote repository..."
git push origin master

echo ""
echo "✅ Cleanup and commit completed!"
echo "📊 Summary:"
echo "  - Kept $(echo "${KEEP_FILES[@]}" | wc -w) essential files"
echo "  - Removed $(echo "${REMOVE_FILES[@]}" | wc -w) test files"
echo "  - Committed and pushed to git"


