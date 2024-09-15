import json
import traceback
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler
from MetodosAPI import MetodosAPI

# Criando uma classe para instanciar a classe dos metodos
class Classe_Handler(BaseHTTPRequestHandler):
    metodos = MetodosAPI()
   
   # Criando um metodo para coletar dados
    def _get_data(self) -> bytes:
        tamanho = int(self.headers["Content-Length"] or 0)
        return self.rfile.read(tamanho)

    # Criando um metodo para retornar
    def _gerar_retorno(self, status_code: int, content: str = None, headers: dict = {}) -> None:
        self.send_response(status_code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        if content:
            self.wfile.write(content.encode("utf-8"))

    def do_GET(self) -> None:
        try:
            path = urlparse(self.path).path.strip("/").split("/")
            if path[0] == "books" and len(path) == 1:
                content = json.dumps(self.metodos.listar_livros())
                self._gerar_retorno(200, content, {"Content-Type": "application/json"})
            elif path[0] == "books" and len(path) == 2:
                book = self.metodos.info_livro(path[1])
                if book:
                    self._gerar_retorno(200, json.dumps(book), {"Content-Type": "application/json"})
                else:
                    self._gerar_retorno(404)
            elif path[0] == "authors" and len(path) == 1:
                content = json.dumps(self.metodos.listar_autores())
                self._gerar_retorno(200, content, {"Content-Type": "application/json"})
            elif path[0] == "authors" and len(path) == 2:
                author = self.metodos.info_autor(path[1])
                if author:
                    self._gerar_retorno(200, json.dumps(author), {"Content-Type": "application/json"})
                else:
                    self._gerar_retorno(404)
            elif path[0] == "authors" and len(path) == 3 and path[2] == "books":
                author_books = self.metodos.listar_livros_do_autor(path[1])
                if author_books:
                    self._gerar_retorno(200, json.dumps(author_books), {"Content-Type": "application/json"})
                else:
                    self._gerar_retorno(404)
            else:
                self._gerar_retorno(404)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self._gerar_retorno(500)

    def do_POST(self) -> None:
        try:
            data = self._get_data()
            path = urlparse(self.path).path.strip("/").split("/")
            content_type = self.headers.get("Content-Type")

            if content_type != "application/json":
                self._gerar_retorno(415, headers={"Accept-Post": "application/json"})
                return

            data = json.loads(data)
            if path == ["books"]:
                response = self.validate_book(data)
                if response["status_code"] == 200:
                    self.metodos.criar_livro(data)
                self._gerar_retorno(response["status_code"], response.get("content"), response.get("headers"))
            elif path == ["authors"]:
                response = self.validate_author(data)
                if response["status_code"] == 200:
                    self.metodos.criar_autor(data)
                self._gerar_retorno(response["status_code"], response.get("content"), response.get("headers"))
            elif len(path) == 4 and path[0] == "authors" and path[2] == "books":
                author = self.metodos.info_autor(path[1])
                book = self.metodos.info_livro(path[3])
                if author and book and not author["books"].get(path[3]):
                    self.metodos.criar_associacao(path[1], path[3])
                    self._gerar_retorno(200)
                else:
                    self._gerar_retorno(409, '{"error": "A associação entre autor e livro já existe."}', {"Content-Type": "application/json"})
            else:
                self._gerar_retorno(404)
        except json.JSONDecodeError:
            self._gerar_retorno(400, '{"error": "Formato JSON inválido."}', {"Content-Type": "application/json"})
        except Exception as e:
            print(e)
            traceback.print_exc()
            self._gerar_retorno(500)

    def do_PUT(self) -> None:
        try:
            data = self._get_data()
            path = urlparse(self.path).path.strip("/").split("/")
            if self.headers.get("Content-Type") != "application/json":
                self._gerar_retorno(415, headers={"Accept-Post": "application/json"})
                return

            data = json.loads(data)
            if len(path) == 2 and path[0] == "books":
                response = self.validate_book(data)
                if response["status_code"] == 200:
                    self.metodos.atualizar_livro(path[1], data)
                self._gerar_retorno(response["status_code"], response.get("content"), response.get("headers"))
            elif len(path) == 2 and path[0] == "authors":
                response = self.validate_author(data)
                if response["status_code"] == 200:
                    self.metodos.atualizar_autor(path[1], data)
                self._gerar_retorno(response["status_code"], response.get("content"), response.get("headers"))
            else:
                self._gerar_retorno(404)
        except json.JSONDecodeError:
            self._gerar_retorno(400, '{"error": "Formato JSON inválido."}', {"Content-Type": "application/json"})
        except Exception as e:
            print(e)
            traceback.print_exc()
            self._gerar_retorno(500)

    def do_DELETE(self) -> None:
        try:
            path = urlparse(self.path).path.strip("/").split("/")
            if len(path) == 2 and path[0] == "books":
                book = self.metodos.info_livro(path[1])
                if book:
                    self.metodos.excluir_livro(path[1])
                    self._gerar_retorno(200)
                else:
                    self._gerar_retorno(404)
            elif len(path) == 2 and path[0] == "authors":
                author = self.metodos.info_autor(path[1])
                if author:
                    self.metodos.excluir_autor(path[1])
                    self._gerar_retorno(200)
                else:
                    self._gerar_retorno(404)
            elif len(path) == 4 and path[0] == "authors" and path[2] == "books":
                author = self.metodos.info_autor(path[1])
                book = self.metodos.info_livro(path[3])
                if author and book:
                    self.metodos.excluir_associacao(path[1], path[3])
                    self._gerar_retorno(200)
                else:
                    self._gerar_retorno(404)
            else:
                self._gerar_retorno(404)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self._gerar_retorno(500)

    def validate_book(self, data: dict) -> dict:
        if not isinstance(data.get("titulo"), str):
            return {"status_code": 400, "content": '{"error": "Título é obrigatório e deve ser uma string."}', "headers": {"Content-Type": "application/json"}}
        if data.get("genero") and not isinstance(data.get("genero"), str):
            return {"status_code": 400, "content": '{"error": "Gênero deve ser uma string."}', "headers": {"Content-Type": "application/json"}}
        if data.get("ano") and not isinstance(data.get("ano"), int):
            return {"status_code": 400, "content": '{"error": "Ano deve ser um número inteiro."}', "headers": {"Content-Type": "application/json"}}
        if data.get("autor_id") and not isinstance(data.get("autor_id"), str):
            return {"status_code": 400, "content": '{"error": "autor_id deve ser uma string."}', "headers": {"Content-Type": "application/json"}}
        return {"status_code": 200}

    def validate_author(self, data: dict) -> dict:
        if not isinstance(data.get("nome"), str):
            return {"status_code": 400, "content": '{"error": "Nome é obrigatório e deve ser uma string."}', "headers": {"Content-Type": "application/json"}}
        if data.get("data_nascimento") and not isinstance(data.get("data_nascimento"), int):
            return {"status_code": 400, "content": '{"error": "Data de nascimento deve ser um número inteiro."}', "headers": {"Content-Type": "application/json"}}
        if data.get("nacionalidade") and not isinstance(data.get("nacionalidade"), str):
            return {"status_code": 400, "content": '{"error": "Nacionalidade deve ser uma string."}', "headers": {"Content-Type": "application/json"}}
        return {"status_code": 200}

