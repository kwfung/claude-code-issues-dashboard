import os
import csv
import time
from dotenv import load_dotenv
import anthropic

# Load API key from .env file
load_dotenv()

# Initialize the Anthropic Client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

# Configuration
INPUT_FILE = 'issues_to_triage.csv'
OUTPUT_FILE = 'prioritized_issues.csv'
MODEL_NAME = "claude-sonnet-4-5-20250929" 

# The System Prompt / Persona
SYSTEM_PROMPT = """
You are a Senior Technical Product Manager at Anthropic. Your goal is to triage GitHub issues using a strict P0-P4 framework to optimize engineering velocity and risk management.

Evaluate each issue based on the following Priority Logic:

1. P0: Critical / Existential (Immediate Hotfix)
   - Definition: Issues costing significant money, brand trust, or causing liability.
   - Triggers: Security vulnerabilities (exposed API keys, secrets), Data Corruption, Total System Outages, or Unbounded Resource Consumption (e.g., infinite loops costing tokens).
   - Label hints: area:security, privacy, data-loss.

2. P1: High Impact / Blocker (Next Cycle)
   - Definition: Issues causing significant friction where workarounds are costly or error-prone.
   - Triggers: Core workflow failures (e.g., Session Context loss, Authentication loops), Viral complaints (>50 reactions OR >20 comments), or Blockers for strategic adoption.

3. P2: Standard / Quality of Life (3 Months)
   - Definition: Important fixes that should happen at a steady cadence. Workarounds are easy/known.
   - Triggers: Cosmetic bugs, Non-blocking UI glitches, Edge-case failures, TUI formatting issues.

4. P3: Minor / Backlog (6 Months)
   - Definition: Tasks we should do, but aren't harming us greatly.
   - Triggers: Typos, minor documentation fixes, "Paper Cut" issues.

5. P4: Won't Do / Icebox
   - Definition: Items below the value line or not worth the setup time.
   - Triggers: Vague requests, duplicates, or issues likely resolved implicitly by future architecture changes.

Task: Analyze the issue data provided and return the result in CSV format with three columns: issue_number, priority, and reasoning.

Format: issue_number,priority,"reasoning"
Constraint: Enclose the reasoning in double quotes. Do not output a header row. Do not include Markdown.
"""


def get_issue_analysis(row, max_retries=3):
    """Sends a single issue row to Claude for analysis with retry logic."""

    # Construct the user message based on the CSV row data
    user_message = f"""
    Input Data for this row:
    Issue Number: {row.get('issue_number', 'N/A')}
    Title: {row.get('title', 'N/A')}
    Labels: {row.get('labels', '')}
    Category: {row.get('Category', '')}
    Sentiment: {row.get('Sentiment', '')}
    Reactions: {row.get('reactions_total', 0)}
    Comments: {row.get('comments_count', 0)}
    Description Snippet: {row.get('body', '')[:300]}
    """

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            return response.content[0].text.strip()
        except anthropic.RateLimitError as e:
            print(f"Rate limit hit for issue {row.get('issue_number')}, attempt {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))  # Exponential backoff
            else:
                print(f"Failed after {max_retries} retries due to rate limiting: {e}")
                return None
        except anthropic.APIError as e:
            print(f"API error processing issue {row.get('issue_number')}, attempt {attempt + 1}/{max_retries}: {type(e).__name__} - {e}")
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                print(f"Failed after {max_retries} retries: {e}")
                return None
        except Exception as e:
            print(f"Unexpected error processing issue {row.get('issue_number')}: {type(e).__name__} - {e}")
            return None

    return None

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please ensure the file exists.")
        return

    print(f"Starting triage process using {MODEL_NAME}...")
    
    # Prepare output file
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write Header
        writer.writerow(['issue_number', 'priority', 'reasoning'])

        # Read Input File
        with open(INPUT_FILE, mode='r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            
            count = 0
            for row in reader:
                count += 1
                print(f"Processing Issue #{row.get('issue_number')}...")
                
                # Get analysis from Claude
                raw_response = get_issue_analysis(row)
                
                if raw_response:
                    # Parse the CSV string returned by Claude
                    # We use the csv module to handle the parsing of the string to respect quotes
                    try:
                        parsed_line = list(csv.reader([raw_response]))[0]

                        # Validate response format
                        if len(parsed_line) != 3:
                            print(f"Invalid response format for issue {row.get('issue_number')}: Expected 3 fields, got {len(parsed_line)}")
                            writer.writerow([row.get('issue_number'), "ERROR", f"Invalid format: {raw_response}"])
                        elif parsed_line[1] not in ['P0', 'P1', 'P2', 'P3', 'P4']:
                            print(f"Invalid priority '{parsed_line[1]}' for issue {row.get('issue_number')}")
                            writer.writerow([row.get('issue_number'), "ERROR", f"Invalid priority: {raw_response}"])
                        else:
                            writer.writerow(parsed_line)
                    except (csv.Error, IndexError) as e:
                        print(f"CSV parsing error for issue {row.get('issue_number')}: {type(e).__name__} - {e}")
                        print(f"Raw response: {raw_response}")
                        writer.writerow([row.get('issue_number'), "ERROR", f"Parse error: {raw_response}"])
                    except Exception as e:
                        print(f"Unexpected parsing error for issue {row.get('issue_number')}: {type(e).__name__} - {e}")
                        writer.writerow([row.get('issue_number'), "ERROR", f"Unexpected error: {raw_response}"])
                else:
                    # No response received (likely due to API errors)
                    writer.writerow([row.get('issue_number'), "ERROR", "No response from API"])
                
                # Sleep briefly to avoid rate limits (optional)
                time.sleep(0.5)

    print(f"Done! {count} issues processed. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()