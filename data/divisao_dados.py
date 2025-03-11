import pandas as pd
from sklearn.model_selection import train_test_split

# Carregar os dados classificados corrigidos
dados_path = "sample_nao_estruturados_classificado_revisado.xlsx"
df_corrigido = pd.read_excel(dados_path)

# Separar os dados entre exames de imagem e não exames
df_exames = df_corrigido[df_corrigido["EXAME_IDENTIFICADO"] != "Nulo"]
df_nao_exames = df_corrigido[df_corrigido["EXAME_IDENTIFICADO"] == "Nulo"]

# Definir proporções para divisão (70% treino, 30% teste)
treino_exames, teste_exames = train_test_split(
    df_exames, test_size=0.3, random_state=42, stratify=df_exames["EXAME_IDENTIFICADO"]
)
treino_nao_exames, teste_nao_exames = train_test_split(
    df_nao_exames, test_size=0.3, random_state=42
)

# Combinar os conjuntos de treino e teste
df_treino = pd.concat([treino_exames, treino_nao_exames])
df_teste = pd.concat([teste_exames, teste_nao_exames])

# Salvar os arquivos resultantes
df_treino.to_excel("sample_treino.xlsx", index=False)
df_teste.to_excel("sample_teste.xlsx", index=False)

print("Divisão concluída! Arquivos 'sample_treino.xlsx' e 'sample_teste.xlsx' foram gerados.")
