"""
GitHub Issues Extraction Script for Claude Code Repository
Extracts issues with all relevant metadata for Product Ops analysis
"""

import requests
import csv
import time
from datetime import datetime
import sys

# Configuration
REPO_OWNER = "anthropics"
REPO_NAME = "claude-code"
TARGET_ISSUES = 1000  # Can be adjusted
OUTPUT_FILE = "raw_issues_1000.csv"

# GitHub API endpoint
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

def fetch_issues(num_issues=1000, state='open'):
    """
    Fetch issues from GitHub repository

    Args:
        num_issues: Number of issues to fetch (default 1000)
        state: 'open', 'closed', or 'all' (default 'all')

    Returns:
        List of issue dictionaries
    """
    issues = []
    page = 1
    per_page = 100  # GitHub API max per page

    print(f"Starting extraction of {num_issues} {state} issues from {REPO_OWNER}/{REPO_NAME}...")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    while len(issues) < num_issues:
        try:
            # GitHub API parameters
            params = {
                'state': state,
                'page': page,
                'per_page': per_page,
                'sort': 'created',
                'direction': 'desc'
            }
            
            print(f"Fetching page {page} (issues {len(issues)+1}-{min(len(issues)+per_page, num_issues)})...", end=' ')
            
            response = requests.get(BASE_URL, params=params)
            
            # Check rate limit
            rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
            if rate_limit_remaining:
                print(f"[Rate limit: {rate_limit_remaining} remaining]", end=' ')
            
            if response.status_code == 200:
                batch = response.json()
                
                if not batch:  # No more issues
                    print("\nNo more issues available.")
                    break
                
                issues.extend(batch)
                print(f"✓ ({len(batch)} issues)")
                
                page += 1
                
                # Respect rate limits with a small delay
                time.sleep(0.5)
                
            elif response.status_code == 403:
                print(f"\n⚠ Rate limit exceeded. Wait before continuing.")
                print(f"Response: {response.json()}")
                break
                
            else:
                print(f"\n✗ Error: {response.status_code}")
                print(f"Response: {response.text}")
                break
                
        except Exception as e:
            print(f"\n✗ Exception: {str(e)}")
            break
    
    # Trim to exact number requested
    issues = issues[:num_issues]
    
    print(f"\n{'='*60}")
    print(f"✓ Successfully extracted {len(issues)} issues")
    print(f"{'='*60}\n")
    
    return issues

def extract_issue_data(issue):
    """
    Extract relevant fields from GitHub issue object

    Args:
        issue: GitHub issue dictionary

    Returns:
        Dictionary with cleaned issue data
    """
    # Extract labels
    labels = [label['name'] for label in issue.get('labels', [])]
    labels_str = ', '.join(labels) if labels else ''

    # Full body (not truncated)
    body = issue.get('body') or ''
    # Clean body for CSV (remove excessive whitespace but keep structure)
    body_clean = ' '.join(body.split())

    # Extract reactions
    reactions = issue.get('reactions', {})
    reactions_total = reactions.get('total_count', 0)
    reactions_plus1 = reactions.get('+1', 0)
    reactions_minus1 = reactions.get('-1', 0)
    reactions_heart = reactions.get('heart', 0)
    reactions_hooray = reactions.get('hooray', 0)
    reactions_rocket = reactions.get('rocket', 0)
    reactions_eyes = reactions.get('eyes', 0)

    # Extract assignees
    assignees = [assignee['login'] for assignee in issue.get('assignees', [])]
    assignees_str = ', '.join(assignees) if assignees else ''

    # Extract milestone
    milestone = issue.get('milestone')
    milestone_title = milestone['title'] if milestone else ''

    # Check if it's a pull request
    is_pull_request = 'pull_request' in issue

    # Extract author association
    author_association = issue.get('author_association', '')

    # Extract closed info
    closed_at = issue.get('closed_at', '')
    closed_by = issue.get('closed_by')
    closed_by_login = closed_by['login'] if closed_by else ''

    # State reason
    state_reason = issue.get('state_reason', '')

    return {
        'issue_number': issue['number'],
        'title': issue['title'],
        'body': body_clean,
        'html_url': issue['html_url'],
        'state': issue['state'],
        'created_at': issue['created_at'],
        'updated_at': issue['updated_at'],
        'closed_at': closed_at,
        'comments_count': issue['comments'],
        'labels': labels_str,
        'author': issue['user']['login'],
        'author_association': author_association,
        'assignees': assignees_str,
        'milestone': milestone_title,
        'is_pull_request': is_pull_request,
        'locked': issue.get('locked', False),
        'state_reason': state_reason,
        'closed_by': closed_by_login,
        'reactions_total': reactions_total,
        'reactions_plus1': reactions_plus1,
        'reactions_minus1': reactions_minus1,
        'reactions_heart': reactions_heart,
        'reactions_hooray': reactions_hooray,
        'reactions_rocket': reactions_rocket,
        'reactions_eyes': reactions_eyes
    }

def save_to_csv(issues, filename):
    """
    Save issues to CSV file
    
    Args:
        issues: List of issue dictionaries
        filename: Output CSV filename
    """
    if not issues:
        print("No issues to save.")
        return
    
    fieldnames = [
        'issue_number',
        'title',
        'body',
        'html_url',
        'state',
        'state_reason',
        'created_at',
        'updated_at',
        'closed_at',
        'comments_count',
        'labels',
        'author',
        'author_association',
        'assignees',
        'milestone',
        'is_pull_request',
        'locked',
        'closed_by',
        'reactions_total',
        'reactions_plus1',
        'reactions_minus1',
        'reactions_heart',
        'reactions_hooray',
        'reactions_rocket',
        'reactions_eyes'
    ]
    
    print(f"Saving to {filename}...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for issue_raw in issues:
            issue_data = extract_issue_data(issue_raw)
            writer.writerow(issue_data)
    
    print(f"✓ Saved {len(issues)} issues to {filename}")
    print(f"\nFields included:")
    for field in fieldnames:
        print(f"  • {field}")

def main():
    """Main execution function"""
    
    # Allow command-line argument for number of issues
    num_issues = TARGET_ISSUES
    if len(sys.argv) > 1:
        try:
            num_issues = int(sys.argv[1])
            print(f"Custom target: {num_issues} issues\n")
        except ValueError:
            print(f"Invalid number. Using default: {TARGET_ISSUES}\n")
    
    # Fetch issues
    issues = fetch_issues(num_issues)
    
    if not issues:
        print("No issues fetched. Exiting.")
        return
    
    # Save to CSV
    output_filename = f"raw_issues_{len(issues)}.csv"
    save_to_csv(issues, output_filename)
    
    # Summary statistics
    print(f"\n{'='*60}")
    print("EXTRACTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total issues extracted: {len(issues)}")
    print(f"Output file: {output_filename}")
    print(f"Date range: {issues[-1]['created_at'][:10]} to {issues[0]['created_at'][:10]}")

    # Calculate statistics
    prs = sum(1 for i in issues if 'pull_request' in i)
    true_issues = len(issues) - prs
    with_reactions = sum(1 for i in issues if i.get('reactions', {}).get('total_count', 0) > 0)
    total_reactions = sum(i.get('reactions', {}).get('total_count', 0) for i in issues)
    open_issues = sum(1 for i in issues if i['state'] == 'open')
    closed_issues = sum(1 for i in issues if i['state'] == 'closed')

    print(f"\nBreakdown:")
    print(f"  • Issues: {true_issues}")
    print(f"  • Pull Requests: {prs}")
    print(f"  • Open: {open_issues}")
    print(f"  • Closed: {closed_issues}")
    print(f"  • With reactions: {with_reactions}")
    print(f"  • Total reactions: {total_reactions}")

    print(f"\nNext step: Use this CSV for AI-powered categorization and prioritization")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
