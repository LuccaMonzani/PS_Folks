import pandas as pd
import re
import unicodedata

# Caminho do arquivo original
sample_nao_estruturados_path = "sample_nao_estruturados.csv"

# Carregar os dados não estruturados
df_nao_estruturados = pd.read_csv(sample_nao_estruturados_path)

# Função para remover acentos
def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Função para normalizar apenas a coluna DS_RECEITA
def tratar_texto(texto):
    if pd.isna(texto):  # Verificar se o valor é NaN
        return ""
    texto = str(texto).lower().strip()  # Converter para minúsculas e remover espaços extras
    texto = remover_acentos(texto)  # Remover acentos
    texto = re.sub(r"[^a-z0-9 ]", "", texto)  # Remover caracteres especiais
    palavras_irrelevantes = {"de", "para", "o", "a", "os", "as", "um", "uma", "e", "do", "da", "dos", "das"}
    texto = " ".join([palavra for palavra in texto.split() if palavra not in palavras_irrelevantes])
    return texto

# Aplicar o tratamento apenas à coluna DS_RECEITA, mantendo as demais colunas intactas
df_nao_estruturados["DS_RECEITA_TRATADO"] = df_nao_estruturados["DS_RECEITA"].apply(tratar_texto)

# Salvar o dataset preprocessado sem alterar as colunas originais
preprocessado_path = "sample_nao_estruturados_preprocessado.csv"
df_nao_estruturados.to_csv(preprocessado_path, index=False)

print(f"Arquivo preprocessado salvo como: {preprocessado_path}")
