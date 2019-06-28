import pandas as pd
from sys import argv
from sklearn.naive_bayes import GaussianNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_score
from sklearn import metrics

ds = pd.read_csv(argv[1])

labels = ds.pop('label').values
ds.drop(columns="method", inplace=True)

#X_train, X_test, y_train, y_test = train_test_split(ds, labels, test)


scor = ('accuracy', 'roc_auc', 'f1_micro', 'f1_macro' )

BNB_model = BernoulliNB()
BNB_cv = cross_val_score(BNB_model, ds, labels, cv=10)
print('Bernouli:')
print(BNB_cv)
print(BNB_cv.mean(), BNB_cv.std())

GNB_model = GaussianNB()
GNB_cv = cross_val_score(GNB_model, ds, labels, cv=10)
print('Gaussian:')
print(GNB_cv)
print(GNB_cv.mean(), GNB_cv.std())

K3NN_classifier = KNeighborsClassifier(3, 'distance', metric='hamming')
K3NN_cv = cross_val_score(GNB_model, ds, labels, cv=10)
print('3NN:')
print(K3NN_cv)
print(K3NN_cv.mean(), K3NN_cv.std())

K5NN_classifier = KNeighborsClassifier(5, 'distance', metric='hamming')
K5NN_cv = cross_val_score(GNB_model, ds, labels, cv=10)
print('5NN:')
print(K5NN_cv)
print(K5NN_cv.mean(), K5NN_cv.std())

K7NN_classifier = KNeighborsClassifier(7, 'distance', metric='hamming')
K7NN_cv = cross_val_score(GNB_model, ds, labels, cv=10)
print('7NN:')
print(K7NN_cv)
print(K7NN_cv.mean(), K7NN_cv.std())

K9NN_classifier = KNeighborsClassifier(9, 'distance', metric='hamming')
K9NN_cv = cross_val_score(GNB_model, ds, labels, cv=10)
print('9NN')
print(K9NN_cv)
print(K9NN_cv.mean(), K9NN_cv.std())
