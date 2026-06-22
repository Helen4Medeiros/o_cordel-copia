CREATE TABLE administrador (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    nome VARCHAR(100) NOT NULL, 
    matricula VARCHAR(30) NOT NULL, -- este campo faz o papel de username
    hash_senha TEXT NOT NULL,
    contato TEXT, 
    ativo BOOL NOT NULL
);
CREATE TABLE curso (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    nome VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE categoria (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    nome VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE autor (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    nome VARCHAR(100) NOT NULL, 
    pseudonimo VARCHAR(100), 
    contato TEXT
);
CREATE TABLE autor_curso (
    id_autor BIGINT NOT NULL,
    id_curso BIGINT NOT NULL,
    PRIMARY KEY (id_autor, id_curso), 
    FOREIGN KEY (id_autor) REFERENCES autor (id) ON UPDATE RESTRICT ON DELETE CASCADE, 
    FOREIGN KEY (id_curso) REFERENCES curso (id) ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE cordel (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    titulo TEXT NOT NULL, 
    subtitulo TEXT, 
    destaque BOOL NOT NULL, 
    visivel BOOL NOT NULL, 
    data_publicacao DATE NOT NULL, 
    data_cadastro DATE NOT NULL, 
    imagem_capa BYTEA, 
    mime_type_capa VARCHAR(100), 
    id_cadastrante BIGINT NOT NULL, 
    FOREIGN KEY (id_cadastrante) REFERENCES administrador (id) ON UPDATE RESTRICT ON DELETE RESTRICT 
);
CREATE TABLE pagina (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    numeracao INTEGER NOT NULL, 
    estrofes TEXT NOT NULL, 
    id_cordel BIGINT NOT NULL, 
    FOREIGN KEY (id_cordel) REFERENCES cordel (id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE cordel_autor (
    id_autor BIGINT NOT NULL,
    id_cordel BIGINT NOT NULL,
    PRIMARY KEY (id_autor, id_cordel), 
    FOREIGN KEY (id_autor) REFERENCES autor (id) ON UPDATE RESTRICT ON DELETE RESTRICT, 
    FOREIGN KEY (id_cordel) REFERENCES cordel (id) ON UPDATE RESTRICT ON DELETE RESTRICT
);
CREATE TABLE cordel_categoria (
    id_categoria BIGINT NOT NULL,
    id_cordel BIGINT NOT NULL,
    PRIMARY KEY (id_categoria, id_cordel), 
    FOREIGN KEY (id_categoria) REFERENCES categoria (id) ON UPDATE RESTRICT ON DELETE RESTRICT, 
    FOREIGN KEY (id_cordel) REFERENCES cordel (id) ON UPDATE RESTRICT ON DELETE RESTRICT
);
