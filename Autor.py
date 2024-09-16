# Criando a classe do autor
class Autor:

    # Criando o construtor da classe
    def __init__(self, id, nome, data_nascimento = None, nacionalidade = None):
        # id
        self.id = id

        # nome
        self.nome = nome

        # data de nascimento
        self.data_nascimento = data_nascimento

        # nacionalidade
        self.nacionalidade = nacionalidade

        # lista com os livros
        self.livros = {}

    # Metodo para retornar todas as informacoes do autor
    def retornar_dicionario(self):
        dicionario = {"nome" : self.nome, "data_nascimento" : self.data_nascimento, "nacionalidade" : self.nacionalidade}
        return dicionario
