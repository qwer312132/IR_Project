import json
from collections import defaultdict

def check(file_name):
    total = defaultdict(list)       # {genre: [{games_name: review_cnt}]}
    statistics = []

    with open(file_name, "r", encoding="utf-8") as file:
        data = json.load(file)

    for game in data:
        genre = game["Genre"]
        title = game["Title"]
        reviews_count = len(game["Reviews"])
        total[genre].append({"Title": title, "Reviews": reviews_count})

    for genre, games in total.items():
        total_reviews = sum(game["Reviews"] for game in games)
        statistics.append({
            "Genre": genre,                     # 策略名稱
            "GameCount": len(games),            # 該策略的遊戲個數
            "TotalReviews": total_reviews,      # 該策略的所有遊戲的所有留言個數
            "Games": [{"Title": game["Title"], "Reviews": game["Reviews"]} for game in games]   # 遊戲名稱: 該遊戲留言數
        })

    with open(f"check_{file_name}", "w", encoding="utf-8") as file:
        json.dump(statistics, file, ensure_ascii=False, indent=4)
