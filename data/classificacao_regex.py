import pandas as pd
import re
import json

# Caminhos dos arquivos
dados_path = "sample_nao_estruturados_preprocessado.csv"
classificado_path = "sample_nao_estruturados_classificado.csv"
exames_dict_path = "exames_dict.json"

# Carregar o dataset preprocessado
df_preprocessado = pd.read_csv(dados_path)

# Criar um dicionário de termos para exames de imagem
exames_dict = {
    "Raio-X": [r"\braio[ -]?x\b", r"\brx\b", r"\bradiografia\b"],
    "Ressonância Magnética": [r"\brm\b", r"\brnm\b", r"\brmn\b", r"\bressonancia\b", r"\bressonancia magnetica\b"],
    "Tomografia Computadorizada": [r"\btc\b", r"\btomografia\b", r"\btomografia computadorizada\b"],
    "Ultrassonografia": [r"\bus\b", r"\busg\b", r"\bultrassom\b", r"\bultrassonografia\b"],
    "Mamografia": [r"\bmamografia\b"],
    "Densitometria Óssea": [r"\bdensitometria\b", r"\bdensitometria ossea\b"],
    "Cintilografia": [r"\bcintilografia\b"],
    "Angiografia": [r"\bangiografia\b", r"\bangiotomografia\b", r"\bAngioTC\b", r"\bangiornm\b"],
    "Ecodoppler": [r"\becodoppler\b", r"\bdoppler\b"],
}

# Função para identificar exames na coluna DS_RECEITA_TRATADO
def identificar_exame(texto):
    if pd.isna(texto):  # Verificar se o valor é NaN
        return "Nulo"
    for exame, padroes in exames_dict.items():
        for padrao in padroes:
            if re.search(padrao, texto):
                return exame
    return "Nulo"

# Garantir que todos os valores em DS_RECEITA_TRATADO sejam strings
df_preprocessado["DS_RECEITA_TRATADO"] = df_preprocessado["DS_RECEITA_TRATADO"].fillna("").astype(str)

# Aplicar a função para identificar exames
df_preprocessado["EXAME_IDENTIFICADO"] = df_preprocessado["DS_RECEITA_TRATADO"].apply(identificar_exame)

# Salvar o dataset classificado
df_preprocessado.to_csv(classificado_path, index=False)

# Salvar o dicionário de exames como JSON
with open(exames_dict_path, "w", encoding="utf-8") as f:
    json.dump(exames_dict, f, indent=4, ensure_ascii=False)

print(f"Classificação concluída! Arquivo salvo em: {classificado_path}")
