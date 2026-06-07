import mysql.connector
from datetime import datetime

conexao = mysql.connector.connect(host='localhost',
                                  database='db_jogo',
                                  user='root',
                                  password='')
if conexao.is_connected():
    print("Banco de Dados Conectado!")

def validarLogin(email, senha):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado

def puxarInfoAluno(idUser):
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM alunos WHERE id_usuario = %s", (idUser,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado

def atualizarProgresso(RA, progressoNovo):
    cursor = conexao.cursor()
    cursor.execute("UPDATE alunos SET progresso = %s WHERE RA = %s", (progressoNovo, RA))
    conexao.commit()
    cursor.execute("SELECT progresso FROM alunos WHERE RA = %s", (RA,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado[0]

def retrieveCasa (numCasa):
    cursor = conexao.cursor()
    cursor.execute("SELECT nome_local, descricao FROM casas WHERE id_casa = %s", (numCasa,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado

def checarCasa (idCasa):
    cursor = conexao.cursor()
    cursor.execute("SELECT travada FROM casas WHERE id_casa = %s", (idCasa,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado[0]

def mudarLibCasa (status, idCasa):
    cursor = conexao.cursor()
    cursor.execute("UPDATE casas SET travada = %s WHERE id_casa = %s", (status, idCasa))
    if cursor.rowcount == 0:
        cursor.close()
        return False
    else:
        conexao.commit()
        cursor.close()
        return True

def buscarCurso(sigla):
    cursor = conexao.cursor()
    cursor.execute("SELECT id_curso FROM cursos WHERE LOWER(TRIM(sigla)) = LOWER(TRIM(%s))",
                    (sigla,))
    resultado = cursor.fetchone()
    cursor.close()
    if resultado == None:
        return None
    return resultado[0]

def criarTarefa(desc, dataEntrega, idCasa, curso):
    x = buscarCurso(curso)
    if x != None:
        cursor = conexao.cursor()

        cursor.execute("SELECT 1 FROM tarefas WHERE id_casa = %s AND id_curso = %s", (idCasa, x))
        existe = cursor.fetchone()

        if existe:
            cursor.close()
            return 1

        cursor.execute("INSERT INTO tarefas (descricao, data_entrega, id_casa, id_curso)"
                        "VALUES (%s, %s, %s, %s)",
                        (desc, dataEntrega, idCasa, x))
        conexao.commit()
        cursor.close()
        return 2
    else:
        return 0
    
def retrieveTarefa(idCasa, idCurso):
    cursor = conexao.cursor()
    cursor.execute("SELECT id_tarefa, descricao, data_entrega FROM tarefas WHERE id_casa = %s AND id_curso = %s", (idCasa, idCurso))
    resultado = cursor.fetchone()
    cursor.close()

    if resultado == None:
        return None

    dataEntrega = resultado[2]
    if isinstance(dataEntrega, str):
        dataEntrega = datetime.strptime(dataEntrega, "%Y-%m-%d").date()
    dataTarefa = dataEntrega.strftime("%d/%m/%Y")
    
    resultFinal = [resultado[0], resultado[1], dataTarefa]
    return resultFinal

def adicionarAluno (nome, email, senha, curso, RA):
    idCurso = buscarCurso(curso)
    if idCurso != None:
        cursor = conexao.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE email = %s",
                        (email,))
        existe = cursor.fetchone()

        if existe:
            cursor.close()
            return 0

        cursor.execute("INSERT INTO usuarios (nome, email, senha, id_curso) "
                        "VALUES (%s, %s, %s, %s)",
                        (nome, email, senha, idCurso))
        conexao.commit()

        idUser = cursor.lastrowid
        cursor.execute("UPDATE alunos SET RA = %s WHERE id_usuario = %s", (RA, idUser))
        conexao.commit()
        cursor.close()
        return 1
    else:
        return -1

def contagemRespostas(idCurso, idCasa):
    curso = buscarCurso(idCurso)
    if curso != None:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(r.id_resposta) "
                        "FROM respostas r "
                        "JOIN alunos a ON r.id_aluno = a.id_aluno "
                        "JOIN usuarios u ON a.id_usuario = u.id_usuario "
                        "JOIN tarefas t ON r.id_tarefa = t.id_tarefa "
                        "WHERE u.id_curso = %s AND t.id_casa = %s",
                        (curso, idCasa))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]
    else:
        return -1

def totalAlunosCurso(idCurso):
    curso = buscarCurso(idCurso)
    if curso != None:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(id_usuario) FROM usuarios WHERE id_curso = %s", (curso,))
        resultado = cursor.fetchone()
        cursor.close()
        return resultado[0]

def responderTarefa(resposta, idAluno, idTarefa):
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO respostas (id_aluno, id_tarefa, resposta)" \
                    "VALUES (%s, %s, %s)",
                    (idAluno, idTarefa, resposta))
    conexao.commit()
    cursor.close()
    return 1

def checarResposta(RA, idCasa):
        cursor = conexao.cursor()
        cursor.execute("SELECT id_aluno, id_usuario FROM alunos WHERE RA = %s",
                        (RA, ))
        ids = cursor.fetchone()
        idAluno = ids[0]
        idUsuario = ids[1]

        cursor.execute("SELECT id_curso FROM usuarios WHERE id_usuario = %s",
                        (idUsuario, ))
        idC = cursor.fetchone()
        idCurso = idC[0]

        cursor.execute("SELECT id_tarefa FROM tarefas WHERE id_casa = %s AND id_curso = %s",
                        (idCasa, idCurso))
        idT = cursor.fetchone()

        if idT == None:
            cursor.close()
            return -1

        idTarefa = idT[0]

        cursor.execute("SELECT resposta FROM respostas WHERE id_aluno = %s AND id_tarefa = %s",
                        (idAluno, idTarefa))
        existe = cursor.fetchone()
        cursor.close()

        if existe != None:
            return existe[0]
        else:
            return 0

def checarData(casaTab, cursoAluno):
    data = retrieveTarefa(casaTab, cursoAluno)
    if data == None:
        return -1
    
    dataEntrega = datetime.strptime(data[2], "%d/%m/%Y").date()
    dataHoje = datetime.now().date()

    if dataEntrega>dataHoje:
        return 1
    else:
        return 0

