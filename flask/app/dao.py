from app import models
from sqlalchemy import text, select, MetaData, join, bindparam
from datetime import date

class CategoriaDAO:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine

    def todos(self):
        sql = text("SELECT id, nome FROM categoria")
        with self.sql_engine.connect() as connection:
            categorias = []
            result = connection.execute(sql)
            for r in result:
                categorias.append(
                    models.Categoria(r[0], r[1])
                )
            return categorias

    def salvar(self, categoria):
        params = {"nome": categoria.nome}
        if categoria.id:
            sql = text("UPDATE categoria SET nome = :nome WHERE id = :id")
            params['id'] = categoria.id
        else:
            sql = text("INSERT INTO categoria (nome) VALUES (:nome)")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, params)
            connection.commit()

    def excluir(self, id_categoria):
        sql = text("DELETE FROM categoria WHERE id = :id")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, {"id": id_categoria})
            connection.commit()

class CursoDAO:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine

    def todos(self):
        sql = text("SELECT id, nome FROM curso")
        with self.sql_engine.connect() as connection:
            cursos = []
            result = connection.execute(sql)
            for r in result:
                cursos.append(
                    models.Curso(r[0], r[1])
                )
            return cursos

    def salvar(self, curso):
        params = {"nome": curso.nome}
        if curso.id:
            sql = text("UPDATE curso SET nome = :nome WHERE id = :id")
            params['id'] = curso.id
        else:
            sql = text("INSERT INTO curso (nome) VALUES (:nome)")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, params)
            connection.commit()

    def excluir(self, id_curso):
        sql = text("DELETE FROM curso WHERE id = :id")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, {"id": id_curso})
            connection.commit()

class AutorDAO:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine

    def get_por_ID(self, id_autor):
        sql = text(
            "SELECT a.id, a.nome, a.pseudonimo, a.contato, c.id, c.nome "
            "FROM autor a LEFT JOIN autor_curso ac ON a.id = ac.id_autor "
            "LEFT JOIN curso c ON ac.id_curso = c.id WHERE a.id = :id_autor"
        )
        with self.sql_engine.connect() as connection:
            result = connection.execute(sql, {'id_autor': id_autor})
            for i, r in enumerate(result):
                if i == 0:
                    id_autor = r[0]
                    autor = models.Autor(id=r[0], nome=r[1], pseudonimo=r[2], contato=r[3], cursos=[])
                if r[4]:
                    autor.cursos.append(models.Curso(r[4], r[5]))
            return autor
        
    def get_nomes_as_dic(self, nome_ou_pseudonimo):
        sql = text(
            "SELECT a.id, a.nome, a.pseudonimo "
            "FROM autor a "
            "WHERE "
            "  a.nome ILIKE :nome OR "
            "  a.pseudonimo ILIKE :pseudonimo "
            "ORDER BY a.nome "
        )
        with self.sql_engine.connect() as connection:
            result = connection.execute(
                sql, 
                {
                    'nome': '%'+nome_ou_pseudonimo+'%', 
                    'pseudonimo': '%'+nome_ou_pseudonimo+'%'
                }
            )
            resultado_dic = {}
            for r in result:
                id_autor = r[0]
                nome = r[1]
                if r[2]:
                    nome += f'({r[2]})'
                resultado_dic[id_autor] = nome
            return resultado_dic

    def pesquisar(self, nome_ou_pseudonimo, id_curso):
        # 1ª etapa: obtém os IDs dos autores que atendem os critérios de pesquisa
        sql_str = (
            "SELECT DISTINCT a.id "
            "FROM autor a LEFT JOIN autor_curso ac ON a.id = ac.id_autor "
            "LEFT JOIN curso c ON ac.id_curso = c.id WHERE "
        )
        # cria filtros com base nos parâmetros informados
        filtros = []
        params = {}
        if nome_ou_pseudonimo:
            filtros.append('(a.nome ILIKE :nome OR a.pseudonimo ILIKE :pseudonimo)')
            params['nome'] = '%'+nome_ou_pseudonimo+'%'
            params['pseudonimo'] = '%'+nome_ou_pseudonimo+'%'
        if id_curso:
            filtros.append('c.id = :id_curso')
            params['id_curso'] = id_curso
        # acrescenta filtros à consulta
        for i, f in enumerate(filtros):
            if i != 0:
                sql_str += " AND "
            sql_str += ' ' + f + ' '
        # cria o objeto de consulta
        primeira_consulta = text(sql_str)
        with self.sql_engine.connect() as connection:
            autores = []
            rs_primeira_consulta = connection.execute(primeira_consulta, params)
            ids_autores = [r[0] for r in rs_primeira_consulta]
            if len(ids_autores) == 0:
                return autores
            # 2ª etapa: obtém os autores e os cursos associados
            segunda_consulta = text(
                "SELECT a.id, a.nome, a.pseudonimo, a.contato, c.id, c.nome "
                "FROM autor a LEFT JOIN autor_curso ac ON a.id = ac.id_autor "
                "LEFT JOIN curso c ON ac.id_curso = c.id WHERE a.id IN :ids_autores "
                "ORDER BY a.id"
            )
            segunda_consulta = segunda_consulta.bindparams(bindparam('ids_autores', expanding=True)) # permite usar uma lista como valor do parâmetro
            result_segunda_consulta = connection.execute(segunda_consulta, {'ids_autores': ids_autores})
            id_autor = None
            for r in result_segunda_consulta:
                if id_autor != r[0]: # mudou o autor
                    id_autor = r[0]
                    a = models.Autor(id=r[0], nome=r[1], pseudonimo=r[2], contato=r[3], cursos=[])
                    autores.append(a)
                if r[4]:
                    a.cursos.append(models.Curso(r[4], r[5]))
            return autores
        
    def salvar(self, autor, id_cursos):
        params = {
            "nome": autor.nome, 
            "pseudonimo": autor.pseudonimo, 
            "contato": autor.contato
        }
        if autor.id:
            sql_autor = text("UPDATE autor SET nome = :nome, pseudonimo = :pseudonimo, contato = :contato WHERE id = :id")
            params['id'] = autor.id
        else:
            sql_autor = text(
                "INSERT INTO autor (nome, pseudonimo, contato) " \
                "VALUES (:nome, :pseudonimo, :contato) " \
                "RETURNING id"
            )
        with self.sql_engine.connect() as connection:
            rs_autor = connection.execute(sql_autor, params)
            if autor.id:
                id_autor = autor.id
            else:
                id_autor = rs_autor.scalar() # obtém o id do autor recém criado
            # associação com cursos
            # 1º etapa: remove todos os cursos do autor
            delete_cursos = text("DELETE FROM autor_curso WHERE id_autor = :id_autor")
            connection.execute(delete_cursos, {'id_autor': id_autor})
            # 2ª etapa: associa os cursos indicados
            sql_autor_curso = text("INSERT INTO autor_curso (id_autor, id_curso) VALUES (:id_autor, :id_curso)")
            for id_curso in id_cursos:
                connection.execute(sql_autor_curso, {'id_autor': id_autor, 'id_curso': id_curso})
            connection.commit()

    def excluir(self, id_autor):
        sql = text("DELETE FROM autor WHERE id = :id")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, {"id": id_autor})
            connection.commit()

class CordelDAO:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine

    def get_por_ID(self, id, is_admin):
        sql_a = (
            "SELECT c.id, c.titulo, c.subtitulo, c.destaque, "
            " c.visivel, c.data_publicacao, c.data_cadastro, "
            " c.mime_type_capa, cat.id, cat.nome, a.id, a.nome, a.pseudonimo "
            "FROM cordel c "
            "INNER JOIN cordel_categoria cc ON c.id = cc.id_cordel "
            "INNER JOIN categoria cat ON cat.id = cc.id_categoria "
            "INNER JOIN cordel_autor ca ON c.id = ca.id_cordel "
            "INNER JOIN autor a ON a.id = ca.id_autor "
            "WHERE c.id = :id "
        )
        if not is_admin:
            sql_a += "AND visivel = TRUE "
        with self.sql_engine.connect() as connection:
            result_a = connection.execute(
                text(sql_a), 
                {"id": id}
            )
            cordel = None
            autores = {}
            categorias = {}
            for r in result_a:
                if not cordel:
                    cordel = models.Cordel()
                    cordel.id = r[0]
                    cordel.titulo = r[1]
                    cordel.subtitulo = r[2]
                    cordel.destaque = r[3]
                    cordel.visivel = r[4]
                    cordel.data_publicacao = r[5]
                    cordel.data_cadastro = r[6]
                    cordel.mime_type_capa = r[7]
                    cordel.autores = autores
                    cordel.categorias = categorias
                if r[8]:
                    categorias[r[8]] = models.Categoria(r[8], r[9])
                if r[10]:
                    autores[r[10]] = models.Autor(r[10], r[11], r[12], None, None)
            cordel.categorias = [c for c in categorias.values()]
            cordel.autores = [a for a in autores.values()]
            result_a.close()
            if not cordel:
                return None
            # obtendo as páginas
            sql_b = text(
                "SELECT id, numeracao, estrofes "
                "FROM pagina WHERE id_cordel = :id_cordel "
            )
            result_b = connection.execute(
                sql_b, 
                {"id_cordel": id}
            )
            paginas = []
            cordel.paginas = paginas
            for r in result_b:
                p = models.Pagina(r[0], r[1], r[2], cordel)
                paginas.append(p)
            result_b.close()
            return cordel
    
    def get_dados_de_capa(self, id_cordel, is_admin):
        sql = (
            "SELECT imagem_capa, mime_type_capa "
            "FROM cordel c WHERE id = :id "
        )
        if not is_admin:
            sql += "AND visivel = TRUE "
        with self.sql_engine.connect() as connection:
            result = connection.execute(
                text(sql), 
                {"id": id_cordel}
            )
            dados = None
            for r in result:
                dados = r[0], r[1]
            result.close()
            return dados

    def pesquisar(
            self, titulo_ou_subtitulo, nome_ou_pseudonimo, \
            id_categoria, id_curso, em_destaque, depois_de, \
            antes_de, texto, invisivel, is_admin
        ):
        # 1º passo: obter IDs dos cordeis que atendem critérios de busca
        sql_str_a = (
            "SELECT DISTINCT co.id FROM cordel co "
            "LEFT JOIN cordel_categoria cc ON co.id = cc.id_cordel "
            "LEFT JOIN categoria cat ON cat.id = cc.id_categoria "
            "LEFT JOIN cordel_autor ca ON co.id = ca.id_cordel "
            "LEFT JOIN autor a ON a.id = ca.id_autor "
            "LEFT JOIN autor_curso ac ON a.id = ac.id_autor "
            "LEFT JOIN curso cu ON cu.id = ac.id_curso "
            "LEFT JOIN pagina p ON p.id_cordel = co.id "
            "WHERE 1=1 "
        )
        # cria filtros com base nos parâmetros informados
        filtros = []
        for f in filtros:
            sql_str += " AND " + f
        params = {}
        if titulo_ou_subtitulo:
            filtros.append('(co.titulo ILIKE :titulo OR co.subtitulo ILIKE :subtitulo)')
            params['titulo'] = '%'+titulo_ou_subtitulo+'%'
            params['subtitulo'] = '%'+titulo_ou_subtitulo+'%'
        if nome_ou_pseudonimo:
            filtros.append('(a.nome ILIKE :nome OR a.pseudonimo ILIKE :pseudonimo)')
            params['nome'] = '%'+nome_ou_pseudonimo+'%'
            params['pseudonimo'] = '%'+nome_ou_pseudonimo+'%'
        if id_categoria:
            filtros.append('cat.id = :id_categoria')
            params['id_categoria'] = id_categoria
        if id_curso:
            filtros.append('cu.id = :id_curso')
            params['id_curso'] = id_curso
        if em_destaque:
            filtros.append('co.destaque = :em_destaque')
            params['em_destaque'] = em_destaque
        if depois_de:
            filtros.append('date(co.data_publicacao) >= date(:depois_de)')
            params['depois_de'] = depois_de.strftime("%Y-%m-%d")
        if antes_de:
            filtros.append('date(co.data_publicacao) <= :antes_de')
            params['antes_de'] = antes_de.strftime("%Y-%m-%d")
        if texto:
            filtros.append('p.estrofes ILIKE :texto')
            params['texto'] = '%'+texto+'%'
        if invisivel:
            filtros.append('co.visivel = FALSE')
        if not is_admin:
            filtros.append('co.visivel = TRUE')
        #print(f"filtros:{filtros}")
        #print(f"parametros:{params}")
        # acrescenta filtros à consulta
        for i, f in enumerate(filtros):
            if i != 0:
                sql_str_a += " AND "
            sql_str_a += ' ' + f + ' '
        
        with self.sql_engine.connect() as connection:
            result_a = connection.execute(text(sql_str_a), params)
            ids_cordeis = [r for r in result_a]
            print(f"ids_cordeis:{ids_cordeis}")
            result_a.close()
            if len(ids_cordeis) == 0:
                return []
            cordeis_dic = {} # chave: id do cordel, valor: objeto cordel
            lista_cordeis = []
            # 2º passo: montar cordeis com respectivas categorias
            sql_b = text(
                "SELECT co.id, co.titulo, co.subtitulo, co.destaque, co.visivel, "
                "co.data_publicacao, co.data_cadastro, cat.id, cat.nome " 
                "FROM cordel co "
                "LEFT JOIN cordel_categoria cc ON co.id = cc.id_cordel "
                "INNER JOIN categoria cat ON cc.id_categoria = cat.id "
                "WHERE co.id IN :ids_cordeis ORDER BY co.id "
            )
            sql_b = sql_b.bindparams(bindparam('ids_cordeis', expanding=True)) # permite usar uma lista como valor do parâmetro
            result_b = connection.execute(sql_b, {'ids_cordeis': ids_cordeis})
            id_cordel = None
            for r in result_b:
                if id_cordel != r[0]: # mudou o cordel
                    c = models.Cordel()
                    c.id = r[0]
                    id_cordel = c.id
                    c.titulo = r[1]
                    c.subtitulo = r[2]
                    c.destaque = r[3]
                    c.visivel = r[4]
                    c.data_publicacao = r[5]
                    c.data_cadastro = r[6]
                    cordeis_dic[c.id] = c
                    lista_cordeis.append(c)
                cat = models.Categoria(r[7], r[8])
                c.categorias.append(cat)
            result_b.close()
            # 3º passo: obter autores com respectivos cursos
            sql_c = text(
                "SELECT a.id, a.nome, a.pseudonimo, a.contato, cu.id, cu.nome, co.id "
                "FROM autor a "
                "LEFT JOIN autor_curso ac ON a.id = ac.id_autor "
                "LEFT JOIN curso cu ON cu.id = ac.id_curso "
                "INNER JOIN cordel_autor ca ON a.id = ca.id_autor "
                "INNER JOIN cordel co ON co.id = ca.id_cordel "
                "WHERE co.id IN :ids_cordeis ORDER BY a.id "
            )
            sql_c = sql_c.bindparams(bindparam('ids_cordeis', expanding=True))
            result_c = connection.execute(sql_c, {'ids_cordeis': ids_cordeis})
            id_autor = None
            cursos_dic = {} # chave: id do curso, valor: objeto curso
            for r in result_c:
                if id_autor != r[0]: # mudou o autor
                    a = models.Autor(r[0], r[1], r[2], r[3], None)
                    id_cordel = r[6]
                    cordeis_dic[id_cordel].autores.append(a)
                if r[4]: # autor tem curso
                    id_curso = r[4]
                    if id_curso in cursos_dic:
                        c = cursos_dic[id_curso]
                    else:
                        c = models.Curso(r[4], r[5])
                        cursos_dic[id_curso] = c
                    if c not in a.cursos:
                        a.cursos.append(c)
            #print(lista_cordeis)
            return lista_cordeis
        
    def _inserir(self, cordel, id_cadastrante, connection):
        sql_a = text(
            "INSERT INTO cordel (titulo, subtitulo, destaque, "
                "visivel, data_publicacao, data_cadastro, "
                "imagem_capa, mime_type_capa, id_cadastrante) "
            "VALUES (:titulo, :subtitulo, :destaque, "
                ":visivel, :data_publicacao, :data_cadastro, "
                ":imagem_capa, :mime_type_capa, :id_cadastrante) "
            "RETURNING id"
        )
        params_cordel = {
            "titulo": cordel.titulo, 
            "subtitulo": cordel.subtitulo, 
            "destaque": cordel.destaque, 
            "visivel": cordel.visivel, 
            "data_publicacao": cordel.data_publicacao.strftime("%Y-%m-%d"), 
            "data_cadastro": date.today().strftime("%Y-%m-%d"), 
            "imagem_capa": cordel.imagem_capa, 
            "mime_type_capa": cordel.mime_type_capa, 
            "id_cadastrante": id_cadastrante
        }
        rs_a = connection.execute(sql_a, params_cordel)
        id_cordel = rs_a.scalar() # obtém o id gerado
        rs_a.close()
        return id_cordel
    
    def _atualizar(self, cordel, connection):
        # atualiza tabela Cordel
        sql_a = (
            "UPDATE cordel SET titulo = :titulo, " 
            "subtitulo = :subtitulo, destaque = :destaque, " 
            "visivel = :visivel, data_publicacao = :data_publicacao "
        )
        params_cordel = {
            "titulo": cordel.titulo, 
            "subtitulo": cordel.subtitulo, 
            "destaque": cordel.destaque, 
            "visivel": cordel.visivel, 
            "data_publicacao": cordel.data_publicacao.strftime("%Y-%m-%d"), 
            "id": cordel.id
        }
        if cordel.imagem_capa:
            sql_a += ", imagem_capa = :imagem_capa, mime_type_capa = :mime_type_capa "
            params_cordel['mime_type_capa'] = cordel.mime_type_capa
            params_cordel['imagem_capa'] = cordel.imagem_capa
        sql_a += "WHERE id = :id "
        sql_a = text(sql_a)
        rs_a = connection.execute(sql_a, params_cordel)
        rs_a.close()
        # remove registros na tabela cordel_autor
        sql_b = text(
            "DELETE FROM cordel_autor WHERE id_cordel = :id_cordel "
        )
        connection.execute(sql_b, {'id_cordel': cordel.id})
        # remove registros na tabela cordel categoria
        sql_c = text(
            "DELETE FROM cordel_categoria WHERE id_cordel = :id_cordel "
        )
        connection.execute(sql_c, {'id_cordel': cordel.id})
        # remove registros na tabela pagina
        sql_d = text(
            "DELETE FROM pagina WHERE id_cordel = :id_cordel "
        )
        connection.execute(sql_d, {'id_cordel': cordel.id})
    
    def salvar(self, cordel, ids_autores, ids_categorias, id_cadastrante):
        if not ids_autores:
            raise ValueError("Um Cordel deve ter pelo menos um autor")
        if not ids_categorias:
            raise ValueError("Um Cordel deve ter pelo menos uma categoria")
        if not cordel.paginas:
            raise ValueError("Um Cordel deve ter pelo menos uma página")
        
        with self.sql_engine.connect() as connection:
            # 1ª etapa: tabela cordel
            if not cordel.id:
                id_cordel = self._inserir(cordel, id_cadastrante, connection)
            else:
                self._atualizar(cordel, connection)
                id_cordel = cordel.id

            # 2ª etapa: inserção na tabela pagina
            sql_b = text(
                "INSERT INTO pagina (numeracao, estrofes, id_cordel) "
                "VALUES (:numeracao, :estrofes, :id_cordel) "
            )
            for p in cordel.paginas:
                connection.execute(
                    sql_b, 
                    {
                        "numeracao": p.numeracao, 
                        "estrofes": p.estrofes, 
                        "id_cordel": id_cordel
                    }
                )
            # 3ª etapa: associação com autores
            sql_c = text(
                "INSERT INTO cordel_autor (id_autor, id_cordel) "
                "VALUES (:id_autor, :id_cordel)"
            )
            for id_autor in ids_autores:
                connection.execute(
                    sql_c, 
                    {"id_autor": id_autor, "id_cordel": id_cordel}
                )
            # 4ª etapa: associação com categorias
            sql_c = text(
                "INSERT INTO cordel_categoria (id_categoria, id_cordel) "
                "VALUES (:id_categoria, :id_cordel)"
            )
            for id_cat in ids_categorias:
                connection.execute(
                    sql_c, 
                    {"id_categoria": id_cat, "id_cordel": id_cordel}
                )
            connection.commit()
        return id_cordel

# ADMINISTRADOR 
class AdministradorDAO:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine


    def todos(self):
        sql = text("SELECT id, nome, hash_senha, matricula, ativo FROM administrador")
        with self.sql_engine.connect() as connection:
            administradores = []
            result = connection.execute(sql)
            for r in result:
                admin = models.Administrador()
                admin.id = r.id
                admin.nome = r.nome
                admin.hash_senha = r.hash_senha
                admin.matricula = r.matricula
                admin.ativo = r.ativo
                administradores.append(admin)
        
        return administradores
    
    def salvar(self, admin):
        params = {"nome": admin.nome, "matricula": admin.matricula, "ativo": admin.ativo, "hash_senha": admin.hash_senha}

        if admin.id:
            sql = text("UPDATE administrador SET nome = :nome, matricula = :matricula, ativo = :ativo, hash_senha = :hash_senha WHERE id = :id")
            params['id'] = admin.id
        else:
            sql = text("INSERT INTO administrador(nome, matricula, ativo, hash_senha) VALUES(:nome, :ativo, :matricula, :hash_senha)")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, params)
            connection.commit()

    def get_por_ID(self, id):
        sql = text(
            "SELECT id, nome, matricula, hash_senha, contato, ativo "
            "FROM administrador "
            "WHERE id = :id "
        )
        with self.sql_engine.connect() as connection:
            result = connection.execute(sql, {'id': id})
            admin = None
            for i, r in enumerate(result):
                admin = models.Administrador()
                admin.id = r[0]
                admin.nome = r[1]
                admin.matricula = r[2]
                admin.hash_senha = r[3]
                admin.contato = r[4]
                admin.ativo = r[5]
            return admin
        
    def get_por_matricula(self, matricula):
        sql = text(
            "SELECT id, nome, matricula, hash_senha, contato, ativo "
            "FROM administrador "
            "WHERE matricula = :matricula "
        )
        with self.sql_engine.connect() as connection:
            result = connection.execute(sql, {'matricula': matricula})
            admin = None
            for i, r in enumerate(result):
                admin = models.Administrador()
                admin.id = r[0]
                admin.nome = r[1]
                admin.matricula = r[2]
                admin.hash_senha = r[3]
                admin.contato = r[4]
                admin.ativo = r[5]
            return admin
    
    def excluir(self, id_admin):
        sql = text("DELETE FROM administrador WHERE id = :id")
        with self.sql_engine.connect() as connection:
            connection.execute(sql, {"id": id_admin})
            connection.commit()