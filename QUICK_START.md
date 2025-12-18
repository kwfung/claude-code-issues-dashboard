# 🚀 QUICK START GUIDE
## Execute Your Take-Home Assignment in 2-3 Hours

This guide gets you from zero to finished deliverables as efficiently as possible.

---

## ⏱️ Time Budget (Total: 2-3 hours)

| Task | Time | What You're Doing |
|------|------|-------------------|
| Setup & Extract | 10 min | Run script, get data |
| AI Processing | 10 min | One upload to Claude |
| Validate & Dashboard | 15 min | Check quality, explore data |
| Write Deliverables | 2 hours | Create memos & plans |

---

## 📝 EXECUTION CHECKLIST

### Phase 1: Data Collection (10 minutes)

```bash
# 1. Install Python dependencies
pip install requests

# 2. Extract 1000 issues from GitHub
python extract_github_issues.py

# ✓ Output: raw_issues_1000.csv
```

**Checkpoint:** You should now have `raw_issues_1000.csv` with 1000 rows

---

### Phase 2: AI Categorization (10 minutes)

1. **Open Claude.ai** (or Gemini)
2. **Upload** `raw_issues_1000.csv`
3. **Paste this EXACT prompt:**

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

4. **Download the result** and save as `enriched_issues.csv`

**Checkpoint:** You should have `enriched_issues.csv` with 1000 rows + 4 new columns

---

### Phase 3: Validate & Explore (15 minutes)

```bash
# Validate data quality
python validate_data.py enriched_issues.csv

# Install dashboard dependencies
pip install streamlit pandas plotly

# Launch dashboard
streamlit run app.py
```

**What to look for in the dashboard:**
- Which categories dominate?
- What's the High priority breakdown?
- Where are frustrated users concentrated?
- What themes emerge from the most-discussed issues?

**Take screenshots** of key charts for your memo!

**Checkpoint:** You understand the data landscape

---

### Phase 4: Write Deliverables (2 hours)

Now create your submission documents:

#### 📊 1. Categorized Issue Tracker (Already Done!)
- ✅ This is `enriched_issues.csv`
- Open in Excel/Google Sheets to verify
- Submit as-is or formatted nicely

#### 📝 2. Themes Synthesis Memo (30 min)

**Structure:**
```
# GitHub Issues Analysis: Claude Code

## Executive Summary
[2-3 sentences on overall findings]

## Top Themes Identified

### Theme 1: [Name] (XXX issues, XX%)
- Description: What the users are experiencing
- Examples: Issue #123, #456
- Impact: Why this matters

### Theme 2: [Name] (XXX issues, XX%)
[Repeat structure]

[Continue for 5-7 themes]

## Opportunities & Risks
- Biggest opportunity: [What would have most impact]
- Biggest risk: [What could hurt users/business most]
```

**Use your dashboard** to get the counts and percentages!

#### 🎯 3. Prioritization Recommendation (20 min)

**Framework to propose:**
```
Prioritization Matrix:
- Axis 1: Impact (User pain × Frequency)
- Axis 2: Effort (Engineering complexity)
- Priority: High Impact + Low Effort first

Top 10 Issues to Address:
1. Issue #XXX - [Title] - [Why it's critical]
2. Issue #XXX - [Title] - [Why it's critical]
[Continue...]
```

Filter your dashboard to High priority + Frustrated sentiment for quick wins

#### 💬 4. User Communication Strategy (20 min)

**Template to include:**

```
**Acknowledgment Template** (Send within 24h of report)
Subject: We've received your Claude Code feedback

Hi [Name],

Thank you for reporting [issue summary]. We've logged this as 
Issue #[number] and our team is reviewing it.

You can track progress here: [GitHub link]

We appreciate you helping us improve Claude Code!
– The Claude Code Team

---

**Status Update** (Weekly digest)
Subject: Claude Code Updates - Week of [Date]

This week we:
• Fixed 5 high-priority bugs
• Shipped 2 new features from your requests
• Are investigating [theme X]

See all updates: [Release notes link]

---

**Resolution Message** (When issue closed)
Subject: Your Claude Code issue has been resolved

Hi [Name],

Good news! Issue #[number] has been resolved in version [X.X.X].

[Brief explanation of fix]

Thanks for your patience!
```

#### 🤝 5. Internal Validation Plan (10 min)

**Stakeholders to engage:**

1. **Engineering Lead (Claude Code)** - First
   - Why: Validate technical feasibility of priorities
   - What: Are the categorizations accurate? Effort estimates?

2. **Product Manager (Claude Code)** - Second
   - Why: Align with product roadmap
   - What: Do themes match known pain points? Strategic priorities?

3. **User Research/Support Team** - Third
   - Why: Cross-reference with qualitative data
   - What: Do sentiment scores match support ticket tone?

4. **Product Ops Peers** - Fourth
   - Why: Process validation
   - What: Is the framework reusable? Any gaps?

#### 🔄 6. Evergreen Program Proposal (10 min)

**Proposed Program:**

```
# Continuous Feedback Loop System

## Cadence
- Weekly: Auto-triage new issues (AI categorization)
- Bi-weekly: Ops review + priority updates
- Monthly: Themes synthesis shared with eng/product
- Quarterly: Process refinement

## Ownership
- Product Ops: System maintenance, synthesis
- Engineering: Technical triage support
- PM: Prioritization decisions

## Tooling
- GitHub API + Python scripts (automated)
- AI categorization (Claude/GPT-4)
- Dashboard (Streamlit or Tableau)
- Slack alerts for High priority issues

## Integration
- Feed into sprint planning (bi-weekly)
- Inform roadmap discussions (quarterly)
- Support OKR tracking (quarterly)
```

---

## 📦 Final Submission Package

Combine everything into a single PDF or Google Drive folder:

```
📁 [YourName]_Anthropic_TakeHome/
├── 📊 categorized_issue_tracker.csv (or Excel)
├── 📝 themes_synthesis_memo.pdf
├── 🎯 prioritization_recommendation.pdf
├── 💬 user_communication_strategy.pdf
├── 🤝 internal_validation_plan.pdf
└── 🔄 evergreen_program_proposal.pdf
```

**OR** combine all into one clean PDF document with sections

---

## ⚡ Time-Saving Tips

1. **Use the one-shot approach** - Claude can handle 1000 rows in one upload
2. **Use dashboard for all stats** - Don't manually count categories
3. **Real issues for Top 10** - Link to actual GitHub issues in your recs
4. **Keep memos concise** - This is a 2-3 hour exercise, not a thesis
5. **Show your work** - Include snippets of your methodology

---

## 🎯 What Great Looks Like

**Great submissions demonstrate:**
- ✅ Clean, accurate data categorization
- ✅ Clear, actionable insights
- ✅ Practical, scalable systems thinking
- ✅ Empathy for users in communication
- ✅ Understanding of cross-functional dynamics

**You're NOT being judged on:**
- ❌ Perfect categorization (AI isn't perfect, that's OK)
- ❌ Length of memos (shorter + clearer wins)
- ❌ Fancy formatting (content > style)

---

## 🆘 Emergency Troubleshooting

**"GitHub API is slow/failing"**
→ The assignment says you can use the 100-issue backup spreadsheet if needed

**"AI won't output CSV"**
→ Say "Please return this as a downloadable CSV file" explicitly

**"AI is taking too long on 1000 rows"**
→ Try with 500 rows first, or split into 2 chunks of 500

**"I'm running out of time"**
→ Do 500 issues instead of 1000 (quality > quantity)

---

## ✅ Pre-Submission Checklist

- [ ] Ran `validate_data.py` and saw "EXCELLENT" quality
- [ ] All 6 deliverables created
- [ ] Used real issue numbers in examples
- [ ] Spell-checked everything
- [ ] Combined into single PDF or organized folder
- [ ] Submitted via Greenhouse link before deadline

---

**You've got this!** 🚀

The scripts handle the heavy lifting. Focus your time on thoughtful analysis and clear communication.
