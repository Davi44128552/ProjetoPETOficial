from Livro import Livro
from Autor import Autor

class MetodosAPI:
    # Criando um construtor
    def __init__(self):
        # Variaveis para armazenar os ids
        self.id_autor = 1
        self.id_livro = 1

        # Dicionarios para armazenar os autores e livros
        self.bd_Autor = {}
        self.bd_Livro = {}

# Trabalhando com livros
    # Metodo para criar um livro
    def criar_livro(self, dicionario):
        livro = Livro(self.id_livro, dicionario["titulo"], dicionario["genero"], dicionario["ano"], dicionario["autor_id"])
        self.bd_Livro[self.id_livro] = livro
        self.id_livro += 1

     # Metodo para listar os livros
    def listar_livros(self):
        livros = {}
        for id, livro in self.bd_Livro.items():
            livros[id] = livro.retornar_dicionario()
        return livros
    
    # Metodo para obter uma info especifica de um livro
    def info_livro(self, id):
        return self.bd_Livro[int(id)].retornar_dicionario()
    
    # Metodo para atualizar um livro
    def atualizar_livro(self, id, dicionario):
        livro = self.bd_Livro[int(id)]
        
        if dicionario["titulo"] != None:
            livro.titulo = dicionario["titulo"]

        if dicionario["genero"] != None:
            livro.genero = dicionario["genero"]

        if dicionario["ano"] != None:
            livro.ano = dicionario["ano"]

        if dicionario["autor_id"] != None:
            livro.autor_id = dicionario["autor_id"]

    # Metodo para excluir um livro
    def excluir_livro(self, id):
        livro = self.bd_Livro[int(id)]
        del self.bd_Livro[int(id)]
        self.excluir_associacao(livro.autor_id,livro.id) 

# Trabalhando com autores
    # Metodo para criar um autor
    def criar_autor(self, dicionario):
        autor = Autor(self.id_autor, dicionario["nome"], dicionario["data_nascimento"], dicionario["nacionalidade"])
        self.bd_Autor[self.id_autor] = autor
        self.id_autor += 1

     # Metodo para listar os autores
    def listar_autores(self):
        autores = {}
        for id, autor in self.bd_Autor.items():
            autores[id] = autor.retornar_dicionario()
        return autores
    
    # Metodo para obter uma info especifica de um autor
    def info_autor(self, id):
        return self.bd_Autor[int(id)].retornar_dicionario()
    
    # Metodo para atualizar um autor
    def atualizar_autor(self, id, dicionario):
        autor = self.bd_Autor[int(id)]
        
        if dicionario["nome"] != None:
            autor.nome = dicionario["nome"]

        if dicionario["data_nascimento"] != None:
            autor.data_nascimento = dicionario["data_nascimento"]

        if dicionario["nacionalidade"] != None:
            autor.nacionalidade = dicionario["nacionalidade"]

    # Metodo para excluir um autor
    def excluir_autor(self, id):
        autor = self.bd_Autor[int(id)]
        for livro in autor.livros:
            self.excluir_associacao(autor.id, livro.id)
        del self.bd_Autor[int(id)]
        
        # Deletar_Associacao(autor) 

# Trabalhando com as associacoes
    # Metodo para criar uma associacao entre um autor e um livro
    def criar_associacao(self, id_autor, id_livro):
        self.bd_Autor[id_autor].livros[self.bd_Livro[id_livro].id] = (self.bd_Livro[id_livro])
        self.bd_Livro[id_livro].autor_id = self.bd_Autor[id_autor].id

    # Metodo para listar todos os livros de um autor
    def listar_livros_do_autor(self, id_autor):
        return self.bd_Autor[int(id_autor)].livros
    
    # Metodo para excluir associacao entre livro e autor
    def excluir_associacao(self, id_autor, id_livro):
        # Procurando livro em autor
        if id_livro in self.bd_Autor[id_autor].livros:
            # Removendo o livro do autor
            del self.bd_Autor[id_autor].livros[id_livro]

            # Removendo o autor do livro
            self.bd_Livro[id_livro].autor_id = None
