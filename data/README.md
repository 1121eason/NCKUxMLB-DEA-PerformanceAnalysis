# 資料字典與來源

[回首頁](../README.md)

本資料集是 2024 年團隊簡報的數值轉錄，並非從官方 MLB API 下載的原始資料。球員屬於報告選取的 Yankees／Dodgers 樣本；球隊欄為報告 2024 年情境，不表示所有 2023 年表現均發生於該隊。

## players.csv

一列為一位 DMU，順序與原簡報相同。打擊與薪資定義分別來自 PDF 第 23、25 頁；投影薪資依第 36 頁補充；效率、被參照次數與名次來自第 33 頁。

| 欄位 | 含義 | 單位／處理 |
|---|---|---|
| dmu_id | 原報告球員順序 | 1–6；非名次 |
| player / team_2024 | 球員／報告所示球隊 | 名稱僅供辨識 |
| runs / hits | 得分／安打 | 2023 年計數 |
| doubles / triples / home_runs | 二壘打／三壘打／全壘打 | 2023 年計數 |
| rbi / walks / stolen_bases | 打點／四壞／盜壘 | 2023 年計數；零值保留 |
| avg / obp / slg / ops | 打擊率／上壘率／長打率／攻擊指數 | 原表小數值，未再推算分母 |
| salary_label_usd | 摘要顯示薪資 | 名目美元；40M 等轉為整數 |
| salary_projection_usd | 重建用薪資 | 投影表精度；Betts 為 30,416,667，其餘與標籤相同 |
| reported_score | 原報告徑向效率 | 三位小數精度 |
| reported_peer_count | 原表被參照次數 | 不含自身；不是指標權重 |
| reported_rank | 原表列出的名次 | 排序方法未明，不能當作已重建超效率結果 |

## reported_peers.csv

`target_dmu` 與 `peer_dmu` 為上述 DMU ID；`reported_lambda` 為原表標竿組合係數。CCR 係數不必合計為 1。只轉錄三位非前沿球員的六筆非零係數；對角線自我參照未重複收錄。

## projections.csv

39 列：3 位非前沿球員各有 1 項薪資與 12 項打擊指標。`original + radial_movement + slack_movement ≈ projected`。金額以美元、打擊值以原單位表示。第 36 頁為完整三位球員表。

原始行動建議與數值投影需分開理解：負的打擊投入移動是原模型的數學輸出，不代表實際要求球員減少產出。

## 結果資料

[reconstruction.json](../results/reconstruction.json) 保存四種情境的分數、λ、原單位鬆弛、數值可行性違反量、來源誤差與平均數。`scale_efficiency_extension` 來自本次 CCR／BCC 的比值；對此資料的經濟解釋受比率指標與樣本限制。

本資料不包含球員照片、私人聯絡資訊或完整簡報。原檔 SHA-256 與來源說明見[來源清單](../docs/sources.md)。
