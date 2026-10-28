# 重現指南

[回首頁](../README.md) · [模型實作](../scripts/dea.py)

## 安裝與執行

本次驗證使用 Python 3.14、NumPy 2.5.4、SciPy 1.18.1、Matplotlib 3.11.2。`requirements.txt` 鎖定直接相依版本，未宣稱所有作業系統與 Python 版本均已驗證。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/reproduce.py --check
python -m unittest discover -s tests -v
python scripts/build_figures.py --check
python scripts/verify_publication.py
```

若要重新產生輸出，移除兩個產生程式的 `--check`：

```bash
python scripts/reproduce.py
python scripts/build_figures.py
```

## 每個檢查在驗證什麼

| 檢查 | 內容 | 沒有驗證的事項 |
|---|---|---|
| reproduce.py --check | 4 種情境共 24 次 LP；既有 JSON；6 個原分數；6 筆 λ；39 列投影；平均數 | 原軟體身分、官方 MLB 資料或合約定義 |
| unittest | 已知前沿、被支配 DMU、單位不變性、VRS 限制、零值與無效輸入 | 樣本代表性或經濟因果性 |
| build_figures.py --check | 依結果重建兩張 SVG 並比對檔案內容 | 圖表以外的原投影片真實性 |
| verify_publication.py | 公開檔案類型、相對連結、24 個情境分數與明顯憑證模式 | 完整第三方權利審查或全面秘密掃描 |

分數與 λ 以原三位小數的 ±0.0005 核對；轉錄投影算術容許 0.0016，模型投影容許 0.002，涵蓋來源各欄位的四捨五入。JSON 重新計算的數值容許差異為 1e-7，圖表為相同依賴環境的確定性文字比對。

`input_slack` 與 `output_slack` 來自求解所得 λ，不代表新增的第二階段鬆弛最佳化。浮點數可能顯示極小負值，應依 1e-7 可行性門檻判讀；不可當成實質負鬆弛。

## 原始檔的界線

公開 CSV 是從 PDF 重建的可核對資料，沒有原軟體專案或歷史程式。重現成功指的是：在明確宣告的 LP 與來源數值下得到相符結果。原 PDF 留在本機，SHA-256 與頁碼在[來源文件](sources.md)；外部讀者可重跑公開資料，但若無原檔便無法自行逐頁核對轉錄。
