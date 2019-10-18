import pandas as pd
dataset = pd.read_csv("ortopedia.csv", delimiter=',')
import joblib
from sklearn.utils import resample
from sklearn.model_selection import cross_validate, cross_val_score

# Exibe o número de linhas e o número de colunas
print('=', dataset.shape)
print(dataset.columns)

#Isolar a base de dados com a classe minoritária
minoritaria = dataset[dataset['class'] == 1]
majoritaria = dataset[dataset['class'] == 0]
minoritaria_upsample = resample(minoritaria, replace=True, n_samples=7900, random_state=None)

#Merge dos dataframes
#dataset = dataset.drop(dataset[dataset['class'] == 1].index)
dataset_balanceado = pd.concat([majoritaria, minoritaria_upsample])

# Divide os dados em dois conjuntos: Atributos e Classes
attributes = dataset_balanceado.drop(['class'], axis=1)
classes = dataset_balanceado['class']

# Cria atributos "dummies" para as colunas que não são numericas no conjunto de dados
new_attributes = pd.get_dummies(attributes, columns=['Sexo', 'CID'],
                                drop_first=True, prefix=['Sexo_', 'CID_'])
# print(new_attributes)

# Dividir os dados aleatoriamente em conjunto para aprendizado e conjunto para testes
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(new_attributes, classes, test_size=0.20) #20% do tamanho do arquivo será usado para testes
# X_train: segmento dos atributos para treinamento do modelo
# X_test : segmento dos atributos para avaliação do modelo
# y_train: segmento das classes para treinamento do modelo
# y_testn: segmento das classes para avaliação do modelo

#Treinar o modelo
from sklearn.tree import DecisionTreeClassifier
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

#Aplicar o modelo gerado sobre os dados separados para testes
y_pred = classifier.predict(X_test)
print(y_pred)

#Avaliar o modelo: Acurácia e matriz de contingência
from sklearn.metrics import classification_report, confusion_matrix
print("Resultado da Avaliação do Modelo")
cm = confusion_matrix(y_test, y_pred)
print(cm)
print(classification_report(y_test, y_pred))

print('CROSS VALIDATION')
scores = cross_val_score(classifier, new_attributes, classes, cv=10)
print('cross_val_score')
# print(scores)
print('Precisao media: ', scores.mean())
print('Desvio padrão: ', scores.std())

#ESPECIFIDADE = Verdadeiros Negativos
#NVM/(NVM + NFP)
especificidade = cm[0][0] / (cm[0][0] + cm[0][1])
print('especificidade:', especificidade)

#SENSIBILIDADE = Verdadeiros Positivos
#NVP/(NVP + NFN)
sensibilidade = cm[1][1] / (cm[1][1] + cm[1][0])
print('sensibilidade: ', sensibilidade)
