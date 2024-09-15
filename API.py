import http.server
import socketserver
from API2 import Classe_Handler  # Importe a classe de manipulação

# Porta que o servidor vai escutar
PORT = 8100

# Criando o servidor com o handler personalizado
Handler = Classe_Handler

# Instanciando o servidor
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Servidor rodando na porta {PORT}")
    httpd.serve_forever()
