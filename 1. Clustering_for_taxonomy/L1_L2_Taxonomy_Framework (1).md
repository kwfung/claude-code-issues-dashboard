# DATA-DRIVEN L1/L2 TAXONOMY FOR CLAUDE CODE GITHUB ISSUES
# Based on analysis of 1,000 actual open issues

## METHODOLOGY
This taxonomy was developed through:
1. Quantitative analysis of 1,000 open issues
2. Label frequency distribution analysis
3. Keyword extraction and clustering
4. Pattern matching on issue content
5. Validation against existing GitHub labels

## KEY FINDINGS FROM DATA

### Volume Distribution
- Total issues analyzed: 1,000
- Bug reports: 633 (63.3%)
- Feature requests: 262 (26.2%)
- Issues with reproduction steps: 590 (59.0%)

### Top Pain Points (by frequency)
1. Core functionality: 360 issues (36.0%)
2. Terminal UI: 207 issues (20.7%)
3. Tools/Execution: 171 issues (17.1%)
4. macOS-specific: 346 issues (34.6%)
5. Windows-specific: 159 issues (15.9%)
6. Context management: 588 mentions (58.8%)

### Existing Label Structure
GitHub already uses structured labels:
- area:* (component-based)
- platform:* (OS-specific)
- api:* (API provider-specific)
- perf:* (performance-related)

## PROPOSED L1/L2 TAXONOMY

### L1: PRIMARY FUNCTIONAL AREA (Mutually Exclusive)

These answer: "Which component/system is affected?"

---

#### **L1.1 CORE FUNCTIONALITY** (360 issues, 36.0%)
Issues affecting fundamental Claude Code operations

**L2 Subcategories:**
- **L2.1.1 Context Management** (229 issues)
  - Context window usage, compaction, token limits
  - Examples: "Context compaction fails", "Token limit errors", "Context overflow"
  
- **L2.1.2 Session Management** (186 issues)
  - Session lifecycle, persistence, state
  - Examples: "Session won't resume", "Lost conversation history", "Session crashes"
  
- **L2.1.3 Agent Behavior** (88 issues)
  - Agentic loop, autonomous execution, task completion
  - Examples: "Agent gets stuck in loop", "Agent doesn't complete task", "Hallucinated steps"
  
- **L2.1.4 Stability & Errors** (122 issues)
  - Crashes, hangs, freezes, unexpected exits
  - Examples: "Process exits with code 3", "CLI freezes", "Unexpected termination"
  
- **L2.1.5 Hooks & Lifecycle** (82 issues)
  - Hook execution, triggers, plugin lifecycle
  - Examples: "Hooks don't fire", "PreCompact hook fails", "Plugin update issues"

---

#### **L1.2 API & INTEGRATION** (86 issues, 8.6%)
Issues with external API connections and integrations

**L2 Subcategories:**
- **L2.2.1 Network & Proxy** (29 issues)
  - Proxy configuration, egress, DNS, connectivity
  - Examples: "Proxy not working", "Cannot connect through firewall", "DNS resolution fails"
  
- **L2.2.2 Authentication & Authorization** (13 issues)
  - API keys, auth errors, permission issues
  - Examples: "401 Unauthorized", "API key invalid", "Auth token expired"
  
- **L2.2.3 Rate Limits & Quotas** (9 issues)
  - Rate limiting, quota management, 429 errors
  - Examples: "Rate limit reached", "Quota exceeded", "429 Too Many Requests"
  
- **L2.2.4 Cloud Provider APIs** (15 issues)
  - AWS Bedrock (12 issues), GCP Vertex (7 issues)
  - Examples: "Bedrock integration fails", "Vertex API error", "Cross-region issues"

---

#### **L1.3 TERMINAL UI (TUI)** (207 issues, 20.7%)
Issues with the command-line interface and user interaction

**L2 Subcategories:**
- **L2.3.1 Rendering & Display** (131 issues)
  - Visual layout, rendering bugs, display issues
  - Examples: "Text overlaps", "Colors wrong", "Progress bar doesn't update"
  
- **L2.3.2 Commands & Controls** (83 issues)
  - Slash commands, keyboard shortcuts, command execution
  - Examples: "/compact doesn't work", "Shortcut conflicts", "Command not recognized"
  
- **L2.3.3 Input Handling** (79 issues)
  - Keyboard input, paste, copy, autocomplete
  - Examples: "Paste doesn't work", "Autocomplete slow", "Input lag"
  
- **L2.3.4 Feedback & Status** (43 issues)
  - Status indicators, notifications, progress feedback
  - Examples: "No progress indicator", "Status line incorrect", "Missing feedback"

---

#### **L1.4 TOOLS & EXECUTION** (171 issues, 17.1%)
Issues with tool invocation and command execution

**L2 Subcategories:**
- **L2.4.1 File Operations** (148 issues)
  - File read/write, edit operations, file system access
  - Examples: "Edit tool fails", "File not saved", "Cannot read file"
  
- **L2.4.2 Bash Execution** (119 issues)
  - Shell command execution, bash tool issues
  - Examples: "Command hangs", "Bash timeout", "Shell error"
  
- **L2.4.3 Git Operations** (110 issues)
  - Git commands, repository access
  - Examples: "Git clone fails", "Cannot push", "Git auth error"
  
- **L2.4.4 Permissions & Sandbox** (56 issues)
  - Security sandbox, allowlists, denylists, permissions
  - Examples: "Sandbox bypass", "Command blocked incorrectly", "Allowlist not working"

---

#### **L1.5 MCP INTEGRATION** (61 issues, 6.1%)
Issues with Model Context Protocol and plugin system

**L2 Subcategories:**
- **L2.5.1 Plugin Management** (focused subcategory)
  - Plugin install, update, lifecycle
  - Examples: "Plugin won't install", "Update fails", "Plugin conflicts"
  
- **L2.5.2 MCP Server Communication** (focused subcategory)
  - MCP server connections, tool discovery
  - Examples: "MCP server disconnects", "Tools not appearing", "OAuth issues"
  
- **L2.5.3 Tool Invocation** (focused subcategory)
  - Using MCP tools, tool results
  - Examples: "MCP tool fails", "Duplicate tool calls", "Tool result error"

---

#### **L1.6 IDE INTEGRATION** (84 issues, 8.4%)
Issues with IDE extensions and integrations

**L2 Subcategories:**
- **L2.6.1 VS Code Extension** (37 issues)
  - VS Code specific issues
  - Examples: "Extension crashes", "Panel won't open", "VS Code hangs"
  
- **L2.6.2 Cursor Integration** (12 issues)
  - Cursor editor specific issues
  - Examples: "Cursor connection fails", "Sync issues"
  
- **L2.6.3 General IDE Issues** (35 issues)
  - Cross-IDE issues, startup, connection
  - Examples: "IDE not connected", "Startup fails", "Settings not synced"

---

#### **L1.7 MODEL & REASONING** (50 issues, 5.0%)
Issues with Claude's model behavior and outputs

**L2 Subcategories:**
- **L2.7.1 Code Quality** (focused subcategory)
  - Incorrect code, logic errors, bugs in generated code
  - Examples: "Generated code has syntax error", "Logic bug", "Wrong implementation"
  
- **L2.7.2 Model Selection** (focused subcategory)
  - Model switching, model availability
  - Examples: "Can't switch to Opus", "Model defaults incorrectly", "Model not available"
  
- **L2.7.3 Reasoning & Understanding** (focused subcategory)
  - Misunderstanding instructions, hallucinations
  - Examples: "Claude doesn't understand task", "Fabricates files", "Ignores instructions"

---

#### **L1.8 PLATFORM-SPECIFIC** (634 issues, 63.4%)
Issues that only occur on specific operating systems

**L2 Subcategories:**
- **L2.8.1 macOS** (346 issues)
  - macOS-only issues
  
- **L2.8.2 Windows** (159 issues)
  - Windows-only issues
  
- **L2.8.3 Linux** (128 issues)
  - Linux-only issues

**Note:** Platform labels are cross-cutting and should be applied IN ADDITION to functional L1/L2 tags

---

#### **L1.9 PERFORMANCE & RESOURCES** (85 issues, 8.5%)
Issues affecting speed, memory, or resource usage

**L2 Subcategories:**
- **L2.9.1 Memory Management** (67 issues)
  - Memory leaks, high memory usage, OOM
  - Examples: "Memory leak", "High RAM usage", "Out of memory"
  
- **L2.9.2 Response Time** (focused subcategory)
  - Latency, slow responses, timeouts
  - Examples: "Slow autocomplete", "Command times out", "Long wait times"
  
- **L2.9.3 Resource Usage** (focused subcategory)
  - CPU, disk I/O, network usage
  - Examples: "High CPU usage", "Disk thrashing", "Network saturation"

---

#### **L1.10 SECURITY** (47 issues, 4.7%)
Security vulnerabilities and concerns

**L2 Subcategories:**
- **L2.10.1 Sandbox Bypass** (focused subcategory)
  - Security model violations, sandbox escapes
  - Examples: "Absolute paths bypass", "Command allowlist bypass"
  
- **L2.10.2 Credential Management** (focused subcategory)
  - API keys, secrets, token handling
  - Examples: "API key exposed", "Secret in logs", "Token leaked"
  
- **L2.10.3 Data Privacy** (focused subcategory)
  - PII handling, data exposure
  - Examples: "Sensitive data in context", "PII in error messages"

---

### CROSS-CUTTING TAGS (Applied in addition to L1/L2)

**Severity:**
- `sev:critical` - Security issue, data loss, complete blocker
- `sev:high` - Major functionality broken, no workaround
- `sev:medium` - Important but has workaround
- `sev:low` - Minor inconvenience

**Issue Type:**
- `type:bug` - Something broken (use existing "bug" label)
- `type:feature` - New capability request (use existing "enhancement" label)
- `type:docs` - Documentation issue
- `type:question` - User question

**Reproducibility:**
- `has-repro` - Detailed reproduction steps provided (already exists as "has repro")
- `needs-repro` - Cannot reproduce, needs more info

**User Impact:**
- `impact:high` - Affects >50% of users
- `impact:medium` - Affects 10-50% of users
- `impact:low` - Affects <10% of users

**Work Effort:**
- `effort:small` - <1 day fix
- `effort:medium` - 1-3 days
- `effort:large` - >3 days or requires design work

---

## MAPPING TO EXISTING LABELS

Our L1 categories map cleanly to existing GitHub labels:

| L1 Category | Existing GitHub Label |
|-------------|----------------------|
| Core Functionality | area:core |
| API & Integration | area:api |
| Terminal UI | area:tui |
| Tools & Execution | area:tools |
| MCP Integration | area:mcp |
| IDE Integration | area:ide |
| Model & Reasoning | area:model |
| Platform-Specific | platform:macos, platform:windows, platform:linux |
| Performance | perf:memory (expand to perf:cpu, perf:latency) |
| Security | area:security |

**Recommendation:** Keep existing label structure, add L2 subcategory labels as needed.

---

## EDGE CASES & DECISION RULES

**Q: Issue spans multiple L1 categories?**
A: Choose the PRIMARY affected component. Add secondary tag if needed.
Example: "API connection fails causing session crash" → L1.2 (API & Integration) + tag:affects-sessions

**Q: Feature request vs. bug?**
A: If it worked and broke = bug. If it never worked = feature.

**Q: Platform-specific issue in a component?**
A: Apply BOTH L1 functional tag AND platform tag.
Example: "Context compaction fails on Windows" → L1.1 (Core) + L2.1.1 (Context Management) + platform:windows

---

## VALIDATION METRICS

To validate this taxonomy is working:
1. **Coverage:** >95% of issues should fit cleanly into L1/L2
2. **Inter-rater reliability:** Two people should tag same issue identically >85% of time
3. **Usefulness:** PM should be able to filter/sort issues effectively for planning

---

## NEXT STEPS

1. Validate taxonomy on holdout sample (100 issues)
2. Train team on tagging guidelines
3. Bulk re-tag existing issues
4. Monitor for edge cases and refine
5. Integrate into triage automation
