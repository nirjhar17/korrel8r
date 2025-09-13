# 🚀 OpenShift AI Log Analyzer

**Proactive AI-powered log analysis and intelligent problem resolution for OpenShift infrastructure**

## 🎯 What This Solves

Your customer's requirements:
1. **Proactive Problem Detection**: AI automatically highlights issues before they become critical
2. **Intelligent Problem Resolution**: When problems are found, AI provides actionable solutions and explanations

## ✨ Key Features

### 🔍 **Stage 1: Proactive Problem Detection**
- **Real-time log monitoring** from all OpenShift components
- **AI-powered anomaly detection** using advanced pattern recognition
- **Automatic problem highlighting** with severity classification
- **OpenShift-specific problem patterns** (nodes, operators, networking, storage, security)

### 🤖 **Stage 2: Intelligent Problem Resolution**
- **Click-through problem analysis** with detailed AI insights
- **Root cause analysis** with step-by-step solutions
- **OpenShift command recommendations** for immediate action
- **Prevention tips** to avoid future occurrences

### 📊 **Enhanced Dashboard**
- **Problem overview** with severity-based color coding
- **Real-time statistics** and trend analysis
- **Interactive problem resolution** interface
- **Alert management** and resolution tracking

### 🚨 **Proactive Alerting**
- **Multi-channel notifications** (Slack, Email, Webhooks)
- **Escalation rules** based on severity levels
- **Immediate alerts** for critical issues
- **Resolution notifications** when problems are fixed

## 🏗️ Architecture

```
OpenShift Cluster Logs → ClusterLogForwarder → AI Analysis Service → Dashboard + Alerts
                                    ↓
                            Problem Detection Engine
                                    ↓
                            AI Solution Generator
                                    ↓
                            Alerting System
```

## 📋 Prerequisites

- OpenShift cluster with logging enabled
- OpenShift CLI (oc) installed and configured
- Python 3.9+ (for local development)
- Groq API key (for AI analysis)
- Slack webhook URL (optional, for notifications)

## 🚀 Quick Start

### 1. **Clone and Setup**
```bash
git clone <your-repo>
cd k8s-anomaly-detection
```

### 2. **Run Automated Setup**
```bash
python setup_openshift_ai.py
```

This will:
- Check prerequisites
- Create environment configuration
- Deploy to OpenShift
- Set up log forwarding
- Verify deployment

### 3. **Configure Environment**
Edit the `.env` file with your actual values:
```bash
GROQ_API_KEY=your_actual_groq_api_key
SLACK_WEBHOOK_URL=your_actual_slack_webhook
# ... other configurations
```

### 4. **Access Dashboard**
The setup script will provide the OpenShift route URL where you can access the AI analyzer dashboard.

## 🔧 Manual Deployment

If you prefer manual deployment:

### 1. **Create Environment File**
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 2. **Deploy to OpenShift**
```bash
oc apply -f openshift-deployment.yaml
oc apply -f openshift-log-forwarder.yaml
```

### 3. **Verify Deployment**
```bash
oc get pods -n openshift-ai-analyzer
oc get route -n openshift-ai-analyzer
```

## 📊 Dashboard Features

### **Problem Detection View**
- 🚨 **Critical Issues**: Node failures, operator crashes
- ⚠️ **High Priority**: Network issues, storage problems
- 🔶 **Medium Priority**: Application errors, configuration issues
- ℹ️ **Low Priority**: Warnings, informational messages

### **AI Solution Interface**
When you click on any problem:
- **Root Cause Analysis**: "This error is caused by..."
- **Impact Assessment**: "This affects these services..."
- **Solution Steps**: "To fix this, do the following..."
- **OpenShift Commands**: Ready-to-run `oc` commands
- **Prevention Tips**: "To prevent this in the future..."

### **Alert Management**
- **Active Alerts**: Currently unresolved issues
- **Alert History**: Past problems and resolutions
- **Escalation Tracking**: Alert escalation levels
- **Resolution Notes**: How problems were fixed

## 🎯 OpenShift-Specific Intelligence

### **Node Issues**
- Node not ready conditions
- Resource pressure (CPU, memory, disk)
- Taint and scheduling problems
- **Solutions**: Node diagnostics, scaling recommendations

### **Operator Failures**
- Operator pod crashes
- Custom resource processing errors
- Webhook failures
- **Solutions**: Operator restart, configuration fixes

### **Network Issues**
- DNS resolution failures
- Service endpoint problems
- Ingress/route configuration errors
- **Solutions**: Network diagnostics, service verification

### **Storage Issues**
- PVC pending states
- Storage class problems
- Volume mount failures
- **Solutions**: Storage provider checks, capacity management

### **Security Issues**
- RBAC permission problems
- Certificate expiration
- Service account issues
- **Solutions**: Permission verification, certificate renewal

## 🔔 Alerting Configuration

### **Severity Levels**
- **Critical**: Immediate notification, all channels
- **High**: Immediate notification, Slack + Email
- **Medium**: Delayed notification, Slack only
- **Low**: Summary notification, Slack only

### **Notification Channels**
- **Slack**: Real-time alerts with rich formatting
- **Email**: Detailed problem reports
- **Webhooks**: Integration with external systems

### **Escalation Rules**
- Automatic escalation based on time and severity
- Multiple escalation levels
- Resolution tracking and notifications

## 🛠️ Customization

### **Adding New Problem Patterns**
Edit `openshift_ai_analyzer.py` and add to `OPENSHIFT_PROBLEM_PATTERNS`:

```python
"custom_issue": {
    "patterns": [
        r"(?i)\b(your pattern here)\b"
    ],
    "severity": "high",
    "category": "Custom Issue",
    "solutions": [
        "Your solution step 1",
        "Your solution step 2"
    ]
}
```

### **Custom Alerting Rules**
Modify `openshift_alerting.py` to adjust escalation rules and notification channels.

### **Knowledge Base Updates**
Update `openshift-knowledge-base.json` with additional troubleshooting information.

## 📈 Monitoring and Metrics

The system exposes Prometheus metrics:
- `openshift_anomalies_total`: Total anomalies detected
- `openshift_problems_by_severity`: Problems by severity level
- `openshift_alerts_active`: Currently active alerts
- `openshift_resolution_time`: Average problem resolution time

## 🔒 Security Considerations

- **RBAC**: Proper service account permissions for log access
- **Network Policies**: Secure communication between components
- **Secret Management**: API keys stored in OpenShift secrets
- **TLS**: Encrypted communication for all external connections

## 🐛 Troubleshooting

### **Common Issues**

1. **Deployment Fails**
   ```bash
   oc describe pod -n openshift-ai-analyzer
   oc logs -n openshift-ai-analyzer <pod-name>
   ```

2. **No Logs Being Analyzed**
   ```bash
   oc get clusterlogforwarder -n openshift-logging
   oc describe clusterlogforwarder instance -n openshift-logging
   ```

3. **AI Analysis Not Working**
   - Check Groq API key in secrets
   - Verify network connectivity
   - Review API rate limits

### **Logs and Debugging**
```bash
# View AI analyzer logs
oc logs -n openshift-ai-analyzer deployment/ai-log-analyzer

# Check log forwarding status
oc get clusterlogforwarder -n openshift-logging

# Monitor alerting system
oc logs -n openshift-ai-analyzer deployment/ai-log-analyzer | grep "Alert"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with OpenShift cluster
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review OpenShift logs
3. Create an issue in the repository
4. Contact the development team

---

**Built with ❤️ for OpenShift administrators who want AI-powered infrastructure insights**

