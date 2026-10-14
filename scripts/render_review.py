"""Render a Markdown draft as an A4-width HTML page for review in Lavish, with markers where PDF pages start.

Uses the same HTML and CSS as render_pdf.py, so line breaks match the PDF.
Run render_pdf.py first: the page markers come from the text of each PDF page.

Usage: python scripts/render_review.py docs/mission1/document.md build/mission1_draft.pdf .lavish/document.html
"""

import json
import re
import pathlib
import sys

from pypdf import PdfReader

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render_pdf import to_html  # noqa: E402

REVIEW_CSS = """
html { background: #d9d9d9; }
body { width: 174mm; margin: 12mm auto; padding: 18mm; background: #fff; box-shadow: 0 1px 6px rgba(0,0,0,.25); }
.page-mark { margin: 10pt -18mm; padding: 2pt 18mm; background: #fde8c8; color: #8a4b00; font-size: 8.5pt;
             border-top: 2px dashed #c77800; border-bottom: 2px dashed #c77800; }
"""

# Finds the block that contains the first words of each PDF page and puts a marker before it.
MARK_JS = """
<script>
(() => {
  const starts = %s;
  const blocks = [...document.body.querySelectorAll("h1,h2,h3,p,li,tr,blockquote")];
  const norm = s => s.replace(/\\s+/g, " ").trim();
  starts.forEach(([page, snippet]) => {
    const hit = blocks.find(b => norm(b.textContent).includes(snippet));
    if (!hit) return;
    let anchor = hit.closest("table") && hit.tagName === "TR" ? hit.closest("table") : hit;
    if (anchor.tagName === "LI") anchor = anchor.closest("ul,ol");
    const mark = document.createElement("div");
    mark.className = "page-mark";
    mark.textContent = "Trang " + page + " của PDF bắt đầu trong khối dưới đây: \\u201c" + snippet + "\\u2026\\u201d";
    anchor.parentNode.insertBefore(mark, anchor);
  });
})();
</script>
"""


def page_starts(pdf: pathlib.Path) -> list:
    starts = []
    for i, page in enumerate(PdfReader(str(pdf)).pages[1:], start=2):
        # The page footer ("2 / 5") comes first in the extracted text.
        text = re.sub(r"^\d+ / \d+ ", "", " ".join(page.extract_text().split()))
        starts.append([i, " ".join(text.split(" ")[:5])])
    return starts


def main() -> None:
    src, pdf, dst = (pathlib.Path(a) for a in sys.argv[1:4])
    html = to_html(src.read_text(encoding="utf-8"))
    html = html.replace("</style>", REVIEW_CSS + "</style>", 1)
    html = html.replace("</body>", MARK_JS % json.dumps(page_starts(pdf), ensure_ascii=False) + "</body>", 1)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(html, encoding="utf-8")
    print(f"{dst}: {len(page_starts(pdf))} page markers")


if __name__ == "__main__":
    main()
