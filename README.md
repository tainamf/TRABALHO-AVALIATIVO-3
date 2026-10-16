# TRABALHO-AVALIATIVO-3
## 1. Descrição do Modelo de Negócio Escolhido
O sistema consiste em uma *API RESTful de gerenciamento de biblioteca, projetada para controlar o acervo literário e o corpo de escritores de uma instituição. O modelo baseia-se em duas entidades principais: **Autores* e *Livros*.

* *Autores:* Representa os escritores cadastrados no sistema (Nome obrigatório e Nacionalidade opcional).
* *Livros:* Representa as obras literárias (Título, Ano de publicação opcional, Status de disponibilidade booleano e vínculo obrigatório com um autor).

*Regras de Negócio Implementadas:*
* *Integridade Referencial:* Validação automática para garantir que um livro só seja cadastrado ou atualizado se o autor correspondente existir (404 se não encontrado).
* *Proteção de Exclusão:* O sistema impede a exclusão de um autor que possua livros cadastrados, retornando o status 409 Conflict.
* *Filtros Dinâmicos:* A listagem de livros (GET /livros/) suporta filtro opcional por autor_id.

---

## 2. Diagrama ou Descrição das Entidades e do Relacionamento

### *Entidades e Atributos*
* *autores*
  * id (INTEGER, Primary Key)
  * nome (VARCHAR(100), Not Null)
  * nacionalidade (VARCHAR(50), Nullable)

* *livros*
  * id (INTEGER, Primary Key)
  * titulo (VARCHAR(150), Not Null)
  * ano_publicacao (INTEGER, Nullable)
  * disponivel (BOOLEAN, Not Null)
  * autor_id (INTEGER, Foreign Key -> autores.id, Not Null)

### *Relacionamento*
* *1 para N (Um para Muitos):* Um *Autor* pode possuir vários *Livros, e cada **Livro* pertence a um único *Autor*.

---

## 3. Instruções de Instalação, Migração e Execução

1. *Clone o repositório:*
   ```bash
   git clone [https://github.com/tainamf/TRABALHO-AVALIATIVO-3.git](https://github.com/tainamf/TRABALHO-AVALIATIVO-3.git)
   cd TRABALHO-AVALIATIVO-3

2.  Crie e ative o ambiente virtual:

Bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

3.Instale as dependências:

Bash
pip install -r requirements.txt
Execute as migrações do banco de dados (Alembic):

Bash
alembic upgrade head

4.Inicie a aplicação:

Bash
uvicorn app.main:app --reload
Acesse a documentação interativa em: http://127.0.0.1:8000/docs
 
 5. Lista dos Endpoints Implementados:

 Autores (/autores)
POST /autores/ — Cadastra um novo autor.

GET /autores/ — Lista todos os autores.

GET /autores/{autor_id} — Busca um autor pelo ID.

PUT /autores/{autor_id} — Atualiza os dados de um autor.

DELETE /autores/{autor_id} — Remove um autor (bloqueado se houver livros vinculados).

 Livros (/livros)
POST /livros/ — Cadastra um novo livro.

GET /livros/ — Lista todos os livros (suporta ?autor_id=X).

GET /livros/{livro_id} — Busca um livro pelo ID (inclui dados do autor).

PUT /livros/{livro_id} — Atualiza os dados de um livro.

DELETE /livros/{livro_id} — Remove um livro do sistema.
