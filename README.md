# IR_Project
## 功能
1. 遊戲內容分群
    - 資料集: content/gameContent.json
    - 2708個遊戲
    - 斷詞、word embedding、clustering
2. 過濾廣告留言 for 天堂M
    - 資料集: comments.json
    - 需補上 斷詞、word embedding、F1-score
3. 留言分類
    - 資料集: data/dataset3.json
    - 原本有9332筆留言，刪去廣告留言後，剩下9078筆
        - 第1部分: 1-2270則留言(2-36320行)(目前標到 遊戲的內容、打怪練功時的細膩度不錯，可是...對於公司那為了錢什麼事都做得出來...實在感到不敢恭維...)
        - 第2部分: 2271-4540則留言(36322-72640行)
        - 第3部分: 4541-6809則留言(72642-108944行)
        - 第4部分: 6810-9078則留言(108946-145249行)
    - 8種標籤: "遊戲場景(事件)"、"遊戲體驗(評價)"、"反應手機設備"、"技術問題"、"外掛問題"、"客服支援"、"支付問題"、"其他"
        - "很會賺錢"、"很燒錢"、"錢錢錢"、"太坑錢了"、"鎖帳號" -> 遊戲體驗(評價)
        - "回憶"、"懷念"、"限制創角" -> 遊戲體驗(評價)
        - "抽到紅娃"-> 遊戲場景(事件)
        - "當機"、"一直閃退是怎樣"、"無法進入遊戲"、"擁擠" -> 技術問題
4. 留言分群
