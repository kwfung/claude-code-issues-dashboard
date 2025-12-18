#!/usr/bin/env python3
"""
analyze_results.py

Generate detailed analysis and reports from classified issues.

Usage:
    python analyze_results.py --input output/classified_issues.csv --output-dir reports/
"""

import pandas as pd
import argparse
from collections import Counter

def generate_summary_report(df, output_file):
    """Generate summary statistics report."""
    
    report = []
    report.append("# CLASSIFICATION SUMMARY REPORT")
    report.append(f"## Total Issues: {len(df)}\n")
    report.append("=" * 80 + "\n")
    
    # By Category
    report.append("## By Issue Type\n")
    for cat, count in df['Category'].value_counts().items():
        pct = (count / len(df)) * 100
        report.append(f"- **{cat}**: {count} ({pct:.1f}%)")
    report.append("")
    
    # By Sentiment
    report.append("## By Sentiment\n")
    for sent, count in df['Sentiment'].value_counts().items():
        pct = (count / len(df)) * 100
        report.append(f"- **{sent}**: {count} ({pct:.1f}%)")
    report.append("")
    
    # By L1 Category
    report.append("## By L1 Category\n")
    l1_counts = df.groupby(['L1_Tag', 'L1_Category']).size().reset_index(name='count')
    l1_counts = l1_counts.sort_values('count', ascending=False)
    for _, row in l1_counts.head(10).iterrows():
        pct = (row['count'] / len(df)) * 100
        report.append(f"- **{row['L1_Tag']}** ({row['L1_Category']}): {row['count']} ({pct:.1f}%)")
    report.append("")
    
    # Top L2 Categories
    report.append("## Top 10 L2 Categories\n")
    l2_counts = df[df['L2_Tag'] != 'Other'].groupby(['L2_Tag', 'L2_Category']).size().reset_index(name='count')
    l2_counts = l2_counts.sort_values('count', ascending=False)
    for idx, row in l2_counts.head(10).iterrows():
        pct = (row['count'] / len(df)) * 100
        report.append(f"{idx+1}. **{row['L2_Tag']}** - {row['L2_Category']}: {row['count']} ({pct:.1f}%)")
    report.append("")
    
    # By Confidence
    report.append("## By Confidence Level\n")
    for conf, count in df['Confidence'].value_counts().items():
        pct = (count / len(df)) * 100
        report.append(f"- **{conf}**: {count} ({pct:.1f}%)")
    report.append("")
    
    # Edge cases
    edge_cases = df[(df['Confidence'] == 'Low') | (df['L1_Tag'] == 'Other') | (df['L2_Tag'] == 'Other')]
    report.append(f"## Edge Cases (Low Confidence or 'Other')\n")
    report.append(f"Total: {len(edge_cases)} issues ({len(edge_cases)/len(df)*100:.1f}%)\n")
    
    # Write report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))
    
    print(f"  ✓ Summary report saved to: {output_file}")

def generate_edge_cases_report(df, output_file):
    """Extract edge cases for manual review."""
    
    edge_cases = df[(df['Confidence'] == 'Low') | 
                    (df['L1_Tag'] == 'Other') | 
                    (df['L2_Tag'] == 'Other')]
    
    edge_cases_report = edge_cases[[
        'issue_number', 'title', 'labels',
        'Category', 'Sentiment',
        'L1_Tag', 'L1_Category',
        'L2_Tag', 'L2_Category',
        'Confidence', 'Tagging_Notes'
    ]]
    
    edge_cases_report.to_csv(output_file, index=False)
    print(f"  ✓ Edge cases report ({len(edge_cases)} issues) saved to: {output_file}")

def generate_l1_breakdown(df, output_dir):
    """Generate breakdown by L1 category."""
    
    for l1_code in df['L1_Tag'].unique():
        if l1_code == 'Other':
            continue
        
        l1_issues = df[df['L1_Tag'] == l1_code]
        l1_name = l1_issues['L1_Category'].iloc[0]
        
        filename = f"{output_dir}/L1_{l1_code}_{l1_name.replace(' ', '_')}.csv"
        l1_issues.to_csv(filename, index=False)
    
    print(f"  ✓ L1 breakdown files saved to: {output_dir}/")

def main():
    parser = argparse.ArgumentParser(description='Analyze classified issues')
    parser.add_argument('--input', required=True, help='Input CSV with classified issues')
    parser.add_argument('--output-dir', required=True, help='Output directory for reports')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("ANALYSIS & REPORTING TOOL")
    print("=" * 80)
    
    # Load data
    print(f"\n[1/4] Loading classified issues...")
    df = pd.read_csv(args.input)
    print(f"  ✓ Loaded {len(df)} classified issues")
    
    # Generate reports
    print(f"\n[2/4] Generating summary report...")
    generate_summary_report(df, f"{args.output_dir}/summary_report.md")
    
    print(f"\n[3/4] Generating edge cases report...")
    generate_edge_cases_report(df, f"{args.output_dir}/edge_cases.csv")
    
    print(f"\n[4/4] Generating L1 category breakdowns...")
    generate_l1_breakdown(df, args.output_dir)
    
    print("\n" + "=" * 80)
    print("✓ Analysis complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
