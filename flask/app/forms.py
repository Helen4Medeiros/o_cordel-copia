from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, HiddenField, SelectMultipleField, \
    SelectField, DateField, TextAreaField 
from wtforms.validators import DataRequired, ValidationError, \
    Optional, EqualTo
from wtforms import widgets
from markupsafe import Markup
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Autenticar')

class CategoriaForm(FlaskForm):
    id = HiddenField('id')
    nome = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class CursoForm(FlaskForm):
    id = HiddenField('id')
    nome = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class AutorForm(FlaskForm):
    id = HiddenField('id')
    nome = StringField('Nome*', validators=[DataRequired()])
    pseudonimo = StringField('Pseudônimo')
    contato = StringField('Contato')
    id_cursos = SelectMultipleField('Cursos')
    submit = SubmitField('Salvar')

    def fill_choices(self, cursos):
        self.id_cursos.choices = []
        self.id_cursos.choices.extend([(c.id, c.nome) for c in cursos])

class PesquisaAutorForm(FlaskForm):
    nome_ou_pseudonimo = StringField('Nome ou Pseudônimo')
    id_curso = SelectField('Curso')
    submit = SubmitField('Pesquisar')
    
    def validate_id_curso(form, field):
        if not form.id_curso.data and not form.nome_ou_pseudonimo.data:
            raise ValidationError('Informe pelo menos um dos campos de pesquisa.')
        return True
    
    def fill_choices(self, cursos):
        self.id_curso.choices = [('', '')]
        self.id_curso.choices.extend([(c.id, c.nome) for c in cursos])

class PesquisaCordeisForm(FlaskForm):
    titulo_ou_subtitulo = StringField('Título ou subtítulo')
    autor = StringField('Autor', render_kw={'placeholder': 'Nome ou pseudônimo'})
    id_categoria = SelectField('Categoria')
    id_curso = SelectField('Curso')
    em_destaque = BooleanField('Em destaque')
    invisivel = BooleanField('Invisível')
    depois_de = DateField('Publicado depois de', validators=[Optional()])
    antes_de = DateField('Publicado antes de', validators=[Optional()])
    texto = StringField('Texto')
    submit = SubmitField('Pesquisar')

    def fill_choices(self, categorias, cursos):
        self.id_categoria.choices = [('','')]
        self.id_categoria.choices.extend([(c.id, c.nome) for c in categorias])
        self.id_curso.choices = [('','')]
        self.id_curso.choices.extend([(c.id, c.nome) for c in cursos])
    
    def validate_id_curso(form, field):
        if not form.titulo_ou_subtitulo.data and not form.autor.data and \
            not form.id_categoria.data and not form.id_curso.data and \
            not form.em_destaque.data and not form.depois_de.data and \
            not form.antes_de.data and not form.texto.data and not form.invisivel.data:
            raise ValidationError('Informe pelo menos um dos campos de pesquisa.')
        return True

class WidgetMultipleHiddenInput:
    '''
    Widget para múltiplas ocorrências de um campo input do tipo 
    hidden, as quais compartilham o mesmo name.
    '''
    html_params = staticmethod(widgets.core.html_params)
    validation_attrs = ["required"]

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", "hidden")
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        input_params = self.html_params(name=field.name, **kwargs)
        html = ''
        for v in field._value():
            html += f"<input {input_params} value=\"{v}\">"
        return Markup(html)

class MultipleHiddenInput(StringField):
    '''
    Campo que permite múltiplas ocorrências de um campo hidden, 
    as quais compartilham o mesmo name.
    '''
    widget = WidgetMultipleHiddenInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist

    def _value(self):
        return self.data if self.data is not None else ""

class CadastroCordelForm(FlaskForm):
    id = HiddenField('id')
    titulo = StringField('*Título', validators=[DataRequired()])
    subtitulo = StringField('Subtítulo')
    # autores
    pesquisa_autor = StringField(
        '*Autores', 
        render_kw={
            'autocomplete': 'off'
        }
    )
    # o campo autores guarda valores no formato ID:NOME DO AUTOR
    autores = MultipleHiddenInput(None, validators=[DataRequired()])
    id_categorias = SelectMultipleField('*Categorias', validators=[DataRequired()])
    em_destaque = BooleanField('Em destaque')
    data_publicacao = DateField('*Data de Publicação', validators=[DataRequired()])
    visivel = BooleanField('Vísivel', default=True)
    # capa
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
    capa = FileField(
        'Capa', 
        validators=[
            FileAllowed(extensoes_permitidas, 'Tipo de arquivo não permitido.')
        ]
    )
    estrofes = TextAreaField(
        '*Estrofes', 
        validators=[DataRequired()], 
        default='##pagina##\nLorem ipsum\nDolor sit amet\n##pagina##\nLorem ipsum\nDolor sit amet'
    )
    submit = SubmitField('Salvar')

    def validar_extensao_da_capa(self):
        arquivoCapa = self.capa.data[0]
        if not arquivoCapa or not arquivoCapa.filename:
            return True
        return '.' in arquivoCapa.filename and \
           arquivoCapa.filename.rsplit('.', 1)[1].lower() in self.extensoes_permitidas

    def fill_choices(self, categorias):
        self.id_categorias.choices = []
        self.id_categorias.choices.extend([(c.id, c.nome) for c in categorias])


# ADMINISTRADOR
class AdministradorForm(FlaskForm):
    id = HiddenField('id')
    nome = StringField('Nome', validators=[DataRequired()])
    matricula = StringField('Matricula', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    ativo = BooleanField("ativo", default=True)
    submit = SubmitField("Salvar")

    