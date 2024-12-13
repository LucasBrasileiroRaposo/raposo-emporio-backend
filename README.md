# Sistema - Raposo Emporio
## Projeto SPRINT 1 - Sistema de Gerenciamento de Usuários

## Raposo Emporio
É uma loja de comidas, bebidas e doces da minha família. Com intuito de praticar meus conhecimentos em programação questionei minhas tias se as interessariam um sistema de gerencia de estoque personalizado e a partir daí tive a idea de usar para o meu projeto. No futuro pretendo completar a implementação desse sistema adicionando produtos, vendas e mais. Considerando que, dependendo da escala que tome até se transformar em um e-commerce.

## Objetivo
Sistema CRUD para gerenciar usuários, para o sistema do Raposo Emporio. Funcionalidade básica, inicial, da construção do sistema da loja para gerencia de clientes e admnistradores.

## Regras de negócio
Usuários podem se cadastrar por si só no sistema, nesse primeiro momento, o próprio pode escolher sua função, entre ADMIN e USER, e após o cadastro o usuário é levado a tela de login. Após a realização correta do login, passa para a tela principal onde se tem algumas informações de todos os usuários cadastrados no sistema, sendo que ADMINs podem ver todos eles, mas um USER pode ver apenas outros USERs. Outra regra do sistema, é que um usuário USER pode editar e excluir apenas o próprio perfil, não tendo se quer acesso a dados não mostrados na página principal, enquanto ADMINs conseguem ver os dados de outros users (mas não edita-los) e tem o poder de excluir o user.

## Back-End

### Tecnologias
- Flask (Python)
- SQLAlchemy
- JWT
- SQLite (Banco de Dados)
- Swagger

### Padrões de projetos
Devido ao conhecimento prévio que tenho na parte de back end, implementei alguns padrões de projetos, preparando o sistema para adições futuras e se tornar uma aplicação de maior escala. Alguns padrões utilizados foram:
- MVC
- Service-Repository
- DTO
- Singleton
- SOLID

O MVC, Service-Repository e SOLID estão presentes em todo o sistema, onde para cada entidade se tem presente um controller, um model, um repository e um service, DTO são utilizados para controle de dados passados, onde ao invés de se utilizar de objetos genéricos se tem o próprio DTO para aquela funcionalidade, favorecendo futuras reutilizações. Quanto ao padrão Singleton, devido a minha maior familiaridade com construção de sistemas em Java e com o uso de SpringBoot estudei padrões que era empregados nessa linguagem e nesse framework e pus em prática, visando maior eficiencia e consistência do sistema.

### Outras informações
Me desafiei a começar com o que mais tenho dificuldade que é a questão de autorização e autenticação, seja em qual for a linguagem. Com o uso de ferramentas como JWT, documentações e vídeos tutoriais, implementei em meu sistema essas funcionalidades

### Instruções para executar

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
    ```

2. Criar ambiente virtual na raiz do projeto
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instalar as dependências
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo .env: Crie um arquivo .env na raiz do projeto como definido no .env.example:
    ```bash
    SECRET_KEY=any_key_you_want
    DATABASE_URI = sqlite:///...
    PORT = 8080
    ```

5. Execute a aplicação:
- Estando na raiz do projeto:
    ```bash
    python .\src\main\raposo_emporio\app.py
    ```
- Estando na diretório raposo_emporio:
    ```bash
    python app.py
    ```
