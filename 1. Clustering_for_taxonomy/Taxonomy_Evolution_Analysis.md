# TAXONOMY EVOLUTION: FROM INTUITION TO DATA-DRIVEN

## What Changed and Why

### ORIGINAL APPROACH (Intuition-Based)
Based on ~24 issues observed and product intuition:
- 8 L1 categories
- Heavy emphasis on categories I *thought* would matter
- Included speculative subcategories with no validation

### DATA-DRIVEN APPROACH  
Based on analysis of 1,000 actual issues:
- 10 L1 categories (added 2 new ones based on data)
- Subcategories sized based on actual issue volume
- Every subcategory backed by real issue counts

---

## KEY DIFFERENCES

### 1. WHAT I GOT RIGHT (Validated by Data)

✅ **Core Functionality as #1 category**
- Intuition: Important
- Reality: 360 issues (36.0%) - largest category
- Context management alone: 229 issues

✅ **API & Integration separation**
- Intuition: Separate category needed
- Reality: 86 issues (8.6%) - confirmed as distinct concern
- Network/proxy issues surprisingly common (29 issues)

✅ **Tools & Execution as major category**
- Intuition: Important for developer tool
- Reality: 171 issues (17.1%) - 3rd largest
- File operations dominate (148 issues)

---

### 2. WHAT I MISSED COMPLETELY

❌ **Platform-Specific Issues**
- Intuition: Treated as metadata tag
- Reality: 634 issues (63.4%!) have platform tags
- macOS alone: 346 issues (34.6%)
- **Learning:** Platform issues aren't just edge cases - they're the majority

❌ **MCP Integration as separate L1**
- Intuition: Bundled under "Integrations"
- Reality: 61 distinct issues warrant own category
- Growing area with plugin marketplace

❌ **Performance as distinct L1**
- Intuition: Treated as subcategory of other issues
- Reality: 85 dedicated performance issues
- Memory issues: 67 issues (plus 23 labeled perf:memory)

---

### 3. WHAT I OVER-ESTIMATED

⚠️ **"Feature Requests" as separate L1**
- Intuition: Major category
- Reality: These span across all functional areas
- Better as cross-cutting type tag, not L1

⚠️ **Security as massive category**
- Intuition: Separate major category
- Reality: Only 47 issues (4.7%)
- Still important but smaller than expected

⚠️ **Model Behavior issues**
- Intuition: Would be major pain point
- Reality: Only 50 issues (5.0%)
- Quality seems good overall

---

### 4. WHAT I UNDER-ESTIMATED

📈 **TUI/Terminal Issues**
- Intuition: Minor category
- Reality: 207 issues (20.7%) - 2nd largest!
- Terminal UI is critical to user experience
- Rendering alone: 131 issues

📈 **IDE Integration complexity**
- Intuition: Small subcategory
- Reality: 84 dedicated issues (8.4%)
- VS Code alone: 37 issues
- Warrants own L1 category

📈 **Context Management dominance**
- Intuition: One of many subcategories
- Reality: 588 issues mention context (58.8%!)
- 229 core issues specifically about context
- Single biggest pain point

---

## SUBCATEGORY SIZING INSIGHTS

### What the Data Revealed

**Within Core Functionality:**
```
Context Management:    229 issues  ← Way bigger than expected
Session Management:    186 issues  ← Validated
Stability/Crashes:     122 issues  ← Bigger than expected  
Agent Behavior:         88 issues  ← Smaller than expected
Hooks/Lifecycle:        82 issues  ← New category from data
```

**Within Tools & Execution:**
```
File Operations:       148 issues  ← Dominant
Bash Execution:        119 issues  ← Close second
Git Operations:        110 issues  ← Surprisingly high
Permissions/Sandbox:    56 issues  ← Important for security
```

**Within Terminal UI:**
```
Rendering/Display:     131 issues  ← Majority of TUI issues
Commands:               83 issues  ← Command UX matters
Input Handling:         79 issues  ← Input is hard
Feedback/Status:        43 issues  ← Users want clarity
```

---

## WHAT THIS TEACHES US

### 1. Data Reveals User Reality
- Users struggle most with: **context limits, terminal UX, file operations**
- Not with: **model quality, security, advanced features**
- This should inform roadmap priorities

### 2. Platform Fragmentation is Real
- 63.4% of issues are platform-specific
- Can't treat macOS/Windows/Linux as "same codebase"
- Need platform-specific testing and fixes

### 3. Developer Experience > Model Capabilities
- 207 TUI issues vs. 50 model issues
- Users care more about tool UX than AI quality
- The terminal is the product, not just a wrapper

### 4. Scale Matters
- What seems like 5 similar issues might be 229 variations
- Need data to know where the real pain is
- Intuition underweights boring problems (like context management)

---

## TAXONOMY EVOLUTION SUMMARY

| Category | Original | Data-Driven | Change |
|----------|----------|-------------|---------|
| Core Functionality | ✓ | ✓ (360 issues) | Validated, expanded |
| API & Integration | ✓ | ✓ (86 issues) | Validated |
| Terminal UI | ✓ (small) | ✓ (207 issues) | **Upgraded to major** |
| Tools & Execution | ✓ | ✓ (171 issues) | Validated |
| Platform-Specific | ✗ (tag only) | ✓ (634 issues) | **New L1 category** |
| MCP Integration | ✗ | ✓ (61 issues) | **New L1 category** |
| IDE Integration | ✗ | ✓ (84 issues) | **New L1 category** |
| Model Behavior | ✓ (overestimated) | ✓ (50 issues) | Validated, right-sized |
| Performance | ✗ (subcategory) | ✓ (85 issues) | **Promoted to L1** |
| Security | ✓ (overestimated) | ✓ (47 issues) | Validated, right-sized |
| Feature Requests | ✓ (L1) | ✗ (cross-cutting) | **Demoted to tag** |

---

## THE MORAL OF THE STORY

### Before Data Analysis:
"I've seen 24 issues and worked on similar products. I know what matters."

### After Data Analysis:
"Oh. Users actually care most about context limits and terminal rendering. And platform issues are 63% of the backlog. My intuition missed the biggest pain points."

### The Lesson:
**Always start with data. Intuition is useful for hypothesis generation, but validation requires real user feedback at scale.**

---

## RECOMMENDATIONS FOR PRODUCT OPS

1. **Never skip the data collection step**
   - Even 100 issues > 0 issues
   - Patterns emerge at scale that aren't visible in samples

2. **Let frequency inform priority**
   - 229 context issues deserve more attention than 50 model issues
   - Even if model issues feel more exciting

3. **Watch for missing categories**
   - If 63% of issues share a trait (platform), that's a category
   - Data tells you what you didn't think to look for

4. **Validate everything**
   - Run the analysis, show the numbers
   - Don't trust intuition alone

5. **Keep iterating**
   - This taxonomy should evolve as the product matures
   - Re-analyze quarterly to catch shifts
