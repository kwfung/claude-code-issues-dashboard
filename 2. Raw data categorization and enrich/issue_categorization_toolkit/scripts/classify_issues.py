#!/usr/bin/env python3
"""
classify_issues.py

Main script to classify GitHub issues using L1/L2 taxonomy.

Usage:
    python classify_issues.py --input data/raw_issues.csv --taxonomy data/taxonomy_l1_l2.csv --output output/classified_issues.csv
"""

import pandas as pd
import re
import argparse
import time
from collections import defaultdict, Counter

# ============================================================================
# CONFIGURATION
# ============================================================================

LABEL_TO_L1 = {
    'area:core': 'L1.1',
    'area:api': 'L1.2',
    'area:tui': 'L1.3',
    'area:tools': 'L1.4',
    'area:mcp': 'L1.5',
    'area:ide': 'L1.6',
    'area:model': 'L1.7',
    'platform:macos': 'L1.8',
    'platform:windows': 'L1.8',
    'platform:linux': 'L1.8',
    'perf:memory': 'L1.9',
    'memory': 'L1.9',
    'area:security': 'L1.10',
}

L2_SPECIFIC_PATTERNS = {
    'L2.1.1': ['context', 'compact', 'token', 'window'],
    'L2.1.2': ['session', 'conversation', 'history', 'resume'],
    'L2.1.3': ['agent', 'loop', 'agentic', 'autonomous'],
    'L2.1.4': ['crash', 'exit', 'hang', 'freeze', 'terminated'],
    'L2.1.5': ['hook', 'sessionstart', 'precompact', 'userpromptsubmit', 'trigger', 'lifecycle'],
    'L2.5.1': ['plugin', 'install', 'update', 'marketplace'],
    'L2.5.2': ['mcp server', 'oauth', 'connection', 'discovery'],
    'L2.5.3': ['mcp tool', 'tool call', 'tool result'],
}

# ============================================================================
# TAXONOMY LOADING
# ============================================================================

def load_taxonomy(taxonomy_path):
    """Load and parse taxonomy CSV."""
    taxonomy_df = pd.read_csv(taxonomy_path)
    
    taxonomy_lookup = {}
    l1_code_to_name = {}
    l2_code_to_name = {}
    
    for _, row in taxonomy_df.iterrows():
        l1_code = row['L1_Code']
        l2_code = row['L2_Code']
        
        l1_code_to_name[l1_code] = row['L1_Category']
        l2_code_to_name[l2_code] = row['L2_Subcategory']
        
        if l1_code not in taxonomy_lookup:
            taxonomy_lookup[l1_code] = {
                'category': row['L1_Category'],
                'description': row['L1_Description'],
                'l2_options': []
            }
        taxonomy_lookup[l1_code]['l2_options'].append({
            'code': l2_code,
            'subcategory': row['L2_Subcategory'],
            'description': row['L2_Description'],
            'keywords': [k.strip() for k in str(row['Example_Keywords']).lower().split(',') if k.strip()]
        })
    
    return taxonomy_lookup, l1_code_to_name, l2_code_to_name

# ============================================================================
# CLASSIFICATION FUNCTIONS
# ============================================================================

def classify_issue_type(title, body):
    """Classify as Bug, Feature Request, or Documentation."""
    title_lower = str(title).lower()
    body_lower = str(body).lower() if pd.notna(body) else ""
    
    if any(tag in title_lower for tag in ['[bug]', '[bug', 'bug:']):
        return 'Bug'
    if any(tag in title_lower for tag in ['[feature]', '[enhancement]', 'feature request']):
        return 'Feature Request'
    if any(tag in title_lower for tag in ['[docs]', '[documentation]']):
        return 'Documentation'
    
    doc_keywords = ['documentation', 'docs', 'unclear instructions']
    if any(kw in title_lower or kw in body_lower[:200] for kw in doc_keywords):
        return 'Documentation'
    
    bug_keywords = ['error', 'crash', 'fail', 'broke', 'broken', 'not working', 'issue']
    if any(kw in title_lower or kw in body_lower[:300] for kw in bug_keywords):
        return 'Bug'
    
    feature_keywords = ['add', 'support', 'want', 'request', 'would like', 'improvement']
    if any(kw in title_lower for kw in feature_keywords):
        return 'Feature Request'
    
    return 'Bug'

def create_summary(title):
    """Create concise summary from title."""
    title = str(title)
    title_clean = re.sub(r'\[.*?\]', '', title).strip()
    title_clean = title_clean.strip('.,;:-')
    words = title_clean.split()
    if len(words) <= 20:
        return title_clean
    return ' '.join(words[:18]) + '...'

def classify_sentiment(title, body):
    """Classify sentiment: Positive, Neutral, or Negative."""
    text = (str(title) + " " + str(body)[:500]).lower()
    
    positive_keywords = ['great', 'love', 'been great', 'fantastic', 'excellent', 'appreciate']
    if any(kw in text for kw in positive_keywords):
        return 'Positive'
    
    negative_keywords = ['frustrated', 'annoying', 'terrible', 'wasted', 'completely', 'useless',
                        'hours', 'realllly', 'lazy', 'poor', 'non-functional', 'spent several hours']
    caps = sum(1 for c in str(title) if c.isupper())
    
    if any(kw in text for kw in negative_keywords) or caps > 15 or text.count('!') > 3:
        return 'Negative'
    
    return 'Neutral'

def find_best_l2(l1_code, text, labels_str, taxonomy_lookup, l2_code_to_name):
    """Find best L2 subcategory. Returns 'Other' if no good match."""
    text_lower = text.lower()
    l2_matches = defaultdict(int)
    
    # Check specific L2 patterns
    for l2_code, patterns in L2_SPECIFIC_PATTERNS.items():
        if not l2_code.startswith(l1_code.replace('L1', 'L2')):
            continue
        for pattern in patterns:
            if pattern in text_lower:
                l2_matches[l2_code] += 3 if pattern in text[:200].lower() else 1
    
    # Check taxonomy keywords
    for l2_option in taxonomy_lookup[l1_code]['l2_options']:
        for keyword in l2_option['keywords']:
            if keyword and keyword in text_lower:
                l2_matches[l2_option['code']] += 1
    
    if l2_matches:
        best_l2 = max(l2_matches, key=l2_matches.get)
        score = l2_matches[best_l2]
        
        if score < 2:
            return 'Other', 'Low', f'Weak L2 match (score={score})'
        
        confidence = 'High' if score >= 4 else 'Medium'
        return best_l2, confidence, ''
    
    return 'Other', 'Low', 'No L2 match found'

def match_l1_l2(title, body, labels, taxonomy_lookup, l1_code_to_name, l2_code_to_name):
    """Match issue to L1 and L2 categories."""
    text = str(title) + " " + str(body)
    labels_str = str(labels).lower()
    
    # PRIORITY 1: Use GitHub labels
    for label, l1_code in LABEL_TO_L1.items():
        if label in labels_str:
            best_l2, confidence, notes = find_best_l2(l1_code, text, labels_str, taxonomy_lookup, l2_code_to_name)
            l1_category = l1_code_to_name.get(l1_code, 'Other')
            l2_category = l2_code_to_name.get(best_l2, 'Other') if best_l2 != 'Other' else 'Other'
            return l1_code, l1_category, best_l2, l2_category, confidence, notes
    
    # PRIORITY 2: Keyword matching
    l1_scores = defaultdict(int)
    for l1_code, l1_info in taxonomy_lookup.items():
        for l2_option in l1_info['l2_options']:
            for keyword in l2_option['keywords']:
                if keyword and keyword in text.lower():
                    l1_scores[l1_code] += 2 if keyword in title.lower() else 1
    
    if l1_scores:
        best_l1 = max(l1_scores, key=l1_scores.get)
        score = l1_scores[best_l1]
        
        if score < 2:
            return 'Other', 'Other', 'Other', 'Other', 'Low', f'Weak L1 match (score={score})'
        
        best_l2, confidence, notes = find_best_l2(best_l1, text, labels_str, taxonomy_lookup, l2_code_to_name)
        l1_category = l1_code_to_name.get(best_l1, 'Other')
        l2_category = l2_code_to_name.get(best_l2, 'Other') if best_l2 != 'Other' else 'Other'
        return best_l1, l1_category, best_l2, l2_category, confidence, notes
    
    # PRIORITY 3: No match
    return 'Other', 'Other', 'Other', 'Other', 'Low', 'No clear L1/L2 match'

def classify_row(row, taxonomy_lookup, l1_code_to_name, l2_code_to_name):
    """Classify a single issue row."""
    title = row['title']
    body = row['body'] if pd.notna(row['body']) else ''
    labels = row['labels'] if pd.notna(row['labels']) else ''
    
    l1_code, l1_category, l2_code, l2_category, confidence, notes = match_l1_l2(
        title, body, labels, taxonomy_lookup, l1_code_to_name, l2_code_to_name
    )
    
    return {
        'Category': classify_issue_type(title, body),
        'Summary': create_summary(title),
        'Sentiment': classify_sentiment(title, body),
        'L1_Tag': l1_code,
        'L1_Category': l1_category,
        'L2_Tag': l2_code,
        'L2_Category': l2_category,
        'Confidence': confidence,
        'Tagging_Notes': notes
    }

# ============================================================================
# MAIN PROCESSING
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Classify GitHub issues using L1/L2 taxonomy')
    parser.add_argument('--input', required=True, help='Input CSV file with raw issues')
    parser.add_argument('--taxonomy', required=True, help='Taxonomy CSV file')
    parser.add_argument('--output', required=True, help='Output CSV file for classified issues')
    parser.add_argument('--progress', action='store_true', help='Show progress during classification')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("ISSUE CLASSIFICATION TOOL")
    print("=" * 80)
    
    # Load data
    print(f"\n[1/4] Loading data...")
    issues_df = pd.read_csv(args.input)
    taxonomy_lookup, l1_code_to_name, l2_code_to_name = load_taxonomy(args.taxonomy)
    print(f"  ✓ Loaded {len(issues_df)} issues")
    print(f"  ✓ Loaded taxonomy with {len(taxonomy_lookup)} L1 categories")
    
    # Classify
    print(f"\n[2/4] Classifying issues...")
    if args.progress:
        print("  Progress: ", end='', flush=True)
    
    start_time = time.time()
    results = []
    
    for idx in range(len(issues_df)):
        result = classify_row(issues_df.iloc[idx], taxonomy_lookup, l1_code_to_name, l2_code_to_name)
        results.append(result)
        
        if args.progress and (idx + 1) % 100 == 0:
            print(f"{idx + 1}...", end='', flush=True)
    
    if args.progress:
        print(" Done!")
    
    elapsed = time.time() - start_time
    print(f"  ✓ Classified {len(results)} issues in {elapsed:.1f} seconds")
    
    # Add results to DataFrame
    print(f"\n[3/4] Adding classification columns...")
    new_columns = ['Category', 'Summary', 'Sentiment', 'L1_Tag', 'L1_Category', 'L2_Tag', 'L2_Category', 'Confidence', 'Tagging_Notes']
    for col in new_columns:
        issues_df[col] = [r[col] for r in results]
    
    # Save
    print(f"\n[4/4] Saving results...")
    issues_df.to_csv(args.output, index=False)
    print(f"  ✓ Saved to: {args.output}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nBy Category:")
    for cat, count in issues_df['Category'].value_counts().items():
        print(f"  {cat:20} {count:4} ({count/len(issues_df)*100:5.1f}%)")
    
    print(f"\nBy Confidence:")
    for conf, count in issues_df['Confidence'].value_counts().items():
        print(f"  {conf:20} {count:4} ({count/len(issues_df)*100:5.1f}%)")
    
    print(f"\n✓ Classification complete!")

if __name__ == "__main__":
    main()
