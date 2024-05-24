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
#calculate idf
N = len(cluster)
idf = {}
all_words = set([word for tokens in tokens_list for word in tokens])
for word in all_words:
    df = sum([1 for tokens in tokens_list if word in tokens])
    idf[word] = math.log(N / df, 10)
#calculate tfidf
tfidf = []
for cluster_comments in group:
    merged_comments = [word for tokens in cluster_comments for word in tokens]
    tf = {}
    for word in merged_comments:
        tf[word] = tf.get(word, 0) + 1
    for word in tf:
        tf[word] = math.log(tf[word] + 1, 10)
    tfidf.append({word: tf[word] * idf[word] for word in tf})
preview = []
#output the top 10 tfidf words of each cluster and their tfidf values
for i, cluster_comments in enumerate(group):
    tfidf_cluster = tfidf[i]
    top5 = sorted(tfidf_cluster.items(), key=lambda x: x[1], reverse=True)[:5]
    words_and_values = {word: tfidf_cluster[word] for word, value in top5}
    preview.append({"words": words_and_values, "comments": comments_of_cluster[i]})
with open('data/dataset3_tfidf_preview3.json', "w", encoding="utf-8") as f:
    json.dump(preview, f, ensure_ascii=False, indent=4)
#output all tfidf values which is sorted of each cluster
all = []
for i, cluster_comments in enumerate(group):
    tfidf_cluster = tfidf[i]
    sorted_tfidf = sorted(tfidf_cluster.items(), key=lambda x: x[1], reverse=True)
    words_and_values = {word: tfidf_cluster[word] for word, value in sorted_tfidf}
    all.append({"words": words_and_values, "comments": comments_of_cluster[i]})
with open('data/dataset3_tfidf_all.json', "w", encoding="utf-8") as f:
    json.dump(all, f, ensure_ascii=False, indent=4)