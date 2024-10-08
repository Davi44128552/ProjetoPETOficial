# ProjetoPET
Equipe F:
  - Livian Jhennifer Nascimento
  - Davi Iury Lopes Souza
  - Isaac Mosiah Bandeira

## API de Gestão de Biblioteca
Uma API REST para gerenciar uma pequena biblioteca. A API permite
adicionar, listar, editar, e remover livros e autores, além de associar livros aos seus respectivos
autores.

## Instalação
Nâo é necessário nenhuma instalação extraordinária. Não foram usadas frameworks. As únicas bibliotecas no código são http.server e json.

## Uso
A API está configurada para rodar no localhost:8000. <br/>
Primeiro, abra um terminal e execute o arquivo `app.py`. Depois, em outro terminal, execute os comandos desejados. <br/>
Você pode fazer as requisições GET utilizando o seu navegador através da barra de navegação. Porém, os métodos POST, PUT e DELETE terão que ser feitos no terminal.

### PowerShell
Se você estiver usando o PowerShell para testar as rotas, recomendamos usar o cmdlet `Invoke-RestMethod` da seguinte maneira:
  - **POST Method (Exceto Associação de Livro e Autor)** <br/>
`Invoke-RestMethod -Method Post -Uri http://localhost:8000/{rota_desejada} -Header @{'Content-Type' = 'application/json'} -Body '{"key":"value"}'` <br/>

  - **PUT Method** <br/>
`Invoke-RestMethod -Method Put -Uri http://localhost:8000/{rota_desejada} -Header @{'Content-Type' = 'application/json'} -Body '{"key":"value"}'` <br/>
_OBS: Não é necessário colocar todos as keys e values no body. A API foi configurada de modo que você possa apenas enviar as keys que serão alteradas._ <br/>

  - **DELETE Method** <br/>
`Invoke-RestMethod -Method Delete -Uri http://localhost:8000/{rota_desejada}` <br/>

  - **POST Method Para Associação de Autores e Livros** <br/>
`Invoke-RestMethod -Method Post -Uri http://localhost:8000/authors/{id_autor}/books/{id_livro} -Header @{'Content-Type' = 'application/json'}` <br/>
O método POST nessa rota faz a associação entre o id do autor e o id do livro automaticamente. <br/>

  - **GET Method** <br/>
Caso você queira testar o método get no terminal, você também pode usar o cmdlet `Invoke-RestMethod` da seguinte forma:
`Invoke-RestMethod -Method Get -Uri http://localhost:8000/{rota_desejada}`

### Curl
Caso você estiver usando Linux, é possível testar as rotas através do `curl` no terminal da seguinte forma:
 - **POST (No caso de livros e autores)** <br/>
`curl -X POST http://localhost:8000/{rota_desejada} -H "Content-Type: application/json" -d '{"chave":"valor"}'` <br/>

 - **POST (No caso de associacoes)** <br/>
`curl -X POST http://localhost:8000/{rota_desejada}`

 - **GET** <br/>
`curl -X GET http://localhost:8000/{rota_desejada}`

 - **PUT** <br/>
 `curl -X PUT http://localhost:8000/{rota_desejada} -H "Content-Type: application/json" -d '{"chave": "valor"}'`

 - **DELETE** <br/>
`curl -X DELETE http://localhost:8000/{rota_desejada}`

### Curl
Aqui estão alguns exemplos
POST:
       ` Associacao`
    `curl -X POST http://localhost:8000/authors/1/books/1`

        Autor
    curl -X POST http://localhost:8000/authors -H "Content-Type: application/json" -d '{"name":"Shakespeare", "birthday":"1800", "nationality":"britanico"}'

        Livro
    curl -X POST http://localhost:8000/books -H "Content-Type: application/json" -d '{"title": "Romeu e Julieta","genre":"romance", "year":1999, "author_id":""}'

  GET:
        `Associacao
    curl -X GET http://localhost:8000/authors/1/books`

        Autores
    curl -X GET http://localhost:8000/authors/{id_autor} 
    curl -X GET http://localhost:8000/authors

        Livros
    curl -X GET http://localhost:8000/books/{id_livro}
    curl -X GET http://localhost:8000/books

  PUT
        `Autores
    curl -X PUT http://localhost:8000/authors/{id_autor} -H "Content-Type: application/json" -d '{informacoes a serem alteradas}'`

        Livros
    curl -X PUT http://localhost:8000/books/{id_livro} -H "Content-Type: application/json" -d '{informacoes a serem alteradas}'

  DELETE
        `Associacao
    curl -X DELETE localhost:8000/authors/{id_autor}/books/{id_livro}`

        Autores
    curl -X DELETE localhost:8000/authors/{id_autor}

        Livros
    curl -X DELETE localhost:8000/books/{id_livro}

  
