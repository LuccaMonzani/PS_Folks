from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def buscar_dados(tabela):
    try:
        con = sqlite3.connect("../criacao_db/cliente.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {tabela} WHERE mensagem IS NULL OR mensagem = ''")
        linhas = cur.fetchall()
        return [dict(linha) for linha in linhas]
    except Exception as e:
        return {"erro": str(e)}

@app.route("/estruturados", methods=["GET"])
def get_estruturados():
    return jsonify(buscar_dados("estruturados"))

@app.route("/nao_estruturados", methods=["GET"])
def get_nao_estruturados():
    return jsonify(buscar_dados("nao_estruturados"))

@app.route("/atualizar_mensagem_estruturados", methods=["POST"])
def atualizar_mensagem_estruturados():
    try:
        data = request.get_json()
        id_registro = data.get("ID")
        status_mensagem = data.get("mensagem")
        
        if not id_registro or not status_mensagem:
            return jsonify({"erro": "ID e mensagem são obrigatórios"}), 400
        
        con = sqlite3.connect("../criacao_db/cliente.db")
        cur = con.cursor()
        cur.execute("UPDATE estruturados SET mensagem = ? WHERE ID = ?", (status_mensagem, id_registro))
        con.commit()
        con.close()
        
        return jsonify({"mensagem": "Registro atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/atualizar_mensagem_nao_estruturados", methods=["POST"])
def atualizar_mensagem_nao_estruturados():
    try:
        data = request.get_json()
        id_registro = data.get("ID")
        status_mensagem = data.get("mensagem")
        
        if not id_registro or not status_mensagem:
            return jsonify({"erro": "ID e mensagem são obrigatórios"}), 400
        
        con = sqlite3.connect("../criacao_db/cliente.db")
        cur = con.cursor()
        cur.execute("UPDATE nao_estruturados SET mensagem = ? WHERE ID = ?", (status_mensagem, id_registro))
        con.commit()
        con.close()
        
        return jsonify({"mensagem": "Registro atualizado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
