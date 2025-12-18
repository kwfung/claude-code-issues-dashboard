"""
Data Quality Validation Script
Checks the enriched CSV for completeness and quality issues
"""

import pandas as pd
import sys

def validate_enriched_data(filename="enriched_issues.csv"):
    """
    Validate the enriched issues CSV for quality and completeness
    
    Args:
        filename: Path to enriched CSV file
    """
    
    print(f"\n{'='*60}")
    print(f"DATA QUALITY VALIDATION REPORT")
    print(f"{'='*60}\n")
    
    try:
        df = pd.read_csv(filename)
        print(f"✓ File loaded successfully: {filename}")
        print(f"  Total rows: {len(df)}")
        print(f"  Total columns: {len(df.columns)}")
    except FileNotFoundError:
        print(f"✗ Error: File '{filename}' not found")
        return
    except Exception as e:
        print(f"✗ Error loading file: {str(e)}")
        return
    
    print(f"\n{'='*60}")
    print("SCHEMA VALIDATION")
    print(f"{'='*60}\n")
    
    # Check for required base columns
    base_columns = [
        'issue_number', 'title', 'body_preview', 'html_url',
        'created_at', 'comments_count'
    ]
    
    enriched_columns = ['Category', 'Priority', 'Summary', 'Sentiment']
    
    missing_base = [col for col in base_columns if col not in df.columns]
    missing_enriched = [col for col in enriched_columns if col not in df.columns]
    
    if missing_base:
        print(f"⚠ Missing base columns: {', '.join(missing_base)}")
    else:
        print("✓ All base columns present")
    
    if missing_enriched:
        print(f"✗ Missing enriched columns: {', '.join(missing_enriched)}")
        print("  → Did you complete AI processing with the Golden Prompt?")
    else:
        print("✓ All enriched columns present")
    
    if missing_base or missing_enriched:
        print("\n⚠ Validation cannot continue with missing columns")
        return
    
    # Data completeness check
    print(f"\n{'='*60}")
    print("COMPLETENESS CHECK")
    print(f"{'='*60}\n")
    
    for col in enriched_columns:
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        
        if null_count == 0:
            print(f"✓ {col}: No missing values")
        else:
            print(f"⚠ {col}: {null_count} missing ({null_pct:.1f}%)")
    
    # Category validation
    print(f"\n{'='*60}")
    print("CATEGORY VALIDATION")
    print(f"{'='*60}\n")
    
    valid_categories = [
        'Bug', 'Feature Request', 'Documentation', 
        'UX/UI', 'Performance', 'Installation/Setup', 'Integration'
    ]
    
    actual_categories = df['Category'].unique()
    invalid_categories = [cat for cat in actual_categories if cat not in valid_categories]
    
    print(f"Found {len(actual_categories)} unique categories:")
    for cat in sorted(actual_categories):
        count = len(df[df['Category'] == cat])
        pct = (count / len(df)) * 100
        marker = "✓" if cat in valid_categories else "⚠"
        print(f"  {marker} {cat}: {count} issues ({pct:.1f}%)")
    
    if invalid_categories:
        print(f"\n⚠ Invalid categories found: {', '.join(invalid_categories)}")
        print("  → Expected categories: " + ', '.join(valid_categories))
    
    # Priority validation
    print(f"\n{'='*60}")
    print("PRIORITY VALIDATION")
    print(f"{'='*60}\n")
    
    valid_priorities = ['High', 'Medium', 'Low']
    actual_priorities = df['Priority'].unique()
    invalid_priorities = [pri for pri in actual_priorities if pri not in valid_priorities]
    
    for priority in valid_priorities:
        count = len(df[df['Priority'] == priority])
        pct = (count / len(df)) * 100
        print(f"  ✓ {priority}: {count} issues ({pct:.1f}%)")
    
    if invalid_priorities:
        print(f"\n⚠ Invalid priorities found: {', '.join(invalid_priorities)}")
    
    # Sentiment validation
    print(f"\n{'='*60}")
    print("SENTIMENT VALIDATION")
    print(f"{'='*60}\n")
    
    valid_sentiments = ['Positive', 'Neutral', 'Frustrated']
    actual_sentiments = df['Sentiment'].unique()
    invalid_sentiments = [sent for sent in actual_sentiments if sent not in valid_sentiments]
    
    for sentiment in valid_sentiments:
        count = len(df[df['Sentiment'] == sentiment])
        pct = (count / len(df)) * 100
        emoji = {'Positive': '😊', 'Neutral': '😐', 'Frustrated': '😤'}[sentiment]
        print(f"  {emoji} {sentiment}: {count} issues ({pct:.1f}%)")
    
    if invalid_sentiments:
        print(f"\n⚠ Invalid sentiments found: {', '.join(invalid_sentiments)}")
    
    # Summary length check
    print(f"\n{'='*60}")
    print("SUMMARY QUALITY CHECK")
    print(f"{'='*60}\n")
    
    df['summary_length'] = df['Summary'].astype(str).str.len()
    avg_length = df['summary_length'].mean()
    too_short = len(df[df['summary_length'] < 20])
    too_long = len(df[df['summary_length'] > 200])
    
    print(f"  Average summary length: {avg_length:.0f} characters")
    if too_short > 0:
        print(f"  ⚠ {too_short} summaries are very short (<20 chars)")
    if too_long > 0:
        print(f"  ⚠ {too_long} summaries are very long (>200 chars)")
    if too_short == 0 and too_long == 0:
        print(f"  ✓ All summaries are reasonable length")
    
    # Duplicate check
    print(f"\n{'='*60}")
    print("DUPLICATE CHECK")
    print(f"{'='*60}\n")
    
    duplicates = df[df.duplicated(subset=['issue_number'], keep=False)]
    if len(duplicates) > 0:
        print(f"⚠ Found {len(duplicates)} duplicate issue numbers")
        print(f"  Duplicated issues: {duplicates['issue_number'].unique()}")
    else:
        print("✓ No duplicate issue numbers found")
    
    # Final summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}\n")
    
    issues = []
    
    if missing_enriched:
        issues.append("Missing enriched columns")
    if invalid_categories:
        issues.append("Invalid category values")
    if invalid_priorities:
        issues.append("Invalid priority values")
    if invalid_sentiments:
        issues.append("Invalid sentiment values")
    if len(duplicates) > 0:
        issues.append("Duplicate issue numbers")
    
    if not issues:
        print("✅ DATA QUALITY: EXCELLENT")
        print("\nYour enriched dataset is ready for:")
        print("  • Submitting as the Categorized Issue Tracker deliverable")
        print("  • Launching the Streamlit dashboard (streamlit run app.py)")
        print("  • Creating your Themes Synthesis Memo")
    else:
        print("⚠️ DATA QUALITY: NEEDS ATTENTION")
        print("\nIssues found:")
        for issue in issues:
            print(f"  • {issue}")
        print("\nRecommendation: Fix these issues before proceeding")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    filename = "enriched_issues.csv"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    validate_enriched_data(filename)
