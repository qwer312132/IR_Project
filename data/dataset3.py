import json

with open('comments.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

new_data = []
for comment in data:
    if comment['ad'] == 0:
        new_data.append(comment)

old_cnt = len(data)
new_cnt = len(new_data)
print("原本有{}筆留言，刪去廣告留言後，剩下{}筆".format(old_cnt, new_cnt))  # 9332, 9078

#print(new_data[2269]['comment'])
#print(new_data[4539]['comment'])
#print(new_data[6808]['comment'])
#print(new_data[9077]['comment'])

# 存入新的檔案
with open('data/dataset3.json', 'w', encoding='utf-8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=4)
