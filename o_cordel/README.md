<div align="center">
  <h1>Ô Cordel</h1>
</div>

Este projeto tem o objetivo de publicizar, valorizar, estimular e preservar o acervo de cordéis escritos por alunos do CNAT/IFRN, que os produzem como atividade da disciplina de Língua Portuguesa e Literatura.

<h2>Equipe </h2>

**Membros atuais**
- [Alexandre Gomes de Lima](https://github.com/alexlimatds)
- [Danielle Freitas](https://github.com/danigfreitas)
- [Maria Júlia Gomes](https://github.com/maju-gomes)
- [Maria Helena Cunha](https://github.com/Helen4Medeiros)
- [Sofia Costa](https://github.com/sofiaacost4)

**Membros anteriores**
- Sílvia Mattos
- [Luís Felipe](https://github.com/LuisFelipe0731)
- [Pedro Lucas](https://github.com/pdroluc4as)
- [Raica Dandara](https://github.com/RaicaDandara)
- [Igor Jair](https://github.com/Igor-jair)
- [Maria Cândida](https://github.com/mmariacandida)
- [Rita de Cássia](https://github.com/Ritinhha)
- [Milton Shyon](https://github.com/Shyon246)

## Preparando o ambiente de desenvolvimento

**Requisitos:** Docker, Docker compose e VS Code.

### Clonando o repositório

Caso tenha problemas em clonar o repositório com seu usuário, abra um terminal e navegue até a pasta que irá conter o repositório. Em seguinda, execute o comando abaixo.

    git clone https://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@github.com/alexlimatds/o_cordel.git

### Construindo as imagens

Na pasta ``flask``, execute o comando:

    docker compose build

Não esqueça de remover os contêineres antigos.

### Criando e inicializando o banco de dados

Na pasta ``flask``, execute os contêineres do Postgres e do PgAdmin:

    docker compose --env-file .env.dev up -d db
    docker compose --env-file .env.dev up -d pgadmin

A execução do contêiner Postgres cria o banco de dados, mas ainda é preciso criar as suas tabelas. Para isso, acesse o PgAdmin no endereço ``localhost:8080``. Use ``admin@mail.com`` como nome de usuário e ``admin`` como senha.

**Adicionando o servidor de banco de dados:** clique com o botão direito do mouse sobre o nó ``servers`` e selecione a opção ``Register`` > ``Server``. Na guia ``General`` da janela de diálogo, preencha o campo ``Name`` com ``Postgres`` e ative a opção ``Connect Now``. Na guia ``Connection``, preencha o campo ``Host name/address`` com ``cordel_db``, o campo ``username`` com ``postgres``, o campo ``Password`` com ``postgres`` e ative a opção ``Save password``. Por fim, clique no botão ``Save``.

**Criando as tabelas:** expanda os nó ``Postgres`` e   depois o nó ``Databases``. Clique com o botão direito do mouse sobre o nó ``cordeldb`` e selecione a opção ``Query Tool``. Copie o conteúdo do arquivo ``bd\tabelas.sql`` no painel aberto e em seguida tecle F5.

**Populando o banco com dados iniciais:** execute as instruções do arquivo ``bd\dados_iniciais.sql`` com a ferramenta Query Tool.

**Populando o banco com dados de teste:** execute as instruções do arquivo ``bd\teste.sql`` com a ferramenta Query Tool.

## Executando a aplicação em ambiente de desenvolvimento

Na pasta ``flask``, execute os contêineres com o comando:

    docker compose --env-file env.dev up

Para encerrar a execução dos contêineres, basta teclar CTRL+C.

Para acessar a aplicação, acesse ``localhost`` ou ``127.0.0.1``.

Para abrir um terminal no contêiner da aplicação, execute:

    docker exec -it cordel_web_dev /bin/bash

**Usando o depurador**: é preciso conectar o VSCode com o depurador instalado no servidor. Para isso, abra a visão **Run and Debug** do VSCode, selecione a opção **Python Debbuger: Remote Attach** no componente drop-down e clique no botão de play (ou tecle F5).

## Diretórios e arquivos
<pre>
bd
docs
flask
  app/
    static/
    templates/
    __init__.py
    dao.py
    forms.py
    models.py
    routes.py
  config.py
  run.py
</pre>

<ul>
  <li>Diretório <b>bd</b>: artefatos do banco de dados.</li>
  <li>Arquivo <b>bd/dados_inicias.sql</b>: script com a carga inicial de dados de produção.</li>
  <li>Arquivo <b>bd/tabelas.sql</b>: script de criação das tabelas do banco de dados.</li>
  <li>Arquivo <b>bd/teste.sql</b>: script com uma carga de dados a ser utilizada em tempo de desenvolvimento.</li>
  <li>Diretório <b>docs</b>: documentação do projeto.</li>
  <li>Diretório <b>flask</b>: código-fonte do projeto (aplicação Flask).</li>
  <li>Diretório <b>app/static</b>: arquivos de HTML estáticos, JavaScript, CSS e imagens.</li>
  <li>Diretório <b>app/templates</b>: arquivos de template Jinja.</li>
  <li>Arquivo <b>app/__init__.py</b>: configurações da aplicação.</li>
  <li>Arquivo <b>app/dao.py</b>: classes de manipulação do banco de dados.</li>
  <li>Arquivo <b>app/forms.py</b>: classes de formulários web.</li>
  <li>Arquivo <b>app/models.py</b>: classes de modelo da aplicação.</li>
  <li>Arquivo <b>app/routes.py</b>: rotas HTTP da aplicação (controlador web/views).</li>
</ul>