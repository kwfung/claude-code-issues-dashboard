#!/usr/bin/env python3
"""
Comprehensive analysis of Claude Code GitHub issues.
Data-driven approach to build L1/L2 taxonomy.
"""

import pandas as pd
import numpy as np
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
print("=" * 80)
print("LOADING DATA")
print("=" * 80)

df = pd.read_csv('/mnt/user-data/uploads/raw_issues_1000.csv')

print(f"\nTotal issues loaded: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head(2))

# Basic stats
print("\n" + "=" * 80)
print("BASIC STATISTICS")
print("=" * 80)

print(f"\nIssue state distribution:")
print(df['state'].value_counts())

print(f"\nIssues with labels: {df['labels'].notna().sum()}")
print(f"Issues without labels: {df['labels'].isna().sum()}")

print(f"\nAverage comments per issue: {df['comments_count'].mean():.2f}")
print(f"Median comments per issue: {df['comments_count'].median():.0f}")

# Parse labels
print("\n" + "=" * 80)
print("LABEL ANALYSIS")
print("=" * 80)

def parse_labels(label_str):
    """Parse comma-separated labels."""
    if pd.isna(label_str):
        return []
    return [l.strip() for l in str(label_str).split(',') if l.strip()]

df['parsed_labels'] = df['labels'].apply(parse_labels)

# Count all labels
all_labels = []
for labels in df['parsed_labels']:
    all_labels.extend(labels)

label_counts = Counter(all_labels)

print(f"\nTotal unique labels: {len(label_counts)}")
print(f"\nTop 30 most common labels:")
for label, count in label_counts.most_common(30):
    pct = (count / len(df)) * 100
    print(f"  {label:40} {count:5} ({pct:5.1f}%)")

# Analyze label patterns
print("\n" + "=" * 80)
print("LABEL PATTERN ANALYSIS")
print("=" * 80)

# Group labels by prefix
label_prefixes = defaultdict(list)
for label, count in label_counts.items():
    if ':' in label:
        prefix = label.split(':')[0]
        label_prefixes[prefix].append((label, count))
    else:
        label_prefixes['_no_prefix'].append((label, count))

print("\nLabel categories (by prefix):")
for prefix in sorted(label_prefixes.keys()):
    labels = label_prefixes[prefix]
    total_issues = sum(count for _, count in labels)
    print(f"\n{prefix}:")
    for label, count in sorted(labels, key=lambda x: -x[1])[:10]:
        print(f"  {label:40} {count:5}")

# Analyze titles
print("\n" + "=" * 80)
print("TITLE ANALYSIS")
print("=" * 80)

def extract_issue_type(title):
    """Extract issue type from title."""
    title_lower = title.lower()
    if title_lower.startswith('[bug]') or title_lower.startswith('[bug'):
        return 'bug'
    elif title_lower.startswith('[feature]') or title_lower.startswith('[feature request]'):
        return 'feature'
    elif title_lower.startswith('[enhancement]'):
        return 'enhancement'
    elif title_lower.startswith('[question]'):
        return 'question'
    elif title_lower.startswith('[docs]') or title_lower.startswith('[documentation]'):
        return 'docs'
    else:
        return 'other'

df['issue_type_from_title'] = df['title'].apply(extract_issue_type)

print("\nIssue types from title:")
print(df['issue_type_from_title'].value_counts())

# Analyze common keywords in titles
print("\n" + "=" * 80)
print("KEYWORD ANALYSIS IN TITLES")
print("=" * 80)

def extract_keywords(title):
    """Extract meaningful keywords from title."""
    # Remove issue type tags
    title = re.sub(r'\[.*?\]', '', title)
    # Convert to lowercase
    title = title.lower()
    # Remove special characters but keep spaces
    title = re.sub(r'[^\w\s-]', ' ', title)
    # Split into words
    words = title.split()
    # Filter out common words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'been', 'be',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                 'can', 'could', 'may', 'might', 'must', 'not', 'when', 'after', 'before',
                 'claude', 'code', 'issue', 'bug', 'feature', 'request'}
    return [w for w in words if w not in stopwords and len(w) > 2]

all_keywords = []
for title in df['title']:
    all_keywords.extend(extract_keywords(str(title)))

keyword_counts = Counter(all_keywords)

print("\nTop 50 keywords in titles:")
for keyword, count in keyword_counts.most_common(50):
    pct = (count / len(df)) * 100
    print(f"  {keyword:30} {count:5} ({pct:5.1f}%)")

# Analyze body text length
print("\n" + "=" * 80)
print("BODY TEXT ANALYSIS")
print("=" * 80)

df['body_length'] = df['body'].fillna('').str.len()
print(f"\nBody length statistics:")
print(f"  Mean: {df['body_length'].mean():.0f} characters")
print(f"  Median: {df['body_length'].median():.0f} characters")
print(f"  Min: {df['body_length'].min():.0f} characters")
print(f"  Max: {df['body_length'].max():.0f} characters")

# Check for common error patterns
print("\n" + "=" * 80)
print("COMMON ERROR PATTERNS")
print("=" * 80)

error_patterns = {
    'API Error': r'api error|anthropic api|error.*400|error.*401|error.*403|error.*429|error.*500',
    'Connection': r'connection|timeout|network|dns|proxy|egress',
    'Crash/Exit': r'crash|exit code|process exited|terminated|killed',
    'Memory': r'memory|out of memory|oom|heap',
    'Performance': r'slow|lag|delay|hang|freeze|unresponsive',
    'File/Path': r'file not found|path|directory|cannot read|cannot write',
    'Install/Setup': r'install|setup|configuration|config|settings',
    'MCP': r'mcp|model context protocol|server',
    'Model': r'model|sonnet|opus|haiku',
    'Context': r'context|token|window|compact',
}

print("\nError pattern frequency in body text:")
for pattern_name, pattern in error_patterns.items():
    matches = df['body'].fillna('').str.contains(pattern, case=False, regex=True).sum()
    pct = (matches / len(df)) * 100
    print(f"  {pattern_name:20} {matches:5} ({pct:5.1f}%)")

# Platform distribution
print("\n" + "=" * 80)
print("PLATFORM DISTRIBUTION")
print("=" * 80)

platform_labels = []
for labels in df['parsed_labels']:
    for label in labels:
        if label.startswith('platform:'):
            platform_labels.append(label)

platform_counts = Counter(platform_labels)
print("\nPlatform-specific issues:")
for platform, count in platform_counts.most_common():
    pct = (count / len(df)) * 100
    print(f"  {platform:30} {count:5} ({pct:5.1f}%)")

# Area distribution
print("\n" + "=" * 80)
print("AREA DISTRIBUTION")
print("=" * 80)

area_labels = []
for labels in df['parsed_labels']:
    for label in labels:
        if label.startswith('area:'):
            area_labels.append(label)

area_counts = Counter(area_labels)
print("\nArea-specific issues:")
for area, count in area_counts.most_common():
    pct = (count / len(df)) * 100
    print(f"  {area:30} {count:5} ({pct:5.1f}%)")

# Co-occurrence analysis
print("\n" + "=" * 80)
print("LABEL CO-OCCURRENCE ANALYSIS")
print("=" * 80)

# Find which labels appear together
label_pairs = Counter()
for labels in df['parsed_labels']:
    if len(labels) >= 2:
        for i, label1 in enumerate(labels):
            for label2 in labels[i+1:]:
                pair = tuple(sorted([label1, label2]))
                label_pairs[pair] += 1

print("\nTop 20 label pairs that appear together:")
for (label1, label2), count in label_pairs.most_common(20):
    print(f"  {label1:30} + {label2:30} = {count:4}")

# Save processed data
print("\n" + "=" * 80)
print("SAVING PROCESSED DATA")
print("=" * 80)

# Save analysis results
analysis_results = {
    'total_issues': len(df),
    'label_distribution': dict(label_counts.most_common(50)),
    'issue_types': df['issue_type_from_title'].value_counts().to_dict(),
    'top_keywords': dict(keyword_counts.most_common(50)),
    'platform_distribution': dict(platform_counts),
    'area_distribution': dict(area_counts),
    'label_categories': {k: dict(v) for k, v in label_prefixes.items()},
}

with open('/home/claude/analysis_results.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)

print("Saved analysis results to analysis_results.json")

# Save DataFrame with parsed labels
df.to_csv('/home/claude/issues_processed.csv', index=False)
print("Saved processed DataFrame to issues_processed.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
