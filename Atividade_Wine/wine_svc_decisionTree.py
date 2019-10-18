import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.utils import resample
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns

dataset = pd.read_csv("winequality-red.csv", delimiter=';', decimal='.')

majoritaria = dataset[dataset['quality'] == 5]
balanceado = majoritaria

for c in [3, 4, 6, 7, 8]:
    minoritaria = dataset[dataset['quality'] == c]
    minoritaria_upsample = resample(minoritaria, replace=True, n_samples=681, random_state=None)
    balanceado = pd.concat([balanceado, minoritaria_upsample])

classes = balanceado['quality']
balanceado = balanceado.drop(['quality'], axis=1)

# Dividir os dados aleatoriamente em conjunto para aprendizado e conjunto para testes
X_train, X_test, y_train, y_test = train_test_split(balanceado, classes,
                                                    test_size=0.20)  # 20% do tamanho do arquivo será usado para testes

# Treinar o modelo
classifier_dt = DecisionTreeClassifier()
classifier_dt.fit(X_train, y_train)

classifier_svc = svm.SVC(gamma='auto')
print(classifier_svc.fit(balanceado, classes))

# Aplicar o modelo gerado sobre os dados separados para testes
pred_dt = classifier_dt.predict(X_test)
pred_svc = classifier_svc.predict(X_test)

# Avaliar o modelo: Acurácia e matriz de contingência
print("Resultado da Avaliação do Modelo ")
print('SCORE DecisionTree', classifier_dt.score(balanceado, classes))
print('SCORE SVC', classifier_svc.score(balanceado, classes))

# Classificar novas instâncias
predict_result = classifier_svc.predict([[7.4, 0.7, 0, 1.9, 0.076, 11, 34, 0.9978, 3.51, 0.56, 9.4]])
print(predict_result)

tips = sns.load_dataset("tips")
sns.relplot(x="pH", y="chlorides", hue="quality", data=dataset)
plt.show()

g = sns.FacetGrid(dataset, col="quality", hue="quality")
g.map(plt.scatter, "quality", "quality", alpha=.7)
g.add_legend();
plt.show()
