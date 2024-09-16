from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data_store = {
    'book_store' : {},
    'author_store' : {}
}

book_id_counter = 1
author_id_counter = 1

class Handler(BaseHTTPRequestHandler):
    #id para os livros (gerado automaticamente)
    @staticmethod
    def generate_book_id():
        global book_id_counter
        book_id = book_id_counter
        book_id_counter += 1
        return book_id
    
    @staticmethod
    def generate_author_id():
        global author_id_counter
        author_id = author_id_counter
        author_id_counter += 1
        return author_id 
    
    #Métodos HTTP para as rotas dos livros
    def do_POST(self):
        if self.path == '/books':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(post_data)
                title = data.get('title')
                genre = data.get('genre','')
                year = data.get('year','')
                author_id = data.get('author_id','')

                if not title:
                    self.send_response(400)
                    response = {'error' : 'title is required'}
                    self.wfile.write(b'Error: Title is Required')
                else:
                    book_id = Handler.generate_book_id()
                    data_store['book_store'][book_id] = {
                        'title': title,
                        'genre' : genre,
                        'year' : year,
                        'author_id' : author_id
                    }
                    self.send_response(200)
                    response = {'message': 'Book created', 'book_id': book_id}
            
            except json.JSONDecodeError:
                self.send_response(400)
                response = {'error': 'Invalid JSON'}
            
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        elif self.path == '/authors':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(post_data)
                name = data.get('name')
                birthday = data.get('birthday','')
                nationality = data.get('nationality','')

                if not name:
                    self.send_response(400)
                    response = {'error' : 'Name is required'}
                    self.wfile.write(b'Error: Name is Required')
                else:
                    author_id = Handler.generate_author_id()
                    data_store['author_store'][author_id] = {
                        'name': name,
                        'birthday' : birthday,
                        'nationality' : nationality
                    }
                    self.send_response(200)
                    response = {'message': 'Author created', 'author_id': author_id}
            
            except json.JSONDecodeError:
                self.send_response(400)
                response = {'error': 'Invalid JSON'}
            
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path.startswith('/authors/') and '/books/' in self.path:
            #rota '/authors/{author_id}/books/{books_id}
            if len(self.path.split('/')) == 5:
                author_id = int(self.path.split('/')[2])
                books_id = int(self.path.split('/')[4])

                if author_id not in data_store['author_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Author not found'}).encode('utf-8'))
                    return
                
                if books_id not in data_store['book_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Book not found'}).encode('utf-8'))
                    return
                
                data_store['book_store'][books_id]['author_id'] = author_id

                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message':'book associated to author'}).encode('utf-8'))
                
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'Invalid request format'}).encode('utf-8'))
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Escolha entre as rotas:\nbooks\nauthors\n')
        
        elif self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = data_store['book_store']
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            book = data_store['book_store'].get(book_id)
            if book:
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(book).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'book not found'}).encode('utf-8'))
        
        elif self.path == '/authors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = data_store['author_store']
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif self.path.startswith('/authors/') and '/books' in self.path:
            if len(self.path.split('/')) == 4:
                author_id = int(self.path.split('/')[2])

                if author_id not in data_store['author_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Author not found'}).encode('utf-8'))
                    return
                
                books = [book for book in data_store['book_store'].values() if book.get('author_id') == author_id]

                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(books).encode('utf-8'))

            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'Invalid request format'}).encode('utf-8'))

        elif self.path.startswith('/authors/') and '/books' not in self.path:
            author_id = int(self.path.split('/')[-1])
            author = data_store['author_store'].get(author_id)
            if author:
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps(author).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'author not found'}).encode('utf-8'))
    
    def do_PUT(self):
        if self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            if book_id not in data_store['book_store']:
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'book not found'}).encode('utf-8'))
            
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            book_data = json.loads(put_data)

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
            
            print(f'Updatind book {book_id}')
            data_store['book_store'][book_id] = {
                'title' : book_data.get('title', ex_title),
                'genre' : book_data.get('genre',ex_genre),
                'year' : book_data.get('year',ex_year),
                'author_id' : book_data.get('author_id',ex_author_id)
            }

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message':'book updated'}).encode('utf-8'))

        elif self.path.startswith('/authors/'):
            author_id = int(self.path.split('/')[-1])
            if author_id not in data_store['author_store']:
                self.send_response(404)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'author not found'}).encode('utf-8'))
            
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length).decode('utf-8')
            author_data = json.loads(put_data)

            ex_name = ""
            ex_birthday = ""
            ex_nationality = ""

            if not author_data.get('name'):
                ex_name = data_store['author_store'][author_id]['name']
            if not author_data.get('birthday'):
                ex_birthday = data_store['author_store'][author_id]['birthday']
            if not author_data.get('nationality'):
                ex_nationality = data_store['author_store'][author_id]['nationality']
            
            print(f'Updatind author {author_id}')
            data_store['author_store'][author_id] = {
                'name' : author_data.get('name', ex_name),
                'birthday' : author_data.get('birthday', ex_birthday),
                'nationality' : author_data.get('nationality',ex_nationality),
            }

            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message':'author updated'}).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            if book_id in data_store['book_store']:
                del data_store['book_store'][book_id]
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                print(f'Deleting book {book_id}')
                self.wfile.write(json.dumps({'message':'book deleted'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'book not found'}).encode('utf-8'))
        
        elif self.path.startswith('/authors/') and '/books/' not in self.path:
            author_id = int(self.path.split('/')[-1])
            if author_id in data_store['author_store']:
                del data_store['author_store'][author_id]
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                print(f'Deleting author {author_id}')
                self.wfile.write(json.dumps({'message':'author deleted'}).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'author not found'}).encode('utf-8'))

        elif self.path.startswith('/authors/') and '/books/':
            if len(self.path.split('/')) == 5:
                author_id = int(self.path.split('/')[2])
                books_id = int(self.path.split('/')[4])

                if author_id not in data_store['author_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Author not found'}).encode('utf-8'))
                    return
                
                if books_id not in data_store['book_store']:
                    self.send_response(404)
                    self.send_header('Content-type','application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error':'Book not found'}).encode('utf-8'))
                    return
                
                book = data_store['book_store'][books_id]
                if book.get('author_id') == author_id:
                    data_store['book_store'][books_id]['author_id'] = ''

                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message':'book desassociated to author'}).encode('utf-8'))
                
            else:
                self.send_response(400)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error':'Invalid request format'}).encode('utf-8'))

def run():
    server_address = ('',8000)
    httpd = HTTPServer(server_address, Handler)
    print('Iniciando servidor...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
