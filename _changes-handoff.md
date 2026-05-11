# 變更摘要 — 開場時間 + Checklist 修正

依據 ticketplus / 台北小巨蛋官網查到的官方資訊:
- **2026/06/19(五)** 17:30 開放入場、**19:00 開演**、預計 21:30 結束
- **實名制驗票**:紙本票券 + 身分證正本,**不收**截圖/影本

---

## 演唱會官方資訊

### 基本資訊
- **演出名稱**:LiVE is Smile Always～15～ in Taipei
- **巡演**:LiSA Asia Tour 2026(出道 15 週年亞洲巡迴)
- **場地**:台北小巨蛋 Taipei Arena
- **地址**:台北市松山區南京東路四段 2 號
- **主辦單位**:好玩國際文化
- **售票系統**:Ticket Plus 遠大售票系統
- **客服專線**:(02) 2778-1570(週一~五 10:00–18:00,國定假日除外)

### 場次時間
| 日期 | 入場 | 開演 | 預計結束 |
|---|---|---|---|
| 2026/06/19(五) | 17:30 | **19:00** | ~21:30 |
| 2026/06/20(六) | 15:30 | **17:00** | ~19:30 |

> 本網站聚焦 **6/19(五)** 場次。

### 票價(共 6 種,均為座席)
NT$ 5,280 / 4,880 / 4,280 / 3,880 / 2,880 / 800

### 抽選 / 購票流程(已過期,留作紀錄)
- 登記期間:2026/02/05(四) 12:00 ~ 02/08(日) 19:00
- 中選公布:2026/02/10 12:00(email + 簡訊 + 我的訂單)
- 繳費期限:2026/02/11(三) 12:00 前(逾期視同放棄)
- 每會員每場最多 2 張,每證件號碼每場限 1 張
- 座位電腦隨機配位,不可指定/更換

### 取票方式
- **ibon(7-11)**:6/12(五) 09:00 起至各場次當日 22:00
- 手續費 NT$30/筆,單筆限 2 張
- 流程:售票系統 → Ticket Plus → 取票 → 輸入手機號碼 + 取票號碼 → 列印繳費單 → 至櫃檯付款取票
- 海外手機需加國碼(如日本 +81)

### 入場規定(實名制)
**需出示「紙本票券」+「證件正本」,二者缺一不可,不接受影本/截圖**
- 本國籍:身分證、駕照、健保卡(三選一)
- 外籍人士:護照正本
- 照片需與本人相符,差異過大可能被拒入場
- 生僻字無法印出時,由主辦現場判定

### 場館特殊規定
- 身高 **110 cm 以下禁止進入 3 樓**(安全考量)
- **2、3 樓觀眾禁止站立跳躍 / 踩踏樓梯**,改以揮手或鼓掌應援

### 禁止攜帶物品
- 外食、未密封飲料、寶特瓶
- 任何金屬或玻璃容器
- 雷射筆、煙火、爆裂物
- 煙具、危險物品
- 違規者將被沒收並拒絕入場

### 應援物參考(無官方明文禁止)
- 手燈、手幅、毛巾、應援小物均可
- 避免大型或具尖銳金屬構件之物品
- 揮舞時注意不擋到後排視線

### 交通資訊
- **捷運**:松山新店線(綠線)→「台北小巨蛋」站 **2 號出口**直達
- **YouBike**:臺北田徑場站(敦化北路)、社教館站(八德路)
- **公車**:33、262、275、277、556、630、672、688、902、903、905、敦化幹線、南京幹線等多線
- **自行開車**:小巨蛋地下停車場(汽車入口在敦化北路,平日 NT$40/hr、假日 NT$60/hr)

### 行李寄存(計時收費櫃)
| 位置 | 尺寸(W×D×H) | 費率 | 數量 |
|---|---|---|---|
| 9 號出入口 | 39×57×31 cm | $10/hr | 40 格 |
| 9 號出入口 | 39×57×84 cm | $20/hr | 15 格 |
| 9 號出入口 | 100×76×79 cm | $30/hr | 6 格 |
| 西側廁所旁 | 39×57×31 cm | $10/hr | 30 格 |
| 西側廁所旁 | 39×57×84 cm | $20/hr | 12 格 |

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
