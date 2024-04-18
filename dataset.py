# 如果要重新下載dataset，要接著跑check.py，更新統計數目
import json
from google_play_scraper import search, app, reviews

search_queries = ["策略", "角色扮演", "動作", "賽車遊戲"]       # 輸入搜尋欄
min_reviews = 120
all_games = []

for query in search_queries:
    search_results = search(query, lang='zh_TW', country='TW', n_hits=50)
    for game in search_results:
        if game["genre"] in search_queries:     # 條件1: 遊戲種類必須是"策略","角色扮演","動作","賽車遊戲"
            app_id = game['appId']                              # 遊戲ID
            game_info = app(app_id, lang='zh_TW', country='TW')                                         # 獲得遊戲資料
            result, continuation_token = reviews(app_id, lang='zh_TW', country='TW', count=min_reviews) # 獲得遊戲留言
            
            if len(result) >= min_reviews:      # 條件2: 遊戲的留言數需要至少120筆
                title = game_info["title"]                      # 遊戲名稱
                genre = game_info["genre"]                      # 遊戲類別
                description = game_info["description"]          # 遊戲簡介
                score = game_info["score"]                      # 遊戲分數

                reviews_list = []
                for review in result:
                    userName = review["userName"]               # 用戶名稱
                    content = review["content"]                 # 留言內容
                    score = review["score"]                     # 用戶評分
                    at = str(review["at"])                      # 留言時間
                    replyContent = review["replyContent"]       # 開發商回覆內容
                    replyAt = str(review["repliedAt"])          # 開發商回覆時間

                    reviews_list.append({
                        "UserName": userName,
                        "Content": content,
                        "Userscore": score,
                        "At": at,
                        "ReplyContent": replyContent,
                        "ReplyAt": replyAt
                    })

                all_games.append({
                    "ID": app_id,
                    "Title": title,
                    "Genre": genre,
                    "Description": description,
                    "Score": score,
                    "Reviews": reviews_list
                })

with open("dataset.json", "w", encoding="utf-8") as file:
    json.dump(all_games, file, ensure_ascii=False, indent=4)

