"""Render a Markdown draft to an A4 PDF via headless Edge, then report the page count.

Usage: python tools/render_pdf.py docs/mission1/document.md build/mission1_draft.pdf
"""

import pathlib
import subprocess
import sys

import markdown
from pypdf import PdfReader

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 18mm 18mm 16mm 18mm;
        @bottom-center { content: counter(page) " / " counter(pages); font-size: 9pt; } }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.38; color: #111; }
h1 { font-size: 17pt; margin: 0 0 4pt; }
h2 { font-size: 13pt; margin: 12pt 0 4pt; border-bottom: 1px solid #999; padding-bottom: 2pt; }
p { margin: 3pt 0; }
ul { margin: 3pt 0; padding-left: 16pt; }
blockquote { margin: 6pt 0; padding: 4pt 8pt; border-left: 3px solid #555; background: #f3f3f3; }
table { border-collapse: collapse; width: 100%; margin: 5pt 0; font-size: 9.5pt; page-break-inside: auto; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #aaa; padding: 2pt 4pt; vertical-align: top; text-align: left; }
th { background: #e8e8e8; }
pre { background: #f6f6f6; border: 1px solid #ccc; padding: 5pt; font-size: 9pt; white-space: pre-wrap; }
.mermaid { text-align: center; margin: 4pt 0; }
"""


def to_html(md_text: str) -> str:
    # Turn ```mermaid fences into divs before Markdown conversion so Mermaid can render them.
    out, inside = [], False
    for line in md_text.splitlines():
        if line.strip() == "```mermaid":
            out.append('<div class="mermaid">')
            inside = True
        elif inside and line.strip() == "```":
            out.append("</div>")
            inside = False
        else:
            out.append(line)
    # Hard line breaks match the one-sentence-per-line source style.
    # tab_length=2 so 2-space indented sub-items (the style used across docs/) render as nested lists.
    body = markdown.markdown("\n".join(out), extensions=["tables", "fenced_code", "nl2br", "md_in_html"], tab_length=2)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad: true, theme: "neutral",
  themeVariables: {{fontSize: "22px"}},
  flowchart: {{useMaxWidth: true, nodeSpacing: 18, rankSpacing: 22, padding: 6}}}});</script>
</head><body>{body}</body></html>"""


def main() -> None:
    src, dst = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    html_path = dst.with_suffix(".html")
    html_path.write_text(to_html(src.read_text(encoding="utf-8")), encoding="utf-8")
    subprocess.run(
        [EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
         f"--print-to-pdf={dst}", html_path.as_uri()],
        check=True, capture_output=True,
    )
    print(f"{dst.name}: {len(PdfReader(str(dst)).pages)} pages")


if __name__ == "__main__":
    main()
