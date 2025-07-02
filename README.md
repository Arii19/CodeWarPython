# API de Livros com FastAPI

Essa é uma API simples para gerenciar uma coleção de livros, criada com FastAPI. Ela permite consultar, criar, editar e excluir livros armazenados em uma lista em memória.

---

## Endpoints

    - localhost/livros (GET)
    - localhost/livros (POST)
    - localhost/livros/id (GET)
    - localhost/livros/id (PUT)
    - localhost/livros (DELETE)


### Consultar todos os livros

- **URL:** `/livros`
- **Método:** GET
- **Descrição:** Retorna a lista completa de livros.
- **Resposta:** Lista de objetos `Livro`.

### Consultar livro por ID

- **URL:** `/livros/{id}`
- **Método:** GET
- **Descrição:** Retorna o livro que corresponde ao ID informado.
- **Resposta:** Objeto `Livro`.
- **Erro:** Retorna 404 se o livro não for encontrado.

### Criar novo livro

- **URL:** `/livros`
- **Método:** POST
- **Descrição:** Adiciona um novo livro à lista.
- **Corpo da Requisição:** Objeto JSON representando um livro com os campos:
  - `id` (int)
  - `título` (string)
  - `autor` (string)
- **Resposta:** Lista atualizada de livros.

### Editar livro por ID

- **URL:** `/livros/{id}`
- **Método:** PUT
- **Descrição:** Atualiza os dados do livro com o ID especificado.
- **Corpo da Requisição:** Objeto JSON com os dados atualizados do livro.
- **Resposta:** Objeto `Livro` atualizado.
- **Erro:** Retorna 404 se o livro não for encontrado.

### Excluir livro por ID

- **URL:** `/livros/{id}`
- **Método:** DELETE
- **Descrição:** Remove o livro com o ID especificado da lista.
- **Resposta:** Lista atualizada de livros.
- **Erro:** Retorna 404 se o livro não for encontrado.

---

## Modelo do Livro

```json
{
  "id": 1,
  "título": "O Senhor dos Anéis - A Sociedade do Anel",
  "autor": "J.R.R Tolkien"
}
