import json
import math
import re
cluster_num = 50
with open('data/sentence_without_stopword.json', "r", encoding="utf-8") as f:
    data = json.load(f)
with open('data/dataset3_sentence_break_token.json', "r", encoding="utf-8") as f:
    tokens_list = json.load(f)
with open('data/dataset3_gmm.json', "r", encoding="utf-8") as f:
    cluster = json.load(f)
with open('data/stopword.txt', "r", encoding="utf-8") as f:
    stopword = []
    for line in f:
        stopword.append(line.strip())
punctuation_pattern = re.compile(r'^[\W\s_]+$', re.UNICODE)
for i, tokens in enumerate(tokens_list):
    tokens_list[i] = [token for token in tokens if not punctuation_pattern.match(token)]
tokens_list = [[word for word in tokens if word not in stopword] for tokens in tokens_list]
temp_tokens_list = []
for i, tokens in enumerate(tokens_list):
    if len(tokens) > 0:
        temp_tokens_list.append(tokens)
tokens_list = temp_tokens_list

group = [[]for i in range(cluster_num)]
for i, tokens in enumerate(tokens_list):
    group[cluster[i]].append(tokens)
comments_of_cluster=[[]for i in range(cluster_num)]
for i, group_id in enumerate(cluster):
    comments_of_cluster[group_id].append(data[i])
#calculate df of each word in each cluster
cluster_df = []
for cluster_comments in group:
    df = {}
    for tokens in cluster_comments:
        for word in set(tokens):
            df[word] = df.get(word, 0) + 1
    cluster_df.append(df)
top_5_words = []
for i, cluster_comments in enumerate(group):
    df = cluster_df[i]
    top5 = sorted(df.items(), key=lambda x: x[1], reverse=True)[:5]
    words = [word for word, value in top5]
    top_5_words.append(words)
preview = []
for i, cluster_comments in enumerate(group):
    preview.append({"df": top_5_words[i], "comments": comments_of_cluster[i]})
with open('data/dataset3_df_sentence.json', "w", encoding="utf-8") as f:
    json.dump(preview, f, ensure_ascii=False, indent=4)