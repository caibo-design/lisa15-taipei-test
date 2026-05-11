from pathlib import Path
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUT_PNG = ROOT / "assets" / "ticket-holder-lisa-twilight.png"
OUT_PDF = ROOT / "assets" / "ticket-twilight.pdf"

W, H = 3508, 2480
HX, HY, HW, HH = 690, 38, 2550, 2404

INK = (38, 18, 18)
CREAM = (248, 234, 215)
COPPER = (205, 93, 42)
RUST = (136, 45, 34)
GOLD = (226, 147, 84)
WINE = (67, 20, 25)

FONT_CN = Path("/System/Library/Fonts/PingFang.ttc")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
FONT_SERIF = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")
FONT_SERIF_BI = Path("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf")
FONT_SCRIPT = Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf")


def font(path, size, index=0):
    return ImageFont.truetype(str(path), size=size, index=index)


def crop_cover(path, size, anchor=(0.5, 0.5)):
    img = Image.open(path).convert("RGB")
    sw, sh = img.size
    tw, th = size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = round((nw - tw) * anchor[0])
    top = round((nh - th) * anchor[1])
    return img.crop((left, top, left + tw, top + th))


def warm_grade(img, strength=0.45, contrast=1.08, darken=0.9):
    img = ImageEnhance.Color(img).enhance(0.78)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    overlay = Image.new("RGB", img.size, (170, 68, 33))
    img = Image.blend(img, overlay, strength)
    img = ImageEnhance.Brightness(img).enhance(darken)
    return img


def gradient(size, stops):
    w, h = size
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    xx, yy = np.meshgrid(x, y)
    t = xx * 0.62 + yy * 0.38
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        local = np.clip((t - p0) / max(p1 - p0, 0.001), 0, 1)
        mask = (t >= p0) & (t <= p1)
        c0 = np.array(c0)
        c1 = np.array(c1)
        arr[mask] = (c0 * (1 - local[..., None]) + c1 * local[..., None])[mask]
    arr[t < stops[0][0]] = stops[0][1]
    arr[t > stops[-1][0]] = stops[-1][1]
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)))


def add_grain(img, amount=22):
    rng = np.random.default_rng(15)
    arr = np.array(img).astype(np.float32)
    noise = rng.normal(0, amount, arr.shape[:2])
    arr[:, :, 0] += noise
    arr[:, :, 1] += noise * 0.75
    arr[:, :, 2] += noise * 0.55
    return Image.fromarray(np.uint8(np.clip(arr, 0, 255)))


def draw_dashed(draw, xy, dash=18, gap=14, fill=(0, 0, 0), width=3):
    x0, y0, x1, y1 = xy
    length = math.hypot(x1 - x0, y1 - y0)
    dx, dy = (x1 - x0) / length, (y1 - y0) / length
    dist = 0
    while dist < length:
        end = min(dist + dash, length)
        draw.line((x0 + dx * dist, y0 + dy * dist, x0 + dx * end, y0 + dy * end), fill=fill, width=width)
        dist += dash + gap


def letter_text(draw, xy, text, fnt, fill, tracking=10, anchor="la"):
    x, y = xy
    if anchor.endswith("m"):
        total = sum(draw.textlength(ch, font=fnt) + tracking for ch in text) - tracking
        x -= total / 2
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill, anchor="la")
        x += draw.textlength(ch, font=fnt) + tracking


def text_center(draw, pos, text, fnt, fill, stroke=0, stroke_fill=INK, spacing=4):
    draw.multiline_text(pos, text, anchor="mm", align="center", font=fnt, fill=fill,
                        stroke_width=stroke, stroke_fill=stroke_fill, spacing=spacing)


def sparkle(draw, cx, cy, r, fill, alpha=180):
    fill = (*fill, alpha)
    pts = [
        (cx, cy - r), (cx + r * 0.08, cy - r * 0.1), (cx + r, cy),
        (cx + r * 0.08, cy + r * 0.1), (cx, cy + r),
        (cx - r * 0.08, cy + r * 0.1), (cx - r, cy), (cx - r * 0.08, cy - r * 0.1)
    ]
    draw.polygon(pts, fill=fill)


def line_script(draw, x, y, text, size=120, fill=(226, 147, 84, 140)):
    draw.text((x, y), text, font=font(FONT_SCRIPT, size), fill=fill, anchor="mm")


def paste_photo_strip(panel, xy, size, image_path, anchor, title_left, title_right=None):
    x, y = xy
    w, h = size
    photo = crop_cover(image_path, size, anchor)
    photo = warm_grade(photo, 0.38, 1.12, 0.88).convert("RGBA")
    glow = Image.new("RGBA", size, (115, 42, 24, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    gd.rectangle((0, 0, w, h), fill=(117, 31, 25, 70))
    gd.ellipse((-80, -160, w * 0.72, h * 1.2), fill=(238, 143, 74, 86))
    photo.alpha_composite(glow)
    panel.alpha_composite(photo, (x, y))
    d = ImageDraw.Draw(panel, "RGBA")
    d.rectangle((x, y, x + w, y + h), outline=(244, 203, 169, 90), width=2)
    letter_text(d, (x + 65, y + 86), title_left, font(FONT_SERIF, 118), CREAM, tracking=16)
    if title_right:
        letter_text(d, (x + w - 360, y + h - 145), title_right, font(FONT_SERIF, 100), CREAM, tracking=14)
    line_script(d, x + w - 320, y + 120, "LiSA", 120, (226, 147, 84, 125))
    d.text((x + w - 210, y + 68), "2026", font=font(FONT_SERIF_BI, 33), fill=(226, 147, 84, 120))
    d.text((x + 60, y + h - 58), "will fall into the gentle twilight, will fall into you",
           font=font(FONT_SERIF_BI, 29), fill=(248, 234, 215, 185))


def draw_holder_guides(draw):
    draw.rectangle((HX + 28, HY + 28, HX + HW - 28, HY + HH - 28), outline=(248, 234, 215, 90), width=3)
    draw_dashed(draw, (HX, HY + 415, HX + HW, HY + 415), fill=(248, 234, 215, 105), width=4)
    draw_dashed(draw, (HX, HY + 1425, HX + HW, HY + 1425), fill=(248, 234, 215, 105), width=4)
    draw.polygon([(HX - 255, HY + 433), (HX, HY + 405), (HX, HY + 1053), (HX - 255, HY + 1030)],
                 fill=(50, 28, 24, 30), outline=(248, 234, 215, 120))
    draw.polygon([(HX + HW, HY + 405), (HX + HW + 255, HY + 433), (HX + HW + 255, HY + 1030), (HX + HW, HY + 1053)],
                 fill=(50, 28, 24, 30), outline=(248, 234, 215, 120))


def build_panel(upside_down=False):
    panel = Image.new("RGBA", (HW, 1010 if upside_down else 979), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel, "RGBA")
    ph = panel.height
    d.rectangle((0, 0, HW, ph), fill=(67, 20, 25, 38))

    if upside_down:
        photo = crop_cover(ROOT / "素材/650996790_1455269059296864_7153961107339767219_n.jpg", (920, 750), (0.55, 0.44))
        photo = warm_grade(photo, 0.5, 1.1, 0.82).convert("RGBA")
        mask = Image.new("L", photo.size, 0)
        md = ImageDraw.Draw(mask)
        md.rectangle((0, 0, photo.width, photo.height), fill=185)
        panel.paste(photo, (1420, 170), mask)
        d.rectangle((1420, 170, 2340, 920), fill=(40, 10, 12, 80))
        letter_text(d, (235, 185), "TWILIGHT", font(FONT_SERIF, 138), CREAM, tracking=13)
        letter_text(d, (235, 330), "PREVIEW", font(FONT_SERIF, 138), CREAM, tracking=13)
        line_script(d, 690, 312, "warm", 175, (226, 147, 84, 135))
        d.text((238, 505), "will fall into the gentle twilight, will fall into you",
               font=font(FONT_SERIF_BI, 38), fill=(248, 234, 215, 210))
        d.text((238, 590), "0619", font=font(FONT_SERIF_BI, 54), fill=(226, 94, 48, 130))
        d.text((2055, 185), "2026", font=font(FONT_SERIF_BI, 62), fill=(226, 94, 48, 105))
        text_center(d, (1770, 525), "LiSA\nLiVE is Smile Always ~15~", font(FONT_SERIF, 82), CREAM, spacing=8)
        d.text((1820, 760), "JUN 19 2026 | 6 PM\nTAIPEI ARENA", font=font(FONT_BOLD, 34),
               fill=(248, 234, 215, 210), anchor="mm", align="center")
        sparkle(d, 1260, 765, 54, GOLD, 130)
        return panel.rotate(180)

    paste_photo_strip(panel, (170, 120), (1010, 320), ROOT / "素材/669036261_1476090733881363_773819450042997474_n.jpg",
                      (0.55, 0.5), "LiSA", "15")
    paste_photo_strip(panel, (170, 510), (1010, 320), ROOT / "素材/650996790_1455269059296864_7153961107339767219_n.jpg",
                      (0.55, 0.42), "LIVE", "SMILE")

    main = crop_cover(ROOT / "素材/662910887_1473856544104782_1797694666298698514_n.jpg", (690, 820), (0.54, 0.22))
    main = warm_grade(main, 0.42, 1.12, 0.9).convert("RGBA")
    panel.alpha_composite(main, (1460, 90))
    d.rectangle((1460, 90, 2150, 910), outline=(248, 234, 215, 75), width=2)
    d.rectangle((1460, 90, 2150, 910), fill=(70, 22, 22, 58))

    letter_text(d, (2185, 170), "LiSA", font(FONT_SERIF, 150), CREAM, tracking=14)
    letter_text(d, (2185, 330), "15th", font(FONT_SERIF, 122), CREAM, tracking=8)
    line_script(d, 2360, 315, "Asia", 165, (226, 147, 84, 140))
    d.text((2190, 470), "LiVE is Smile Always ~15~\nASIA TOUR 2026",
           font=font(FONT_SERIF_BI, 37), fill=(248, 234, 215, 210), spacing=12)
    d.text((2190, 610), "JUN 19 2026 | 6 PM\nTAIPEI ARENA",
           font=font(FONT_BOLD, 34), fill=(248, 234, 215, 220), spacing=9)
    d.text((2190, 805), "TAIPEI  . . . . . .  LiSA",
           font=font(FONT_SERIF, 45), fill=(248, 234, 215, 180))
    sparkle(d, 2200, 760, 45, GOLD, 120)
    sparkle(d, 1280, 210, 24, CREAM, 160)
    return panel


def main():
    random.seed(15)
    bg = gradient((W, H), [
        (0, (116, 50, 33)),
        (0.23, (147, 64, 36)),
        (0.52, (88, 28, 29)),
        (0.77, (48, 17, 23)),
        (1, (135, 55, 31)),
    ])
    bg = add_grain(bg, 16).convert("RGBA")
    d = ImageDraw.Draw(bg, "RGBA")

    d.rectangle((66, 1590, 250, 2190), fill=(80, 25, 24, 210))
    note_font = font(FONT_CN, 65, index=0)
    for i, ch in enumerate("票夾模板"):
        d.text((158, 1665 + i * 105), ch, font=note_font, fill=CREAM, anchor="mm")
    d.text((90, 2320), "請以A4尺寸列印", font=font(FONT_CN, 54, index=0), fill=CREAM, anchor="lm")
    d.line((90, 2362, 560, 2362), fill=CREAM, width=4)

    holder = gradient((HW, HH), [
        (0, (157, 71, 38)),
        (0.34, (95, 32, 31)),
        (0.66, (44, 15, 22)),
        (1, (167, 76, 39)),
    ])
    holder = add_grain(holder, 18).filter(ImageFilter.GaussianBlur(0.15)).convert("RGBA")
    hd = ImageDraw.Draw(holder, "RGBA")
    for x in range(-200, HW, 190):
        hd.line((x, HH, x + 880, 0), fill=(234, 126, 65, 26), width=5)
    hd.ellipse((HW - 950, -300, HW + 250, 680), fill=(226, 147, 84, 42))
    hd.ellipse((-260, 1260, 740, 2500), fill=(54, 16, 22, 90))
    bg.alpha_composite(holder, (HX, HY))
    d = ImageDraw.Draw(bg, "RGBA")
    draw_holder_guides(d)

    upper = build_panel(upside_down=True)
    bg.alpha_composite(upper, (HX, HY + 415))
    lower = build_panel(upside_down=False)
    bg.alpha_composite(lower, (HX, HY + 1425))

    final = bg.convert("RGB")
    OUT_PNG.parent.mkdir(exist_ok=True)
    final.save(OUT_PNG, quality=95)
    final.save(OUT_PDF, "PDF", resolution=300.0)
    print(f"saved {OUT_PNG}")
    print(f"saved {OUT_PDF}")


if __name__ == "__main__":
    main()
