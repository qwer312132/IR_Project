from google_play_scraper import app
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
data = []
for i in range(len(gameId)):
    ID = gameId[i]
    print(i, ID)
    # print(ID)
    game_data = {}
    try:
        app_info = app(ID, lang='zh_TW', country='TW')
        game_data['ID'] = ID
        game_data['title'] = app_info['title']
        game_data["description"] = app_info["description"]
        game_data["genre"] = app_info["genre"]
        data.append(game_data)
    except:
        continue
# print(data)
print(len(data))
with open('gameContent.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False)
