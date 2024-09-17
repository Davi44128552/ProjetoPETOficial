from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Base de dados que vai armazenar todos os livros e autores
data_store = {
    'book_store' : {},
    'author_store' : {}
}

# Contador de id de todos os livros e autores
book_id_counter = 1
author_id_counter = 1

class Handler(BaseHTTPRequestHandler):
    # Criando metodos para atribuir um id aos componentes
        # Livros
    @staticmethod
    def generate_book_id():
        global book_id_counter
        book_id = book_id_counter
        book_id_counter += 1
        return book_id
    
        # Autores
    @staticmethod
    def generate_author_id():
        global author_id_counter
        author_id = author_id_counter
        author_id_counter += 1
        return author_id 
    
    #Criando os metodos HTTP para as rotas
        # POST
    def do_POST(self):
        # Adicionando um novo livro ao banco de dados
        if self.path == '/books':
            # Recebendo o conteudo enviado na requisicao
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Armazenando os dados recebidos na base de dados
            try:
                data = json.loads(post_data)
                title = data.get('title')
                genre = data.get('genre','')
                year = data.get('year','')
                author_id = data.get('author_id','')

                # Verificando se foi adicionado um titulo para o livro a ser criado
                    # Caso nao
                if not title:
                    self.send_response(400)
                    response = {'error' : 'title is required'}
                    self.wfile.write(b'Error: Title is Required')

                    # Caso sim
                else:
                    # Criando um "registro" para livro na "tabela" livros
                    book_id = Handler.generate_book_id()
                    data_store['book_store'][book_id] = {
                        'title': title,
                        'genre' : genre,
                        'year' : year,
                        'author_id' : author_id
                    }

                    # Registrando uma resposta ao usuario
                    self.send_response(200)
                    response = {'message': 'Book created', 'book_id': book_id}
            
            # Tratando erros referente à invalidade do arquivo json
            except json.JSONDecodeError:
                self.send_response(400)
                response = {'error': 'Invalid JSON'}
            
            # Envinado a resposta ao usuario
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        # Adicionando um novo autor ao banco de dados
        elif self.path == '/authors':

            # Recebendo o conteudo enviado
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Armazenando as informacoes recebidas no banco de dados
            try:
                data = json.loads(post_data)
                name = data.get('name')
                birthday = data.get('birthday','')
                nationality = data.get('nationality','')

                # Analisando a falta de nome
                    # Caso haja
                if not name:
                    self.send_response(400)
                    response = {'error' : 'Name is required'}
                    self.wfile.write(b'Error: Name is Required')

                    # Caso contrario
                else:
                    # Criando o registro para um novo autor
                    author_id = Handler.generate_author_id()
                    data_store['author_store'][author_id] = {
                        'name': name,
                        'birthday' : birthday,
                        'nationality' : nationality
                    }

                    # Registrando uma resposta a ser enviada
                    self.send_response(200)
                    response = {'message': 'Author created', 'author_id': author_id}
            
            # Analisando caso de erro de leitura de json
            except json.JSONDecodeError:
                self.send_response(400)
                response = {'error': 'Invalid JSON'}
            
            # Enviando a resposta
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        # Criando uma relacao entre um autor e um livro
        elif self.path.startswith('/authors/') and '/books/' in self.path:
            #rota '/authors/{author_id}/books/{books_id}

            # Coletando o id do livro e do autor a serem relacionados
            if len(self.path.split('/')) == 5:
                author_id = int(self.path.split('/')[2])
                books_id = int(self.path.split('/')[4])

                # Verificando se o id do autor existe no banco de dados
                if author_id not in data_store['author_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Author not found'}).encode('utf-8'))
                    return
                
                # Verificando se o id do livro existe no banco de dados
                if books_id not in data_store['book_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Book not found'}).encode('utf-8'))
                    return
                
                # Vinculando autor e livro pelo id do autor
                data_store['book_store'][books_id]['author_id'] = author_id

                # Gerando e enviando resposta
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message':'book associated to author'}).encode('utf-8'))
                
            # Considerando uma requisicao inexistente
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'Invalid request format'}).encode('utf-8'))
    
        # GET
    def do_GET(self):
        # Definindo a rota geral (sem parametros)
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Escolha entre as rotas:\nbooks\nauthors\n')
        
        #  Acessando os livros da "tabela"
        elif self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # "Retornando" todos os livros
            response = data_store['book_store']
            self.wfile.write(json.dumps(response).encode('utf-8'))

        # Acessando informacoes de um livro especifico
        elif self.path.startswith('/books/'):

            # Obtendo o livro a partir do id
            book_id = int(self.path.split('/')[-1])
            book = data_store['book_store'].get(book_id)

            # Caso o livro exista
            if book:
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(book).encode('utf-8'))

            # Caso contrario
            else:
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'book not found'}).encode('utf-8'))
        
        # Acessando todos os autores
        elif self.path == '/authors':

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Gerando e retornando a resposta
            response = data_store['author_store']
            self.wfile.write(json.dumps(response).encode('utf-8'))

        # Acessando informacoes especificas de um autor
        elif self.path.startswith('/authors/') and '/books' not in self.path:

            # Obtendo o autor
            author_id = int(self.path.split('/')[-1])
            author = data_store['author_store'].get(author_id)

            # Verificando a existencia do autor
                # Caso ele exista
            if author:
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(author).encode('utf-8'))

                # Caso contrario
            else:
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'author not found'}).encode('utf-8'))

        # Acessando os livros de um autor especifico
        elif self.path.startswith('/authors/') and '/books' in self.path:

            # Anotando o id do autor
            if len(self.path.split('/')) == 4:
                author_id = int(self.path.split('/')[2])

                # Verificando se o autor esta na base de dados
                if author_id not in data_store['author_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Author not found'}).encode('utf-8'))
                    return
                
                # Caso contrario, pega-se os livros do autor
                books = [book for book in data_store['book_store'].values() if book.get('author_id') == author_id]

                # Enviando um resposta
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(books).encode('utf-8'))

            # Considerando formato invalido de requisicao
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'Invalid request format'}).encode('utf-8'))

        # PUT   
    def do_PUT(self):
        # Atualizando algum valor de livros
        if self.path.startswith('/books/'):

            # Pegando o id do livro a ser atualizado
            book_id = int(self.path.split('/')[-1])

            # Verificando a existencia do livro na base de dados
                # Caso nao exista
            if book_id not in data_store['book_store']:
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'book not found'}).encode('utf-8'))
            
            # Caso contrario
                # Obtendo os dados a serem atualizados
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            book_data = json.loads(put_data)

            # Criando variaveis para dados de livro existentes para caso nao seja alterado
            ex_title = ""
            ex_genre = ""
            ex_year = ""
            ex_author_id = ""


            if not book_data.get('title'):
                ex_title = data_store['book_store'][book_id]['title']
            if not book_data.get('genre'):
                ex_genre = data_store['book_store'][book_id]['genre']
            if not book_data.get('year'):
                ex_year = data_store['book_store'][book_id]['year']
            if not book_data.get('author_id'):
                ex_author_id = data_store['book_store'][book_id]['author_id']
            
            print(f'Updating book {book_id}')

            # Atualizando as coisas que precisam ser mudadas
            data_store['book_store'][book_id] = {

                # Caso não haja alteracoes, pega a variavel do valor anterior
                'title' : book_data.get('title', ex_title),
                'genre' : book_data.get('genre',ex_genre),
                'year' : book_data.get('year',ex_year),
                'author_id' : book_data.get('author_id',ex_author_id)
            }

            # Enviando uma resposta
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message':'book updated'}).encode('utf-8'))

        # Atualizando um autor
        elif self.path.startswith('/authors/'):
            author_id = int(self.path.split('/')[-1])

            # Verificando se o autor nao esta presente no banco de dados
            if author_id not in data_store['author_store']:
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'author not found'}).encode('utf-8'))
            
            # Recebendo as informacoes a serem atualizadas
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            author_data = json.loads(put_data)

            # Criando variaveis para dados de livro existentes para caso nao seja alterado
            ex_name = ""
            ex_birthday = ""
            ex_nationality = ""

            if not author_data.get('name'):
                ex_name = data_store['author_store'][author_id]['name']
            if not author_data.get('birthday'):
                ex_birthday = data_store['author_store'][author_id]['birthday']
            if not author_data.get('nationality'):
                ex_nationality = data_store['author_store'][author_id]['nationality']
            
            # Atualizando o autor
            print(f'Updating author {author_id}')
            data_store['author_store'][author_id] = {
                'name' : author_data.get('name', ex_name),
                'birthday' : author_data.get('birthday', ex_birthday),
                'nationality' : author_data.get('nationality',ex_nationality),
            }

            # Enviando uma resposta
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message':'author updated'}).encode('utf-8'))

        # DELETE
    def do_DELETE(self):
        # Removendo um livro do banco de dados
        if self.path.startswith('/books/'):

            # Anotando o id do livro a ser deletado
            book_id = int(self.path.split('/')[-1])

            # Verificando a existencia do livro
                # Caso V, deleta o livro da base de dados
            if book_id in data_store['book_store']:
                del data_store['book_store'][book_id]
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                print(f'Deleting book {book_id}')
                self.wfile.write(json.dumps({'message':'book deleted'}).encode('utf-8'))

                # Caso F
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'book not found'}).encode('utf-8'))
        
        # Removendo um autor da base de dados
        elif self.path.startswith('/authors/') and '/books/' not in self.path:

            # Anotando o id do autor a ser deletado
            author_id = int(self.path.split('/')[-1])

            # Verificando se autor esta na base de dados
                # Caso sim
            if author_id in data_store['author_store']:
                del data_store['author_store'][author_id]
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                print(f'Deleting author {author_id}')
                self.wfile.write(json.dumps({'message':'author deleted'}).encode('utf-8'))

                # Caso nao
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'author not found'}).encode('utf-8'))

        # Removendo uma relacao entre autor e livro
        elif self.path.startswith('/authors/') and '/books/':

            # Verificando se o caminho do comando esta correto
            if len(self.path.split('/')) == 5:

                # Anotando os ids da relacao para remover
                author_id = int(self.path.split('/')[2])
                books_id = int(self.path.split('/')[4])

                # Verificando a inexistencia do autor na base de dados
                if author_id not in data_store['author_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Author not found'}).encode('utf-8'))
                    return
                
                # Verificando a inexistencia do livro na base de dados
                if books_id not in data_store['book_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Book not found'}).encode('utf-8'))
                    return
                
                # Recebendo o livro para tirar a relacao
                book = data_store['book_store'][books_id]
                if book.get('author_id') == author_id:

                    # Removendo a relacao, caso exista
                    data_store['book_store'][books_id]['author_id'] = ''

                # Enviando uma resposta
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message':'book desassociated to author'}).encode('utf-8'))
                
            # Considerando o erro de requisicao incorreta
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'Invalid request format'}).encode('utf-8'))

# Criando um metodo para rodar o servidor
def run():
    server_address = ('',8000)
    httpd = HTTPServer(server_address, Handler)
    print('Iniciando servidor...')
    httpd.serve_forever()

# Rodando o codigo
if __name__ == "__main__":
    run()
