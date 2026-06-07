-- /*
DROP DATABASE IF EXISTS db_jogo;
CREATE DATABASE db_jogo;
USE db_jogo;
 
-- 1. cursos
CREATE TABLE cursos (
    id_curso INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    sigla VARCHAR(45) NOT NULL,
    nome_curso TEXT
);

-- 2. tabuleiro
CREATE TABLE tabuleiro (
    id_tabuleiro INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome VARCHAR(45) NOT NULL,
    descricao TEXT
);

-- 3. casas
CREATE TABLE casas (
    id_casa INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome_local VARCHAR(45) NOT NULL,
    descricao TEXT,
    travada INT NOT NULL DEFAULT 1,
    id_tabuleiro INT NOT NULL,
    FOREIGN KEY (id_tabuleiro) REFERENCES tabuleiro(id_tabuleiro) ON DELETE RESTRICT
);

-- 4. usuarios
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(45) NOT NULL,
    senha VARCHAR(45) NOT NULL,
	is_professor TINYINT(1) NOT NULL DEFAULT 0,
    id_curso INT NOT NULL,

    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE RESTRICT
);

-- 5. alunos
CREATE TABLE alunos (
    id_aluno INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_usuario INT NOT NULL,
    RA VARCHAR(45) NOT NULL,
    progresso FLOAT NOT NULL DEFAULT 0.0,
    avatar INT NOT NULL DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

-- 6. materiais
CREATE TABLE materiais (
    id_material INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    titulo VARCHAR(45) NOT NULL,
    descricao TEXT,
    arquivo VARCHAR(255),
    data_postagem DATE,
    id_usuario INT NOT NULL,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE RESTRICT
);

-- 7. tarefas
CREATE TABLE tarefas (
    id_tarefa INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    descricao TEXT,
    data_entrega DATE,
    id_casa INT NOT NULL,
    id_curso INT NOT NULL,
    FOREIGN KEY (id_casa) REFERENCES casas(id_casa) ON DELETE RESTRICT,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso) ON DELETE RESTRICT
);

-- 8. progresso
CREATE TABLE progresso (
    id_progresso INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_usuario INT NOT NULL,
    id_casa INT NOT NULL,
    concluida TINYINT,
    data_conclusao DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    FOREIGN KEY (id_casa) REFERENCES casas(id_casa) ON DELETE RESTRICT
);

-- 9. entrega_tarefas
CREATE TABLE entrega_tarefas (
    id_entrega INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_tarefa INT NOT NULL,
    id_usuario INT NOT NULL,
    resposta TEXT,
    arquivo_resposta VARCHAR(255),
    nota FLOAT,
    status VARCHAR(45),
    data_entrega DATETIME,
    FOREIGN KEY (id_tarefa) REFERENCES tarefas(id_tarefa) ON DELETE RESTRICT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

CREATE TABLE respostas (
	id_resposta INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    id_aluno INT NOT NULL,
    id_tarefa INT NOT NULL,
    resposta VARCHAR(500) NOT NULL,
    FOREIGN KEY (id_tarefa) REFERENCES tarefas(id_tarefa) ON DELETE RESTRICT,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

INSERT INTO cursos (sigla, nome_curso) VALUES
('ADM', 'Administração'),
('ARQ', 'Arquitetura e Urbanismo'),
('CIC', 'Ciência da Computação'),
('DES', 'Design'),
('EAL', 'Engenharia de Alimentos'),
('ECI', 'Engenharia Civil'),
('ECOMP', 'Engenharia de Computação'),
('ECA', 'Engenharia de Controle e Automação'),
('EEL', 'Engenharia Elétrica'),
('EELT', 'Engenharia Eletrônica'),
('EM', 'Engenharia Mecânica'),
('EP', 'Engenharia de Produção'),
('EQ', 'Engenharia Química'),
('IACD', 'Inteligência Artificial e Ciência de Dados'),
('RI', 'Relações Internacionais'),
('SIN', 'Sistemas de Informação');

-- serve para add aluno
DELIMITER $$
CREATE TRIGGER trg_criar_aluno
AFTER INSERT ON usuarios
FOR EACH ROW
BEGIN
    IF NEW.is_professor = 0 THEN
        INSERT INTO alunos (id_usuario, RA)
        VALUES (NEW.id_usuario, NEW.email);
    END IF;
END$$
DELIMITER ;

INSERT INTO usuarios (nome, email, senha, id_curso) VALUES
('Julio Cesar Carnevalli dos Santos Gualtieroni', '26.00722-9@maua.br', '54556218829', '3'),
('Rafael Grespan de Souza', '26.00987-8@maua.br', '50812371836', '3'),
('Murilo Rodriguez Quiqueti', '26.00314-5@maua.br', '53206113822', '3');

UPDATE alunos SET RA = '26.00722-9' WHERE RA = '26.00722-9@maua.br';
UPDATE alunos SET RA = '26.00987-8' WHERE RA = '26.00987-8@maua.br';
UPDATE alunos SET RA = '26.00314-5' WHERE RA = '26.00314-5@maua.br';

INSERT INTO usuarios
(nome, email, senha, is_professor, id_curso)
VALUES
('Rudolf', 'rudolf@maua.br', '123', 1, 3);

INSERT INTO tabuleiro (nome, descricao)
VALUES ('Tabuleiro Principal', 'Mapa principal');

INSERT INTO casas (nome_local, descricao, id_tabuleiro)
VALUES
('Conhecendo o IMT', 'Seja bem-vindo(a) à Mauá!', 1),
('Conhecendo a Disciplina', 'Apresentação da Disciplina', 1),
('Ética Acadêmica', 'Questionário de Perfil', 1),
('O que Sabemos', 'Matriz, suposições e dúvidas', 1),
('Propósito', 'Encontre o seu Propósito!', 1),
('O que te inspira?', 'Entenda suas Inspirações', 1),
('Desapegue!', 'Livre-se das Distrações!', 1),
('O que Admiro?', 'O que você mais admira no mundo', 1),
('Saindo da Zona de Conforto', 'Faça algo que você nunca fez', 1),
('Relação com o Mundo', 'Faça uma análise profunda', 1),
('Planeje sua Vida', 'Sua missão e seus valores', 1),
('Crie uma Rede de Relacionamento', 'Descubra quem pode te ajudar', 1),
('O que o Mercado Espera', 'Mercado no Século XXI', 1),
('Vamos projetar!', 'Você está disposto a passar perrengue?', 1),
('Indo além do Papel', 'Tirando a ideia do papel', 1),
('Mapeando Desafios', 'Problemas que seu projeto pode resolver', 1),
('Vamos Projetar', 'Organizar por Importância e Urgência', 1),
('Resolvendo Desafios', 'O que é o seu projeto?', 1),
('Preparado para o Imprevisto', 'Esteja pronto para quaisquer surpresas', 1),
('Vamos Comunicar', 'Como você explicaria seu projeto às pessoas?', 1),
('Agregando Valor', 'Qual valor seu projeto vai entregar', 1),
('Mão na Massa', 'Vamos Prototipar!', 1),
('Vendendo Soluções', 'Tente vender o seu produto!', 1),
('Cápsula do Tempo', 'O que aprendi que não devo fazer?', 1)
;

SELECT * FROM usuarios; SELECT * FROM cursos; SELECT * FROM alunos; SELECT * FROM casas;