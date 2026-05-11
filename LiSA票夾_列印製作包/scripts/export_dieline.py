from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "assets"

PAGE_W_MM = 297.0
PAGE_H_MM = 210.0
SRC_W = 3508.0
SRC_H = 2480.0


def mmx(px):
    return px / SRC_W * PAGE_W_MM


def mmy(px):
    return px / SRC_H * PAGE_H_MM


def pt(mm):
    return mm * 72.0 / 25.4


holder_x = 690
holder_y = 38
holder_w = 2550
holder_h = 2404
border_inset = 28

cut_px = [
    (690, 38),
    (3240, 38),
    (3240, 443),
    (3495, 471),
    (3495, 1068),
    (3240, 1091),
    (3240, 2442),
    (690, 2442),
    (690, 1091),
    (435, 1068),
    (435, 471),
    (690, 443),
    (690, 38),
]

folds_px = [
    ((690, 453), (3240, 453)),
    ((690, 1463), (3240, 1463)),
    ((690, 443), (690, 1091)),
    ((3240, 443), (3240, 1091)),
]

safe_px = [
    (holder_x + border_inset, holder_y + border_inset),
    (holder_x + holder_w - border_inset, holder_y + border_inset),
    (holder_x + holder_w - border_inset, holder_y + holder_h - border_inset),
    (holder_x + border_inset, holder_y + holder_h - border_inset),
    (holder_x + border_inset, holder_y + border_inset),
]


def svg_points(points):
    return " ".join(f"{mmx(x):.3f},{mmy(y):.3f}" for x, y in points)


def make_svg():
    fold_lines = "\n".join(
        f'      <line x1="{mmx(a[0]):.3f}" y1="{mmy(a[1]):.3f}" x2="{mmx(b[0]):.3f}" y2="{mmy(b[1]):.3f}" />'
        for a, b in folds_px
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W_MM}mm" height="{PAGE_H_MM}mm" viewBox="0 0 {PAGE_W_MM} {PAGE_H_MM}" version="1.1">
  <title>LiSA 15th Taipei Ticket Holder Dieline</title>
  <desc>A4 landscape dieline. Magenta solid lines are cut lines; blue dashed lines are fold lines; gray line is safe artwork boundary.</desc>
  <defs>
    <style>
      .cut-line {{ fill: none; stroke: #ff00ff; stroke-width: 0.25; vector-effect: non-scaling-stroke; }}
      .fold-line {{ fill: none; stroke: #0099ff; stroke-width: 0.25; stroke-dasharray: 2 1.5; vector-effect: non-scaling-stroke; }}
      .safe-line {{ fill: none; stroke: #808080; stroke-width: 0.18; stroke-dasharray: 1.5 1.2; vector-effect: non-scaling-stroke; }}
      .page-line {{ fill: none; stroke: #cccccc; stroke-width: 0.18; vector-effect: non-scaling-stroke; }}
      .label {{ font-family: Arial, sans-serif; font-size: 3.2px; fill: #111111; }}
    </style>
  </defs>
  <g id="A4_Artboard">
    <rect class="page-line" x="0.2" y="0.2" width="{PAGE_W_MM - 0.4:.3f}" height="{PAGE_H_MM - 0.4:.3f}" />
  </g>
  <g id="Safe_Area_Guide">
    <polyline class="safe-line" points="{svg_points(safe_px)}" />
  </g>
  <g id="Fold_Lines">
{fold_lines}
  </g>
  <g id="Cut_Lines">
    <polyline class="cut-line" points="{svg_points(cut_px)}" />
  </g>
  <g id="Labels">
    <text class="label" x="12" y="196">A4 landscape / units: millimeters</text>
    <text class="label" x="12" y="201">CUT: magenta solid | FOLD: blue dashed | SAFE: gray dashed</text>
  </g>
</svg>
"""


def pdf_cmd_path(points):
    parts = []
    for i, (x_px, y_px) in enumerate(points):
        x = pt(mmx(x_px))
        y = pt(PAGE_H_MM - mmy(y_px))
        parts.append(f"{x:.3f} {y:.3f} {'m' if i == 0 else 'l'}")
    return "\n".join(parts)


def pdf_line(a, b):
    x1 = pt(mmx(a[0]))
    y1 = pt(PAGE_H_MM - mmy(a[1]))
    x2 = pt(mmx(b[0]))
    y2 = pt(PAGE_H_MM - mmy(b[1]))
    return f"{x1:.3f} {y1:.3f} m {x2:.3f} {y2:.3f} l S"


def make_pdf_bytes():
    page_w_pt = pt(PAGE_W_MM)
    page_h_pt = pt(PAGE_H_MM)
    stream = f"""q
0.8 0.8 0.8 RG 0.5 w
0.567 0.567 {page_w_pt - 1.134:.3f} {page_h_pt - 1.134:.3f} re S
0.5 0.5 0.5 RG 0.5 w [4 3] 0 d
{pdf_cmd_path(safe_px)}
S
0 0.6 1 RG 0.7 w [6 4] 0 d
{chr(10).join(pdf_line(a, b) for a, b in folds_px)}
1 0 1 RG 0.7 w [] 0 d
{pdf_cmd_path(cut_px)}
S
0 0 0 rg /F1 9 Tf
34 40 Td (A4 landscape / units: millimeters) Tj
0 -12 Td (CUT: magenta solid | FOLD: blue dashed | SAFE: gray dashed) Tj
Q
"""
    objects = []
    objects.append("1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n")
    objects.append("2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n")
    objects.append(
        f"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_w_pt:.3f} {page_h_pt:.3f}] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n"
    )
    objects.append("4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n")
    stream_bytes = stream.encode("latin-1")
    objects.append(f"5 0 obj << /Length {len(stream_bytes)} >> stream\n{stream}endstream endobj\n")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(out))
        out.extend(obj.encode("latin-1"))
    xref = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("latin-1"))
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
    out.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("latin-1")
    )
    return bytes(out)


def main():
    OUT_DIR.mkdir(exist_ok=True)
    svg_path = OUT_DIR / "ticket-holder-dieline.svg"
    pdf_path = OUT_DIR / "ticket-holder-dieline.pdf"
    ai_path = OUT_DIR / "ticket-holder-dieline.ai"
    svg_path.write_text(make_svg(), encoding="utf-8")
    pdf_bytes = make_pdf_bytes()
    pdf_path.write_bytes(pdf_bytes)
    ai_path.write_bytes(pdf_bytes)
    print(svg_path)
    print(pdf_path)
    print(ai_path)


if __name__ == "__main__":
    main()
