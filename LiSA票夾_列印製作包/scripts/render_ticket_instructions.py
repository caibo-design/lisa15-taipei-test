from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "ticket-holder-instructions.png"
OUT_PDF = ROOT / "assets" / "ticket-holder-instructions.pdf"
PREVIEW = ROOT / "assets" / "ticket-holder-lisa.png"

W, H = 1800, 2600
PINK = (255, 47, 159)
INK = (20, 18, 20)
PAPER = (250, 248, 246)
MUTED = (102, 96, 102)
BLUE = (0, 153, 255)
GRAY = (230, 226, 224)


def font(path, size, index=0):
    return ImageFont.truetype(str(path), size=size, index=index)


FONT_CN = Path("/System/Library/Fonts/PingFang.ttc")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
FONT_COND = Path("/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")


def f_cn(size):
    return font(FONT_CN, size, 0)


def f_bold(size):
    return font(FONT_BOLD, size)


def dashed_line(draw, xy, fill, width=4, dash=18, gap=12):
    x0, y0, x1, y1 = xy
    length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    if length == 0:
        return
    dx, dy = (x1 - x0) / length, (y1 - y0) / length
    pos = 0
    while pos < length:
        end = min(pos + dash, length)
        draw.line((x0 + dx * pos, y0 + dy * pos, x0 + dx * end, y0 + dy * end), fill=fill, width=width)
        pos += dash + gap


def fit_text(draw, text, box, font_obj, fill=INK, line_gap=8):
    x, y, w, h = box
    lines = []
    for raw in text.split("\n"):
        current = ""
        for ch in raw:
            test = current + ch
            if draw.textlength(test, font=font_obj) <= w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = ch
        lines.append(current)
    yy = y
    for line in lines:
        draw.text((x, yy), line, font=font_obj, fill=fill)
        yy += font_obj.size + line_gap


def card(draw, box, title, body, number, icon_fn):
    x, y, w, h = box
    draw.rounded_rectangle((x, y, x + w, y + h), radius=28, fill=(255, 255, 255), outline=(34, 30, 34), width=4)
    draw.ellipse((x + 30, y + 30, x + 106, y + 106), fill=PINK)
    draw.text((x + 68, y + 69), str(number), font=f_bold(40), fill="white", anchor="mm")
    icon_fn(draw, x + w - 148, y + 36)
    draw.text((x + 130, y + 40), title, font=f_cn(42), fill=INK)
    fit_text(draw, body, (x + 36, y + 128, w - 72, h - 150), f_cn(31), fill=MUTED, line_gap=10)


def icon_printer(draw, x, y):
    draw.rounded_rectangle((x, y + 44, x + 112, y + 112), radius=10, fill=INK)
    draw.rectangle((x + 20, y, x + 92, y + 48), fill=(255, 255, 255), outline=INK, width=4)
    draw.rectangle((x + 20, y + 78, x + 92, y + 134), fill=(255, 255, 255), outline=INK, width=4)
    draw.ellipse((x + 82, y + 58, x + 94, y + 70), fill=PINK)


def icon_cut(draw, x, y):
    draw.line((x + 15, y + 25, x + 105, y + 115), fill=INK, width=9)
    draw.line((x + 105, y + 25, x + 15, y + 115), fill=INK, width=9)
    draw.ellipse((x, y, x + 48, y + 48), outline=INK, width=8)
    draw.ellipse((x + 72, y, x + 120, y + 48), outline=INK, width=8)
    draw.line((x + 18, y + 118, x + 108, y + 118), fill=PINK, width=7)


def icon_fold(draw, x, y):
    draw.polygon([(x + 10, y + 10), (x + 105, y + 10), (x + 105, y + 125), (x + 10, y + 125)], fill=(255, 255, 255), outline=INK)
    dashed_line(draw, (x + 58, y + 18, x + 58, y + 117), BLUE, width=5, dash=14, gap=9)
    draw.polygon([(x + 58, y + 10), (x + 105, y + 52), (x + 105, y + 125), (x + 58, y + 117)], fill=(255, 223, 239), outline=INK)


def icon_glue(draw, x, y):
    draw.rounded_rectangle((x + 35, y + 20, x + 88, y + 118), radius=10, fill=(255, 255, 255), outline=INK, width=5)
    draw.rectangle((x + 43, y + 5, x + 80, y + 28), fill=PINK, outline=INK, width=4)
    draw.text((x + 62, y + 69), "膠", font=f_cn(32), fill=INK, anchor="mm")


def icon_ticket(draw, x, y):
    draw.rounded_rectangle((x + 5, y + 35, x + 125, y + 105), radius=12, fill=PINK, outline=INK, width=5)
    draw.ellipse((x - 10, y + 60, x + 18, y + 88), fill="white", outline=INK, width=4)
    draw.ellipse((x + 112, y + 60, x + 140, y + 88), fill="white", outline=INK, width=4)
    draw.text((x + 65, y + 72), "TICKET", font=f_bold(20), fill="white", anchor="mm")


def icon_export(draw, x, y):
    draw.rectangle((x + 20, y + 10, x + 105, y + 120), fill=(255, 255, 255), outline=INK, width=5)
    draw.polygon([(x + 82, y + 10), (x + 105, y + 33), (x + 82, y + 33)], fill=GRAY, outline=INK)
    draw.line((x + 62, y + 50, x + 62, y + 98), fill=PINK, width=8)
    draw.polygon([(x + 38, y + 75), (x + 62, y + 102), (x + 86, y + 75)], fill=PINK)


def draw_mini_dieline(draw, x, y, scale=1.0):
    pts = [
        (x + 80 * scale, y), (x + 520 * scale, y), (x + 520 * scale, y + 70 * scale),
        (x + 585 * scale, y + 80 * scale), (x + 585 * scale, y + 180 * scale),
        (x + 520 * scale, y + 190 * scale), (x + 520 * scale, y + 380 * scale),
        (x + 80 * scale, y + 380 * scale), (x + 80 * scale, y + 190 * scale),
        (x + 15 * scale, y + 180 * scale), (x + 15 * scale, y + 80 * scale),
        (x + 80 * scale, y + 70 * scale), (x + 80 * scale, y)
    ]
    draw.line(pts, fill=PINK, width=max(3, int(5 * scale)), joint="curve")
    dashed_line(draw, (x + 80 * scale, y + 70 * scale, x + 520 * scale, y + 70 * scale), BLUE, width=max(2, int(4 * scale)))
    dashed_line(draw, (x + 80 * scale, y + 190 * scale, x + 520 * scale, y + 190 * scale), BLUE, width=max(2, int(4 * scale)))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    for yy in range(0, H, 145):
        for xx in range(0, W, 145):
            if (xx // 145 + yy // 145) % 2 == 0:
                draw.rectangle((xx, yy, xx + 145, yy + 145), fill=(255, 235, 247))
    for i in range(-300, W, 155):
        draw.line((i, H, i + 1200, 0), fill=(255, 197, 220), width=5)

    draw.rectangle((0, 0, W, 265), fill=INK)
    draw.text((90, 78), "LiSA 票夾：列印與製作圖解", font=f_cn(72), fill="white")
    draw.text((92, 178), "A4 橫式列印｜沿刀模裁切｜虛線對折｜側翼黏合", font=f_cn(38), fill=(255, 210, 232))
    draw.rounded_rectangle((1390, 76, 1698, 182), radius=52, fill=PINK)
    draw.text((1544, 129), "PRINT GUIDE", font=font(FONT_COND, 48), fill="white", anchor="mm")

    preview = Image.open(PREVIEW).convert("RGB")
    preview.thumbnail((720, 510), Image.Resampling.LANCZOS)
    px, py = 80, 345
    draw.rounded_rectangle((px - 18, py - 18, px + preview.width + 18, py + preview.height + 18), radius=28, fill="white", outline=INK, width=5)
    img.paste(preview, (px, py))
    draw.text((850, 345), "列印組裝步驟", font=f_cn(62), fill=INK)
    draw.text((850, 430), "給拿到 PDF 的人看：照這 5 步做就能完成票夾。", font=f_cn(36), fill=MUTED)
    draw_mini_dieline(draw, 890, 550, 1.2)
    draw.text((900, 1035), "線條說明", font=f_cn(40), fill=INK)
    draw.line((900, 1110, 1130, 1110), fill=PINK, width=7)
    draw.text((1160, 1088), "洋紅實線：裁切", font=f_cn(33), fill=INK)
    dashed_line(draw, (900, 1175, 1130, 1175), BLUE, width=6)
    draw.text((1160, 1152), "藍色虛線：對折", font=f_cn(33), fill=INK)

    start_y = 1290
    gap = 36
    cw, ch = 520, 290
    cards = [
        ("開 PDF 列印", "選擇 assets/ticket.pdf，紙張設為 A4 橫式，比例請用 100% 或實際大小。", icon_printer),
        ("先裁外框", "沿洋紅色實線裁切外輪廓，左右兩片側翼也要保留。", icon_cut),
        ("沿虛線對折", "依藍色虛線折出上下折線，先輕壓定位，再壓平。", icon_fold),
        ("黏左右側翼", "在左右側翼背面上膠，往內貼合成票夾口袋。", icon_glue),
        ("放入票券", "確認開口方向後，把票券放入即可。建議先用普通紙試做一次。", icon_ticket),
        ("完成檢查", "邊緣有沒有翹起、折線是否平整、票券是否能順利抽取。", icon_export),
    ]
    for i, (title, body, icon) in enumerate(cards):
        col = i % 3
        row = i // 3
        card(draw, (80 + col * (cw + gap), start_y + row * (ch + gap), cw, ch), title, body, i + 1, icon)

    y2 = 2050
    draw.rounded_rectangle((70, y2, W - 70, H - 80), radius=34, fill=(255, 255, 255), outline=INK, width=5)
    draw.rectangle((70, y2, W - 70, y2 + 105), fill=INK)
    draw.text((110, y2 + 54), "設計製作流程", font=f_cn(48), fill="white", anchor="lm")
    steps = [
        ("1 素材", "整理 LiSA 主視覺、活動日期與地點。"),
        ("2 版面", "依票夾模板配置上下兩面與倒置封面。"),
        ("3 刀模", "建立裁切線、折線與安全邊界。"),
        ("4 輸出", "匯出 PDF 列印版、PNG 預覽與 AI 可編輯刀模。"),
    ]
    for i, (title, body) in enumerate(steps):
        x = 120 + i * 410
        y = y2 + 165
        draw.ellipse((x, y, x + 78, y + 78), fill=PINK)
        draw.text((x + 39, y + 39), str(i + 1), font=f_bold(38), fill="white", anchor="mm")
        draw.text((x, y + 110), title, font=f_cn(38), fill=INK)
        fit_text(draw, body, (x, y + 165, 330, 130), f_cn(28), fill=MUTED, line_gap=7)
        if i < 3:
            draw.line((x + 300, y + 40, x + 380, y + 40), fill=PINK, width=8)
            draw.polygon([(x + 380, y + 40), (x + 350, y + 22), (x + 350, y + 58)], fill=PINK)

    draw.text((90, H - 38), "檔案：assets/ticket.pdf｜assets/ticket-holder-dieline.ai｜assets/ticket-holder-lisa.png",
              font=f_cn(27), fill=MUTED, anchor="lm")

    OUT.parent.mkdir(exist_ok=True)
    img.save(OUT, quality=95)
    img.save(OUT_PDF, "PDF", resolution=200.0)
    print(OUT)
    print(OUT_PDF)


if __name__ == "__main__":
    main()
