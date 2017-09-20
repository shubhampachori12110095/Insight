import cPickle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from transform import *
from classify import *
from cnn_core import *

# -------------------------------------------------------------------------------------------------------------
data_file = "../Data/train_mat_filtered.pkl"
#vocab_file = "../Data/vocab_filtered.pkl"
vocab_inv_file = "../Data/vocab_inv_filtered.pkl"

with open(data_file) as f:
    data, labels, _ = cPickle.load(f)
with open(vocab_inv_file) as f:
    vocabulary_inv = cPickle.load(f)

algorithm = 'svm'
type = 'concat_emb'
results = {'accuracy': [], 'precision': [], 'recall': [], 'f1': []}

# -------------------------------------------------------------------------------------------------------------
embeddings, labels = getEmbeddings(data, labels, vocabulary_inv, type)
# Random split
X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.1, random_state=42)
print X_train.shape, X_test.shape
cPickle.dump([X_train, X_test, y_train, y_test], open('../Data/concat_embeddings.pkl', 'wb'))

# Run the classification algorithm
#classify(algorithm, X_train, y_train, X_test, y_test, results)

model = CNN()
model.fit(X_train, y_train, batch_size=batch_size, epochs=num_epochs,
          validation_data=(X_test, y_test), verbose=2)
predictions_valid = model.predict(X_test, batch_size=batch_size, verbose=1)
score = log_loss(y_test, predictions_valid)
print('Score log_loss: ', score)

# Cross-validation
#for k, (train, test) in enumerate(KFold(10).split(embeddings, labels)):
#    X_train, X_test, y_train, y_test = embeddings[train], embeddings[test], labels[train], labels[test]
#    print classify(algorithm, X_train, y_train, X_test, y_test, results)

