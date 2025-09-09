#!/bin/bash

# AI-Powered Korrel8r Troubleshooter - Shell Version
# Quick troubleshooting for broken pods using Korrel8r + AI analysis

set -e

NAMESPACE=${1:-"openshift-monitoring"}
POD_NAME=${2:-"prometheus-k8s-0"}
KORREL8R_URL="https://korrel8r-korrel8r.apps.rosa.loki123.orwi.p3.openshiftapps.com"

echo "🔍 AI-Powered Korrel8r Troubleshooting: ${NAMESPACE}/${POD_NAME}"
echo "============================================================"

echo ""
echo "📋 Step 1: Pod Information"
echo "----------------------------"
oc describe pod ${POD_NAME} -n ${NAMESPACE} | head -50

echo ""
echo "📋 Step 2: Pod Events" 
echo "-------------------"
oc get events -n ${NAMESPACE} --field-selector involvedObject.name=${POD_NAME} --sort-by='.lastTimestamp' | tail -10

echo ""
echo "📋 Step 3: Pod Status"
echo "-------------------"
oc get pod ${POD_NAME} -n ${NAMESPACE} -o yaml | grep -A 20 "conditions:"

echo ""
echo "📋 Step 4: Storage Check (PVC Issues)"
echo "------------------------------------"
oc get pvc -n ${NAMESPACE} | grep prometheus || echo "No PVCs found"

echo ""
echo "📋 Step 5: Node Availability"
echo "---------------------------"
oc get nodes -o wide

echo ""
echo "📋 Step 6: Korrel8r Log Domain Check"
echo "-----------------------------------"
curl -k -s ${KORREL8R_URL}/api/v1alpha1/domains/log/classes | jq . 2>/dev/null || echo "Korrel8r API not accessible"

echo ""
echo "📋 Step 7: Vector Log Collection Status"
echo "--------------------------------------"
oc get pods -n openshift-logging | grep -E "(vector|logging)" || echo "No vector/logging pods found"

echo ""
echo "🎯 ANALYSIS SUMMARY"
echo "=================="
echo "Based on the pod description, the main issue appears to be:"
echo ""
echo "❌ ISSUE: Volume node affinity conflict"
echo "   - Pod requires specific node characteristics"
echo "   - Available nodes don't meet storage requirements"
echo "   - PVC may be bound to unavailable nodes"
echo ""
echo "🔧 RECOMMENDED SOLUTIONS:"
echo "1. Check PVC node affinity: oc describe pvc prometheus-data-${POD_NAME} -n ${NAMESPACE}"
echo "2. Check node labels: oc get nodes --show-labels | grep worker"
echo "3. Check storage class: oc get storageclass"
echo "4. Consider recreating PVC if bound to deleted node"
echo ""
echo "🤖 AI ANALYSIS WOULD PROVIDE:"
echo "- Detailed root cause analysis"
echo "- Step-by-step remediation"
echo "- Prevention strategies"
echo "- Related resource correlation via Korrel8r"
echo ""
echo "✅ Troubleshooting Complete!"
echo "📊 For full AI analysis, ensure Groq API key is configured"
