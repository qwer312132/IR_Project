from utils import check
import json
import re
from zhconv import convert

traditional_chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

with open('dataset.json', 'r', encoding='utf-8') as file:
    dataset = json.load(file)

cleaned_dataset = []
for game in dataset:
    if traditional_chinese_pattern.search(game['Description']):         # 去除非中文簡介後，轉換成繁中
        game['Description'] = convert(game['Description'], 'zh-tw')

        reviews = game['Reviews']
        cleaned_reviews = []

        for review in reviews:
            review_content = review['Content']
            if traditional_chinese_pattern.search(review_content):      # 去除非中文留言後，轉換成繁中
                review['Content'] = convert(review_content, 'zh-tw')
                cleaned_reviews.append(review)
                
        game['Reviews'] = cleaned_reviews
        cleaned_dataset.append(game)

with open('prepocess.json', 'w', encoding='utf-8') as file:
    json.dump(cleaned_dataset, file, ensure_ascii=False, indent=4)

check('prepocess.json')

