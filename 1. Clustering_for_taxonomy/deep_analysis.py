#!/usr/bin/env python3
"""
Deep dive into issue themes through clustering and sampling.
"""

import pandas as pd
import json
from collections import defaultdict, Counter
import random

# Load processed data
df = pd.read_csv('/home/claude/issues_processed.csv')

print("=" * 80)
print("DEEP THEME ANALYSIS")
print("=" * 80)

# Function to sample and display issues
def sample_issues(df_subset, n=5):
    """Sample n issues and show their key info."""
    sample = df_subset.sample(min(n, len(df_subset)))
    for idx, row in sample.iterrows():
        print(f"\n  #{row['issue_number']}: {row['title'][:80]}")
        # Show labels
        labels = eval(row['parsed_labels']) if pd.notna(row['parsed_labels']) else []
        if labels:
            print(f"    Labels: {', '.join(labels[:5])}")

# 1. CORE FUNCTIONALITY ISSUES
print("\n" + "=" * 80)
print("1. CORE FUNCTIONALITY ISSUES (area:core)")
print("=" * 80)

core_issues = df[df['labels'].str.contains('area:core', na=False)]
print(f"Total: {len(core_issues)} issues")

# Subcategories within core
core_keywords = defaultdict(list)
for idx, row in core_issues.iterrows():
    title_lower = str(row['title']).lower()
    body_lower = str(row['body']).lower()
    
    if any(kw in title_lower or kw in body_lower for kw in ['session', 'conversation', 'history']):
        core_keywords['session_management'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['context', 'token', 'compact', 'window']):
        core_keywords['context_management'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['agent', 'loop', 'agentic', 'autonomous']):
        core_keywords['agent_behavior'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['hook', 'lifecycle', 'trigger']):
        core_keywords['hooks_lifecycle'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['crash', 'exit', 'hang', 'freeze']):
        core_keywords['stability'].append(idx)

print("\nCore subcategories:")
for subcat, indices in sorted(core_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {subcat:30} {len(indices):4} issues")
    sample_issues(df.loc[indices], n=2)

# 2. API & INTEGRATION ISSUES
print("\n" + "=" * 80)
print("2. API & INTEGRATION ISSUES")
print("=" * 80)

api_issues = df[df['labels'].str.contains('area:api', na=False)]
print(f"Total area:api: {len(api_issues)} issues")

# API subcategories
api_keywords = defaultdict(list)
for idx, row in api_issues.iterrows():
    title_lower = str(row['title']).lower()
    body_lower = str(row['body']).lower()
    
    if any(kw in body_lower for kw in ['rate limit', '429', 'quota', 'throttle']):
        api_keywords['rate_limits'].append(idx)
    if any(kw in body_lower for kw in ['401', '403', 'unauthorized', 'authentication', 'api key']):
        api_keywords['authentication'].append(idx)
    if any(kw in body_lower for kw in ['bedrock', 'aws']):
        api_keywords['bedrock'].append(idx)
    if any(kw in body_lower for kw in ['vertex', 'gcp', 'google cloud']):
        api_keywords['vertex'].append(idx)
    if any(kw in body_lower for kw in ['proxy', 'network', 'egress', 'dns']):
        api_keywords['network_proxy'].append(idx)

print("\nAPI subcategories:")
for subcat, indices in sorted(api_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {subcat:30} {len(indices):4} issues")
    sample_issues(df.loc[indices], n=2)

# 3. USER INTERFACE ISSUES (TUI)
print("\n" + "=" * 80)
print("3. USER INTERFACE ISSUES (area:tui)")
print("=" * 80)

tui_issues = df[df['labels'].str.contains('area:tui', na=False)]
print(f"Total: {len(tui_issues)} issues")

tui_keywords = defaultdict(list)
for idx, row in tui_issues.iterrows():
    title_lower = str(row['title']).lower()
    body_lower = str(row['body']).lower()
    
    if any(kw in title_lower or kw in body_lower for kw in ['render', 'display', 'visual', 'layout', 'ui']):
        tui_keywords['rendering_display'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['input', 'keyboard', 'paste', 'copy', 'shortcut']):
        tui_keywords['input_handling'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['command', '/command', 'slash']):
        tui_keywords['commands'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['notification', 'alert', 'status', 'progress']):
        tui_keywords['feedback_status'].append(idx)

print("\nTUI subcategories:")
for subcat, indices in sorted(tui_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {subcat:30} {len(indices):4} issues")
    sample_issues(df.loc[indices], n=2)

# 4. TOOLS & EXECUTION
print("\n" + "=" * 80)
print("4. TOOLS & EXECUTION (area:tools)")
print("=" * 80)

tools_issues = df[df['labels'].str.contains('area:tools', na=False)]
print(f"Total: {len(tools_issues)} issues")

tools_keywords = defaultdict(list)
for idx, row in tools_issues.iterrows():
    title_lower = str(row['title']).lower()
    body_lower = str(row['body']).lower()
    
    if any(kw in title_lower or kw in body_lower for kw in ['bash', 'shell', 'command execution']):
        tools_keywords['bash_execution'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['file', 'read', 'write', 'edit']):
        tools_keywords['file_operations'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['git']):
        tools_keywords['git_operations'].append(idx)
    if any(kw in title_lower or kw in body_lower for kw in ['sandbox', 'permission', 'deny', 'allow']):
        tools_keywords['permissions_sandbox'].append(idx)

print("\nTools subcategories:")
for subcat, indices in sorted(tools_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {subcat:30} {len(indices):4} issues")
    sample_issues(df.loc[indices], n=2)

# 5. MCP INTEGRATION
print("\n" + "=" * 80)
print("5. MCP INTEGRATION (area:mcp)")
print("=" * 80)

mcp_issues = df[df['labels'].str.contains('area:mcp', na=False)]
print(f"Total: {len(mcp_issues)} issues")
sample_issues(mcp_issues, n=5)

# 6. IDE INTEGRATION
print("\n" + "=" * 80)
print("6. IDE INTEGRATION (area:ide)")
print("=" * 80)

ide_issues = df[df['labels'].str.contains('area:ide', na=False)]
print(f"Total: {len(ide_issues)} issues")

ide_keywords = defaultdict(list)
for idx, row in ide_issues.iterrows():
    title_lower = str(row['title']).lower()
    body_lower = str(row['body']).lower()
    
    if 'vscode' in title_lower or 'vscode' in body_lower:
        ide_keywords['vscode'].append(idx)
    if 'cursor' in title_lower or 'cursor' in body_lower:
        ide_keywords['cursor'].append(idx)

print("\nIDE subcategories:")
for subcat, indices in sorted(ide_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {subcat:30} {len(indices):4} issues")
    sample_issues(df.loc[indices], n=2)

# 7. MODEL BEHAVIOR
print("\n" + "=" * 80)
print("7. MODEL BEHAVIOR (area:model)")
print("=" * 80)

model_issues = df[df['labels'].str.contains('area:model', na=False)]
print(f"Total: {len(model_issues)} issues")
sample_issues(model_issues, n=5)

# 8. SECURITY
print("\n" + "=" * 80)
print("8. SECURITY (area:security)")
print("=" * 80)

security_issues = df[df['labels'].str.contains('area:security', na=False)]
print(f"Total: {len(security_issues)} issues")
sample_issues(security_issues, n=5)

# 9. MEMORY & PERFORMANCE
print("\n" + "=" * 80)
print("9. MEMORY & PERFORMANCE")
print("=" * 80)

memory_issues = df[df['labels'].str.contains('memory|perf:', na=False)]
print(f"Total: {len(memory_issues)} issues")
sample_issues(memory_issues, n=5)

# 10. FEATURE REQUESTS
print("\n" + "=" * 80)
print("10. FEATURE REQUESTS (enhancement)")
print("=" * 80)

feature_issues = df[df['labels'].str.contains('enhancement', na=False)]
print(f"Total: {len(feature_issues)} issues")

# Categorize feature requests
feature_keywords = defaultdict(list)
for idx, row in feature_issues.iterrows():
    title_lower = str(row['title']).lower()
    
    if any(kw in title_lower for kw in ['workflow', 'improve', 'better', 'easier']):
        feature_keywords['workflow_improvements'].append(idx)
    if any(kw in title_lower for kw in ['add', 'support', 'new']):
        feature_keywords['new_capabilities'].append(idx)
    if any(kw in title_lower for kw in ['config', 'setting', 'option', 'customize']):
        feature_keywords['configuration'].append(idx)
    if any(kw in title_lower for kw in ['integration', 'connect', 'mcp']):
        feature_keywords['integrations'].append(idx)

print("\nFeature request categories:")
for subcat, indices in sorted(feature_keywords.items(), key=lambda x: -len(x[1])):
    print(f"  {subcat:30} {len(indices):4} issues")
    sample_issues(df.loc[indices], n=2)

# Save categorization results
categorization = {
    'core_functionality': {
        'total': len(core_issues),
        'subcategories': {k: len(v) for k, v in core_keywords.items()}
    },
    'api_integration': {
        'total': len(api_issues),
        'subcategories': {k: len(v) for k, v in api_keywords.items()}
    },
    'user_interface': {
        'total': len(tui_issues),
        'subcategories': {k: len(v) for k, v in tui_keywords.items()}
    },
    'tools_execution': {
        'total': len(tools_issues),
        'subcategories': {k: len(v) for k, v in tools_keywords.items()}
    },
    'mcp_integration': {
        'total': len(mcp_issues)
    },
    'ide_integration': {
        'total': len(ide_issues),
        'subcategories': {k: len(v) for k, v in ide_keywords.items()}
    },
    'model_behavior': {
        'total': len(model_issues)
    },
    'security': {
        'total': len(security_issues)
    },
    'memory_performance': {
        'total': len(memory_issues)
    },
    'feature_requests': {
        'total': len(feature_issues),
        'subcategories': {k: len(v) for k, v in feature_keywords.items()}
    }
}

with open('/home/claude/categorization_results.json', 'w') as f:
    json.dump(categorization, f, indent=2)

print("\n" + "=" * 80)
print("Saved categorization results to categorization_results.json")
print("=" * 80)
