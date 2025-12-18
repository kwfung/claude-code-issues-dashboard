# REUSABLE PROMPT: TAXONOMY VALIDATION & REFINEMENT

## Purpose
This prompt helps you validate whether your existing issue taxonomy is still accurate and relevant as new issues come in. Run this quarterly or when you have 1000+ new issues to analyze.

---

## PROMPT TO USE

```
I need you to validate and potentially refine my existing L1/L2 taxonomy for GitHub issues.

CONTEXT:
I have an existing taxonomy with these L1 categories:
1. Core Functionality (L1.1)
2. API & Integration (L1.2)
3. Terminal UI (L1.3)
4. Tools & Execution (L1.4)
5. MCP Integration (L1.5)
6. IDE Integration (L1.6)
7. Model & Reasoning (L1.7)
8. Platform-Specific (L1.8)
9. Performance & Resources (L1.9)
10. Security (L1.10)

Each L1 has multiple L2 subcategories. The full taxonomy is attached as: [taxonomy_l1_l2.csv]

TASK:
I'm attaching a CSV file with [NUMBER] new GitHub issues collected since our last analysis. Please:

1. QUANTITATIVE ANALYSIS
   - Load and analyze all issues systematically
   - Count issues by existing labels
   - Extract keywords from titles and bodies
   - Identify error patterns in issue content
   - Calculate label co-occurrence
   - Generate frequency distributions

2. TAXONOMY VALIDATION
   - Map issues to existing L1/L2 categories
   - Calculate coverage: What % of issues fit cleanly into existing taxonomy?
   - Identify gaps: What issues don't fit well?
   - Measure category sizes: Are proportions still similar to baseline?

3. EMERGING THEMES
   - Identify NEW themes that have emerged
   - Flag categories that have grown/shrunk significantly
   - Detect new subcategories within existing L1s
   - Find new co-occurrence patterns

4. RECOMMENDATIONS
   For EACH of the following, provide specific data-backed recommendations:
   - Should any L1 categories be added?
   - Should any L1 categories be merged or removed?
   - Should any L2 subcategories be added/removed?
   - Should any categories be promoted/demoted based on volume?
   - Are there new cross-cutting tags needed?

5. DELIVERABLES
   Provide:
   a) Updated taxonomy CSV with new issue counts and percentages
   b) "Changes Report" documenting what shifted and why
   c) Top 10 issues in each L1 category (by volume) for spot-check validation
   d) Statistical comparison: old vs. new distributions
   e) Confidence assessment: How confident are you the taxonomy still works?

ANALYSIS METHODOLOGY:
- Use the same data-driven approach as the original analysis
- Run statistical tests to detect significant shifts
- Sample issues for qualitative validation
- Show your work with actual issue counts and percentages
- Be honest about limitations and edge cases

ATTACHED FILES:
1. [new_issues_1000.csv] - New issues to analyze
2. [taxonomy_l1_l2.csv] - Current taxonomy baseline (optional but helpful)

Begin with loading and exploring the data, then proceed systematically through each analysis step.
```

---

## WHAT TO ATTACH

1. **Required:** CSV file with new issues (same format as before)
   - Columns: issue_number, title, body, labels, created_at, etc.
   
2. **Optional but helpful:** The taxonomy baseline CSV
   - This helps me compare against the original distribution

---

## EXPECTED OUTPUT

You should receive:

1. **Updated Taxonomy CSV** 
   - Same structure as original
   - New issue counts and percentages
   - Flagged changes (e.g., "↑ 45% increase")

2. **Validation Report** covering:
   - Coverage: X% of issues fit existing taxonomy
   - New themes identified: [list]
   - Significant shifts: [category] grew from X% to Y%
   - Recommendations: Add/remove/modify [specific categories]

3. **Statistical Comparison**
   - Old vs. new distribution table
   - Chi-square test or similar to detect significant changes
   - Confidence score on taxonomy stability

4. **Sample Issues**
   - Top 5-10 issues per category for spot-checking
   - Edge cases that don't fit well
   - Representative examples of new themes

---

## INTERPRETATION GUIDE

### When to Update Taxonomy

**DEFINITELY UPDATE if:**
- Coverage drops below 90% (too many issues don't fit)
- A new theme represents >5% of issues and has no category
- An existing L1 category drops below 3% (consider merging/removing)
- A subcategory grows >15% and needs promotion to L1

**CONSIDER UPDATING if:**
- Proportions shift >20% within an L1 category
- New L2 subcategories emerge with >10 issues
- User language changes (new keywords/terms)
- Co-occurrence patterns shift significantly

**PROBABLY DON'T UPDATE if:**
- Proportions shift <10%
- Coverage remains >95%
- Changes are random noise, not systematic trends
- It's been <3 months since last analysis (too soon)

### Red Flags

Watch for these warning signs:
- Many issues tagged "other" or "miscellaneous"
- Frequent need for multiple L1 tags per issue
- Team debates about which category to use
- Categories become catch-alls (>40% of issues)

---

## FREQUENCY OF VALIDATION

Recommended cadence:

**Monthly:** Quick spot-check of new issues
- Sample 50 recent issues
- Quick review: Do they fit taxonomy?
- Flag any obvious gaps

**Quarterly:** Full validation (use this prompt)
- Analyze all new issues since last full validation
- Statistical comparison
- Update taxonomy if needed

**Annually:** Complete taxonomy redesign
- Start fresh with full year of data
- Rebuild from ground up
- Major version change (e.g., v1 → v2)

---

## TIPS FOR BEST RESULTS

1. **Provide context in your prompt**
   - How long has it been since last validation?
   - Any known product changes that might shift issues?
   - Specific concerns you're investigating?

2. **Use consistent data format**
   - Same CSV columns as original analysis
   - Same label naming conventions
   - Include full issue bodies, not just titles

3. **Set expectations for rigor**
   - Request statistical significance testing
   - Ask for confidence intervals
   - Demand data backing every recommendation

4. **Don't over-react to small shifts**
   - Taxonomy doesn't need to be perfect
   - Some instability is normal
   - Update when patterns are clear, not on noise

---

## EXAMPLE FOLLOW-UP QUESTIONS

After initial validation, you might ask:

- "The 'Context Management' category grew 30%. Can you sample 20 of these issues and tell me if they're genuinely new patterns or just volume?"

- "You identified 'Plugin Ecosystem' as an emerging theme. Is this big enough to be a new L1 category, or should it be a L2 under MCP Integration?"

- "Coverage dropped to 87%. Show me the 50 issues that don't fit well. What's the common thread?"

- "Performance issues grew from 8.5% to 15%. Drill into this - what specifically changed? Memory? Latency? CPU?"

---

## AUTOMATION POTENTIAL

This validation process can be partially automated:

**Automate:**
- Data loading and cleaning
- Label frequency counting
- Keyword extraction
- Statistical comparison
- Coverage calculation

**Keep manual:**
- Qualitative assessment of new themes
- Decision on taxonomy changes
- Spot-checking representative issues
- Strategic recommendations

Consider building a lightweight dashboard that auto-runs this analysis monthly and flags when manual review is needed.

---

## VERSION CONTROL

Maintain taxonomy versions:

```
v1.0 (Dec 2025): Initial taxonomy based on 1,000 issues
v1.1 (Mar 2026): Added "Plugin Ecosystem" L2 under MCP Integration
v1.2 (Jun 2026): Promoted "Performance" subcategories to dedicated L2s
v2.0 (Dec 2026): Major redesign based on full year of data
```

Track:
- What changed
- Why it changed
- When it changed
- What the data showed

This creates an audit trail and helps you understand taxonomy evolution over time.

---

## FINAL NOTE

The goal isn't a perfect taxonomy that never changes. The goal is a *useful* taxonomy that:
1. Covers 90%+ of real issues
2. Enables effective prioritization
3. Routes issues to right teams
4. Surfaces strategic patterns

If your taxonomy is doing those things, it's good enough. Don't over-optimize.
