# GitHub Issue Categorization Toolkit

A systematic toolkit for classifying and analyzing GitHub issues using a data-driven L1/L2 taxonomy.

---

## 📋 Overview

This toolkit helps you:
- ✅ Classify GitHub issues into categories (Bug, Feature Request, Documentation)
- ✅ Tag issues with L1 (primary) and L2 (subcategory) taxonomy codes
- ✅ Analyze sentiment (Positive, Neutral, Negative)
- ✅ Generate summary reports and insights
- ✅ Identify edge cases requiring manual review

---

## 🗂️ Project Structure

```
issue_categorization_toolkit/
├── scripts/
│   ├── classify_issues.py      # Main classification script
│   └── analyze_results.py      # Analysis and reporting script
├── data/
│   ├── raw_issues.csv          # Your input: GitHub issues (place here)
│   └── taxonomy_l1_l2.csv      # Your taxonomy definition
├── output/
│   └── classified_issues.csv   # Output: Classified issues
├── docs/
│   └── TAXONOMY_GUIDE.md       # Taxonomy reference
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pandas library

Install dependencies:
```bash
pip install pandas
```

### Step 1: Prepare Your Data

Place two files in the `data/` folder:

**1. `raw_issues.csv`** - Your GitHub issues export with these columns:
- `issue_number` (required)
- `title` (required)
- `body` (required)
- `labels` (required)
- Other columns (optional, will be preserved)

**2. `taxonomy_l1_l2.csv`** - Your taxonomy with these columns:
- `L1_Category` - Primary category name (e.g., "Core Functionality")
- `L1_Code` - Primary code (e.g., "L1.1")
- `L1_Description` - Description of L1 category
- `L2_Subcategory` - Subcategory name (e.g., "Context Management")
- `L2_Code` - Subcategory code (e.g., "L2.1.1")
- `L2_Description` - Description of L2 subcategory
- `Example_Keywords` - Comma-separated keywords for matching

### Step 2: Run Classification

```bash
cd issue_categorization_toolkit

python scripts/classify_issues.py \
    --input data/raw_issues.csv \
    --taxonomy data/taxonomy_l1_l2.csv \
    --output output/classified_issues.csv \
    --progress
```

This will:
- Read your issues and taxonomy
- Classify each issue
- Add 9 new columns with classifications
- Save results to `output/classified_issues.csv`

### Step 3: Generate Reports

```bash
python scripts/analyze_results.py \
    --input output/classified_issues.csv \
    --output-dir output/reports/
```

This generates:
- `summary_report.md` - Statistics and insights
- `edge_cases.csv` - Issues needing manual review
- `L1_*.csv` - Breakdown by L1 category

---

## 📊 Output Columns

The classified CSV includes all original columns plus:

| Column | Description | Example Values |
|--------|-------------|----------------|
| `Category` | Issue type | Bug, Feature Request, Documentation |
| `Summary` | Concise summary (10-20 words) | "Hooks fail silently on Windows 11..." |
| `Sentiment` | User emotion | Positive, Neutral, Negative |
| `L1_Tag` | Primary category code | L1.1, L1.5, Other |
| `L1_Category` | Primary category name | "Core Functionality", "MCP Integration" |
| `L2_Tag` | Subcategory code | L2.1.1, L2.5.2, Other |
| `L2_Category` | Subcategory name | "Context Management", "MCP Server Communication" |
| `Confidence` | Classification confidence | High, Medium, Low |
| `Tagging_Notes` | Notes on edge cases | "No L2 match found", "" |

---

## 🔧 Configuration

### Customizing Label Mapping

Edit `LABEL_TO_L1` in `classify_issues.py` to map your GitHub labels to L1 categories:

```python
LABEL_TO_L1 = {
    'area:core': 'L1.1',
    'area:api': 'L1.2',
    # Add your custom mappings here
}
```

### Customizing L2 Pattern Matching

Edit `L2_SPECIFIC_PATTERNS` to improve L2 subcategory matching:

```python
L2_SPECIFIC_PATTERNS = {
    'L2.1.1': ['context', 'compact', 'token', 'window'],
    'L2.1.2': ['session', 'conversation', 'history'],
    # Add your patterns here
}
```

---

## 📖 How It Works

### Classification Logic

**1. Issue Type (Category)**
- Checks title tags: `[Bug]`, `[Feature]`, `[Docs]`
- Checks for keywords in title and body
- Defaults to "Bug" if ambiguous

**2. Sentiment**
- **Positive**: Contains "great", "love", "appreciate", etc.
- **Negative**: Contains "frustrated", "terrible", "wasted hours", etc.
- **Neutral**: Neither positive nor negative

**3. L1 (Primary) Category**
- **Priority 1**: Uses GitHub labels (e.g., `area:core` → `L1.1`)
- **Priority 2**: Keyword matching against taxonomy
- **Priority 3**: Defaults to "Other" if no match

**4. L2 (Subcategory)**
- Matches specific patterns (e.g., "hook" → `L2.1.5`)
- Uses taxonomy keywords
- Returns "Other" if score < 2

**5. Confidence**
- **High**: Strong keyword match (score ≥ 4)
- **Medium**: Moderate match (score 2-3)
- **Low**: Weak or no match (score < 2)

---

## 🎯 Best Practices

### For Classification

1. **Start with good taxonomy** - Ensure your `taxonomy_l1_l2.csv` has:
   - Clear, non-overlapping categories
   - Good example keywords
   - 3-7 L2 subcategories per L1

2. **Review edge cases** - Always manually review:
   - Issues with `Confidence: Low`
   - Issues tagged as `Other`
   - Issues with `Negative` sentiment

3. **Iterate on patterns** - Update `L2_SPECIFIC_PATTERNS` based on:
   - Common misclassifications
   - New issue patterns
   - User feedback

### For Analysis

1. **Focus on top categories** - Prioritize:
   - L1 categories with >30% of issues
   - L2 subcategories with >10% of issues
   - High-confidence negative sentiment issues

2. **Track over time** - Re-run classification:
   - Monthly: Quick spot-check (sample 50 issues)
   - Quarterly: Full re-classification
   - Annually: Taxonomy redesign

3. **Use for planning** - Apply insights to:
   - Sprint planning (focus on top L1/L2)
   - Bug bash events (target specific L2s)
   - Documentation updates (address confusion points)

---

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas
```

### "FileNotFoundError: [Errno 2] No such file or directory: 'data/raw_issues.csv'"
- Ensure your input file is in the correct location
- Check file name matches exactly (case-sensitive)

### "KeyError: 'title'" or "KeyError: 'body'"
- Your input CSV must have columns: `issue_number`, `title`, `body`, `labels`
- Check column names match exactly

### Too many "Low" confidence classifications
- Update `L2_SPECIFIC_PATTERNS` with more keywords
- Add more example keywords to `taxonomy_l1_l2.csv`
- Review if L1/L2 categories need refinement

### Too many "Other" tags
- Check if taxonomy covers all common issue types
- Consider adding new L1 or L2 categories
- Review edge cases to identify patterns

---

## 📈 Example Workflow

### Initial Setup (One-time)
```bash
# 1. Clone or download this toolkit
# 2. Place your files in data/
cp ~/Downloads/github_issues.csv data/raw_issues.csv
cp ~/Downloads/taxonomy.csv data/taxonomy_l1_l2.csv

# 3. Run classification
python scripts/classify_issues.py \
    --input data/raw_issues.csv \
    --taxonomy data/taxonomy_l1_l2.csv \
    --output output/classified_issues.csv \
    --progress

# 4. Generate reports
python scripts/analyze_results.py \
    --input output/classified_issues.csv \
    --output-dir output/reports/

# 5. Review results
open output/reports/summary_report.md
open output/reports/edge_cases.csv
```

### Ongoing Use (Monthly/Quarterly)
```bash
# 1. Export new issues from GitHub
# 2. Place in data/ folder
# 3. Re-run classification
python scripts/classify_issues.py --input data/new_issues.csv --taxonomy data/taxonomy_l1_l2.csv --output output/new_classified.csv --progress

# 4. Compare with previous results
# 5. Update taxonomy if needed
# 6. Repeat
```

---

## 🧪 Testing

Test on a small sample first:

```bash
# Create a 10-issue sample
head -n 11 data/raw_issues.csv > data/test_sample.csv

# Run classification
python scripts/classify_issues.py \
    --input data/test_sample.csv \
    --taxonomy data/taxonomy_l1_l2.csv \
    --output output/test_results.csv

# Review results manually
open output/test_results.csv
```

---

## 📚 Additional Resources

### Taxonomy Reference
See `docs/TAXONOMY_GUIDE.md` for:
- Full L1/L2 taxonomy breakdown
- Example issues for each category
- Decision rules for edge cases

### Claude AI Integration
To use with Claude AI (claude.ai):
1. Upload your `raw_issues.csv` and `taxonomy_l1_l2.csv`
2. Copy the prompt from `docs/CLAUDE_PROMPT.md`
3. Let Claude classify your issues
4. Download results and compare with script output

### VS Code Integration
1. Open this folder in VS Code
2. Install Python extension
3. Run scripts from integrated terminal
4. Use Jupyter notebooks for interactive analysis (optional)

---

## 🤝 Contributing

To improve this toolkit:
1. Test on your own data
2. Document edge cases and improvements
3. Share updated patterns and keywords
4. Refine taxonomy based on learnings

---

## 📝 License

This toolkit is provided as-is for internal use.

---

## ❓ Support

For questions or issues:
1. Check the Troubleshooting section
2. Review `docs/TAXONOMY_GUIDE.md`
3. Examine edge cases in `output/reports/edge_cases.csv`
4. Iterate on taxonomy and patterns

---

## 🎉 Success Metrics

Your classification is working well if:
- ✅ High confidence rate > 60%
- ✅ "Other" tags < 5%
- ✅ Manual review confirms 90%+ accuracy
- ✅ Results are actionable for planning

---

**Happy Classifying! 🚀**
