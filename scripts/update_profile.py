#!/usr/bin/env python3
"""Update the open-source contribution tables and stats card in the profile README.

Regenerates two things between the markers / in assets:

  * the `<!-- OPEN_SOURCE_CONTRIBUTIONS:START -->` … `:END -->` block in README.md
  * assets/open-source-stats.svg

Only external pull requests count (everything outside the profile owner's own
repositories), which is what makes the number mean something: it is work landed
in codebases the owner does not control.

Usage:
    python scripts/update_profile.py            # write files in place
    python scripts/update_profile.py --dry-run  # print, do not write
    python scripts/update_profile.py --check    # exit 1 if files are stale

Env:
    GITHUB_TOKEN       optional, raises rate limit and is required in Actions
    PROFILE_USERNAME   default Smilewithoutfalling
    README_PATH        default README.md
    STATS_PATH         default assets/open-source-stats.svg
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USERNAME = os.environ.get("PROFILE_USERNAME", "Smilewithoutfalling")
TOKEN = os.environ.get("GITHUB_TOKEN")
README_PATH = Path(os.environ.get("README_PATH", "README.md"))
STATS_PATH = Path(os.environ.get("STATS_PATH", "assets/open-source-stats.svg"))

START_MARKER = "<!-- OPEN_SOURCE_CONTRIBUTIONS:START -->"
END_MARKER = "<!-- OPEN_SOURCE_CONTRIBUTIONS:END -->"
BADGES_START = "<!-- PROFILE_BADGES:START -->"
BADGES_END = "<!-- PROFILE_BADGES:END -->"

# How many merged PRs stay in the visible table. The rest fold into <details>.
# 33 merged PRs in a flat table reads as a log file, not as a portfolio.
MAIN_TABLE_LIMIT = 10

# Human-readable one-liners, keyed by PR URL. Anything missing falls back to the
# PR title, so a new contribution shows up immediately and gets a better
# sentence the next time someone edits this dict.
DESCRIPTIONS = {
    # --- Tencent/teamai-cli
    "https://github.com/Tencent/teamai-cli/pull/1741": (
        "Made `remove` fail loudly instead of silently succeeding when nothing matched"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1739": (
        "Surfaced a skipped skill in `--update-quality` and matched learnings by topic"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1734": (
        "Documented the non-zero exit returned for an unreadable manifest"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1731": (
        "Returned a non-zero exit when a roles or projects edit is refused, not success"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1745": (
        "Delivered the user's files to the root the app actually launches from"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1703": (
        "Made a failed self-update exit non-zero instead of reporting success"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1702": (
        "Persisted self-update failures to `debug.log` so they survive the terminal"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1427": (
        "Recognised an origin-less `--dir` checkout by hashing its git root"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1408": (
        "Retried the session-pull temp cleanup that races `git gc`"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1403": (
        "Timed out a stalled `gh` org request instead of retrying it forever"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1271": (
        "Reported an async command error as one line instead of a stack trace"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1165": (
        "Honoured both tool roots that Cursor CLI actually records"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1117": (
        "Added a config switch for the SessionStart merge-request hint"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1064": (
        "Made `doctor` prove the SessionStart hook answers, not just that it exists"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1047": (
        "Delivered the ZCode SessionStart hook through a Node launcher"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1017": (
        "Accepted tool roots nested below `~/.config/<name>`"
    ),
    "https://github.com/Tencent/teamai-cli/pull/994": (
        "Kept the token out of the clone's remote URL"
    ),
    "https://github.com/Tencent/teamai-cli/pull/966": (
        "Vetoed a Swift bare call only inside a type body"
    ),
    "https://github.com/Tencent/teamai-cli/pull/944": (
        "Stopped `.gitignore` self-healing under `--dry-run`"
    ),
    "https://github.com/Tencent/teamai-cli/pull/928": (
        "Collected Swift shadowing from binding positions"
    ),
    "https://github.com/Tencent/teamai-cli/pull/896": (
        "Threaded `dryRun` into the queue lock so a preview stops creating work"
    ),
    "https://github.com/Tencent/teamai-cli/pull/866": (
        "Threaded `dryRun` through the loaders pull, push and status paths"
    ),
    "https://github.com/Tencent/teamai-cli/pull/847": (
        "Resolved Swift symbols across files in the same module"
    ),
    "https://github.com/Tencent/teamai-cli/pull/842": (
        "Added Swift support to the AST and heuristic code-knowledge tracks"
    ),
    "https://github.com/Tencent/teamai-cli/pull/943": (
        "Pinned the binding fix with a test that fails without it"
    ),
    "https://github.com/Tencent/teamai-cli/pull/1048": (
        "Pointed both guides at the renamed SessionStart check"
    ),
    # --- deepset-ai/haystack
    "https://github.com/deepset-ai/haystack/pull/13566": (
        "Documented the pandas row-index assumption behind XLSX row numbering"
    ),
    "https://github.com/deepset-ai/haystack/pull/13549": (
        "Clarified what `word_count_threshold` actually counts"
    ),
    "https://github.com/deepset-ai/haystack/pull/13279": (
        "Validated `inputs_from_state` when a tool takes no inputs"
    ),
    "https://github.com/deepset-ai/haystack/pull/13578": (
        "Sorted numeric metadata numerically in `get_metadata_field_unique_values`"
    ),
    # --- other
    "https://github.com/langbot-app/LangBot/pull/2564": (
        "Throttled intermediate stream frames in WebSocket mode"
    ),
    "https://github.com/bytedance/deer-flow/pull/7328": (
        "Retargeted the label docs at `triage.yml` and guarded applied labels"
    ),
    "https://github.com/KKKKhazix/AIHOT/pull/16": (
        "Made the Markdown export filename follow the site's own identity"
    ),
    "https://github.com/KKKKhazix/AIHOT/pull/186": (
        "Removed a `modelStops` field from the alert config that nothing read"
    ),
    "https://github.com/KKKKhazix/AIHOT/pull/188": (
        "Added an unread-only filter to the curated timeline"
    ),
    "https://github.com/agentscope-ai/agentscope/pull/3658": (
        "Ignored duplicate index tasks for documents that are already ready"
    ),
}


@dataclass(frozen=True)
class PullRequest:
    repository: str
    number: int
    title: str
    url: str
    state: str
    merged_at: str | None
    updated_at: str

    @property
    def is_merged(self) -> bool:
        return self.merged_at is not None

    @property
    def is_open(self) -> bool:
        return self.state == "open"

    @property
    def description(self) -> str:
        return DESCRIPTIONS.get(self.url, self.title)

    @property
    def sort_key(self) -> str:
        return self.merged_at or self.updated_at


def github_request(url: str, attempts: int = 4) -> dict[str, object]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-readme",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    # A daily cron has exactly one shot; a 504 from the search API should not
    # paint the workflow red and leave the profile stale for 24 hours.
    transient = {429, 500, 502, 503, 504}
    last: Exception | None = None
    for attempt in range(attempts):
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            last = RuntimeError(f"GitHub API returned HTTP {exc.code}: {detail}")
            if exc.code not in transient or attempt == attempts - 1:
                raise last from exc
        except URLError as exc:
            last = RuntimeError(f"GitHub API request failed: {exc.reason}")
            if attempt == attempts - 1:
                raise last from exc
        time.sleep(2**attempt)

    raise last if last else RuntimeError("GitHub API request failed without an error")


def fetch_pull_requests() -> list[PullRequest]:
    # `-user:` is what makes this "external": it drops PRs opened against the
    # owner's own repositories, which would be self-reporting.
    query = f"is:pr author:{USERNAME} is:public -user:{USERNAME}"
    found: list[PullRequest] = []

    for page in range(1, 11):
        params = urlencode(
            {
                "q": query,
                "sort": "updated",
                "order": "desc",
                "per_page": 100,
                "page": page,
            }
        )
        payload = github_request(f"https://api.github.com/search/issues?{params}")
        items = payload.get("items", [])
        if not isinstance(items, list):
            raise RuntimeError("GitHub search response did not contain an items list")

        for item in items:
            if not isinstance(item, dict):
                continue
            pull_request = item.get("pull_request")
            if not isinstance(pull_request, dict):
                continue

            merged_at = pull_request.get("merged_at")
            merged_at = str(merged_at) if merged_at else None
            state = str(item.get("state", ""))

            # Closed without merging is not a contribution; counting it would
            # inflate the number and nobody would trust the rest of the page.
            if state != "open" and merged_at is None:
                continue

            repository = str(item.get("repository_url", "")).split("/repos/", 1)[-1]
            if not repository:
                continue

            found.append(
                PullRequest(
                    repository=repository,
                    number=int(item["number"]),
                    title=str(item.get("title", "")).strip(),
                    url=str(item.get("html_url", "")).strip(),
                    state=state,
                    merged_at=merged_at,
                    updated_at=str(item.get("updated_at", "")),
                )
            )

        if len(items) < 100:
            break

    return found


def split_pull_requests(
    pull_requests: list[PullRequest],
) -> tuple[list[PullRequest], list[PullRequest]]:
    merged = sorted(
        (pr for pr in pull_requests if pr.is_merged),
        key=lambda pr: pr.sort_key,
        reverse=True,
    )
    in_review = sorted(
        (pr for pr in pull_requests if pr.is_open),
        key=lambda pr: pr.updated_at,
        reverse=True,
    )
    return merged, in_review


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def pull_request_table(pull_requests: list[PullRequest]) -> list[str]:
    lines = [
        "| Project | Contribution | PR |",
        "|---|---|---|",
    ]
    for pull_request in pull_requests:
        project = f"[{pull_request.repository}](https://github.com/{pull_request.repository})"
        contribution = escape_cell(pull_request.description)
        link = f"[#{pull_request.number}]({pull_request.url})"
        lines.append(f"| {project} | {contribution} | {link} |")
    return lines


def render_section(pull_requests: list[PullRequest]) -> str:
    merged, in_review = split_pull_requests(pull_requests)
    repositories = {pr.repository for pr in pull_requests}

    head = merged[:MAIN_TABLE_LIMIT]
    rest = merged[MAIN_TABLE_LIMIT:]

    summary = (
        f"> Automatically updated daily · {len(merged)} merged · "
        f"{len(in_review)} in review · {len(repositories)} repositories"
    )

    lines = [
        START_MARKER,
        "## Open Source Contributions",
        "",
        summary,
        "",
        "### Merged Pull Requests",
        "",
    ]
    lines.extend(
        pull_request_table(head) if head else ["_No merged external pull requests yet._"]
    )

    if rest:
        lines.extend(
            [
                "",
                "<details>",
                f"<summary>{len(rest)} earlier merged pull requests</summary>",
                "",
                *pull_request_table(rest),
                "",
                "</details>",
            ]
        )

    lines.extend(["", "### Pull Requests In Review", ""])
    lines.extend(
        pull_request_table(in_review)
        if in_review
        else ["_No open external pull requests._"]
    )
    lines.append(END_MARKER)
    return "\n".join(lines)


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_stats_svg(pull_requests: list[PullRequest]) -> str:
    merged, in_review = split_pull_requests(pull_requests)

    by_repository: dict[str, list[PullRequest]] = {}
    for pull_request in pull_requests:
        by_repository.setdefault(pull_request.repository, []).append(pull_request)

    ranked = sorted(by_repository.items(), key=lambda item: (-len(item[1]), item[0].lower()))
    repositories = ranked[:6]
    hidden = len(ranked) - len(repositories)
    largest = max((len(items) for _, items in repositories), default=1)

    row_height = 52
    chart_x = 500
    # 400 leaves the row totals room on the right; at 430 the widest bar ran
    # straight into its own number.
    chart_width = 400
    scale = chart_width / largest
    # Rows start below the two KPI cards (which end at y=212). The upstream
    # layout started them at 190, so the first repository name was drawn on top
    # of the MERGED box — invisible on a short label, obvious on a long one.
    chart_y = 262  # vertical centre of the first row
    height = chart_y + max(len(repositories) - 1, 0) * row_height + 5 + 40

    font = "Segoe UI, Arial, sans-serif"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-label="Open source contribution summary">',
        "  <defs>",
        '    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '      <stop offset="0%" stop-color="#0d1117"/>',
        '      <stop offset="100%" stop-color="#161b22"/>',
        "    </linearGradient>",
        "  </defs>",
        f'  <rect width="1000" height="{height}" rx="24" fill="url(#bg)"/>',
        f'  <text x="48" y="62" fill="#f0f6fc" font-size="30" font-weight="700" font-family="{font}">Open Source Contributions</text>',
        f'  <text x="48" y="92" fill="#8b949e" font-size="16" font-family="{font}">Public pull requests outside my own repositories · {len(ranked)} repositories</text>',
        '  <rect x="48" y="124" width="190" height="88" rx="16" fill="#132a1b" stroke="#238636"/>',
        f'  <text x="68" y="158" fill="#8b949e" font-size="14" font-family="{font}">MERGED</text>',
        f'  <text x="68" y="198" fill="#3fb950" font-size="36" font-weight="700" font-family="{font}">{len(merged)}</text>',
        '  <rect x="258" y="124" width="190" height="88" rx="16" fill="#211936" stroke="#8957e5"/>',
        f'  <text x="278" y="158" fill="#8b949e" font-size="14" font-family="{font}">IN REVIEW</text>',
        f'  <text x="278" y="198" fill="#a371f7" font-size="36" font-weight="700" font-family="{font}">{len(in_review)}</text>',
        f'  <text x="500" y="148" fill="#f0f6fc" font-size="16" font-weight="600" font-family="{font}">Pull requests by repository</text>',
        '  <circle cx="818" cy="142" r="5" fill="#3fb950"/>',
        f'  <text x="830" y="147" fill="#8b949e" font-size="13" font-family="{font}">merged</text>',
        '  <circle cx="900" cy="142" r="5" fill="#a371f7"/>',
        f'  <text x="912" y="147" fill="#8b949e" font-size="13" font-family="{font}">open</text>',
    ]

    if not repositories:
        out.append(
            f'  <text x="500" y="205" fill="#8b949e" font-size="16" font-family="{font}">No external pull requests found.</text>'
        )
    else:
        for index, (repository, items) in enumerate(repositories):
            repo_merged = sum(1 for item in items if item.is_merged)
            repo_open = sum(1 for item in items if item.is_open)
            # min 6px so a single PR is still a visible mark rather than a speck
            merged_width = max(repo_merged * scale, 6) if repo_merged else 0
            open_width = max(repo_open * scale, 6) if repo_open else 0
            cy = chart_y + index * row_height  # bar centre, so label and bar line up
            baseline = cy + 5
            label = repository if len(repository) <= 34 else repository[:31] + "..."
            out.extend(
                [
                    f'  <text x="48" y="{baseline}" fill="#c9d1d9" font-size="14" font-family="{font}">{xml_escape(label)}</text>',
                    f'  <text x="952" y="{baseline}" text-anchor="end" fill="#8b949e" font-size="13" font-family="{font}">{len(items)}</text>',
                    f'  <rect x="{chart_x}" y="{cy - 5}" width="{chart_width}" height="10" rx="5" fill="#30363d"/>',
                    f'  <rect x="{chart_x}" y="{cy - 5}" width="{merged_width}" height="10" rx="5" fill="#3fb950"/>',
                    f'  <rect x="{chart_x + merged_width}" y="{cy - 5}" width="{open_width}" height="10" rx="5" fill="#a371f7"/>',
                ]
            )
        if hidden:
            out.append(
                f'  <text x="48" y="{chart_y + len(repositories) * row_height + 4}" fill="#6e7681" font-size="13" font-family="{font}">+{hidden} more repositories</text>'
            )

    out.append("</svg>")
    return "\n".join(out) + "\n"


def load_snapshot(path: Path) -> list[PullRequest]:
    """Rebuild the PR list from a saved search response.

    Lets you iterate on the layout without spending the unauthenticated search
    quota (10 requests/minute), and keeps --check usable when the API is down.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise RuntimeError(f"{path} does not look like a search response")

    out: list[PullRequest] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        pull_request = item.get("pull_request")
        if not isinstance(pull_request, dict):
            continue
        merged_at = pull_request.get("merged_at")
        merged_at = str(merged_at) if merged_at else None
        state = str(item.get("state", ""))
        if state != "open" and merged_at is None:
            continue
        repository = str(item.get("repository_url", "")).split("/repos/", 1)[-1]
        if not repository:
            continue
        out.append(
            PullRequest(
                repository=repository,
                number=int(item["number"]),
                title=str(item.get("title", "")).strip(),
                url=str(item.get("html_url", "")).strip(),
                state=state,
                merged_at=merged_at,
                updated_at=str(item.get("updated_at", "")),
            )
        )
    return out


def update_badges(readme: str, merged: int, total: int) -> str:
    """Keep the two counting badges honest.

    They live outside the contribution block so the header can lead with the
    number instead of "View on GitHub", which tells a visitor nothing.
    """
    if BADGES_START not in readme or BADGES_END not in readme:
        return readme

    pattern = re.compile(
        rf"{re.escape(BADGES_START)}.*?{re.escape(BADGES_END)}",
        flags=re.DOTALL,
    )
    block = pattern.search(readme)
    if block is None:
        return readme

    updated = re.sub(r"(badge/External_PRs-)\d+", rf"\g<1>{total}", block.group(0))
    updated = re.sub(r"(badge/Merged_PRs-)\d+", rf"\g<1>{merged}", updated)
    return readme[: block.start()] + updated + readme[block.end() :]


def update_readme(readme: str, section: str) -> str:
    if START_MARKER not in readme or END_MARKER not in readme:
        raise RuntimeError(f"README must contain both {START_MARKER} and {END_MARKER}")

    pattern = re.compile(
        rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}",
        flags=re.DOTALL,
    )
    return pattern.sub(lambda _match: section, readme, count=1)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    check = "--check" in sys.argv

    snapshot = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--from-json=")), None)

    readme = README_PATH.read_text(encoding="utf-8")
    pull_requests = load_snapshot(Path(snapshot)) if snapshot else fetch_pull_requests()
    if not pull_requests:
        print("No external pull requests found; refusing to erase the section.")
        return 1

    merged_prs, _in_review = split_pull_requests(pull_requests)
    updated = update_readme(readme, render_section(pull_requests))
    updated = update_badges(updated, len(merged_prs), len(pull_requests))
    stats = render_stats_svg(pull_requests)

    if dry_run:
        merged, in_review = split_pull_requests(pull_requests)
        print(f"# {len(merged)} merged, {len(in_review)} in review")
        print(updated)
        print(stats)
        return 0

    readme_stale = updated != readme
    current_stats = STATS_PATH.read_text(encoding="utf-8") if STATS_PATH.exists() else ""
    stats_stale = stats != current_stats

    if check:
        if readme_stale or stats_stale:
            print("Profile files are stale; rerun without --check.")
            return 1
        print("Profile files are up to date.")
        return 0

    # Path.write_text(newline=) only exists on 3.10+, and a profile repo should
    # run on whatever python3 the contributor already has.
    def write(path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)

    if readme_stale:
        write(README_PATH, updated)
        print("README updated")
    else:
        print("README already up to date")

    if stats_stale:
        write(STATS_PATH, stats)
        print("Stats chart updated")
    else:
        print("Stats chart already up to date")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
