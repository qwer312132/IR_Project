import json
import math
with open('data/dataset3.json', "r", encoding="utf-8") as f:
    data = json.load(f)
with open('data/dataset3_token2.json', "r", encoding="utf-8") as f:
    tokens_list = json.load(f)
with open('data/dataset3_gmm.json', "r", encoding="utf-8") as f:
    cluster = json.load(f)
with open('data/stopword.txt', "r", encoding="utf-8") as f:
    stopword = []
    for line in f:
        stopword.append(line.strip())
#remove stopword
tokens_list = [[word for word in tokens if word not in stopword] for tokens in tokens_list]
group = [[]for i in range(10)]
for i, tokens in enumerate(tokens_list):
    group[cluster[i]].append(tokens)
comments_of_cluster=[[]for i in range(10)]
for i, group_id in enumerate(cluster):
    comments_of_cluster[group_id].append(data[i]['comment'])
#calculate df
N = len(cluster)
df_of_cluster = []
for cluster_comments in group:
    merged_comments = [word for tokens in cluster_comments for word in tokens]
    df = {}
    for word in merged_comments:
        df[word] = df.get(word, 0) + 1
    df_of_cluster.append(df)
preview = []
#output the top 5 df words of each cluster and their df values
for i, cluster_comments in enumerate(group):
    df_cluster = df_of_cluster[i]
    top5 = sorted(df_cluster.items(), key=lambda x: x[1], reverse=True)[:5]
    words_and_values = {word: df_cluster[word] for word, value in top5}
    preview.append({"words": words_and_values, "comments": comments_of_cluster[i]})
with open('data/dataset3_df_preview.json', "w", encoding="utf-8") as f:
    json.dump(preview, f, ensure_ascii=False, indent=4)