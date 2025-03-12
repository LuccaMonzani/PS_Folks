from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Função para buscar dados em uma tabela específica do banco de dados.
# Recebe o nome da tabela e retorna os registros que não possuem mensagem (nula ou vazia).
def buscar_dados(tabela):
    try:
        # Conecta ao banco de dados SQLite localizado no diretório ../criacao_db/
        con = sqlite3.connect("../criacao_db/cliente.db")
        con.row_factory = sqlite3.Row  # Permite acessar os dados como dicionário
        cur = con.cursor()
        # Executa a query para selecionar registros sem mensagem
        cur.execute(f"SELECT * FROM {tabela} WHERE mensagem IS NULL OR mensagem = ''")
        linhas = cur.fetchall()
        # Retorna uma lista de dicionários representando os registros
        return [dict(linha) for linha in linhas]
    except Exception as e:
        # Em caso de erro, retorna um dicionário com a mensagem de erro
        return {"erro": str(e)}

# Endpoint para obter os dados dos registros estruturados.
@app.route("/estruturados", methods=["GET"])
def get_estruturados():
    return jsonify(buscar_dados("estruturados"))

# Endpoint para obter os dados dos registros não estruturados.
@app.route("/nao_estruturados", methods=["GET"])
def get_nao_estruturados():
    return jsonify(buscar_dados("nao_estruturados"))

# Endpoint para atualizar a mensagem dos registros estruturados.
@app.route("/atualizar_mensagem_estruturados", methods=["POST"])
def atualizar_mensagem_estruturados():
    try:
        data = request.get_json()  # Obtém os dados enviados em JSON no corpo da requisição
        id_registro = data.get("ID")
        status_mensagem = data.get("mensagem")
        
        # Verifica se o ID e a mensagem foram fornecidos; caso contrário, retorna erro 400.
        if not id_registro or not status_mensagem:
            return jsonify({"erro": "ID e mensagem são obrigatórios"}), 400
        
        # Conecta ao banco de dados e atualiza o registro correspondente.
        con = sqlite3.connect("../criacao_db/cliente.db")
        cur = con.cursor()
        cur.execute("UPDATE estruturados SET mensagem = ? WHERE ID = ?", (status_mensagem, id_registro))
        con.commit()  # Salva as alterações
        con.close()
        
        # Retorna uma mensagem de sucesso
        return jsonify({"mensagem": "Registro atualizado com sucesso!"}), 200
    except Exception as e:
        # Em caso de exceção, retorna o erro com status 500
        return jsonify({"erro": str(e)}), 500

# Endpoint para atualizar a mensagem dos registros não estruturados.
@app.route("/atualizar_mensagem_nao_estruturados", methods=["POST"])
def atualizar_mensagem_nao_estruturados():
    try:
        data = request.get_json()  # Obtém os dados JSON da requisição
        id_registro = data.get("ID")
        status_mensagem = data.get("mensagem")
        
        # Verifica se o ID e a mensagem estão presentes, caso contrário, retorna erro.
        if not id_registro or not status_mensagem:
            return jsonify({"erro": "ID e mensagem são obrigatórios"}), 400
        
        # Conecta ao banco de dados e atualiza o registro na tabela de não estruturados.
        con = sqlite3.connect("../criacao_db/cliente.db")
        cur = con.cursor()
        cur.execute("UPDATE nao_estruturados SET mensagem = ? WHERE ID = ?", (status_mensagem, id_registro))
        con.commit()  # Confirma a alteração
        con.close()
        
        # Retorna mensagem de sucesso
        return jsonify({"mensagem": "Registro atualizado com sucesso!"}), 200
    except Exception as e:
        # Retorna erro 500 com detalhes da exceção
        return jsonify({"erro": str(e)}), 500

# Endpoint para atualizar os contadores do dashboard para registros estruturados.
@app.route("/atualizar_dashboard_estruturados", methods=["POST"])
def atualizar_dashboard_estruturados():
    try:
        data = request.get_json()  # Obtém dados da requisição no formato JSON
        metric = data.get("metric")
        incremento = data.get("incremento", 1)  # Incremento padrão de 1 caso não seja informado
        if not metric:
            return jsonify({"erro": "Metric é obrigatório"}), 400
        
        # Conecta ao banco de dados e atualiza (ou insere) o registro na tabela do dashboard.
        con = sqlite3.connect("../criacao_db/cliente.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO dashboard_estruturados (metric, valor)
            VALUES (?, ?)
            ON CONFLICT(metric) DO UPDATE SET valor = valor + ?;
            """, (metric, incremento, incremento))
        con.commit()  # Salva as alterações
        con.close()
        # Retorna mensagem de sucesso com a métrica atualizada
        return jsonify({"mensagem": f"Dashboard estruturados atualizado: {metric} + {incremento}"}), 200
    except Exception as e:
        # Em caso de erro, retorna status 500 e a mensagem de erro
        return jsonify({"erro": str(e)}), 500

# Endpoint para atualizar os contadores do dashboard para registros não estruturados.
@app.route("/atualizar_dashboard_nao_estruturados", methods=["POST"])
def atualizar_dashboard_nao_estruturados():
    try:
        data = request.get_json()  # Captura os dados JSON enviados na requisição
        metric = data.get("metric")
        incremento = data.get("incremento", 1)  # Define o incremento padrão como 1
        if not metric:
            return jsonify({"erro": "Metric é obrigatório"}), 400
        
        # Conecta ao banco de dados e realiza a inserção ou atualização do contador na tabela do dashboard.
        con = sqlite3.connect("../criacao_db/cliente.db")
        cur = con.cursor()
        cur.execute("""
            INSERT INTO dashboard_nao_estruturados (metric, valor)
            VALUES (?, ?)
            ON CONFLICT(metric) DO UPDATE SET valor = valor + ?;
            """, (metric, incremento, incremento))
        con.commit()  # Confirma as alterações
        con.close()
        # Retorna mensagem indicando que o dashboard foi atualizado
        return jsonify({"mensagem": f"Dashboard não estruturados atualizado: {metric} + {incremento}"}), 200
    except Exception as e:
        # Em caso de exceção, retorna o erro com status 500
        return jsonify({"erro": str(e)}), 500

# Inicializa o servidor Flask se este script for executado diretamente.
if __name__ == "__main__":
    # Inicia o servidor em modo debug e ouvindo em todas as interfaces na porta 5000.
    app.run(debug=True, host="0.0.0.0", port=5000)
