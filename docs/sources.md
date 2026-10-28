# 來源與頁碼對照

[回首頁](../README.md)

## S1：使用者提供的原始報告

- 原檔名：`第二組_李奕成 劉煒暄 蘇芳誼 潘妍亘 林羿如.pdf`
- PDF 標題：`進階績效管理_期中報告`；封面英文為 Advanced Applied Efficiency Management, Midterm Presentation – Group 2。
- 國立成功大學課程背景由使用者提供的來源目錄辨識。
- 封面共同署名：李奕成、劉煒暄、蘇芳誼、潘妍亘、林羿如。
- 55 頁；PDF 中繼資料建立日期 2024-12-08，非繳交時間或評分證明。
- SHA-256：`630e78dfb85f7357f6581b3b566eea230d611238efba3bf4a7b953dabb886b08`
- 完整 PDF 保留於本機，不公開複製球員照片、新聞圖片及投影片版面。

| PDF 頁碼（1 起算） | 原內容 | 公開版用途 |
|---|---|---|
| 1 | 課程、組別、共同署名 | 來源定位 |
| 2–3 | 討論題、績效與價值 | 個案問題 |
| 5、10–19 | 球員與運動商業關係圖 | 重寫利害關係人分析 |
| 20–22 | 球員與薪資標籤 | DMU 名稱與摘要薪資 |
| 23 | 2023 打擊投入／2024 薪資產出 | 原分析視角 |
| 25 | 六位球員的 12 項打擊值 | players.csv |
| 33 | 分數、λ、被參照次數、名次 | 分數與標竿核對 |
| 34–37，完整表見 36 | 原值、徑向、鬆弛、投影 | projections.csv；Betts 薪資口徑 |
| 40–42 | Stanton 與 Freeman 對照 | 個案的反差敘事 |
| 43–44 | 績效＋商業利益的價值概念 | 管理解讀 |
| 47–51 | 事前／事後價值、長約、風險 | 重寫概念分析，保留推論界線 |

第 7、9、46 頁等商業金額與占比未能從現有材料獨立定位其原始統計來源，故未納入公開分析的量化證據。第 51 頁的長約文獻引文書目資訊不完整；公開版不逐字重製，也不將其當作本樣本的因果證據。

## S2：作者對分工的確認

2026-10-28，作者在本次整理對話中確認整份原報告由本人完成。此說明支援個人貢獻範圍；原 PDF 的共同署名背景另行保留。[貢獻說明](contribution.md)

## 方法及實作的一手來源

1. Charnes, A., Cooper, W. W., & Rhodes, E. (1978). *Measuring the efficiency of decision making units*. European Journal of Operational Research, 2(6), 429–444. [DOI](https://doi.org/10.1016/0377-2217(78)90138-8)。用於 CCR 的多投入多產出相對效率背景。
2. Banker, R. D., Charnes, A., & Cooper, W. W. (1984). *Some Models for Estimating Technical and Scale Inefficiencies in Data Envelopment Analysis*. Management Science, 30(9), 1078–1092. [DOI](https://doi.org/10.1287/mnsc.30.9.1078)。用於 BCC 與技術／規模效率區分。
3. SciPy 官方文件：[linprog(method='highs')](https://docs.scipy.org/doc/scipy/reference/optimize.linprog-highs.html)。用於 LP 介面、限制形式與求解狀態。

方法書目與官方文件於 2026-10-28 查核；出版者搜尋摘要可讀，部分全文端點受存取限制。公開版沒有聲稱完整審閱兩篇方法論文全文。使用者提供的 DEA 一般說明作為需求背景，沒有將部落格內容當成球員資料來源。
