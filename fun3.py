import json
from sklearn.model_selection import StratifiedKFold
import re
from transformers import BertTokenizer, BertModel
import torch
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

with open('data/dataset3.json', "r", encoding="utf-8") as f:
    data = json.load(f)
comments = [d['comment'] for d in data]
comment_class = [d['class'] for d in data]
comment_scene = np.array([cc["遊戲場景(事件)"]for cc in comment_class])
comment_experence = np.array([cc["遊戲體驗(評價)"]for cc in comment_class])
comment_device = np.array([cc["反應手機設備"]for cc in comment_class])
comment_technical = np.array([cc["技術問題"]for cc in comment_class])
comment_service = np.array([cc["客服支援"]for cc in comment_class])
comment_payment = np.array([cc["支付問題"]for cc in comment_class])
comment_script = np.array([cc["外掛問題"]for cc in comment_class])
comment_other = np.array([cc["其他"]for cc in comment_class])

#print the number of each class that is not 0
# print("scene:",len([c for c in comment_scene if c!=0]))
# print("experence:",len([c for c in comment_experence if c!=0]))
# print("device:",len([c for c in comment_device if c!=0]))
# print("technical:",len([c for c in comment_technical if c!=0]))
# print("service:",len([c for c in comment_service if c!=0]))
# print("payment:",len([c for c in comment_payment if c!=0]))
# print("script:",len([c for c in comment_script if c!=0]))
# print("other:",len([c for c in comment_other if c!=0]))
# exit()

embeddings = np.load('data/comment_embeddings.npy')
X_train, X_test, y_train, y_test, train_indices, test_indices = train_test_split(embeddings, comment_other, range(len(comments)), test_size=0.2, random_state=42)
num_folds = 5
kfold = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=42)
print("Successfully split data")
train_scores = []
val_scores = []
for fold, (train_index, val_index) in enumerate(kfold.split(X_train, y_train)):
    print(f"Training on fold {fold + 1}/{num_folds}...")
    trainX = X_train[train_index]
    valX = X_train[val_index]
    trainY = y_train[train_index]
    valY = y_train[val_index]

    unique_classes = np.unique(trainY)
    train_class_weights = compute_class_weight('balanced', classes=unique_classes, y=trainY)
    train_class_weights_dict = dict(zip(unique_classes, train_class_weights))
    
    
    train_class_weights = dict(enumerate(train_class_weights))

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=[tf.keras.metrics.PrecisionAtRecall(0.8)])

    train_sample_weights = np.array([train_class_weights_dict[class_label] for class_label in trainY])


    history = model.fit(trainX,
                        trainY,
                        batch_size=32,
                        epochs=50,
                        validation_data=(valX, valY),
                        sample_weight=train_sample_weights)
    

    train_scores.append(history.history['loss'])
    val_scores.append(history.history['val_loss'])
    #save the image of training history

print("Average training scores:", np.mean(train_scores, axis=0))
print("Average validation scores:", np.mean(val_scores, axis=0))
y_pred = model.predict(X_test)
y_pred = np.where(y_pred > 0.6, 1, 0)

#recall and precision
TP = 0
FP = 0
FN = 0
TN = 0
for i in range(len(y_test)):
    if y_test[i] == 1 and y_pred[i] == 1:
        TP += 1
    elif y_test[i] == 0 and y_pred[i] == 1:
        FP += 1
    elif y_test[i] == 1 and y_pred[i] == 0:
        FN += 1
    else:
        TN += 1
recall = TP / (TP + FN)
precision = TP / (TP + FP)
print("TP:", TP)
print("FP:", FP)
print("FN:", FN)
print("TN:", TN)
print("Recall:", recall)
print("Precision:", precision)

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig('data/fun3/fun3_other.png')
plt.show()

output = [{}for i in range(4)]
output[0]["type"] = "TP"
output[0]["comment"] = []
output[1]["type"] = "FP"
output[1]["comment"] = []
output[2]["type"] = "FN"
output[2]["comment"] = []
output[3]["type"] = "TN"
output[3]["comment"] = []
for i in range(len(y_test)):
    if y_test[i] == 1 and y_pred[i] == 1:
        output[0]["comment"].append(comments[test_indices[i]])
    elif y_test[i] == 0 and y_pred[i] == 1:
        output[1]["comment"].append(comments[test_indices[i]])
    elif y_test[i] == 1 and y_pred[i] == 0:
        output[2]["comment"].append(comments[test_indices[i]])
    else:
        output[3]["comment"].append(comments[test_indices[i]])
with open('data/fun3/output_other.json', "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)