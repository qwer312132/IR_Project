import json

with open("data/dataset1_token.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open('content/gameContent.json', 'r', encoding='utf-8') as file:
  data2 = json.load(file)

import torch
from transformers import BertTokenizer, BertModel
import numpy as np

tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

def bert_embedding(tokenized_documents, max_length=512):
  embedding = []
  for doc in tokenized_documents:
    inputs = tokenizer.convert_tokens_to_ids(doc)
    if len(inputs) > max_length:
      inputs = inputs[:max_length]
    inputs = torch.tensor([inputs])
    #attention_mask = (inputs != tokenizer.pad_token_id).long()
    
    with torch.no_grad():
      outputs = model(input_ids=inputs)
      #outputs = model(input_ids=inputs, attention_mask=attention_mask)

    embedding.append(outputs.last_hidden_state.mean(dim=1).squeeze().numpy())
  return np.vstack(embedding)

embeddings = bert_embedding(data)

from sklearn.cluster import AgglomerativeClustering
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

n_clusters_list = [21, 42, 84, 168, 336, 672, 1345]
correct_counts_list = []

for n_clusters in n_clusters_list:
    agg_clustering = AgglomerativeClustering(n_clusters=n_clusters)
    clusters = agg_clustering.fit_predict(embeddings)

    for k in range(0, n_clusters):
        cluster_indices = np.where(clusters == k)[0]
        for i in cluster_indices:
            data2[i]["cluster_id"]=k
    
    with open('content/gameContent.json', 'w', encoding='utf-8') as file:
        json.dump(data2, file, indent=4, ensure_ascii=False)

    genre_total_count = Counter()
    cluster_genre_count = defaultdict(Counter)

    for item in data2:
        genre = item['genre']
        cluster_id = item['cluster_id']
        cluster_genre_count[cluster_id][genre] += 1
        genre_total_count[genre] += 1

    cluster_info = []
    for cluster_id in sorted(cluster_genre_count.keys()):
        genre_counter = cluster_genre_count[cluster_id]
        most_common_genre, most_common_count = genre_counter.most_common(1)[0]
        total_predicted_count = sum(genre_counter.values())
        total_genre_count = genre_total_count[most_common_genre]
        cluster_info.append({
            'cluster_id': cluster_id,
            'predicted_genre': most_common_genre,
            'predicted_count': total_predicted_count,
            'actual_count': total_genre_count,
            'genre_counter': genre_counter
        })

    # 總和相同genre的cluster_id
    genre_cluster_mapping = defaultdict(lambda: {"clusters": set(), "predicted_count": 0, "actual_count": 0})
    for info in cluster_info:
        genre = info['predicted_genre']
        genre_cluster_mapping[genre]["clusters"].add(info['cluster_id'])
        genre_cluster_mapping[genre]["predicted_count"] += info['predicted_count']
        genre_cluster_mapping[genre]["actual_count"] = info['actual_count']

    # 判斷分群結果
    correct_counts = defaultdict(int)
    incorrect_counts = defaultdict(int)

    for genre, data in genre_cluster_mapping.items():
        actual_genre = data['actual_count']
        predicted_genre = data['predicted_count']
        
        for cluster_id in data['clusters']:
            for entry in data2:
                if entry['cluster_id'] == cluster_id:
                    if entry['genre'] == genre:
                        correct_counts[genre] += 1
                    else:
                        incorrect_counts[genre] += 1

    total_correct = sum(correct_counts.values())
    correct_counts_list.append(total_correct)
    print(f"分成{n_clusters}群，總共{len(data2)}個, 正確{total_correct}個, 錯誤{sum(incorrect_counts.values())}個")

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(10, 6))
plt.plot(n_clusters_list, correct_counts_list, marker='o')
plt.xlabel('分群數')
plt.ylabel('正確資料數')
plt.title('分群數 vs 正確資料數')
plt.grid(True)
plt.savefig("fun1(1).jpg")
plt.show() 