import pandas as pd
dataset = pd.read_csv("diabetes.csv")
import joblib

# Exibe o número de linhas e o número de colunas
print('=', dataset.shape)
print(dataset.describe())

# Divide os dados em dois conjuntos: Atributos e Classes
attributes = dataset.drop(['class'], axis=1)
classes = dataset['class']
print(classes.shape)

# Dividir os dados aleatoriamente em conjunto para aprendizado e conjunto para testes
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(attributes, classes, test_size=0.20) #20% do tamanho do arquivo será usado para testes
# X_train: segmento dos atributos para treinamento do modelo
# X_test : segmento dos atributos para avaliação do modelo
# y_train: segmento das classes para treinamento do modelo
# y_testn: segmento das classes para avaliação do modelo

#Treinar o modelo
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
classifier.fit(X_train, y_train)

#Aplicar o modelo gerado sobre os dados separados para testes
y_pred = classifier.predict(X_test)
print(y_pred)

#Score
print("predict_proba")
print(classifier.predict_proba(X_test))

#Avaliar o modelo: Acurácia e matriz de contingência
from sklearn.metrics import classification_report, confusion_matrix
print("Resultado da Avaliação do Modelo")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

#Classificar uma nova instância
print("Classificar Nova")
nova_instancia = [[6, 148, 72, 35, 0, 33.6, 0.627, 50]]
print(classifier.predict(nova_instancia))

#Salvar o modelo para uso posterior
joblib.dump(classifier, 'modelo.joblib')

classifier = joblib.load('modelo.joblib')
nova_instancia=[[8, 148, 2, 35, 0, 33.6, 0.8, 50]]
print("Com o modelo salvo: ")
print(classifier.predict(nova_instancia))

# ##################
# # UTILIZAR CROSS VALIDATION
# ##################
from sklearn.model_selection import cross_validate, cross_val_score
print('CROSS VALIDATION')
scores = cross_val_score(classifier, attributes, classes, cv=10)
print('cross_val_score')
print(scores)
print('Precisao media: ', scores.mean())
