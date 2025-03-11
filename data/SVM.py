import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Lista de stopwords em português
stopwords_portugues = [
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "não",
    "uma", "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas",
    "foi", "ao", "ele", "das", "tem", "à", "seu", "sua", "ou", "quando", "muito"
]

# Caminhos dos arquivos revisados
treino_path = "sample_treino_revisado.xlsx"
teste_path = "sample_teste_revisado.xlsx"

# Carregar os dados revisados
df_treino = pd.read_excel(treino_path)
df_teste = pd.read_excel(teste_path)

# Ajustar as features (X) e rótulos (y) usando a coluna DS_RECEITA original
X_treino, y_treino = df_treino["DS_RECEITA"], df_treino["EXAME_IDENTIFICADO"]
X_teste, y_teste = df_teste["DS_RECEITA"], df_teste["EXAME_IDENTIFICADO"]

# Garantir que todas as entradas de texto sejam strings
X_treino = X_treino.fillna("").astype(str)
X_teste = X_teste.fillna("").astype(str)

# Criar um pipeline com vetorização TF-IDF + SVM
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words=stopwords_portugues, ngram_range=(1,2), min_df=2, max_df=0.9)),
    ("svm", SVC(kernel="linear", probability=True, random_state=42))
])

# Definir os hiperparâmetros para ajuste
param_grid = {
    "svm__C": [0.1, 1, 10],  # Ajuste de regularização
    "svm__class_weight": [None, "balanced"]  # Lidar com desbalanceamento
}

# Aplicar GridSearchCV para encontrar os melhores hiperparâmetros
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring="accuracy", verbose=2, n_jobs=-1)
grid_search.fit(X_treino, y_treino)

# Melhor modelo encontrado
melhor_modelo = grid_search.best_estimator_

# Fazer previsões no conjunto de teste
y_pred = melhor_modelo.predict(X_teste)

# Avaliar o desempenho do modelo
relatorio = classification_report(y_teste, y_pred, output_dict=True)
acuracia = accuracy_score(y_teste, y_pred)

# Exibir melhores hiperparâmetros encontrados
print("Melhores Hiperparâmetros:")
print(grid_search.best_params_)

# Exibir métricas de desempenho
print("Relatório de Classificação:")
print(classification_report(y_teste, y_pred))
print(f"Acurácia: {acuracia:.2f}")

# Caminhos para salvar o modelo e o vetorizador
modelo_path = "modelo_svm.pkl"
vectorizer_path = "vectorizer.pkl"

# Salvar o modelo treinado
joblib.dump(melhor_modelo, modelo_path)

# Salvar o vetorizador extraído do pipeline
joblib.dump(melhor_modelo.named_steps["tfidf"], vectorizer_path)

print(f"Modelo salvo em {modelo_path}")
print(f"Vetorizador salvo em {vectorizer_path}")