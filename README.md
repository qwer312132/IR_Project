# IR_Project

[google-play-scraper文件](https://pypi.org/project/google-play-scraper/) ```pip install google-play-scraper```

## 功能
1. 遊戲內容分群
    - 根據google play的"關於這個遊戲"的內容做分群
    - 解決只能使用遊戲名稱搜尋的問題，可以改使用遊戲內容的詞搜尋
    - 分群的問題: 分群分法多種，可能會有多個小群
        - 目前想到解法: 遊戲有4個種類，每個種類有20-40種遊戲，每個種類再做分群，共4個分群系統
2. 過濾廣告留言
    - 刪除廣告留言
    - 人工標籤: 開發者的回覆
    - 機器學習: 遊戲名稱、留言、標籤(是否為廣告)
    - "天堂M"的廣告留言較多，可能只針對該遊戲做功能
        - 需要增加留言數
        - dataset.json可以刪除不必要欄位
3. 留言分類
    - 對留言進行句子分類
    - 還沒做人工標籤
    - 斷句系統
4. 留言分群
    - 留言做重點分群，類似google map評論
    - 分群的問題: 分群分法多種，可能會有多個小群
        - 目前想到解法: 遊戲有4個種類，每個種類有20-40種遊戲，每個種類再做分群，共4個分群系統

## 資料集處理
1. 下載資料 -> dataset.py -> dataset.json
    - 使用google_play_scraper API下載資料
    - 針對"策略", "角色扮演", "動作", "賽車遊戲"4種遊戲種類下載20-40種遊戲，每個遊戲的留言數取120則
    - {遊戲封包名ID、遊戲名稱Title、遊戲類別Genre、遊戲簡介Description、遊戲分數Score、留言Reviews:{用戶名稱UserName、留言內容Content、用戶評分Userscore、留言時間At、開發商回覆內容ReplyContent、開發商回覆時間ReplyAt}}
2. 資料集前處理 -> preprocessing.py -> dataset.json
    - 刪除英文、簡體
    - 判斷語言API https://cloud.google.com/translate/docs/basic/detecting-language?hl=zh-cn
3. 統計最終資料集 -> check.py -> check.json