# IR_Project
## 功能
1. 遊戲內容分群
    - 資料集: data\preprocess.json (統計資料: data\check_preprocess.json)
    - 根據google play的"關於這個遊戲"的內容做分群
    - 解決只能使用遊戲名稱搜尋的問題，可以改使用遊戲內容的詞搜尋
    - 分群的問題: 分群分法多種，可能會有多個小群
        - 目前解法: 遊戲有4個種類，每個種類有20-40種遊戲，每個種類再做分群，共4個分群系統
2. 過濾廣告留言 for 天堂M
    - 資料集: data\preprocess2.json
    - 人工標籤: 開發者的回覆
    - 機器學習: 遊戲名稱、遊戲簡介、留言、標籤(是否為廣告)
3. 留言分類
    - 資料集: data\preprocess2.json
    - 對留言進行句子分類
    - 還沒做人工標籤
    - 斷句系統
4. 留言分群
    - 資料集: data\preprocess.json (統計資料: data\check_preprocess.json)
    - 留言做重點分群，類似google map評論
    - 分群的問題: 分群分法多種，可能會有多個小群
        - 目前解法: 遊戲有4個種類，每個種類有20-40種遊戲，每個種類再做分群，共4個分群系統

## 資料集
1. for 14: dataset.py -> dataset.json, check_dataset.json -> preprocess.py -> preprocess.json, check_preprocess.json
    - 4個領域, 106個遊戲, 9263則留言
2. for 23: gamecomment.py -> gamecomment.json -> preprocess2.py -> preprocess2.json
    - 9332則留言，開發者回復6229則留言