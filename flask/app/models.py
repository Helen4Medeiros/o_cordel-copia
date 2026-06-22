from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Curso:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Autor:
    def __init__(self, id, nome, pseudonimo, contato, cursos):
        self.id = id
        self.nome = nome
        self.pseudonimo = pseudonimo
        self.contato = contato
        self.cursos = [*cursos] if cursos else []

class Cordel:
    def __init__(self):
        self.id = None
        self.titulo = None
        self.subtitulo = None
        self.destaque = False
        self.visivel = True
        self.data_publicacao = None
        self.data_cadastro = None
        self.imagem_capa = None
        self.mime_type_capa = None
        self.autores = []
        self.paginas = []
        self.categorias = []
    
    def __str__(self):
        return f'Cordel(id={self.id}, titulo="{self.titulo}")'
    
    def cursos_dos_autores(self):
        cursos = set()
        for a in self.autores:
            if a.cursos:
                cursos.update(a.cursos)
        return cursos

class Pagina:
    def __init__(self, id, numeracao, estrofes, cordel):
        self.id = id
        self.numeracao = numeracao
        self.estrofes = estrofes
        self.cordel = cordel

class Administrador(UserMixin):
    def __init__(self):
        self.id = None
        self.nome = None
        self.matricula = None
        self.ativo = False
        self.hash_senha = None
    
    def senha_valida(self, senha):
        return check_password_hash(self.hash_senha, senha)
    
    def set_senha(self, senha):
        self.hash_senha = generate_password_hash(senha)

    def __repr__(self):
        return '<Admin %r>' % self.nome

    # Métodos do Flask-Login
    def get_id(self):
        return self.id
    
    @property
    def is_active(self):
        return self.ativo