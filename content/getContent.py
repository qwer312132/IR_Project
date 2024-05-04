from google_play_scraper import app, reviews
import json
def remove_prefix_and_suffix(string):
    prefix = "https://app.sensortower.com/overview/"
    suffix = "?country=TW"
    return string[len(prefix):-len(suffix)]
    
f = open('url.txt', 'r')
gameId = []
for line in f:
    gameId.append(remove_prefix_and_suffix(line.strip()))
f.close()
gameId = list(set(gameId))
# print(len(gameId))
# exit()
data = []
review_count = 100
for ID in gameId:
    # print(ID)
    game_data = {}
    app_info = app(ID, lang='zh_TW', country='TW')
    game_data['ID'] = ID
    game_data['title'] = app_info['title']
    game_data["description"] = app_info["description"]
    data.append(game_data)
# print(data)
with open('gameContent.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
