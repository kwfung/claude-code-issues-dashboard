# 📊 WORKFLOW VISUALIZATION

## The Complete Data Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     ANTHROPIC TAKE-HOME EXERCISE                 │
│            GitHub Issues Analysis for Claude Code Team           │
└─────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: EXTRACTION                                    [10 min]│
│                                                                  │
│  python extract_github_issues.py                                │
│                                                                  │
│  GitHub API ──> 1,000 Open Issues ──> raw_issues_1000.csv      │
│                                                                  │
│  Captures: Issue #, Title, Body, URL, Dates, Comments, Labels  │
└─────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 2: AI CATEGORIZATION                             [10 min]│
│                                                                  │
│  Upload raw_issues_1000.csv to Claude.ai                        │
│  + Paste "Golden Prompt"                                        │
│  = Download enriched_issues.csv                                 │
│                                                                  │
│  Adds: Category, Priority, Summary, Sentiment                   │
│                                                                  │
│  Why one-shot? Claude has 200K token context window            │
│  1000 rows ≈ 150-200K tokens = Perfect fit!                    │
└─────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 3: VALIDATION                                     [5 min]│
│                                                                  │
│  python validate_data.py enriched_issues.csv                    │
│                                                                  │
│  Validates: Schema, Completeness, Category/Priority values      │
└─────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 4: VISUALIZATION                                 [15 min]│
│                                                                  │
│  streamlit run app.py                                           │
│                                                                  │
│  enriched_issues.csv ──> Interactive Dashboard                 │
│                                                                  │
│  Dashboard Features:                                            │
│    • Category distribution (bar chart)                          │
│    • Priority breakdown (pie chart)                             │
│    • Sentiment analysis (stacked bars)                          │
│    • Priority × Category heatmap                                │
│    • Timeline of issues                                         │
│    • Filterable issue explorer                                  │
│    • Top 10 most discussed issues                               │
└─────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────┐
│  PHASE 5: DELIVERABLES                                  [2 hrs] │
│                                                                  │
│  Using enriched_issues.csv + Dashboard insights:                │
│                                                                  │
│  1. ✅ Categorized Issue Tracker (enriched_issues.csv)         │
│  2. 📝 Themes Synthesis Memo (1-2 pages)                       │
│  3. 🎯 Prioritization Recommendation (1 page)                   │
│  4. 💬 User Communication Strategy (1 page)                     │
│  5. 🤝 Internal Validation Plan (0.5-1 page)                    │
│  6. 🔄 Evergreen Program Proposal (0.5-1 page)                  │
│                                                                  │
│  Package as: Single PDF or Google Drive folder                 │
└─────────────────────────────────────────────────────────────────┘

                              ▼

┌─────────────────────────────────────────────────────────────────┐
│  SUBMISSION                                                      │
│                                                                  │
│  Submit via Greenhouse link                                     │
│  https://app8.greenhouse.io/tests/...                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
GitHub Issues (API)
        │
        ├── Extract (Python)
        │         │
        │         ▼
        │   raw_issues_1000.csv
        │         │
        │         ├── AI Processing (Claude.ai)
        │         │   • Upload CSV
        │         │   • Golden Prompt
        │         │   • Download result
        │         │
        │         ▼
        │   enriched_issues.csv ← DELIVERABLE #1
        │         │
        │         ├──────────────────┬───────────────┐
        │         │                  │               │
        │         ▼                  ▼               ▼
        │   Dashboard       Analysis Memos    Program Design
        │   (Streamlit)     (Word/Docs)       (Word/Docs)
        │         │                  │               │
        │         └──────────────────┴───────────────┘
        │                            │
        │                            ▼
        │                     Final Submission
        │                      (PDF Package)
```

---

## Tool Stack

```
┌──────────────────────┐
│   Data Sources       │
├──────────────────────┤
│ • GitHub API         │
│ • Open Issues        │
│ • Issue Metadata     │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   Extraction Layer   │
├──────────────────────┤
│ • Python requests    │
│ • CSV export         │
│ • Rate limit mgmt    │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Processing Layer     │
├──────────────────────┤
│ • CSV manipulation   │
│ • Batch splitting    │
│ • Data validation    │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   AI Layer           │
├──────────────────────┤
│ • Claude (Anthropic) │
│ • Gemini (Google)    │
│ • Structured prompt  │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Synthesis Layer      │
├──────────────────────┤
│ • pandas (Python)    │
│ • Merge & validate   │
│ • Quality checks     │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Visualization Layer  │
├──────────────────────┤
│ • Streamlit          │
│ • Plotly charts      │
│ • Interactive UI     │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│ Documentation Layer  │
├──────────────────────┤
│ • Word/Google Docs   │
│ • PDF compilation    │
│ • Final submission   │
└──────────────────────┘
```

---

## Files Created & Their Purpose

| File | Purpose | When You Use It |
|------|---------|----------------|
| `extract_github_issues.py` | Pull issues from GitHub API | Phase 1 - Data collection |
| `validate_data.py` | Check data quality | Phase 3 - After AI processing |
| `app.py` | Dashboard visualization | Phase 4 - Understand data |
| `README.md` | Full documentation | Reference throughout |
| `QUICK_START.md` | Fast execution guide | Your main playbook |

**Note:** `split_csv.py` and `merge_enriched_chunks.py` are still included as backup tools if you need to split the data (e.g., if processing 5000+ issues or if you hit rate limits).

---

## Quality Gates

```
✓ GATE 1: raw_issues_1000.csv created with 1000 rows
    └── Proceed to: AI Processing

✓ GATE 2: enriched_issues.csv with 4 new columns added
    └── Proceed to: Validation

✓ GATE 3: validate_data.py shows "EXCELLENT" quality
    └── Proceed to: Dashboard & deliverables

✓ GATE 4: Dashboard launches and shows insights
    └── Proceed to: Writing memos

✓ GATE 5: All 6 deliverables completed
    └── Proceed to: Final submission
```

---

## Time Allocation (2-3 Hour Plan)

```
First 30 Minutes: Data Pipeline
├── 00:00-00:10  Extract from GitHub
├── 00:10-00:20  AI Processing (one upload!)
└── 00:20-00:30  Validate & launch dashboard

Next 2 Hours: Analysis & Writing
├── 00:30-01:00  Themes Synthesis Memo
├── 01:00-01:20  Prioritization Framework
├── 01:20-01:40  User Communication Strategy
├── 01:40-01:50  Internal Validation Plan
├── 01:50-02:00  Evergreen Program Proposal
├── 02:00-02:25  Review & polish all docs
└── 02:25-02:30  Package & submit
```

---

## Success Criteria

Your submission should demonstrate:

### Technical Competence
- [x] Successfully extracted data via API
- [x] Handled 1000+ records systematically
- [x] Leveraged AI tools appropriately
- [x] Validated data quality

### Product Ops Skills
- [x] Clear categorization schema
- [x] Actionable prioritization framework
- [x] User-centric communication plan
- [x] Cross-functional validation approach
- [x] Sustainable process design

### Communication
- [x] Concise, clear writing
- [x] Data-driven insights
- [x] Practical recommendations
- [x] Professional formatting
