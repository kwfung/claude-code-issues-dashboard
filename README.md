# Claude Code GitHub Issues Analysis
## Product Operations Workflow

This repository contains a **manual two-step approach** for analyzing 1,000 GitHub issues from the `anthropics/claude-code` repository .

---

## 🎯 Overview

**Goal**: Review and groom 1,000 open issues from Claude Code's GitHub repository to demonstrate:
- Voice of customer synthesis
- Analytical rigor  
- Cross-functional communication
- Systems thinking
- Tool fluency (AI-assisted workflow)

**Approach**: Clean data extraction → AI-powered batch categorization → Dashboard visualization

---

## 📋 Prerequisites

- Python 3.8+
- Internet connection (for GitHub API)
- Access to Claude/Gemini (for AI categorization)
- VS Code or any Python IDE

---

## 🚀 Step-by-Step Workflow

### **STEP 1: Extract Raw Issues from GitHub**

This creates your "source of truth" dataset.

```bash
# Install dependencies
pip install -r requirements_extract.txt

# Run extraction script (fetches 1000 issues by default)
python extract_github_issues.py

# Output: raw_issues_1000.csv
```

**What this does:**
- Fetches the most recent 1,000 open issues via GitHub API
- Captures: issue #, title, body preview (500 chars), URL, dates, comments count, labels, author
- Saves to `raw_issues_1000.csv` - this is your backup if anything fails later

**Pro tip:** You can customize the number of issues:
```bash
python extract_github_issues.py 500  # Fetch only 500 issues
```

---

### **STEP 2: AI-Powered Categorization**

Upload the entire CSV to Claude with the **Golden Prompt**:

#### 🌟 The Golden Prompt

```
I am uploading a CSV of GitHub issues from the Claude Code repository. 
For each row, please analyze the 'title' and 'body_preview' columns and 
add the following new columns:

1. **Category**: Choose ONE from:
   - Bug (broken functionality, errors, crashes)
   - Feature Request (new capability, enhancement)
   - Documentation (docs issues, unclear instructions)
   - UX/UI (usability, interface design)
   - Performance (speed, resource usage)
   - Installation/Setup (environment, dependencies)
   - Integration (third-party tools, APIs)

2. **Priority**: (High/Medium/Low)
   - High: Blocks core functionality, affects many users, data loss risk
   - Medium: Impacts workflow but has workarounds
   - Low: Nice-to-have, edge cases, cosmetic issues

3. **Summary**: A single sentence capturing the user's pain point

4. **Sentiment**: (Positive/Neutral/Frustrated)
   - Look for language indicating user emotion

Please return the output as a CSV with the original columns PLUS these 
four new columns. Maintain the exact same row order and issue numbers.
```

#### Processing Workflow

1. **Open Claude.ai** (or Gemini)
2. **Upload** `raw_issues_1000.csv`
3. **Paste** the Golden Prompt above
4. **Download** the enriched CSV as `enriched_issues.csv`

**That's it!** Claude can handle all 1000 rows in one shot with its 200K token context window.

---

### **STEP 3: Validate Data Quality**

Check your enriched dataset for completeness:

```bash
python validate_data.py enriched_issues.csv
```

**Output:** `enriched_issues.csv` with all original columns + 4 new AI-generated columns:
- ✅ Category
- ✅ Priority  
- ✅ Summary
- ✅ Sentiment

This is your **Categorized Issue Tracker deliverable** - you can submit this directly or open it in Excel/Google Sheets.

---

### **STEP 4: Launch Dashboard**

Visualize your analysis with an interactive Streamlit dashboard:

```bash
# Install dashboard dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

**Dashboard Features:**
- 📊 **Key Metrics**: Total issues, high priority count, frustrated users, avg comments
- 📂 **Category Distribution**: Bar chart of issues by category
- 🎯 **Priority Breakdown**: Pie chart with High/Medium/Low split
- 😊 **Sentiment Analysis**: Sentiment distribution across categories
- 🔥 **Priority × Category Heatmap**: Where to focus efforts
- 📅 **Timeline**: Issues opened over time
- 🔍 **Issue Explorer**: Filterable table with all issues
- 💬 **Most Discussed**: Top 10 issues by comment count

---

## 📂 File Structure

```
.
├── extract_github_issues.py      # Step 1: Pull issues from GitHub
├── validate_data.py              # Step 3: Validate enriched data
├── app.py                        # Step 4: Streamlit dashboard
├── requirements_extract.txt      # Dependencies for extraction
├── requirements.txt              # Dependencies for dashboard
├── README.md                     # This file
│
├── raw_issues_1000.csv          # ← Output from Step 1
│
└── enriched_issues.csv          # ← Output from Step 2 (DELIVERABLE!)
```

---

## 📦 Deliverables Checklist

Using the enriched dataset, you need to create:

- [ ] **Categorized Issue Tracker** (spreadsheet)
  - ✅ `enriched_issues.csv` serves as this
  - Contains: Issue #, Title, Category, Priority, Summary, Sentiment
  
- [ ] **Themes Synthesis Memo** (1-2 pages)
  - Top 5-7 themes across issues
  - Supporting data (counts per theme)
  - Assessment of opportunities/risks
  
- [ ] **Prioritization Recommendation** (1 page)
  - Recommended prioritization framework
  - Top 10 issues to address with rationale
  
- [ ] **User Communication Strategy** (1 page)
  - Communication channels, cadence, tone
  - 2-3 example templates (acknowledgment, update, resolution)
  
- [ ] **Internal Validation Plan** (0.5-1 page)
  - Stakeholders to engage before sharing findings
  - What input you'd seek from each
  - Conversation sequencing
  
- [ ] **Evergreen Program Proposal** (0.5-1 page)
  - How to make this a sustainable, ongoing process
  - Cadence, ownership, tooling, integration with product planning

---

## 💡 Pro Tips

### Why This Approach Works

1. **Separation of Concerns**: Raw data extraction is separate from AI processing - if AI fails, you don't lose data
2. **Quality over Speed**: Batch processing (250 issues at a time) maintains high categorization quality
3. **Auditability**: Each step produces a clear output you can review
4. **Scalability**: This same workflow could handle 10,000 issues

### Time Management (2-3 hours total)

- **Data Extraction**: 10 minutes
- **Splitting & Setup**: 5 minutes  
- **AI Processing** (4 chunks): 30-40 minutes
- **Merging**: 2 minutes
- **Dashboard Review**: 15 minutes
- **Writing Deliverables**: 60-90 minutes

### AI Tool Choice

- **Claude** (claude.ai): Great for nuanced categorization, handles CSV well
- **Gemini**: Fast batch processing, good structured output
- **Both work!** Use what you're comfortable with

---

## 🎓 What This Demonstrates

This workflow showcases Product Ops competencies:

✅ **Tool Fluency**: Python scripts + AI tools + data visualization  
✅ **Systems Thinking**: Designed for scalability, not one-time use  
✅ **Analytical Rigor**: Structured categorization schema with clear definitions  
✅ **Resourcefulness**: Practical approach using GitHub API + AI  
✅ **Quality Focus**: Batch processing maintains high AI output quality

---

## 🔧 Troubleshooting

**GitHub API Rate Limit?**
- Default limit: 60 requests/hour (unauthenticated)
- Script includes rate limit handling and will pause if needed
- If hitting limits, wait 1 hour or use a GitHub Personal Access Token

**AI Output Not CSV?**
- If Claude/Gemini returns Markdown tables, ask it to "return as downloadable CSV"
- Emphasize "maintain exact same row order and issue numbers"

**Chunks Won't Merge?**
- Check that column names match exactly (case-sensitive)
- Ensure all chunks are in `enriched_chunks/` directory
- Verify each chunk has the 4 new columns: Category, Priority, Summary, Sentiment

**Dashboard Won't Load?**
- Check that `enriched_issues.csv` exists in the same directory as `app.py`
- Ensure all requirements are installed: `pip install -r requirements.txt`

---

## 📬 Questions?

This README should give you everything needed to complete the exercise. Good luck! 🚀

---

## 📄 License

This is for interview/educational purposes. Anthropic's Claude Code issues are public on GitHub.
