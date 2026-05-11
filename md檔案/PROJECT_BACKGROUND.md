# LiSA 15th 台北場粉絲資源站 — 專案背景

> 更新日期：2026/05/11  
> 專案位置：`/Users/caipu/Desktop/Lisa15th-taipei`  
> 製作者 / 署名：`@caibo_design`

## 1. 專案定位

這是一個為 LiSA `LiVE is Smile Always ～15～ ASIA TOUR` 台北場製作的非官方粉絲資源站。目標是讓粉絲從 LINE 群組、Instagram、Threads 等社群點進來後，可以快速完成演唱會前的預習與當天準備。

核心用途：

- 整理台北場基本資訊。
- 提供歌單預測與 YouTube 外部連結。
- 彙整入場、交通、應援、周邊與票袋列印提醒。
- 未來提供票袋 PDF 下載。

專案不是官方網站，也不是售票頁；所有內容應維持「粉絲整理給粉絲」的語氣。

## 2. 活動資訊

- 活動名稱：`LiVE is Smile Always ～15～ ASIA TOUR`
- 台北場日期：`2026/06/19`
- 開演時間：`18:00`
- 時區：台北時間 `UTC+8`
- 場地：台北小巨蛋 / Taipei Arena
- 倒數目標：`new Date('2026-06-19T18:00:00+08:00')`

注意：倒數時間已在 `index.html` 寫死為 UTC+8，不要改成瀏覽器所在地時間推算。

## 3. 目標受眾

主要受眾是準備參加台北場的 LiSA 粉絲。多數使用者可能從手機點入，因此目前專案採手機優先設計。

使用情境：

- 演唱會前想快速預習歌單。
- 當天在路上確認開演時間、交通與入場提醒。
- 想下載或列印票袋。
- 想看周邊購買提醒與準備清單。

## 4. 目前專案狀態

這是一個無建置流程的靜態網站。正式入口是 `index.html`，共用樣式放在 `assets/style.css`。

目前沒有 `package.json`、Vite、Next.js 或其他前端框架，也沒有 Git repository 初始化紀錄。

執行方式：

```bash
python3 -m http.server 8000
```

或直接用瀏覽器開啟 `index.html`。

## 5. 檔案結構與角色

```text
.
├── CLAUDE.md
├── PROJECT_BACKGROUND.md
├── index.html
├── assets/
│   └── style.css
├── 素材/
│   ├── 650996790_1455269059296864_7153961107339767219_n.jpg
│   ├── 662910887_1473856544104782_1797694666298698514_n.jpg
│   ├── 667863751_1476061287217641_1401771218230708810_n.jpg
│   ├── 669036261_1476090733881363_773819450042997474_n.jpg
│   └── 678706569_1487002586123511_918994064303536647_n.jpg
├── lisa15th_project_brief.md
├── lisa15th_web_design_proposal.md
├── lisa15th_design_mockup.html
├── lisa15th-desktop-updated.png
├── lisa15th-mobile-updated.png
├── X/
│   ├── lisa15th-desktop.png
│   ├── lisa15th-desktop-updated.png
│   └── lisa15th-mobile.png
└── old/
    ├── lisa_15th_concert_guide.html
    ├── homura_singalong.html
    └── homura_singalong (1).html
```

### 現行正式檔案

- `index.html`：目前正式首頁，單頁式粉絲資源站。
- `assets/style.css`：全站共用 CSS，包含 reset、導覽列、hero、歌單、資訊卡、票袋區、footer 與響應式設定。

### 專案規劃與參考文件

- `CLAUDE.md`：給 AI / 開發者的專案約束與維護說明。
- `lisa15th_project_brief.md`：早期架構文件，定義首頁、about 頁、歌單、注意事項、票袋下載等內容。
- `lisa15th_web_design_proposal.md`：視覺與內容提案，定義「粉紅噪音拼貼 × 15 週年應援基地」方向。
- `lisa15th_design_mockup.html`：較完整的高保真設計稿 / 原型參考，包含周邊區與更完整的視覺拼貼概念。

### 視覺與截圖

- `素材/`：官方視覺與周邊圖片，供網站設計使用。
- `lisa15th-desktop-updated.png`、`lisa15th-mobile-updated.png`：目前視覺驗證截圖。
- `X/`：歷史截圖或備份截圖資料夾。

### 舊版 / 封存

- `old/lisa_15th_concert_guide.html`：早期歌單預習指南。
- `old/homura_singalong.html`、`old/homura_singalong (1).html`：炎 Homura 跟唱練習頁。此功能已明確排除在正式範圍外，不應重新加入主站。

## 6. 現行首頁結構

`index.html` 是單頁式網站，主要區塊如下：

1. `nav`
   - 固定頂部導覽列。
   - 錨點連至 `#setlist`、`#info`、`#ticket`。

2. `.hero`
   - 首屏主視覺。
   - 背景使用 `素材/669036261_1476090733881363_773819450042997474_n.jpg`。
   - 顯示活動名稱、日期、地點、開演時間與倒數。
   - CTA：歌單預習、票袋下載。

3. `#setlist`
   - 歌單預測。
   - 主歌單 18 首。
   - 安可 3 首。
   - 台北追加確定：`炎 Homura`。
   - YouTube 連結皆為外開，不使用 iframe。

4. `#info`
   - 當天注意事項。
   - 四組資訊卡：時間 & 地點、應援準備、票袋、周邊攻略。

5. `#ticket`
   - 票袋下載區。
   - 目前是佔位狀態。
   - 下載連結指向 `assets/ticket.pdf`，但目前專案內尚未看到該 PDF。

6. `footer`
   - `@caibo_design` 署名。
   - Instagram 連結。
   - 資料來源與非官方聲明。
   - 有 `about.html` 連結，但目前專案內尚未看到 `about.html`。

## 7. 設計方向

核心概念來自 `lisa15th_web_design_proposal.md`：

> 粉紅噪音拼貼 × 15 週年應援基地

視覺關鍵字：

- 黑、白、亮粉色高對比。
- 少量紅色作為手寫感點綴。
- 拼貼、撕紙、網點、掃描質感、舞台前興奮感。
- 手機優先，資訊要短、清楚、好掃讀。

目前正式版偏乾淨、輕量，尚未完整套入 mockup 中較豐富的拼貼視覺。

## 8. 設計系統

主要 CSS 變數定義於 `assets/style.css`：

```css
:root {
  --pink: #ff2f9f;
  --pink-dim: #c4177a;
  --black: #080708;
  --dark: #111011;
  --paper: #f4f1ef;
  --red: #d8282f;
  --gray: #888;
  --border: rgba(255, 47, 159, 0.35);
}
```

字體：

- 英文標題 / 數字：`Bebas Neue`
- 中文內文：`Noto Sans TC`
- 字體由 Google Fonts 載入。

UI 特徵：

- 小圓角或直角，避免柔和大圓角。
- 黑底、粉色描邊、粉色 CTA。
- 資訊以卡片與列表呈現。
- 手機優先，`600px` 開始資訊卡變成兩欄，`768px` 增加 padding。

## 9. 素材用途建議

依照設計提案，目前素材可這樣理解：

- `669036261_1476090733881363_773819450042997474_n.jpg`
  - 現行 hero 背景。

- `650996790_1455269059296864_7153961107339767219_n.jpg`
  - 可作為 LACE UP / 專輯視覺相關輔助素材。

- `662910887_1473856544104782_1797694666298698514_n.jpg`
  - 可作為活動資訊、巡迴海報或人物視覺切片。

- `667863751_1476061287217641_1401771218230708810_n.jpg`
  - 可作為中段 highlight 或成就資訊視覺。

- `678706569_1487002586123511_918994064303536647_n.jpg`
  - 官方周邊總覽圖，可用於未來周邊區。

## 10. 內容與功能限制

請維持下列限制：

- 不使用 iframe。
- YouTube 連結用外開連結或按鈕，需包含 `target="_blank"` 與 `rel="noopener"`。
- 不加入跟唱功能。
- 介面文字使用繁體中文。
- 日文歌名保留原文。
- 倒數目標固定為 `2026-06-19T18:00:00+08:00`。
- 本站需清楚標示非官方粉絲網站。

## 11. 已知缺口

目前檔案與連結存在幾個未完成處：

- `about.html` 尚未建立，但 footer 已連結。
- `assets/ticket.pdf` 尚未存在，但票袋下載按鈕已指向該路徑。
- `CLAUDE.md` 提到 `assets/ticket.pdf` 是 placeholder，等待 final design from `@caibo_design`。
- `lisa15th_design_mockup.html` 有比現行首頁更完整的周邊與視覺設計，可作為第二階段改版參考。
- `old/` 裡有跟唱頁，但正式需求明確不包含 singalong。

## 12. 建議下一步

短期 MVP：

- 建立 `about.html`。
- 放入或移除 `assets/ticket.pdf` 下載連結，避免使用者點到不存在檔案。
- 檢查手機版 hero 裁切與文字可讀性。
- 確認所有外部連結可用。

第二階段：

- 將 `lisa15th_design_mockup.html` 的視覺語言整合回正式 `index.html`。
- 補上官方周邊區。
- 加入更完整的票袋預覽。
- 將目前 inline style 移回 `assets/style.css`，讓結構更乾淨。

長期：

- 如果內容持續增加，可考慮拆成 `about.html`、`goods.html` 或資料 JSON。
- 若要持續維護歌單與連結，可把歌曲資料從 HTML 中抽出成結構化資料。

