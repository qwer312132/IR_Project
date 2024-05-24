import json
from transformers import BertTokenizer, BertModel
import torch
from sklearn.mixture import GaussianMixture
import re
with open('data/dataset3_token.json', "r", encoding="utf-8") as f:
    data = json.load(f)
with open('data/stopword.txt', "r", encoding="utf-8") as f:
    stopword = []
    for line in f:
        stopword.append(line.strip())
tokens_list = []
for item in data:
    tokens_list.append(item)
#preprocess
punctuation_pattern = re.compile(r'^[\W\s_]+$', re.UNICODE)
for i, tokens in enumerate(tokens_list):
	tokens_list[i] = [token for token in tokens if not punctuation_pattern.match(token)]
tokens_list = [[word for word in tokens if word not in stopword] for tokens in tokens_list]
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
embeddings = []
for tokens in tokens_list:
	input_ids = tokenizer.convert_tokens_to_ids(tokens)
	input_ids = torch.tensor([input_ids])
	with torch.no_grad():
		outputs = model(input_ids)
		token_embeddings = outputs.last_hidden_state.squeeze(0).numpy()
	embeddings.append(token_embeddings.mean(axis=0))
gmm = GaussianMixture(n_components=10, random_state=0)
clusters = gmm.fit_predict(embeddings)
with open('data/dataset3_gmm.json', "w", encoding="utf-8") as f:
	json.dump(clusters.tolist(), f)