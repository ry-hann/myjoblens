"""
ingestion/parse.py
==================

Reads HTML files from `data/raw/` and extracts clean, Markdown-formatted
article text. Output is written as one .md file per source under
`data/chunks/`.

Pipeline:
    data/raw/<slug>.html  ->  data/chunks/<slug>.md

Design choices:
- Trafilatura: extracts article body, drops nav/ads/footer/comments.
- html2text: turns remaining HTML into Markdown (preserves headings, lists,
  emphasis). LLM readers parse Markdown better than flat text.
- One chunk = one source file. (Step 3 will split each chunk into ~500-token
  pieces before embedding - keeping them whole at this layer keeps the
  provenance and citations clean.)

Run:
    python ingestion/parse.py <source-filename>
  or
    python ingestion/parse.py            # processes all .html in data/raw/
"""
from __future__ import annotations

import sys
from pathlib import Path

import trafilatura
from html2text import html2text

ROOT = Path(__file__).resolve().parent.parent          # .../myjoblens/
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "chunks"

def html_to_markdown(html: str) -> str:
    """
    Two-step cleaner:
      1. Trafilatura strips boilerplate, returns clean HTML of the article body.
      2. html2text converts that clean HTML to Markdown.

    Markdown keeps headings and lists, which improves LLM answer quality.
    """
    clean_html = trafilatura.extract(html, include_comments=False,
                                     include_tables=True, favor_recall=True)
    if not clean_html:
        # Article extraction failed; fall back to minimal strip to avoid
        # producing an empty file (operator can inspect the input).
        clean_html = "<p>(no content extracted)</p>"
    md = html2text(clean_html, bodywidth=0)            # 0 = no wrapping
    # Normalize excessive blank lines for cleanliness.
    md = "\n".join(line for line in md.splitlines() if line.strip())
    return md.strip() + "\n"

def process_one(path: Path) -> Path:
    html = path.read_text(encoding="utf-8", errors="ignore")
    md = html_to_markdown(html)
    out_path = OUT_DIR / (path.stem + ".md")
    out_path.write_text(md, encoding="utf-8")
    return out_path

def main(argv: list[str]) -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    targets = (
        [RAW_DIR / argv[1]] if len(argv) > 1
        else sorted(RAW_DIR.glob("*.html"))
    )
    if not targets:
        print(f"No .html files found in {RAW_DIR}", file=sys.stderr)
        return 1
    for path in targets:
        if not path.exists():
            print(f"Missing: {path}", file=sys.stderr)
            return 1
        out = process_one(path)
        in_size = path.stat().st_size
        out_size = out.stat().st_size
        print(f"{path.name}  ({in_size:>7,} bytes)  ->  "
              f"{out.name}  ({out_size:>7,} bytes)")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))