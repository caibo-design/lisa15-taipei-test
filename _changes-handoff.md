# 變更摘要 — 開場時間 + Checklist 修正

依據 ticketplus / 台北小巨蛋官網查到的官方資訊:
- **2026/06/19(五)** 17:30 開放入場、**19:00 開演**、預計 21:30 結束
- **實名制驗票**:紙本票券 + 身分證正本,**不收**截圖/影本

---

## index.html

### ① Hero 開演時間文字

```html
<!-- before -->
<div class="date">2026.06.19 FRI — 18:00 START</div>

<!-- after -->
<div class="date">2026.06.19 FRI — 19:00 START</div>
```

### ② 倒數計時 target

```js
// before
const targetTime = new Date("2026-06-19T18:00:00+08:00").getTime();

// after
const targetTime = new Date("2026-06-19T19:00:00+08:00").getTime();
```

### ③ Google Calendar 事件

`addToCalendar()` 函式內:

```js
// before
+ '&dates=20260619T100000Z/20260619T130000Z'
+ '&details=' + encodeURIComponent('Taipei Arena 台北小巨蛋\n18:00 開演,建議 17:00 前入場\n官方應援色:粉紅色')

// after
+ '&dates=20260619T110000Z/20260619T133000Z'
+ '&details=' + encodeURIComponent('Taipei Arena 台北小巨蛋\n17:30 開放入場,19:00 開演\n實名制驗票:紙本票券 + 身分證正本\n官方應援色:粉紅色')
```

> UTC 換算:19:00 UTC+8 = 11:00Z,21:30 UTC+8 = 13:30Z

### ④ Checklist 第 1、2 項 (重要修正)

`#checklist` 區塊內:

```html
<!-- before -->
<label class="check">
  <input type="checkbox">
  <span class="box" aria-hidden="true"></span>
  <span><strong>票券帶好</strong><span>先截圖或加入錢包,入口不要慌。</span></span>
</label>
<label class="check">
  <input type="checkbox">
  <span class="box" aria-hidden="true"></span>
  <span><strong>手機靜音</strong><span>開演前先調整,現場更沉浸。</span></span>
</label>

<!-- after -->
<label class="check">
  <input type="checkbox">
  <span class="box" aria-hidden="true"></span>
  <span><strong>票證合一</strong><span>紙本票券 + 身分證正本,實名制不收截圖影本。</span></span>
</label>
<label class="check">
  <input type="checkbox">
  <span class="box" aria-hidden="true"></span>
  <span><strong>提早抵達</strong><span>17:30 開放入場、19:00 開演,建議 17:00 到場。</span></span>
</label>
```

> ⚠️ 第 1 項原本寫「截圖即可」是**錯誤資訊**,實名制必須帶紙本+證件正本,務必修正。

---

## CLAUDE.md

### ⑤ Project overview 時間

```md
<!-- before -->
... LiSA's LiVE is Smile Always ～15～ ASIA TOUR Taipei show (2026/06/19 18:00 UTC+8 at Taipei Arena). ...

<!-- after -->
... LiSA's LiVE is Smile Always ～15～ ASIA TOUR Taipei show (2026/06/19, 17:30 開放入場 / 19:00 開演 UTC+8 at Taipei Arena). ...
```

### ⑥ Countdown target 註記

```md
<!-- before -->
- **Countdown target**: `new Date('2026-06-19T18:00:00+08:00')` — do not adjust the timezone.

<!-- after -->
- **Countdown target**: `new Date('2026-06-19T19:00:00+08:00')` — 對齊官方開演時間,do not adjust the timezone.
```

---

## 資料來源
- 台北小巨蛋官網: https://www.arena.taipei/News_Content.aspx?n=2E1489AFE4B1BEA1
- Trip.com 整理: https://tw.trip.com/blog/lisa-concert-tw/
- Ticket Plus 活動頁: https://ticketplus.com.tw/activity/c42d8d28d858c5ac4efa54360dbaf4db
