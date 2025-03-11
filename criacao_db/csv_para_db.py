import pandas as pd
import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conector = sqlite3.connect("cliente.db")

# Carregar os arquivos CSV e salvar no SQLite
for arquivo_csv, nome_tabela in [("sample_estruturados.csv", "estruturados"), ("sample_nao_estruturados.csv", "nao_estruturados")]:
    df = pd.read_csv(arquivo_csv)  # Lendo o CSV
    df.to_sql(nome_tabela, conector, if_exists="replace", index=False)  # Salvando no SQLite

print("Tabelas criadas com sucesso!")

# Fechar conexão
conector.close()
