import json
import re
with open('data/dataset3.json', "r", encoding="utf-8") as f:
    data = json.load(f)
comments = [d['comment'] for d in data]
# comments = [d['comment'] for d in data[:10]]
# comments = ["qwer qwer ..","wqwer，，qeer。"]
punctuation = r"。！？；，、.!?;,…"
whitespace = r"\s"
sentence_break = []
for comment in comments:
    start = 0
    for i, char in enumerate(comment):
        if char in punctuation or re.match(whitespace, char):
            sentence_break.append(comment[start:i+1])
            start = i+1
    if start < len(comment):
        sentence_break.append(comment[start:])
# exit()
output = []
for sentence in sentence_break:
    if sentence[-1] in punctuation or re.match(whitespace, sentence[-1]):
        sentence = sentence[:-1]
    if len(sentence) > 0:
        output.append(sentence)
# print(output)
# exit()
with open('data/dataset3_sentence_break.json', "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)