class Livro:
    # Criando o construtor
    def __init__(self, id, titulo, genero = None, ano = None, autor_id = None):
        # id
        self.id = id

        # titulo
        self.titulo = titulo

        # genero
        self.genero = genero

        # ano
        self.ano = ano

        #id do autor
        self.autor_id = autor_id


    # Metodo para retornar todas as informacoes do livro
    def retornar_dicionario(self):
        dicionario = {"id": self.id, "titulo" : self.titulo, "genero" : self.genero, "ano" : self.ano, "autor_id" : self.autor_id}
        return dicionario