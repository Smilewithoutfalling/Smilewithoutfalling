<h1 align="center">AI Application Engineering · LLM Agents · Retrieval</h1>

<p align="center"><strong>Agent loops, tool calling, and retrieval pipelines — built to be measured, not just demoed</strong></p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=21&pause=1000&color=58A6FF&center=true&vCenter=true&random=false&width=760&lines=Agent+Loop+%2F+Tool+Calling+%2F+MCP;LangGraph+%2F+StateGraph+%2F+ReAct;RAG+%2F+Hybrid+Retrieval+%2F+Rerank;Evaluation+Harness+%2F+Reproducible+Scores" alt="Agent loop, tool calling, MCP, LangGraph and ReAct, RAG hybrid retrieval, evaluation harness" />
</p>

<p align="center">
  I build LLM applications that have to hold up — agents that run their own code and recover
  from their own errors, retrieval that says where an answer came from, and evaluation that
  turns "looks right" into a number.
</p>

<!-- PROFILE_BADGES:START -->
<p align="center">
  <a href="https://github.com/search?q=is%3Apr+author%3ASmilewithoutfalling+-user%3ASmilewithoutfalling+is%3Amerged&type=pullrequests"><img src="https://img.shields.io/badge/Merged_PRs-33-2ea44f?style=for-the-badge&logo=github&logoColor=white" alt="Merged pull requests" /></a>
  <a href="https://github.com/search?q=is%3Apr+author%3ASmilewithoutfalling+-user%3ASmilewithoutfalling&type=pullrequests"><img src="https://img.shields.io/badge/External_PRs-35-0366d6?style=for-the-badge&logo=github&logoColor=white" alt="External pull requests" /></a>
  <a href="https://github.com/Smilewithoutfalling?tab=followers"><img src="https://img.shields.io/github/followers/Smilewithoutfalling?label=Followers&style=for-the-badge&logo=github&color=181717" alt="GitHub followers" /></a>
  <a href="https://github.com/Smilewithoutfalling"><img src="https://komarev.com/ghpvc/?username=Smilewithoutfalling&label=Profile%20Views&color=0e75b6&style=for-the-badge" alt="Profile views" /></a>
</p>
<!-- PROFILE_BADGES:END -->

## What I Build

- 🤖 **Terminal AI Coding Agents** — [MedCode](https://github.com/Smilewithoutfalling/MedCode): a local `model → tool → model` loop with MCP servers mounted at runtime, skills that load only when a task actually hits them, diff review before any write, and path/command permission checks fencing the workspace
- 📊 **Data Analysis Agents** — [DataChat](https://github.com/Smilewithoutfalling/datachat): question → plan → generated pandas → sandboxed run → read the traceback, fix, rerun. One kernel, two control flows — a fixed state graph when you need to debug it, ReAct when the model should decide
- 🔍 **Retrieval That Cites** — hybrid BM25 + vector search fused by weighted RRF, HyDE query expansion, cross-encoder rerank; every answer carries the chunk it came from, marked at the source
- 🧪 **Evaluation Before Opinion** — deterministic scorers replayed over JSONL sessions (tool-sequence alignment, veto on failure, token budget), plus retrieval metrics from recall@k to nDCG@k with Top-K and rerank ablations
- ⚡ **Runtime Correctness** — streaming, cancellation, timeouts, context compaction and session persistence, because an agent that works for three turns and dies on the thirtieth is not working

<!-- OPEN_SOURCE_CONTRIBUTIONS:START -->
## Open Source Contributions

> Automatically updated daily · 33 merged · 2 in review · 6 repositories

### Merged Pull Requests

| Project | Contribution | PR |
|---|---|---|
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Made `remove` fail loudly instead of silently succeeding when nothing matched | [#1741](https://github.com/Tencent/teamai-cli/pull/1741) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Surfaced a skipped skill in `--update-quality` and matched learnings by topic | [#1739](https://github.com/Tencent/teamai-cli/pull/1739) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | Documented the pandas row-index assumption behind XLSX row numbering | [#13566](https://github.com/deepset-ai/haystack/pull/13566) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Documented the non-zero exit returned for an unreadable manifest | [#1734](https://github.com/Tencent/teamai-cli/pull/1734) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Returned a non-zero exit when a roles or projects edit is refused, not success | [#1731](https://github.com/Tencent/teamai-cli/pull/1731) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | Clarified what `word_count_threshold` actually counts | [#13549](https://github.com/deepset-ai/haystack/pull/13549) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Made a failed self-update exit non-zero instead of reporting success | [#1703](https://github.com/Tencent/teamai-cli/pull/1703) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Persisted self-update failures to `debug.log` so they survive the terminal | [#1702](https://github.com/Tencent/teamai-cli/pull/1702) |
| [langbot-app/LangBot](https://github.com/langbot-app/LangBot) | Throttled intermediate stream frames in WebSocket mode | [#2564](https://github.com/langbot-app/LangBot/pull/2564) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Recognised an origin-less `--dir` checkout by hashing its git root | [#1427](https://github.com/Tencent/teamai-cli/pull/1427) |

<details>
<summary>23 earlier merged pull requests</summary>

| Project | Contribution | PR |
|---|---|---|
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Timed out a stalled `gh` org request instead of retrying it forever | [#1403](https://github.com/Tencent/teamai-cli/pull/1403) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Retried the session-pull temp cleanup that races `git gc` | [#1408](https://github.com/Tencent/teamai-cli/pull/1408) |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | Retargeted the label docs at `triage.yml` and guarded applied labels | [#7328](https://github.com/bytedance/deer-flow/pull/7328) |
| [deepset-ai/haystack](https://github.com/deepset-ai/haystack) | Validated `inputs_from_state` when a tool takes no inputs | [#13279](https://github.com/deepset-ai/haystack/pull/13279) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Reported an async command error as one line instead of a stack trace | [#1271](https://github.com/Tencent/teamai-cli/pull/1271) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Honoured both tool roots that Cursor CLI actually records | [#1165](https://github.com/Tencent/teamai-cli/pull/1165) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Added a config switch for the SessionStart merge-request hint | [#1117](https://github.com/Tencent/teamai-cli/pull/1117) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Made `doctor` prove the SessionStart hook answers, not just that it exists | [#1064](https://github.com/Tencent/teamai-cli/pull/1064) |
| [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT) | Added an unread-only filter to the curated timeline | [#188](https://github.com/KKKKhazix/AIHOT/pull/188) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Pointed both guides at the renamed SessionStart check | [#1048](https://github.com/Tencent/teamai-cli/pull/1048) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Delivered the ZCode SessionStart hook through a Node launcher | [#1047](https://github.com/Tencent/teamai-cli/pull/1047) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Accepted tool roots nested below `~/.config/<name>` | [#1017](https://github.com/Tencent/teamai-cli/pull/1017) |
| [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT) | Removed a `modelStops` field from the alert config that nothing read | [#186](https://github.com/KKKKhazix/AIHOT/pull/186) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Kept the token out of the clone's remote URL | [#994](https://github.com/Tencent/teamai-cli/pull/994) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Vetoed a Swift bare call only inside a type body | [#966](https://github.com/Tencent/teamai-cli/pull/966) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Stopped `.gitignore` self-healing under `--dry-run` | [#944](https://github.com/Tencent/teamai-cli/pull/944) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Pinned the binding fix with a test that fails without it | [#943](https://github.com/Tencent/teamai-cli/pull/943) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Collected Swift shadowing from binding positions | [#928](https://github.com/Tencent/teamai-cli/pull/928) |
| [KKKKhazix/AIHOT](https://github.com/KKKKhazix/AIHOT) | Made the Markdown export filename follow the site's own identity | [#16](https://github.com/KKKKhazix/AIHOT/pull/16) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Resolved Swift symbols across files in the same module | [#847](https://github.com/Tencent/teamai-cli/pull/847) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Threaded `dryRun` into the queue lock so a preview stops creating work | [#896](https://github.com/Tencent/teamai-cli/pull/896) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Threaded `dryRun` through the loaders pull, push and status paths | [#866](https://github.com/Tencent/teamai-cli/pull/866) |
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Added Swift support to the AST and heuristic code-knowledge tracks | [#842](https://github.com/Tencent/teamai-cli/pull/842) |

</details>

### Pull Requests In Review

| Project | Contribution | PR |
|---|---|---|
| [Tencent/teamai-cli](https://github.com/Tencent/teamai-cli) | Delivered the user's files to the root the app actually launches from | [#1745](https://github.com/Tencent/teamai-cli/pull/1745) |
| [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope) | Ignored duplicate index tasks for documents that are already ready | [#3658](https://github.com/agentscope-ai/agentscope/pull/3658) |
<!-- OPEN_SOURCE_CONTRIBUTIONS:END -->

## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <br />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain" />
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge" alt="LangGraph" />
  <img src="https://img.shields.io/badge/MCP-000000?style=for-the-badge" alt="Model Context Protocol" />
  <img src="https://img.shields.io/badge/Tool_Calling-4B5563?style=for-the-badge" alt="Tool calling" />
  <br />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL" />
  <img src="https://img.shields.io/badge/ChromaDB-FF6B35?style=for-the-badge" alt="ChromaDB" />
  <br />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/OpenSlide-1F6FEB?style=for-the-badge" alt="OpenSlide" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />
</p>

## Contribution Dashboard

<p align="center">
  <img width="96%" src="./assets/open-source-stats.svg" alt="Open source contribution summary" />
</p>
