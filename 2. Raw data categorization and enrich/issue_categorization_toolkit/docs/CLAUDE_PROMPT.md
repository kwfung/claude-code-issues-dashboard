# Claude AI Classification Prompt

Use this prompt when classifying issues with Claude AI at claude.ai

---

## Prompt Template

```markdown
I am uploading a CSV of GitHub issues that needs systematic classification.

INPUT FILES:
1. **github_issues.csv** - Contains issue data with columns: issue_number, title, body, labels
2. **taxonomy_l1_l2.csv** - Contains the L1/L2 taxonomy with columns: L1_Category, L1_Code, L1_Description, L2_Subcategory, L2_Code, L2_Description, Example_Keywords

TASK:
For each row in github_issues.csv, analyze the 'title' and 'body' columns and add these NEW columns:

---

### 1. **Category** (Issue Type)
Choose EXACTLY ONE:
- **Bug** - Broken functionality, errors, crashes, regressions, unexpected behavior
- **Feature Request** - New capability, enhancement, improvement to existing feature
- **Documentation** - Docs issues, unclear instructions, missing documentation

**Decision Rules:**
- If it worked before and broke → Bug
- If it never worked and user wants it → Feature Request
- If functionality works but explanation is lacking → Documentation
- When ambiguous, default to Bug if there's any mention of "error", "fails", "doesn't work"

---

### 2. **Summary** 
A single concise sentence (10-20 words) capturing the user's core pain point or request.

**Format:** "[User/System] cannot [action] because [reason]" OR "[User] wants to [capability]"

**Good Examples:**
- "Context compaction fails with 'conversation too long' error in multi-agent workflows"
- "Users want Git-like history navigation to branch conversations without context pollution"

**Bad Examples:**
- "Issue with context" (too vague)
- "The user is experiencing problems when they try to use the context management feature..." (too long)

---

### 3. **Sentiment**
Choose EXACTLY ONE:
- **Positive** - Appreciative, constructive, enthusiastic (e.g., "Love the tool but would like...")
- **Neutral** - Factual, matter-of-fact, no emotion (e.g., "Feature X doesn't work")
- **Negative** - Annoyed, blocked, urgent (e.g., "This is completely broken", "Wasted hours")

**Decision Rules:**
- Look for: exclamation marks, capital letters, "frustrated", "annoying", "terrible", "broken"
- Positive indicators: "love", "great", "appreciate", "thanks", constructive tone
- Default to Neutral when unclear

---

### 4. **L1_Tag** (Primary Category)
Map each issue to EXACTLY ONE L1 category from the taxonomy_l1_l2.csv file.

**Matching Process:**
1. Read the issue title and body
2. Identify primary affected component/system
3. Match against L1_Description and Example_Keywords columns
4. Choose the BEST FIT L1_Code (e.g., "L1.1", "L1.2", etc.)

**Decision Rules:**
- Use Example_Keywords from taxonomy for fuzzy matching
- If issue spans multiple L1s, choose the PRIMARY one (what's most broken/requested)
- If truly ambiguous, choose the L1 that would own the fix
- If no good match (score < 2), use "Other"

**Output Format:** Use L1_Code (e.g., "L1.1", "L1.3") NOT the category name

---

### 5. **L1_Category**
The category NAME corresponding to L1_Tag.

**Output Format:** Use the L1_Category name from taxonomy (e.g., "Core Functionality", "MCP Integration")
If L1_Tag is "Other", use "Other"

---

### 6. **L2_Tag** (Subcategory)
Map each issue to EXACTLY ONE L2 subcategory that aligns with the chosen L1_Tag.

**Matching Process:**
1. Filter taxonomy to only L2s under the chosen L1
2. Match issue content against L2_Description and Example_Keywords
3. Choose the BEST FIT L2_Code (e.g., "L2.1.1", "L2.3.2", etc.)

**Decision Rules:**
- L2_Tag MUST be a subcategory of the chosen L1_Tag (e.g., if L1 = L1.1, L2 must be L2.1.x)
- Use the most specific L2 that applies
- If no L2 fits well (score < 2), use "Other"

**Output Format:** Use L2_Code (e.g., "L2.1.1", "L2.3.4") NOT the subcategory name

---

### 7. **L2_Category**
The subcategory NAME corresponding to L2_Tag.

**Output Format:** Use the L2_Subcategory name from taxonomy (e.g., "Context Management", "MCP Server Communication")
If L2_Tag is "Other", use "Other"

---

### 8. **Confidence**
For L1 and L2 tagging, rate your confidence:
- **High** - Clear match, obvious category (90%+ certain)
- **Medium** - Reasonable match, some ambiguity (70-90% certain)
- **Low** - Best guess, significant ambiguity (<70% certain)

This helps identify issues that need manual review.

---

### 9. **Tagging_Notes**
Brief note on tagging decisions, especially for:
- Low confidence tags
- Issues that span multiple categories
- Unusual or ambiguous cases
- Issues that don't fit taxonomy well

Leave blank if straightforward.

---

## OUTPUT REQUIREMENTS

**Return a CSV file with:**
1. ALL original columns from github_issues.csv (in same order)
2. NEW columns appended: Category, Summary, Sentiment, L1_Tag, L1_Category, L2_Tag, L2_Category, Confidence, Tagging_Notes
3. SAME row order as input (sorted by issue_number)
4. NO missing values - every cell must have a value (use "Unknown" if truly cannot classify)

**CSV Format Requirements:**
- Use comma as delimiter
- Escape commas within fields with quotes
- UTF-8 encoding
- Include header row
- Preserve issue_number as first column for easy validation

---

## QUALITY CHECKS (Run Before Returning)

Before providing the output CSV, verify:
1. ✓ Row count matches input exactly
2. ✓ All issue_numbers present and in correct order
3. ✓ No missing values in new columns
4. ✓ All L1_Tag values are valid L1_Codes from taxonomy (L1.1 through L1.10) or "Other"
5. ✓ All L2_Tag values are valid L2_Codes from taxonomy (L2.x.x) or "Other"
6. ✓ Each L2_Tag is a child of its corresponding L1_Tag (e.g., L1.1 → L2.1.x)
7. ✓ Category values are only: Bug, Feature Request, or Documentation
8. ✓ Sentiment values are only: Positive, Neutral, or Negative
9. ✓ Confidence values are only: High, Medium, or Low

---

## DELIVERABLES

1. **Classified CSV file** - Full output with all columns
2. **Summary Statistics** - Count by Category, L1_Tag, L2_Tag, Sentiment, Confidence
3. **Edge Cases Report** - List of issues with Low confidence or unusual Tagging_Notes
4. **Validation Report** - Confirmation that all quality checks passed

Begin by showing me sample output for first 5 rows for validation before processing all issues.
```

---

## How to Use

1. Go to claude.ai
2. Start a new conversation
3. Upload your files:
   - `github_issues.csv`
   - `taxonomy_l1_l2.csv`
4. Copy-paste the prompt above
5. Review the 5-row sample Claude provides
6. Approve processing of all issues
7. Download the classified CSV

---

## Tips for Best Results

- Upload clean CSVs (UTF-8 encoded, no special characters in headers)
- Start with a small sample (10-20 issues) to verify taxonomy fit
- Review edge cases and adjust taxonomy as needed
- Re-run quarterly to track taxonomy drift

---
