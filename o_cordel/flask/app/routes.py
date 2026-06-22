from flask import render_template, flash, redirect, request, jsonify, Response
from flask_login import login_required, current_user, login_user, logout_user
from app import myApp, dao, forms, models, sql_engine, login_manager
from markupsafe import Markup, escape
from datetime import datetime, time, timezone

@myApp.template_filter()
def nl2br(value):
    """Securely replace all newline characters '\\n' by HTML '<br>' break tags."""
    safe_value = str(escape(value))
    formatted_value = safe_value.replace("\n", "<br>")
    return Markup(formatted_value)

def get_CategoriaDAO():
    return dao.CategoriaDAO(sql_engine)

def get_CursoDAO():
    return dao.CursoDAO(sql_engine)

def get_AutorDAO():
    return dao.AutorDAO(sql_engine)

def get_CordelDAO():
    return dao.CordelDAO(sql_engine)

def get_AdministradorDAO():
    return dao.AdministradorDAO(sql_engine)

@myApp.route('/')
@myApp.route('/index')
def index():
    return render_template('index.html')

### Login ###

@login_manager.user_loader
def load_user(user_id):
    return get_AdministradorDAO().get_por_ID(user_id)

@myApp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = get_AdministradorDAO().get_por_matricula(
            form.matricula.data
        )
        if user is None or not user.senha_valida(form.senha.data):
            flash('Usuário ou senha inválidos')
            return redirect('/login')
        login_user(user)
        return redirect('/')
    return render_template('login.html', form=form)

@myApp.route('/logout')
@login_required
def logout():
    logout_user() # Faz o logout do usuário
    return redirect('/')

@myApp.route('/novidades')
def novidades():
    lista_de_novidades = [
        {
            "titulo": "SECITEX IX",
            "descricao": "Convidamos toda a comunidade para prestigiar o projeto...",
            "imagem": "ilustracao-1.jpg"
        },
        {
            "titulo": "RETIRADA",
            "descricao": "Lamentamos informar que o cordel foi retirado...",
            "imagem": None  
        }
    ]
    falso_destaque = [
        {
            "titulo": "Título de Teste do Carrossel",
            "descricao": "Testando o layout",
            "imagem": "ilustracao-1.png"
        },
        {
            "titulo": "Segundo Destaque",
            "descricao": "Testando a troca de slide",
            "imagem": "ilustracao-1.png"
        }
    ]
    return render_template(
        'novidades.html',
        novidades=lista_de_novidades,
        destaques=falso_destaque  
    )

### Cordel ###
@myApp.route('/cordel_pesquisa')
def cordel_pesquisa():
    form = forms.PesquisaCordeisForm()
    form.fill_choices(
        get_CategoriaDAO().todos(), 
        get_CursoDAO().todos()
    )
    return render_template(
        'cordel_pesquisa.html', 
        form=form, 
        titulo="Pesquisa de cordéis"
    )

@myApp.route('/pesquisar_cordeis')
def pesquisar_cordeis():
    form = forms.PesquisaCordeisForm(request.args) # request.args é necessário devido ao método GET
    form.fill_choices(
        get_CategoriaDAO().todos(), 
        get_CursoDAO().todos()
    )
    if form.validate():
        id_curso = int(form.id_curso.data) if form.id_curso.data else None
        id_categoria = int(form.id_categoria.data) if form.id_categoria.data else None
        cordeis = get_CordelDAO().pesquisar(
            form.titulo_ou_subtitulo.data,
            form.autor.data, 
            id_categoria,
            id_curso, 
            form.em_destaque.data, 
            form.depois_de.data, 
            form.antes_de.data, 
            form.texto.data, 
            form.invisivel.data, 
            current_user.get_id()
        )
        return render_template(
            'cordel_pesquisa.html', 
            form=form, 
            titulo="Pesquisa de cordéis", 
            cordeis=cordeis
        )
    else:
        return render_template(
            'cordel_pesquisa.html', 
            form=form, 
            titulo="Pesquisa de cordéis"
        )

@myApp.route('/autores_por_nome_json')
def autores_por_nome_json():
    nome_ou_pseudonimo = request.args.get('nome')
    dados = get_AutorDAO().get_nomes_as_dic(nome_ou_pseudonimo)
    return jsonify(dados)

@myApp.route('/cordel_cadastro')
@login_required
def cordel_cadastro():
    form = forms.CadastroCordelForm()
    form.fill_choices(
        get_CategoriaDAO().todos()
    )
    return render_template(
        'cordel_cadastro.html', 
        form=form, 
        titulo="Cadastro de Cordel"
    )

@myApp.route('/alterar_cordel/<id>')
@login_required
def alterar_cordel(id):
    form = forms.CadastroCordelForm()
    form.fill_choices(
        get_CategoriaDAO().todos()
    )
    admin = True if current_user.is_authenticated else False
    cordel = get_CordelDAO().get_por_ID(id, admin)
    form.id.data = cordel.id
    form.titulo.data = cordel.titulo
    form.subtitulo.data = cordel.subtitulo
    form.em_destaque.data = cordel.destaque
    form.data_publicacao.data = cordel.data_publicacao
    form.visivel.data = cordel.visivel
    form.estrofes.data = "##pagina##\n" + \
        "\n##pagina##\n".join([pg.estrofes for pg in cordel.paginas])
    form.autores.data = [f'{a.id}:{a.nome}' for a in cordel.autores]
    form.id_categorias.data = [str(c.id) for c in cordel.categorias]
    if cordel.mime_type_capa:
        request.view_args['tem_capa'] = True
    return render_template(
        'cordel_cadastro.html', 
        form=form, 
        titulo="Alterar Cordel"
    )

@myApp.route('/salvar_cordel', methods=['POST'])
@login_required
def salvar_cordel():
    form = forms.CadastroCordelForm()
    form.fill_choices(
        get_CategoriaDAO().todos()
    )
    if form.validate_on_submit():
        cordel = models.Cordel()
        cordel.id = form.id.data
        cordel.titulo = form.titulo.data
        cordel.subtitulo = form.subtitulo.data
        cordel.destaque = form.em_destaque.data
        cordel.visivel = form.visivel.data
        cordel.data_publicacao = form.data_publicacao.data
        # paginas
        paginas = str_to_paginas(form.estrofes.data)
        cordel.paginas.extend(paginas)   
        # capa
        arquivoCapa = form.capa.data[0]
        if arquivoCapa and form.validar_extensao_da_capa():
            cordel.mime_type_capa = arquivoCapa.content_type
            cordel.imagem_capa = arquivoCapa.read()
        ids_autores = []
        for s in form.autores.data: # obtém ids dos autores
            idx = s.index(":")
            ids_autores.append( int(s[:idx]) )
        ids_categorias = [int(s) for s in form.id_categorias.data]
        get_CordelDAO().salvar(
            cordel, ids_autores, ids_categorias, current_user.get_id()
        )
        flash('Cordel salvo com sucesso')
        if cordel.id:
            return redirect(f'/alterar_cordel/{cordel.id}')
        return redirect(f'/cordel_cadastro')
    else:
        return render_template(
            'cordel_cadastro.html', 
            form=form, 
            titulo="Cadastro de Cordel"
        )

def str_to_paginas(str):
    '''
    Converte o conteúdo do campo de estrofes, presente na 
    página de cadastro de cordel, em objetos Pagina.
    '''
    paginas = []
    numero_pagina = 1
    blocos = str.split("##pagina##")
    for b in blocos:
        if b:
            estrofe = b.lstrip('\r').lstrip('\n').rstrip('\n').lstrip('\r')
            paginas.append(
                models.Pagina(None, numero_pagina, estrofe, None)
            )
            numero_pagina += 1
    return paginas

@myApp.route('/cordel/<id>')
def cordel(id):
    admin = True if current_user.is_authenticated else False
    cordel = get_CordelDAO().get_por_ID(id, admin)
    # TODO: tratar cordel não encontrado
    return render_template(
        'cordel.html', 
        cordel=cordel, 
        titulo=cordel.titulo
    )

@myApp.route('/capa_cordel/<id>')
def capa_cordel(id):
    admin = True if current_user.is_authenticated else False
    dados = get_CordelDAO().get_dados_de_capa(id, admin)
    if dados:
        imagem = dados[0]
        mime_type = dados[1]
        return Response(imagem, mimetype=mime_type)
    else:
        return "Imagem não encontrada", 404

### CRUD Categoria ###

@myApp.route('/crud_categorias')
@login_required
def crud_categorias():
    daoCat = get_CategoriaDAO()
    categorias = daoCat.todos()
    form = forms.CategoriaForm()
    return render_template('crud_categorias.html', categorias=categorias, form=form, titulo="Categorias")

@myApp.route('/salvar_categoria', methods=['POST'])
@login_required
def salvar_categoria():
    form = forms.CategoriaForm()
    daoCat = get_CategoriaDAO()
    if form.validate_on_submit():
        c = models.Categoria(id=form.id.data, nome=form.nome.data)
        daoCat.salvar(c)
        flash('Categoria salva com sucesso')
        return redirect('/crud_categorias')
    else:
        return render_template('crud_categorias.html', categorias=daoCat.todos(), form=form, titulo="Categorias")

@myApp.route('/excluir_categoria/<id>')
@login_required
def excluir_categoria(id):
    daoCat = get_CategoriaDAO()
    try:
        daoCat.excluir(id)
        flash('Categoria excluída com sucesso')
    except Exception as ex:
        print(ex) # TODO: log
        flash('Ocorreu um erro. Certifique-se de que a categoria não esteja em uso.')
    return redirect('/crud_categorias')

@myApp.route('/alterar_categoria/<id>')
@login_required
def alterar_categoria(id):
    daoCat = get_CategoriaDAO()
    categorias = daoCat.todos()
    form = forms.CategoriaForm()
    id_int = int(id)
    for c in categorias:
        if c.id == id_int:
            form.id.data = id_int
            form.nome.data = c.nome
    return render_template('crud_categorias.html', categorias=categorias, form=form, titulo="Categorias")

### CRUD Curso ###

@myApp.route('/crud_cursos')
@login_required
def crud_cursos():
    daoCurso = get_CursoDAO()
    cursos = daoCurso.todos()
    form = forms.CursoForm()
    return render_template('crud_cursos.html', cursos=cursos, form=form, titulo="Cursos")

@myApp.route('/salvar_curso', methods=['POST'])
@login_required
def salvar_curso():
    form = forms.CursoForm()
    daoCurso = get_CursoDAO()
    if form.validate_on_submit():
        c = models.Curso(id=form.id.data, nome=form.nome.data)
        daoCurso.salvar(c)
        flash('Curso salvo com sucesso')
        return redirect('/crud_cursos')
    else:
        return render_template('crud_cursos.html', cursos=daoCurso.todos(), form=form, titulo="Cursos")

@myApp.route('/excluir_curso/<id>')
@login_required
def excluir_curso(id):
    daoCurso = get_CursoDAO()
    try:
        daoCurso.excluir(id)
        flash('Curso excluído com sucesso')
    except Exception as ex:
        print(ex) # TODO: log
        flash('Ocorreu um erro. Certifique-se de que o curso não esteja em uso.')
    return redirect('/crud_cursos')

@myApp.route('/alterar_curso/<id>')
@login_required
def alterar_curso(id):
    daoCurso = get_CursoDAO()
    cursos = daoCurso.todos()
    form = forms.CursoForm()
    id_int = int(id)
    for c in cursos:
        if c.id == id_int:
            form.id.data = id_int
            form.nome.data = c.nome
    return render_template('crud_cursos.html', cursos=cursos, form=form, titulo="Cursos")

### CRUD Autor ###

@myApp.route('/crud_autores')
@login_required
def crud_autores():
    cursos = get_CursoDAO().todos()
    formAutor = forms.AutorForm()
    formAutor.fill_choices(cursos)
    formPesquisa = forms.PesquisaAutorForm()
    formPesquisa.fill_choices(cursos)
    return render_template('crud_autores.html', formAutor=formAutor, formPesquisa=formPesquisa, titulo="Autores")

@myApp.route('/pesquisar_autores', methods=['POST'])
@login_required
def pesquisar_autores():
    cursos = get_CursoDAO().todos()
    formPesquisa = forms.PesquisaAutorForm()
    formPesquisa.fill_choices(cursos)
    formAutor = forms.AutorForm()
    formAutor.fill_choices(cursos)
    if formPesquisa.validate_on_submit():
        daoAutor = get_AutorDAO()
        id_curso = int(formPesquisa.id_curso.data) if formPesquisa.id_curso.data else None
        autores = daoAutor.pesquisar(formPesquisa.nome_ou_pseudonimo.data, id_curso)
        return render_template('crud_autores.html', autores=autores, formAutor=formAutor, formPesquisa=formPesquisa, titulo="Autores")
    else:
        return render_template('crud_autores.html', formAutor=formAutor, formPesquisa=formPesquisa, titulo="Autores")

@myApp.route('/salvar_autor', methods=['POST'])
@login_required
def salvar_autor():
    cursos = get_CursoDAO().todos()
    formAutor = forms.AutorForm()
    formAutor.fill_choices(cursos)
    daoAutor = get_AutorDAO()
    if formAutor.validate_on_submit():
        a = models.Autor(
            id=formAutor.id.data, 
            nome=formAutor.nome.data, 
            pseudonimo=formAutor.pseudonimo.data, 
            contato=formAutor.contato.data, 
            cursos=[]
        )
        ids_cursos = [int(id_str) for id_str in formAutor.id_cursos.data]
        daoAutor.salvar(a, ids_cursos)
        flash('Autor salvo com sucesso')
        return redirect('/crud_autores')
    else:
        formPesquisa = forms.PesquisaAutorForm()
        formPesquisa.fill_choices(cursos)
        return render_template('crud_autores.html', formAutor=formAutor, formPesquisa=formPesquisa, titulo="Autores")

@myApp.route('/excluir_autor/<id>')
@login_required
def excluir_autor(id):
    daoAutor = get_AutorDAO()
    try:
        daoAutor.excluir(id)
        flash('Autor excluído com sucesso')
    except Exception as ex:
        print(ex) # TODO: log
        flash('Ocorreu um erro. Certifique-se de que o autor não tenha cordéis cadastrados.')
    return redirect('/crud_autores')

@myApp.route('/alterar_autor/<id>')
@login_required
def alterar_autor(id):
    cursos = get_CursoDAO().todos()
    formAutor = forms.AutorForm()
    formAutor.fill_choices(cursos)
    formPesquisa = forms.PesquisaAutorForm()
    formPesquisa.fill_choices(cursos)
    daoAutor = get_AutorDAO()
    autor = daoAutor.get_por_ID(int(id))
    formAutor.id.data = autor.id
    formAutor.nome.data = autor.nome
    formAutor.pseudonimo.data = autor.pseudonimo
    formAutor.contato.data = autor.contato
    formAutor.id_cursos.data = [str(c.id) for c in autor.cursos]
    return render_template('crud_autores.html', formAutor=formAutor, formPesquisa=formPesquisa, titulo="Autores")


@myApp.route('/crud_admin')
@login_required
def crud_admin():
    daoAdmin = get_AdministradorDAO()
    form = forms.AdministradorForm()
    administradores = daoAdmin.todos()
    return render_template('crud_admin.html',  form=form, administradores=administradores, titulo="Administradores")

@myApp.route('/salvar_admin', methods=['POST'])
@login_required
def salvar_admin():
    form = forms.AdministradorForm()
    daoAdmin = get_AdministradorDAO()
    if form.validate_on_submit():
        admin = models.Administrador()
        admin.id = form.id.data
        admin.nome = form.nome.data
        admin.matricula = form.matricula.data
        admin.ativo = form.ativo.data
        admin.hash_seha = admin.set_senha(form.password.data)
        if not admin.id:
            daoAdmin.salvar(admin)
            flash("Administrador criado com sucesso.")
        else:
            daoAdmin.salvar(admin)
            flash("Administrador alterado com sucesso.")
        return redirect('crud_admin')
    else:
        return render_template('crud_admin.html', form=form, titulo="Criar Administrador")
    
@myApp.route('/alterar_admin/<int:id>', methods=['POST', 'GET'])
@login_required
def alterar_admin(id):
    daoAdmin = get_AdministradorDAO()
    administradores = daoAdmin.todos()
    form = forms.AdministradorForm()
    id_int = int(id)
    for admin in administradores:
        if admin.id == id_int:
            form.id.data = id_int
            form.nome.data = admin.nome
            form.password.data = admin.hash_senha
            form.confirm_password.data = admin.hash_senha
            form.matricula.data = admin.matricula
            form.ativo.data = admin.ativo

    return render_template('crud_admin.html', administradores=administradores, form=form, titulo="Administradores")



@myApp.route('/excluir_admin/<int:id>', methods=['POST', 'GET'])
@login_required
def excluir_admin(id):
    daoAdmin = get_AdministradorDAO()
    try:
        daoAdmin.excluir(id)
        flash('Administrador excluído com sucesso')
    except Exception as ex:
        print(ex) # TODO: log
        flash('Ocorreu um erro.')
    
    return redirect('/crud_admin')

def metr_visitante(req):
    '''
        Coleta metricas do visitante
    '''
    now = datetime.now(timezone.utc)

    data = {
        'url': req.url, # url acessada
        'method': req.method, # metodo da requisição
        'user_agent': req.req.user_agent.string, # identifica o dispositivo e navegador
        'view_args': req.view_args, # Argumentos extraídos da URL
        'remote_addr': req.remote_addr, # O endereço IP do visitante.
        'authorization': bool(req.authorization), # bool que indica se a requisição tinha dados de autenticação.
        'path': req.path, # A parte do caminho da URL
        'date': int(time.mktime(now.timetuple())), # A data e hora atual convertida para um timestamp Unix
        'url_args': dict( # Um dicionário contendo todos os parâmetros de query da URL
            [(k, req.args[k]) for k in req.args] 
        )
    }
    
    

