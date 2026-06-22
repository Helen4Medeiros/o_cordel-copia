DO $$
DECLARE
    id_autor_criado BIGINT;
    id_admin_criado BIGINT;
    id_cordel_criado BIGINT;
BEGIN
    INSERT INTO administrador (nome, matricula, ativo, hash_senha)  
        VALUES ('Admin Teste', '12345', TRUE, 
        'scrypt:32768:8:1$L6g9Y0U1vbZ7sPhp$2e21656329d2ac9abf0b086f937874e50853af13aa2f8d02fede36fc2838dd854bc5aa7fb4521842ee34949a3bd4aa4e830b1161394f8238a6ea108cf7266a84') -- hash da string senha
        RETURNING id INTO id_admin_criado;

    -- Autor com cordel
    INSERT INTO autor (nome) VALUES ('Cícero Carlos Duarte') RETURNING id INTO id_autor_criado;
    INSERT INTO autor_curso (id_autor, id_curso) VALUES (id_autor_criado, 1);

    -- Autores sem cordel
    INSERT INTO autor (nome, pseudonimo, contato) VALUES ('Francisco Martins', 'Chico Bioca', 'chicobioca@mail.com');
    INSERT INTO autor (nome, contato) VALUES ('Francisco Silva', 'fsilva@mail.com');
    INSERT INTO autor (nome, contato) VALUES ('Francisco Carlos', 'fcarlos@mail.com');

    -- Cordel 
    INSERT INTO cordel (titulo, data_publicacao, data_cadastro, destaque, visivel, id_cadastrante) 
        VALUES ('O Coronavírus', '2024-03-01', '2024-10-20', FALSE, TRUE, 1)
        RETURNING id INTO id_cordel_criado;
    INSERT INTO cordel_autor (id_autor, id_cordel) VALUES (id_autor_criado, id_cordel_criado);
    INSERT INTO cordel_categoria (id_categoria, id_cordel) VALUES (1, id_cordel_criado);
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        1, 
    'Relato neste momento
    Em forma de poesia
    Um assunto preocupante
    Que aumenta a cada dia
    O Covid dezenove
    O vírus que nos envolve
    Com a sua pandemia

    Misturo neste cordel
    Humor e veracidade
    Com um dom dado por Deus
    Me expresso com humildade
    E falo da pandemia
    E o vírus que contagia
    Toda nossa humanidade'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        2, 
    'Raul Seixas no passado
    Foi incrível, quem diria
    Previu o nosso futuro
    Através de uma melodia
    Pois ninguém nunca pensou
    Dia em que a Terra parou
    Fosse esta pandemia

    Nesta música de sucesso
    Raul Seixas revelou
    Que a Terra ia parar
    E ninguém acreditou
    E depois de tanto tempo
    É chegado o momento
    Dia em que a Terra parou

    A música fala de um sonho
    Longe da realidade
    Um assunto sem sentido
    Hoje aos olhos da verdade
    Um triste acontecimento
    Que até hoje no momento
    Se alastra em toda a cidade'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        3, 
    'Com certeza um grande artista
    Que sempre será lembrado
    Raul Seixas um fenômeno
    Fez sucesso no passado
    Não é que a Terra parou
    Pois essa música provou
    Este momento chegado

    O corona vem matando
    Trabalhador brasileiro
    Dona de casa idosa
    Motorista e açougueiro
    Abalou a economia
    Pois essa tal pandemia
    Traz um vírus traiçoeiro

    Tem coisas que tenho dúvida
    Ao ouvir fico calado
    Com uma pulga atrás da orelha
    Cada vez desconfiado
    Morre gente todo dia
    Por que nessa pandemia
    Não morreu um deputado?'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        4, 
    'Eu tenho um compadre meu
    Feio e cheio de marmota
    O cabelo “arrupiado”
    Doutor em fazer lorota
    Fez uma rima engraçada
    Preste atenção camarada
    O vírus virou chacota

    O homem quando é valente
    Mostra se é forte ou fraco
    Briga com coronavírus
    Até dentro de um buraco
    Se agarra com ele na tapa
    Que o suor vira garapa
    Mas bota dentro de um saco

    Amarra a boca do saco
    E sacode para cima
    Que vai na velocidade
    Desafia a medicina
    Vou te dizer por que sei
    Vai cair de onde “vei”
    No país chamado China'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        5, 
    'Nem aqui e nem na China
    Nunca se ouviu falar
    De um político com corona
    Você pode me explicar?
    Pois a origem do jogo
    Onde tem fumaça tem fogo
    Partiu do lado de lá

    Tenha cuidado meu amigo
    Com a tal situação
    O corona é oportunista
    E é mais que um vilão
    Todo cuidado é pouco
    Não entre neste sufoco
    Evite aglomeração

    É pior do que a dengue
    Do mosquito traiçoeiro
    O Covid dezenove
    Desafia o mundo inteiro
    Pra te falar a verdade
    Vem matando sem piedade
    Nosso povo brasileiro'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        6, 
    'Seu sintoma é doloroso
    Dificulta o respirar
    Limpe as mãos com álcool gel
    Use máscara pra evitar
    Preserve sua saúde
    Tome logo uma atitude
    Pra não se contaminar

    O corona é um intruso
    E não veio para ficar
    A vacina está chegando
    E tudo vai melhorar
    Como diz a medicina
    O vírus que veio da China
    Tá perto de se acabar

    O Covid dezenove
    É um vírus audacioso
    Se alojando no organismo
    Ele é muito perigoso
    Podendo até matar
    O jovem pode evitar
    Principalmente o idoso'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        7, 
    'Este tal coronavírus
    Causador desta agonia
    Parou o nosso comércio
    Que voltou com a caristia
    Arroz e feijão aumentando
    Tem gente se aproveitando
    Depois desta pandemia

    Quando for para o mercado
    Anote o que for comprar
    E preste atenção nos preços
    Para poder comparar
    Dentro da ética e conceito
    Cada um tem o direito
    Até de fiscalizar

    Logo veio a quarentena
    Mudando o comportamento
    Todo povo respeitando
    Regras de isolamento
    Homem, mulher e criança
    Todos com a esperança
    De acabar com o sofrimento'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        8, 
    'É triste a realidade
    De se doer na consciência
    O Brasil estacionou
    E o povo pede clemência
    Sem saber o que fazer
    Só Deus pra nos proteger
    Desta terrível doença

    No tempo da minha avó
    Tudo era diferente
    Existia mais saúde
    A população contente
    E o tempo foi passando
    A situação mudando
    Só se ver gente doente

    E o ar que respiramos
    Hoje é preocupação
    Tem vírus e bactérias
    Que prejudica o pulmão
    Nosso povo está morrendo
    E a natureza sofrendo
    Com tanta poluição'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        9, 
    'As matas estão acabando
    E os rios em extinção
    Agora o coronavírus
    Matando a população
    Ele quem tem o poder
    Só Deus pra nos proteger
    Contra essa maldição

    O corona é um vírus
    Que não podemos enxergar
    Ele está no mundo todo
    Ou mesmo em qualquer lugar
    Sua contaminação
    Basta um aperto de mão
    Pra o ser humano pegar

    A higiene das mãos
    É o propósito principal
    Se prevenir todo dia
    Lutando contra esse mal
    O vírus não terá vez
    Só depende de vocês
    Esta batalha final'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        10, 
    'Nascemos para viver
    Viver a vida e lutar
    Resolver qualquer problema
    Com sucesso prosperar
    Quem tem Deus em sua vida
    O vírus não intimida
    Só ele pra nos salvar

    Já se passaram oito meses
    Tudo está se resolvendo
    Tudo voltando ao normal
    Menos pessoas morrendo
    Prevenir e acreditar
    Que o vírus vai acabar
    É o que a gente tá querendo

    Nosso Brasil é guerreiro
    O povo tem esperança
    Tem força, tem energia
    A começar de criança
    Um país que tem amor
    Nunca perde seu valor
    Tá sempre na liderança'
    );
    INSERT INTO pagina (id_cordel, numeracao, estrofes) VALUES (
        id_cordel_criado, 
        11, 
    'O vírus não tem mais vez
    Está entrando em extinção
    Por que nosso santo é forte
    Temos Deus no coração
    Será o fim da pandemia
    É só ter fé todo dia
    E acreditar na nação

    O corona está morrendo
    Logo será esquecido
    E vamos recuperar
    Todo momento perdido
    O vírus será finado
    Corona será passado
    Tudo vai ser resolvido

    Finalizo este cordel
    Livre de qualquer censura
    Rimei a realidade
    Com minha desenvoltura
    O Sesc eu parabenizo
    Neste momento preciso
    Linda Mostra de Cultura.'
    );
END $$;