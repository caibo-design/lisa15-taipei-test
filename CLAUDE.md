# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Non-official fan resource site for LiSA's LiVE is Smile Always ～15～ ASIA TOUR Taipei show (2026/06/19, 17:30 開放入場 / 19:00 開演 UTC+8 at Taipei Arena). Made by @caibo_design. Target audience: fans linking in from LINE groups and Instagram — mobile-first.

## Running the site

No build system. Open `index.html` directly in a browser, or serve with any static server:

```
python3 -m http.server 8000
# then open http://localhost:8000
```

## File structure

```
index.html          — main single-page site (all sections in one file)
about.html          — planned but not yet created
assets/style.css    — shared stylesheet for all pages
assets/ticket.pdf   — placeholder; final design from @caibo_design pending
素材/               — official visual assets (5 JPG images used in CSS/HTML)
old/                — archived prototype HTMLs, not part of the live site
```

## Design system

Defined as CSS custom properties in `assets/style.css`:

| Variable | Value | Use |
|---|---|---|
| `--pink` | `#ff2f9f` | Primary accent, LiSA official fan color |
| `--pink-dim` | `#c4177a` | Button hover |
| `--black` | `#080708` | Page background |
| `--paper` | `#f4f1ef` | Body text |
| `--red` | `#d8282f` | Decorative accent |
| `--border` | `rgba(255,47,159,0.35)` | Card and component borders |

Fonts loaded from Google Fonts: `Bebas Neue` (headings, numbers, logo) and `Noto Sans TC` (body text).

## Key constraints

- **No iframes** — all YouTube links must use `target="_blank"` button elements with `rel="noopener"`.
- **No singalong feature** — was explicitly excluded from scope.
- **Language**:繁體中文 for all UI text; Japanese song titles preserved as-is.
- **Responsive breakpoints**: mobile-first; 600px (2-col info grid) and 768px (larger padding).
- **Countdown target**: `new Date('2026-06-19T19:00:00+08:00')` — 對齊官方開演時間,do not adjust the timezone.

## Page sections (index.html)

1. `nav` — fixed top bar with anchor links to `#setlist`, `#info`, `#ticket`
2. `.hero` — full-viewport hero using `素材/669036261_…jpg` as background; countdown to concert
3. `#setlist` — three track groups: 主歌單 (18 tracks), 安可 (EN1–EN3), 台北追加確定 (炎 Homura)
4. `#info` — 2×2 info card grid (時間/地點, 應援準備, 票袋, 周邊攻略)
5. `#ticket` — ticket holder download (PDF placeholder)
6. `footer` — @caibo_design credit, IG link, disclaimer

## about.html (not yet built)

Should share `assets/style.css`. Content: site purpose, @caibo_design one-liner intro, portfolio link (TBD), IG link, back-to-home button.
