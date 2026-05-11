from pathlib import Path
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT_PNG = ROOT / "assets" / "ticket-holder-lisa.png"
OUT_PDF = ROOT / "assets" / "ticket.pdf"

W, H = 3508, 2480
HX, HY, HW, HH = 690, 38, 2550, 2404
PINK = (255, 47, 159)
RED = (216, 40, 47)
INK = (17, 17, 17)
PAPER = (251, 250, 248)


def font(path, size, index=0):
    return ImageFont.truetype(str(path), size=size, index=index)


FONT_CN = Path("/System/Library/Fonts/PingFang.ttc")
FONT_HEAVY = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
FONT_COND = Path("/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")
FONT_SERIF_BI = Path("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf")
FONT_SERIF = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")


def crop_cover(path, size, anchor=(0.5, 0.5)):
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    ax, ay = anchor
    left = round((nw - tw) * ax)
    top = round((nh - th) * ay)
    return img.crop((left, top, left + tw, top + th))


def gradient(size, stops):
    w, h = size
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    xx, yy = np.meshgrid(x, y)
    t = (xx * 0.78 + yy * 0.22)
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        mask = (t >= p0) & (t <= p1)
        local = np.clip((t - p0) / max(p1 - p0, 0.001), 0, 1)
        c0 = np.array(c0)
        c1 = np.array(c1)
        arr[mask] = (c0 * (1 - local[..., None]) + c1 * local[..., None])[mask]
    arr[t < stops[0][0]] = stops[0][1]
    arr[t > stops[-1][0]] = stops[-1][1]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)))


def draw_checker(draw, box, cell=150, color=(255, 255, 255, 72)):
    x0, y0, x1, y1 = box
    for y in range(y0, y1, cell):
        for x in range(x0, x1, cell):
            if ((x - x0) // cell + (y - y0) // cell) % 2 == 0:
                draw.rectangle((x, y, min(x + cell, x1), min(y + cell, y1)), fill=color)


def draw_dashed(draw, xy, dash=18, gap=14, fill=(0, 0, 0), width=3):
    x0, y0, x1, y1 = xy
    length = math.hypot(x1 - x0, y1 - y0)
    dx, dy = (x1 - x0) / length, (y1 - y0) / length
    dist = 0
    while dist < length:
        end = min(dist + dash, length)
        draw.line((x0 + dx * dist, y0 + dy * dist, x0 + dx * end, y0 + dy * end), fill=fill, width=width)
        dist += dash + gap


def sparkle(draw, cx, cy, r, fill, outline=None, width=0):
    pts = [
        (cx, cy - r),
        (cx + r * 0.11, cy - r * 0.14),
        (cx + r, cy),
        (cx + r * 0.11, cy + r * 0.14),
        (cx, cy + r),
        (cx - r * 0.11, cy + r * 0.14),
        (cx - r, cy),
        (cx - r * 0.11, cy - r * 0.14),
    ]
    draw.polygon(pts, fill=fill, outline=outline)
    if outline and width > 1:
        draw.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


def strawberry(draw, cx, cy, scale=1.0):
    r = 120 * scale
    pts = [
        (cx, cy - r),
        (cx + r * 0.8, cy - r * 0.45),
        (cx + r, cy + r * 0.3),
        (cx + r * 0.35, cy + r),
        (cx, cy + r * 0.62),
        (cx - r * 0.35, cy + r),
        (cx - r, cy + r * 0.3),
        (cx - r * 0.8, cy - r * 0.45),
    ]
    draw.polygon(pts, fill=PINK)
    draw.text((cx, cy + 10 * scale), "15", fill="white", anchor="mm",
              font=font(FONT_COND, int(108 * scale)), stroke_width=int(5 * scale), stroke_fill=INK)


def paste_masked(dst, src, xy, mask_poly, shadow=None):
    mask = Image.new("L", src.size, 0)
    md = ImageDraw.Draw(mask)
    md.polygon(mask_poly, fill=255)
    if shadow:
        sx, sy, color = shadow
        sh = Image.new("RGBA", src.size, color)
        dst.paste(sh, (xy[0] + sx, xy[1] + sy), mask)
    dst.paste(src.convert("RGBA"), xy, mask)


def text_center(draw, pos, text, fnt, fill, stroke=0, stroke_fill="white", spacing=4):
    draw.multiline_text(pos, text, anchor="mm", align="center", font=fnt, fill=fill,
                        stroke_width=stroke, stroke_fill=stroke_fill, spacing=spacing)


def main():
    page = Image.new("RGB", (W, H), (248, 247, 246))
    page_rgba = page.convert("RGBA")
    d = ImageDraw.Draw(page_rgba, "RGBA")

    d.rectangle((66, 1590, 250, 2190), fill=PINK)
    note_font = font(FONT_CN, 65, index=0)
    for i, ch in enumerate("票夾模板"):
        d.text((158, 1665 + i * 105), ch, font=note_font, fill="white", anchor="mm")
    d.text((90, 2320), "請以A4尺寸列印", font=font(FONT_CN, 54, index=0), fill=(35, 35, 35), anchor="lm")
    d.line((90, 2362, 560, 2362), fill=(35, 35, 35), width=4)

    holder = gradient((HW, HH), [
        (0, (248, 246, 244)),
        (0.25, (255, 47, 159)),
        (0.52, (252, 250, 248)),
        (0.82, (213, 213, 213)),
        (1, (255, 112, 186)),
    ]).convert("RGBA")
    hd = ImageDraw.Draw(holder, "RGBA")
    draw_checker(hd, (0, 0, HW, HH), 150, (255, 255, 255, 70))
    for off in range(-800, HW, 130):
        hd.line((off, HH, off + 1400, 0), fill=(216, 40, 47, 42), width=4)
    hd.rectangle((28, 28, HW - 28, HH - 28), outline=(0, 0, 0, 115), width=3)
    draw_dashed(hd, (0, 415, HW, 415), fill=(0, 0, 0, 88), width=4)
    draw_dashed(hd, (0, 1425, HW, 1425), fill=(0, 0, 0, 88), width=4)

    page_rgba.alpha_composite(holder, (HX, HY))
    d = ImageDraw.Draw(page_rgba, "RGBA")
    d.polygon([(HX - 255, HY + 433), (HX, HY + 405), (HX, HY + 1053), (HX - 255, HY + 1030)],
              fill=(251, 250, 248, 244), outline=(0, 0, 0, 120))
    d.polygon([(HX + HW, HY + 405), (HX + HW + 255, HY + 433), (HX + HW + 255, HY + 1030), (HX + HW, HY + 1053)],
              fill=(251, 250, 248, 244), outline=(0, 0, 0, 120))

    upper = Image.new("RGBA", (HW, 1010), (255, 255, 255, 0))
    ud = ImageDraw.Draw(upper, "RGBA")
    ud.rectangle((0, 0, HW, 1010), fill=(248, 246, 244, 190))
    art = crop_cover(ROOT / "素材/669036261_1476090733881363_773819450042997474_n.jpg", (1245, 1010), (0.58, 0.48)).convert("RGBA")
    upper.alpha_composite(art, (1305, 0))
    wash = gradient((HW, 1010), [(0, (255, 47, 159)), (0.5, (252, 250, 248)), (1, (252, 250, 248))]).convert("RGBA")
    wash.putalpha(Image.new("L", (HW, 1010), 210))
    upper.alpha_composite(wash, (0, 0))
    ud = ImageDraw.Draw(upper, "RGBA")
    ud.text((740, 185), "ASIA TOUR 2026", fill=INK, anchor="mm", font=font(FONT_COND, 68))
    ud.text((740, 330), "LiSA", fill=PINK, anchor="mm", font=font(FONT_COND, 235),
            stroke_width=9, stroke_fill=INK)
    text_center(ud, (740, 510), "LiVE is Smile Always\n~15~", font(FONT_SERIF_BI, 108),
                INK, stroke=5, stroke_fill="white", spacing=-12)
    ud.rounded_rectangle((480, 735, 1000, 850), radius=58, fill=(255, 255, 255, 175), outline=INK, width=4)
    text_center(ud, (740, 792), "JUN 19 2026 | 6 PM\nTAIPEI ARENA", font(FONT_HEAVY, 35), INK, spacing=6)
    strawberry(ud, 1565, 555, 1.0)
    sparkle(ud, 155, 770, 95, INK)
    sparkle(ud, 2290, 155, 110, PINK)
    upper = upper.rotate(180)
    page_rgba.alpha_composite(upper, (HX, HY + 415))

    lower = Image.new("RGBA", (HW, 979), (255, 255, 255, 0))
    ld = ImageDraw.Draw(lower, "RGBA")
    ld.rectangle((0, 0, HW, 979), fill=(255, 255, 255, 65))
    main_img = crop_cover(ROOT / "素材/650996790_1455269059296864_7153961107339767219_n.jpg", (1050, 920), (0.57, 0.41)).convert("RGBA")
    paste_masked(lower, Image.new("RGBA", (1050, 920), (*PINK, 255)), (1390 - 28, 59 + 22),
                 [(84, 0), (1050, 0), (987, 920), (0, 920)])
    paste_masked(lower, main_img, (1390, 59), [(84, 0), (1050, 0), (987, 920), (0, 920)])
    ld = ImageDraw.Draw(lower, "RGBA")
    ld.rectangle((138, 110, 850, 168), fill=INK)
    ld.text((160, 139), "LiSA 15th Taipei Fan Ticket Holder", font=font(FONT_COND, 39), fill="white", anchor="lm")
    ld.multiline_text((138, 238), "LiVE is Smile\nAlways ~15~", font=font(FONT_SERIF_BI, 116),
                      fill=INK, spacing=-14, stroke_width=5, stroke_fill="white")
    ld.text((138, 520), "2026.06.19 FRI | 18:00\nTAIPEI ARENA", font=font(FONT_HEAVY, 45),
            fill=INK, spacing=12)
    strip_paths = [
        (ROOT / "素材/662910887_1473856544104782_1797694666298698514_n.jpg", "TAIPEI", (0.48, 0.20)),
        (ROOT / "素材/667863751_1476061287217641_1401771218230708810_n.jpg", "DECOTORA15", (0.50, 0.36)),
        (ROOT / "素材/669036261_1476090733881363_773819450042997474_n.jpg", "LACE UP", (0.62, 0.46)),
    ]
    for i, (p, label, anc) in enumerate(strip_paths):
        x = 135 + i * 273
        y = 502
        img = crop_cover(p, (245, 385), anc).convert("RGBA")
        ld.rectangle((x - 8, y - 8, x + 253, y + 393), fill="white")
        lower.alpha_composite(img, (x, y))
        ld.rectangle((x + 22, y + 350, x + 185, y + 412), fill="white", outline=INK, width=4)
        ld.text((x + 103, y + 382), label, font=font(FONT_HEAVY, 23), fill=INK, anchor="mm")
    ld.rounded_rectangle((820, 887, 1265, 944), radius=30, fill=PINK, outline=INK, width=4)
    ld.text((1042, 915), "LiSA 15th ASIA TOUR", font=font(FONT_COND, 34), fill="white", anchor="mm")
    ld.rounded_rectangle((1875, 887, 2395, 944), radius=30, fill=PINK, outline=INK, width=4)
    ld.text((2135, 915), "LiVE is Smile Always", font=font(FONT_COND, 34), fill="white", anchor="mm")
    sparkle(ld, 960, 210, 65, PINK)
    sparkle(ld, 1180, 832, 43, INK)
    sparkle(ld, 1530, 705, 48, INK)
    ld.text((1040, 78), "x x x", font=font(Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"), 92),
            fill=RED, anchor="lm")
    page_rgba.alpha_composite(lower, (HX, HY + 1425))

    final = page_rgba.convert("RGB")
    OUT_PNG.parent.mkdir(exist_ok=True)
    final.save(OUT_PNG, quality=95)
    final.save(OUT_PDF, "PDF", resolution=300.0)
    print(f"saved {OUT_PNG}")
    print(f"saved {OUT_PDF}")


if __name__ == "__main__":
    main()
