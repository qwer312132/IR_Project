import json

with open('preprocess2.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)

train_data = []
test_data = []

for review in dataset:
    if review['reply'] != 'None':
        review['ad'] = 0
        train_data.append(review)
    else:
        test_data.append(review)

with open('train.json', 'w', encoding='utf-8') as train_file:
    json.dump(train_data, train_file, ensure_ascii=False, indent=4)

with open('test.json', 'w', encoding='utf-8') as test_file:
    json.dump(test_data, test_file, ensure_ascii=False, indent=4)
