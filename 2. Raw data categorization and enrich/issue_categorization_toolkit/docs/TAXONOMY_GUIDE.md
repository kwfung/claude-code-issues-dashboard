# L1/L2 Taxonomy Guide

Complete reference for the GitHub Issue Classification Taxonomy

---

## L1 Categories (Primary)

### L1.1 - Core Functionality
**Description:** Issues affecting fundamental Claude Code operations

**L2 Subcategories:**
- **L2.1.1 - Context Management**: Context window usage, compaction, token limits
  - Keywords: context, compact, token, window
  - Examples: "Context compaction fails", "Token limit errors"

- **L2.1.2 - Session Management**: Session lifecycle, persistence, state
  - Keywords: session, conversation, history, resume
  - Examples: "Session won't resume", "Lost conversation history"

- **L2.1.3 - Agent Behavior**: Agentic loop, autonomous execution, task completion
  - Keywords: agent, loop, agentic, autonomous, task
  - Examples: "Agent gets stuck in loop", "Task doesn't complete"

- **L2.1.4 - Stability & Errors**: Crashes, hangs, freezes, unexpected exits
  - Keywords: crash, exit, hang, freeze, terminated
  - Examples: "Process exits with code 3", "CLI freezes"

- **L2.1.5 - Hooks & Lifecycle**: Hook execution, triggers, plugin lifecycle
  - Keywords: hook, sessionstart, precompact, userpromptsubmit, trigger, lifecycle
  - Examples: "Hooks don't fire", "PreCompact hook fails"

---

### L1.2 - API & Integration
**Description:** Issues with external API connections and integrations

**L2 Subcategories:**
- **L2.2.1 - Network & Proxy**: Proxy configuration, egress, DNS, connectivity
- **L2.2.2 - Authentication & Authorization**: API keys, auth errors, permissions
- **L2.2.3 - Rate Limits & Quotas**: Rate limiting, quota management, 429 errors
- **L2.2.4 - Cloud Provider APIs**: AWS Bedrock, GCP Vertex integrations

---

### L1.3 - Terminal UI (TUI)
**Description:** Issues with the command-line interface and user interaction

**L2 Subcategories:**
- **L2.3.1 - Rendering & Display**: Visual layout, rendering bugs, display issues
- **L2.3.2 - Commands & Controls**: Slash commands, keyboard shortcuts
- **L2.3.3 - Input Handling**: Keyboard input, paste, copy, autocomplete
- **L2.3.4 - Feedback & Status**: Status indicators, notifications, progress

---

### L1.4 - Tools & Execution
**Description:** Issues with tool invocation and command execution

**L2 Subcategories:**
- **L2.4.1 - File Operations**: File read/write, edit operations
- **L2.4.2 - Bash Execution**: Shell command execution, bash tool issues
- **L2.4.3 - Git Operations**: Git commands, repository access
- **L2.4.4 - Permissions & Sandbox**: Security sandbox, allowlists, denylists

---

### L1.5 - MCP Integration
**Description:** Issues with Model Context Protocol and plugin system

**L2 Subcategories:**
- **L2.5.1 - Plugin Management**: Plugin install, update, lifecycle
- **L2.5.2 - MCP Server Communication**: MCP server connections, tool discovery
- **L2.5.3 - Tool Invocation**: Using MCP tools, tool results

---

### L1.6 - IDE Integration
**Description:** Issues with IDE extensions and integrations

**L2 Subcategories:**
- **L2.6.1 - VS Code Extension**: VS Code specific issues
- **L2.6.2 - Cursor Integration**: Cursor editor specific issues
- **L2.6.3 - General IDE Issues**: Cross-IDE issues, startup, connection

---

### L1.7 - Model & Reasoning
**Description:** Issues with Claude's model behavior and outputs

**L2 Subcategories:**
- **L2.7.1 - Code Quality**: Incorrect code, logic errors
- **L2.7.2 - Model Selection**: Model switching, model availability
- **L2.7.3 - Reasoning & Understanding**: Misunderstanding instructions

---

### L1.8 - Platform-Specific
**Description:** Issues that only occur on specific operating systems

**L2 Subcategories:**
- **L2.8.1 - macOS**: macOS-only issues
- **L2.8.2 - Windows**: Windows-only issues
- **L2.8.3 - Linux**: Linux-only issues

---

### L1.9 - Performance & Resources
**Description:** Issues affecting speed, memory, or resource usage

**L2 Subcategories:**
- **L2.9.1 - Memory Management**: Memory leaks, high memory usage, OOM
- **L2.9.2 - Response Time**: Latency, slow responses, timeouts
- **L2.9.3 - Resource Usage**: CPU, disk I/O, network usage

---

### L1.10 - Security
**Description:** Security vulnerabilities and concerns

**L2 Subcategories:**
- **L2.10.1 - Sandbox Bypass**: Security model violations, sandbox escapes
- **L2.10.2 - Credential Management**: API keys, secrets, token handling
- **L2.10.3 - Data Privacy**: PII handling, data exposure

---

## Edge Case Decision Rules

### When to use "Other"

Use `L1_Tag: Other` when:
- Issue doesn't fit any L1 category cleanly
- Issue spans 3+ L1 categories equally
- Keyword match score < 2

Use `L2_Tag: Other` when:
- L1 is clear but no L2 subcategory fits
- Keyword match score < 2 for all L2s
- Issue is too general for specific L2

### Multi-Category Issues

When an issue spans multiple L1s, choose PRIMARY by asking:
1. What's most broken?
2. What team would fix this?
3. What's the root cause?

Example:
- "API connection fails causing session crash"
- Could be L1.2 (API) or L1.1 (Core/Session)
- Choose L1.2 because root cause is API connection
- Note alternative in Tagging_Notes

### Platform-Specific Issues

Always apply BOTH:
- Functional L1 tag (e.g., L1.1, L1.3)
- Platform label (e.g., platform:macos)

Don't use L1.8 unless issue is ONLY about platform differences with no functional category.

---

## Validation Checklist

Before finalizing taxonomy:
- [ ] All L2 codes start with corresponding L1 prefix (L1.1 → L2.1.x)
- [ ] No overlap between L2 subcategories within same L1
- [ ] Each L2 has 3-5 clear example keywords
- [ ] "Other" usage < 5% of total issues
- [ ] High confidence rate > 60%

---

## Update Log

- **v1.0** (Dec 2025): Initial taxonomy based on 1000 issue analysis
- Add updates here as taxonomy evolves

---
