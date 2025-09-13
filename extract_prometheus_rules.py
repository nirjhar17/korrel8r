#!/usr/bin/env python3
"""
Extract and format PrometheusRule resources for AI context
"""
import json
import sys

def extract_alerting_rules(rules_file):
    """Extract alerting rules from PrometheusRule resources"""
    
    with open(rules_file, 'r') as f:
        data = json.load(f)
    
    alerting_rules = []
    
    for item in data.get('items', []):
        namespace = item['metadata']['namespace']
        rule_name = item['metadata']['name']
        
        spec = item.get('spec', {})
        for group in spec.get('groups', []):
            group_name = group.get('name', 'unknown')
            
            for rule in group.get('rules', []):
                # Only process alerting rules (not recording rules)
                if 'alert' in rule:
                    alert_rule = {
                        'alert_name': rule['alert'],
                        'namespace': namespace,
                        'rule_resource': rule_name,
                        'group': group_name,
                        'expr': rule['expr'].strip(),
                        'for_duration': rule.get('for', '0s'),
                        'severity': rule.get('labels', {}).get('severity', 'unknown'),
                        'description': rule.get('annotations', {}).get('description', ''),
                        'summary': rule.get('annotations', {}).get('summary', ''),
                        'runbook_url': rule.get('annotations', {}).get('runbook_url', ''),
                        'labels': rule.get('labels', {}),
                        'annotations': rule.get('annotations', {})
                    }
                    alerting_rules.append(alert_rule)
    
    return alerting_rules

def format_rules_for_llm(rules):
    """Format rules for LLM context window"""
    
    # Group by severity for better organization
    critical_rules = [r for r in rules if r['severity'] == 'critical']
    warning_rules = [r for r in rules if r['severity'] == 'warning']
    other_rules = [r for r in rules if r['severity'] not in ['critical', 'warning']]
    
    context = """# OPENSHIFT PRODUCTION ALERTING RULES KNOWLEDGE BASE
# These are the actual alerting rules used in your OpenShift cluster
# Use these thresholds and conditions to provide contextual analysis

## CRITICAL SEVERITY ALERTS ({} rules)
""".format(len(critical_rules))
    
    for rule in critical_rules:
        context += f"""
### {rule['alert_name']} (CRITICAL)
- **Namespace**: {rule['namespace']}
- **Condition**: {rule['expr']}
- **Duration**: {rule['for_duration']}
- **Description**: {rule['description']}
- **Summary**: {rule['summary']}"""
        if rule['runbook_url']:
            context += f"\n- **Runbook**: {rule['runbook_url']}"
        context += "\n"
    
    context += f"\n## WARNING SEVERITY ALERTS ({len(warning_rules)} rules)\n"
    
    for rule in warning_rules:
        context += f"""
### {rule['alert_name']} (WARNING)
- **Namespace**: {rule['namespace']}
- **Condition**: {rule['expr']}
- **Duration**: {rule['for_duration']}
- **Description**: {rule['description']}"""
        if rule['summary']:
            context += f"\n- **Summary**: {rule['summary']}"
        if rule['runbook_url']:
            context += f"\n- **Runbook**: {rule['runbook_url']}"
        context += "\n"
    
    if other_rules:
        context += f"\n## OTHER SEVERITY ALERTS ({len(other_rules)} rules)\n"
        for rule in other_rules:
            context += f"""
### {rule['alert_name']} ({rule['severity'].upper()})
- **Condition**: {rule['expr']}
- **Duration**: {rule['for_duration']}
- **Description**: {rule['description']}
"""
    
    return context

def main():
    rules_file = '/tmp/all-prometheus-rules.json'
    
    print("🔍 Extracting alerting rules...")
    rules = extract_alerting_rules(rules_file)
    
    print(f"📊 Found {len(rules)} alerting rules")
    
    # Statistics
    severity_counts = {}
    for rule in rules:
        severity = rule['severity']
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print("📈 Severity breakdown:")
    for severity, count in sorted(severity_counts.items()):
        print(f"   {severity}: {count} rules")
    
    print("\n🎯 Top 10 most common alerts:")
    alert_names = [r['alert_name'] for r in rules]
    from collections import Counter
    for alert, count in Counter(alert_names).most_common(10):
        print(f"   {alert}: {count}")
    
    # Format for LLM
    print("\n📝 Formatting for LLM context...")
    llm_context = format_rules_for_llm(rules)
    
    # Save formatted context
    with open('/tmp/prometheus_rules_context.txt', 'w') as f:
        f.write(llm_context)
    
    print(f"✅ LLM context saved to /tmp/prometheus_rules_context.txt")
    print(f"📏 Context size: {len(llm_context)} characters (~{len(llm_context)//4} tokens)")
    
    # Save structured data for Python integration
    with open('/tmp/prometheus_rules_structured.json', 'w') as f:
        json.dump(rules, f, indent=2)
    
    print(f"💾 Structured data saved to /tmp/prometheus_rules_structured.json")

if __name__ == "__main__":
    main()





