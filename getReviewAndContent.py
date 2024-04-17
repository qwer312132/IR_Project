from google_play_scraper import app, reviews
import json
f = open('topgrossing.txt', 'r')
gameId = []
for line in f:
    gameId.append(line.strip())
# print(len(gameId))
f.close()
# store in json file
data = []
review_count = 100
for ID in gameId:
    # print(ID)
    game_data = {}
    app_info = app(ID, lang='zh_TW', country='TW')
    game_data['ID'] = ID
    game_data['title'] = app_info['title']
    game_data["description"] = app_info["description"]
    result, continuation_token = reviews(
        ID,
        lang='zh_TW',
        country='TW',
        count=review_count
    )
    review_list = []
    for review in result:
        review_data = {}
        review_data['userName'] = review['userName']
        review_data['score'] = review['score']
        review_data['content'] = review['content']
        review_list.append(review_data)
    game_data['reviews'] = review_list
    data.append(game_data)
# print(data)
with open('review.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
