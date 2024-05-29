from transformers import BertTokenizer, BertModel
import json
import numpy as np
import re
import torch
with open('data/dataset3_token2.json', "r", encoding="utf-8") as f:
    comment_token = json.load(f)
with open('data/stopword.txt', "r", encoding="utf-8") as f:
    stopword = []
    for line in f:
        stopword.append(line.strip())
punctuation_pattern = re.compile(r'^[\W\s_]+$', re.UNICODE)
for i, tokens in enumerate(comment_token):
	comment_token[i] = [token for token in tokens if not punctuation_pattern.match(token)]
comment_token = [[word for word in tokens if word not in stopword] for tokens in comment_token]
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
embeddings = []
for tokens in comment_token:
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_ids = torch.tensor([input_ids])
    with torch.no_grad():
        outputs = model(input_ids)
        token_embeddings = outputs.last_hidden_state.squeeze(0).numpy()
    embeddings.append(token_embeddings.mean(axis=0))
embeddings = np.array(embeddings)
np.save('data/comment_embeddings.npy', embeddings)