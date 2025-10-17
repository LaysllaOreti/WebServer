import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import mysql.connector
import cgi  # para lidar com multipart/form-data

# Pasta onde as fotos serão salvas
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Conexão com o banco de dados MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="locadora_marquise"  # ✅ nome do seu banco atualizado
)

class ServidorHTTP(SimpleHTTPRequestHandler):
    def do_POST(self):
        """Lida com requisições POST"""
        if self.path == "/inserir_filme":
            self.inserir_filme()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Rota nao encontrada")

    def inserir_filme(self):
        """Processa o formulário e insere o filme no banco"""
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        # Obtém os campos do formulário
        titulo = form.getvalue("titulo")
        atores = form.getvalue("atores")
        diretor = form.getvalue("diretor")
        ano = form.getvalue("ano")
        genero = form.getvalue("genero")
        produtora = form.getvalue("produtora")
        duracao = form.getvalue("duracao")
        orcamento = form.getvalue("orcamento")
        sinopse = form.getvalue("sinopse")

        # Upload do poster (se enviado)
        poster_path = None
        poster_file = form["poster"] if "poster" in form else None
        if poster_file and poster_file.filename:
            filename = os.path.basename(poster_file.filename)
            poster_path = os.path.join(UPLOAD_DIR, filename)

            with open(poster_path, "wb") as f:
                f.write(poster_file.file.read())

            # Caminho relativo (para armazenar no banco)
            poster_path = f"/{UPLOAD_DIR}/{filename}"

        # Inserir no banco de dados
        try:
            mycursor = mydb.cursor()
            sql = """
                INSERT INTO filme (
                    titulo, atores, diretor, ano, genero, produtora, 
                    duracao, orcamento, poster, sinopse
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (
                titulo, atores, diretor, ano, genero, produtora,
                duracao, orcamento, poster_path, sinopse
            )

            mycursor.execute(sql, valores)
            mydb.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            resposta = {"status": "sucesso", "mensagem": "Filme inserido com sucesso!"}
            self.wfile.write(json.dumps(resposta).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            resposta = {"status": "erro", "mensagem": str(e)}
            self.wfile.write(json.dumps(resposta).encode('utf-8'))

# Configuração do servidor HTTP
if __name__ == "__main__":
    porta = 8080
    servidor = HTTPServer(("localhost", porta), ServidorHTTP)
    print(f"Server Running: http://localhost:{porta}")
    servidor.serve_forever()
