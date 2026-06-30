"""Generate a "Top-N most popular questions (with answers)" wiki page.

Self-contained: reads ONLY committed wiki content under ``docs/``. Popularity comes from the
badges already rendered on the section headings, e.g. ``### Що таке GIL? ... [🔥89/100]`` -
the number in the badge is the popularity score (🔥 ≥30, 💡 10-29). A heading without a badge
scores below 10 and can never make the top list, so it is ignored.

Pipeline:
  1. walk ``docs/**/*.md`` and collect every ``### `` section that has a popularity badge;
  2. rank the sections by score and keep the top N;
  3. write each question + its full answer body into a single generated page
     (default ``docs/top_questions.md``).

Idempotent and safe to re-run:

    python3 scripts/generate_top_questions.py            # top 100 -> docs/top_questions.md
    python3 scripts/generate_top_questions.py --top 50

The output page is generated content - do not edit it by hand; edit the underlying section
and re-run. (The badges are refreshed by the maintainers' internal tooling; this script just
reflects whatever scores are committed.) Keep the page in ``mkdocs.yml`` nav.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
import re

# --- paths ----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent  # scripts/<this file> -> repo root
DOCS_DIR = ROOT / "docs"
DEFAULT_OUTPUT = DOCS_DIR / "top_questions.md"

# --- markdown patterns ----------------------------------------------------
# Popularity badge at the END of a heading, e.g. "...Question? [🔥89/100]".
#   group 1 = tier emoji (a run of non-digits)  - shown next to the score
#   group 2 = the score                         - what we rank by
BADGE_RE = re.compile(r"\s*\[(\D+?)(\d+)/\d+]\s*$")
# A code-fence line that opens or closes a ``` / ~~~ block (may be indented).
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
# A markdown heading of level 1-3 ("# ", "## ", "### "); NOT "#### " or deeper.
HEADING_RE = re.compile(r"^#{1,3} ")
# A run of 3+ newlines (i.e. 2+ blank lines) - collapsed to one blank line.
BLANK_RUN_RE = re.compile(r"\n{3,}")

HEADING_PREFIX = "### "  # the heading level that marks a question


@dataclass
class Question:
    """One badged ``### `` wiki section: a question heading plus its answer body."""

    heading: str      # heading text, with the trailing badge stripped off
    score: int        # popularity score (the number taken from the badge)
    emoji: str        # tier emoji from the badge (🔥 / 💡), shown beside the score
    source_file: str  # path relative to docs/, e.g. "python/async.md"
    body: str         # everything under the heading, kept verbatim


def heading_line_numbers(lines: list[str]) -> list[int]:
    """Indexes of every level 1-3 heading line that sits OUTSIDE a code fence.

    Tracking fences is essential: a Python ``# comment`` (or a ``## step`` in a shell
    snippet) inside a ``` block looks exactly like a markdown heading. If we mistook one
    for a heading, a section would be cut in the middle of a code block and the fences
    would end up unbalanced in the output.
    """
    headings: list[int] = []
    inside_fence = False
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            inside_fence = not inside_fence  # flip on each ``` / ~~~ line
        elif not inside_fence and HEADING_RE.match(line):
            headings.append(index)
    return headings


def clean_body(text: str) -> str:
    """Trim surrounding blank lines and collapse 2+ blank lines into one."""
    return BLANK_RUN_RE.sub("\n\n", text.strip("\n")).strip()


def iter_questions(doc_text: str, source_file: str) -> Iterator[Question]:
    """Yield a Question for every badged ``### `` section in one markdown file."""
    lines = doc_text.splitlines()
    headings = heading_line_numbers(lines)

    for position, start in enumerate(headings):
        line = lines[start]

        # Only level-3 headings are questions; skip "# " / "## " section titles.
        if not line.startswith(HEADING_PREFIX):
            continue

        # No badge means the section scored below 10 - it can never reach the top N.
        badge = BADGE_RE.search(line)
        if badge is None:
            continue

        # The answer body runs from the line after the heading up to the NEXT heading
        # (the next entry in `headings`), or to end-of-file for the last one. Because
        # `headings` only holds levels 1-3, any "#### " sub-block stays inside the body.
        end = headings[position + 1] if position + 1 < len(headings) else len(lines)

        yield Question(
            heading=BADGE_RE.sub("", line[len(HEADING_PREFIX):]).strip(),
            score=int(badge.group(2)),
            emoji=badge.group(1).strip(),
            source_file=source_file,
            body=clean_body("\n".join(lines[start + 1 : end])),
        )


def collect_questions(output_path: Path) -> list[Question]:
    """Gather questions from every doc under docs/, except the generated page itself."""
    questions: list[Question] = []
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        if md_file.resolve() == output_path.resolve():
            continue  # never ingest the page we are about to (re)write
        source_file = md_file.relative_to(DOCS_DIR).as_posix()
        questions.extend(iter_questions(md_file.read_text(encoding="utf-8"), source_file))
    return questions


def render_page(questions: list[Question]) -> str:
    """Render the already-ranked questions into the final markdown page."""
    blocks = [f"# Топ-{len(questions)} найпопулярніших питань\n"]
    for rank, q in enumerate(questions, start=1):
        source_link = f"[`{q.source_file}`]({q.source_file})"
        blocks.append(f"## {rank}. {q.heading}\n")
        blocks.append(f"*{q.emoji} {q.score}/100 · {source_link}*\n")
        blocks.append(q.body or "_(дивись розділ за посиланням вище)_")
        blocks.append("\n---\n")
    # Single trailing newline, no trailing separator noise.
    return "\n".join(blocks).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--top", type=int, default=100,
                        help="how many questions to include (default 100)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="output markdown path")
    args = parser.parse_args()

    questions = collect_questions(args.output)
    # Rank by score, highest first. Break ties by (file, heading) so the order is stable
    # and reproducible from run to run.
    questions.sort(key=lambda q: (-q.score, q.source_file, q.heading))
    top = questions[: args.top]

    args.output.write_text(render_page(top), encoding="utf-8")
    print(f"Wrote {len(top)} questions to {args.output.relative_to(ROOT)} "
          f"(from {len(questions)} badged sections across docs/)")


if __name__ == "__main__":
    main()
