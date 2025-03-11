import requests
import json
import joblib
import os

# URLs da API
URL_ESTRUTURADOS = "http://127.0.0.1:5000/estruturados"
URL_NAO_ESTRUTURADOS = "http://127.0.0.1:5000/nao_estruturados"
URL_ATUALIZAR_ESTRUTURADOS = "http://127.0.0.1:5000/atualizar_mensagem_estruturados"
URL_ATUALIZAR_NAO_ESTRUTURADOS = "http://127.0.0.1:5000/atualizar_mensagem_nao_estruturados"

# Carregar o modelo treinado e o vetorizador
modelo_svm = joblib.load("../SVM/modelo_svm.pkl")
vectorizer = joblib.load("../SVM/vectorizer.pkl")

# Função para obter dados via API
def obter_dados(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return []

# Função para prever exame usando IA local
def prever_exame(ds_receita):
    """Recebe um texto de receita médica e retorna a previsão do exame."""
    
    # Verifica se a receita é None e substitui por string vazia
    if ds_receita is None:
        ds_receita = ""
    
    # Aplica a previsão
    predicao = modelo_svm.predict([ds_receita])[0]
    
    return predicao


# Função para atualizar mensagens via API
def atualizar_mensagem(api_url, id_registro, status):
    try:
        payload = {"ID": id_registro, "mensagem": status}
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        print(f"Registro {id_registro} atualizado com status: {status}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao atualizar via API: {e}")

def carregar_dicionario_tuss():
    """Carrega o dicionário de TUSS a partir do arquivo JSON na mesma pasta do script."""
    caminho_arquivo = os.path.join(os.path.dirname(__file__), "dicionario_tuss.json")
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)  # Carrega o JSON como um dicionário
    except FileNotFoundError:
        print("Erro: Arquivo 'dicionario_tuss.json' não encontrado.")
        return {}
    except json.JSONDecodeError:
        print("Erro: Problema ao decodificar o JSON do 'dicionario_tuss.json'.")
        return {}

# Processamento dos dados estruturados
def processar_dados_estruturados():
    dados = obter_dados(URL_ESTRUTURADOS)
    
    # Carrega o dicionário de códigos TUSS de exames de imagem
    dicionario_tuss = carregar_dicionario_tuss()
    
    for dado in dados:
        id_registro = dado.get("ID")
        nome_paciente = dado.get("SOLICITANTE", "Paciente")
        telefone = dado.get("TEL", "Não informado")
        cd_tuss = str(dado.get("CD_TUSS"))  # Convertendo para string para garantir compatibilidade

        # Verificando se o código TUSS está no dicionário
        exame = dicionario_tuss.get(cd_tuss)

        if exame:  # Se encontrou o exame correspondente no dicionário
            mensagem = (
                f"Olá, {nome_paciente}!\n"
                f"Verificamos que você precisa realizar o seguinte exame: {exame}\n"
                f"Acessando o link abaixo você pode agendar o seu exame de forma prática e rápida:\n"
                f"https://link-do-sistema.com"
            )
            print(f"Enviando mensagem para {telefone}:\n{mensagem}\n")
            atualizar_mensagem(URL_ATUALIZAR_ESTRUTURADOS, id_registro, "mensagem enviada")
        else:
            # Caso o código não esteja no dicionário, indicar que não há necessidade de mensagem
            atualizar_mensagem(URL_ATUALIZAR_ESTRUTURADOS, id_registro, "sem necessidade de mensagem")


# Processamento dos dados não estruturados
def processar_dados_nao_estruturados():
    dados = obter_dados(URL_NAO_ESTRUTURADOS)
    
    for dado in dados:
        id_registro = dado["ID"]
        nome_paciente = dado["SOLICITANTE"]
        telefone = dado["TEL"]
        ds_receita = dado["DS_RECEITA"]

        # Usar a IA para prever o exame localmente
        exame = prever_exame(ds_receita)

        if exame != "Nulo":
            mensagem = (
                f"Olá, {nome_paciente}!\n"
                f"Verificamos que você precisa realizar o seguinte exame: {exame}\n"
                f"Acessando o link abaixo você pode agendar o seu exame de forma prática e rápida:\n"
                f"https://link-do-sistema.com"
            )
            print(f"Enviando mensagem para {telefone}:\n{mensagem}\n")
            atualizar_mensagem(URL_ATUALIZAR_NAO_ESTRUTURADOS, id_registro, "mensagem enviada")
        else:
            atualizar_mensagem(URL_ATUALIZAR_NAO_ESTRUTURADOS, id_registro, "sem necessidade de mensagem")

# Executar processamento
if __name__ == "__main__":
    processar_dados_estruturados()
    processar_dados_nao_estruturados()
