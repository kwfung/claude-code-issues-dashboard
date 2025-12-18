# 🚀 START HERE

## Complete Your Take-Home in 4 Simple Steps

### ⏱️ Total Time: 2-3 hours

---

## STEP 1: Extract Data (10 minutes)

```bash
pip install requests
python extract_github_issues.py
```

✅ **Output:** `raw_issues_1000.csv`

---

## STEP 2: AI Categorization (10 minutes)

1. Go to **claude.ai**
2. Upload `raw_issues_1000.csv`
3. Paste this prompt:

```
I am uploading a CSV of GitHub issues from the Claude Code repository. 
For each row, please analyze the 'title' and 'body_preview' columns and 
add the following new columns:

1. Category: Choose ONE from:
   - Bug (broken functionality, errors, crashes)
   - Feature Request (new capability, enhancement)
   - Documentation (docs issues, unclear instructions)
   - UX/UI (usability, interface design)
   - Performance (speed, resource usage)
   - Installation/Setup (environment, dependencies)
   - Integration (third-party tools, APIs)

2. Priority: (High/Medium/Low)
   - High: Blocks core functionality, affects many users, data loss risk
   - Medium: Impacts workflow but has workarounds
   - Low: Nice-to-have, edge cases, cosmetic issues

3. Summary: A single sentence capturing the user's pain point

4. Sentiment: (Positive/Neutral/Frustrated)
   - Look for language indicating user emotion

Please return the output as a CSV with the original columns PLUS these 
four new columns. Maintain the exact same row order and issue numbers.
```

4. Download as **`enriched_issues.csv`**

✅ **Output:** `enriched_issues.csv` (your main deliverable!)

---

## STEP 3: Validate & Visualize (15 minutes)

```bash
python validate_data.py enriched_issues.csv

pip install streamlit pandas plotly
streamlit run app.py
```

✅ **Output:** Dashboard opens in browser

**Take screenshots** of key charts for your memo!

---

## STEP 4: Write Deliverables (2 hours)

Using the dashboard data, create:

1. **Categorized Issue Tracker** ✅ (You already have this: `enriched_issues.csv`)

2. **Themes Synthesis Memo** (30 min)
   - Top 5-7 themes from the issues
   - How many issues per theme
   - Opportunities & risks

3. **Prioritization Recommendation** (20 min)
   - Your prioritization framework
   - Top 10 issues to address first

4. **User Communication Strategy** (20 min)
   - Communication channels & cadence
   - 2-3 example templates

5. **Internal Validation Plan** (10 min)
   - Stakeholders to engage
   - What input to seek from each

6. **Evergreen Program Proposal** (10 min)
   - How to make this ongoing
   - Cadence, ownership, tooling

---

## 📦 Final Submission

Package all 6 deliverables as:
- Single PDF, OR
- Google Drive folder

Submit at: https://app8.greenhouse.io/tests/0e034d8ffe96f756093563f0a6382286

---

## 📚 Need More Details?

- **QUICK_START.md** - Detailed step-by-step guide with examples
- **README.md** - Full technical documentation
- **WORKFLOW_VISUAL.md** - Visual flowcharts

---

## ✨ Why This Works

- **Efficient**: Claude handles 1000 rows in one shot (200K token window)
- **Simple**: 4 steps total, no complex merging
- **Professional**: Dashboard shows you're data-fluent
- **Complete**: All deliverables use the enriched dataset

**You've got this!** 🎯
