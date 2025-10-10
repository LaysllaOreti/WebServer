import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json # para salvar o cadastro dos filmes
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "locadora_marquise" # database que vai puxar os dados
)

class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # tenta abrir o arquivo 'index.html' no caminho solicitado.
            with open(os.path.join(path, 'index.html'), 'r', encoding='utf-8') as f:
                self.send_response(200) # se o arquivo for encontrado, uma resposta 200 é enviada.
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8')) # o conteúdo do arquivo é lido e enviado na resposta.
            return None
        
        # caso dê errado:
        except FileNotFoundError:
            return super().list_directory(path)
        
    def loadFilminhos(self):
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM locadora_marquise.diretor")
        result = cursor.fetchall()

        print("******************\n", result)

        for res in result:
            id_diretor = res[0]
            nome = res[1]
            sobrenome = res[2]
            genero = res[3]
            print(id_diretor, nome, sobrenome, genero)

    # verificação simples de usuário logado ou não logado
    def accont_user(self, login,password):
        loga = "laysllaeduarda@gmail.com"
        senha = "1008"
        return login == loga and senha == password

    # lida com as requisições do tipo get.
    def do_GET(self):
        # analisa a url para separar o caminho dos parâmetros de consulta
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if self.path == '/api/filmes':
            try:
                cursor = mydb.cursor(dictionary=True)
                cursor.execute(""" SELECT * FROM filme """)
                filmes = cursor.fetchall()

                if not filmes:
                    filmes = []

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(filmes, ensure_ascii=False).encode("utf-8"))
            except mysql.connector.Error as err:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))
            return
        
        if path == '/editar_filme':
            query_params = parse_qs(parsed_path.query)
            titulo_para_editar = query_params.get('titulo', [None])[0]

            if not titulo_para_editar:
                self.send_error(400, "título do filme não fornecido")
                return

            try:
                with open("filmes.json", "r", encoding="utf-8") as f:
                    filmes = json.load(f)
                
                # encontra o filme específico para editar
                filme_encontrado = next((f for f in filmes if f['titulo'] == titulo_para_editar), None)

                if not filme_encontrado:
                    self.send_error(404, "filme não encontrado")
                    return

                # carrega o html de edição e preenche os campos do formulário
                with open("editar_filme.html", "r", encoding="utf-8") as f:
                    content = f.read()
                
                # preenche os valores do formulário
                content = content.replace('value=""', f'value="{filme_encontrado.get("titulo", "")}"', 1)
                content = content.replace('name="titulo"', f'name="titulo" value="{filme_encontrado.get("titulo", "")}"')
                content = content.replace('name="atores"', f'name="atores" value="{filme_encontrado.get("atores", "")}"')
                content = content.replace('name="diretor"', f'name="diretor" value="{filme_encontrado.get("diretor", "")}"')
                content = content.replace('name="ano"', f'name="ano" value="{filme_encontrado.get("ano", "")}"')
                content = content.replace('name="genero"', f'name="genero" value="{filme_encontrado.get("genero", "")}"')
                content = content.replace('name="produtora"', f'name="produtora" value="{filme_encontrado.get("produtora", "")}"')
                # para o textarea (sinopse), o preenchimento é diferente
                content = content.replace('</textarea>', f'{filme_encontrado.get("sinopse", "")}</textarea>')
                # adiciona um campo oculto com o título antigo para referência
                content = content.replace('</form>', f'<input type="hidden" name="titulo_antigo" value="{titulo_para_editar}"></form>')

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))

            except FileNotFoundError:
                self.send_error(404, "arquivo de filmes ou template de edição não encontrado")
            return

        # um dicionário de rotas para encaminhar aos htmls específicos.
        routes = {
            "/login": "login.html",
            "/cadastro_filmes": "cadastro_filmes.html",
            "/listar_filmes": "listar_filmes.html",
            "/editar_filme": "editar_filme.html",
        }

        # verifica se o caminho da requisição está presente no dicionário de rotas.
        if self.path in routes:
            file_path = os.path.join(os.getcwd(), routes[self.path])
            try:
                # tenta abrir e ler o arquivo html especificado pela rota.
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                # caso o arquivo não seja encontrado, envia uma resposta de erro 404.
                self.send_error(404, "file not found")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/send_login':
            # tamanho da requisição que está sendo mandada
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('email',[""])[0]
            password = form_data.get('senha',[""])[0]
 
            if self.accont_user(login, password):
                # sucesso no login
                self.send_response(303)
                self.send_header("Location", "/cadastro_filmes")
                self.end_headers()
            else:
                # falha no login
                self.send_response(401)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("usuário ou senha inválidos".encode('utf-8'))
            return

        elif self.path == '/cadastro_filme':
            # tamanho da requisição que está sendo mandada
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            titulo = form_data.get('titulo', [""])[0]
            atores = form_data.get('atores', [""])[0]
            diretor = form_data.get('diretor', [""])[0]
            ano = form_data.get('ano', [""])[0]
            genero = form_data.get('genero', [""])[0]
            produtora = form_data.get('produtora', [""])[0]
            sinopse = form_data.get('sinopse', [""])[0]

            # alterado: grava no banco mysql em vez de json
            cursor = mydb.cursor()
            sql = """
                INSERT INTO filme (titulo, atores, diretor, ano, genero, produtora, sinopse)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val = (titulo, atores, diretor, ano, genero, produtora, sinopse)
            cursor.execute(sql, val)
            mydb.commit()
            
            self.send_response(303)
            self.send_header("Location", "/listar_filmes")
            self.end_headers()
            return

        else:
            super(MyHandle, self).do_POST()
            return

# função que cofigura e inicia o servidor.
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("server running in http://localhost:8000")
    httpd.serve_forever()

# garante que a função `main()` seja chamada apenas quando o script é executado.
if __name__ == "__main__":
    main()
