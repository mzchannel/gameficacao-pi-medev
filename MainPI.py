# import classes
from ClasseCaixaTexto import TextBox # importa caixa de texto
from ClasseBotao import Button # importa Botão
from BibliotecaImagemGerador import GerarImagem as imgGen
from ClasseTexto import TextMessage as textGen
from ClasseTabuleiro import Tabuleiro as tab
from ClasseCasaTabuleiro import CasaTab
from ClasseSelo import Selo

# import bibliotecas minhas
import BibliotecaCodigoBD as SQL # importa função de leitura do SQL
import BibliotecaAudioPlayer as audio

# import bibliotecas prontas
import pygame # importa pygame
from sys import exit # forma de fechar o programa
from datetime import datetime
import pyperclip

# informações da janela
jan_larg = 1080 # largura da janela (X)
jan_alt = 540 # altura da janela (Y)

# placeholder
gatoFDP = pygame.image.load("imagens/bleh.png")

# imagens botões
imagemBotaoEntrar = pygame.image.load("imagens/botão-acesso-login.png") # puxa a imagem para o projeto em uma variável
imagemBotaoSair = pygame.image.load("imagens/botão-sair.png")
imagemBotaoOk = pygame.image.load("imagens/botão-ok.png")
imagemSenha = pygame.image.load("imagens/olho-senha.png")
imagemSenhaOff = pygame.image.load("imagens/olho-senha-off.png")
imagemTarefa = pygame.image.load("imagens/botão-tarefa.png")
imagemTarefaFora = pygame.image.load("imagens/botão-tarefa-fora.png")
imagemAdd = pygame.image.load("imagens/botão-add-aluno.png")
imagemAddFora = pygame.image.load("imagens/botão-add-aluno-off.png")
imagemNewTarefa = pygame.image.load("imagens/botão-tarefa-add.png")
imagemNewAluno = pygame.image.load("imagens/botão-add-aluno-prof.png")
imagemFinishTarefa = pygame.image.load("imagens/botão-concluir-tarefa.png")
imagemAnaliseDesemp = pygame.image.load("imagens/botão-analise-efic.png")
imagemCopyResposta = pygame.image.load("imagens/botão-copy-resposta.png")

# imagens botões abas
imagemAbaTab = pygame.image.load("imagens/botão-mapa.png")
imagemAbaTabOut = pygame.image.load("imagens/botão-mapa-fora.png")

imagemAbaPerf = pygame.image.load("imagens/botão-perfil.png")
imagemAbaPerfOut = pygame.image.load("imagens/botão-perfil-fora.png")

# imagens setas
imagemSetaEsq = pygame.image.load("imagens/arrow-esq.png")
imagemSetaDir = pygame.image.load("imagens/arrow-dir.png")

# casas azuis e brancas
casaAzBr_Travada = pygame.image.load("casas/azulbranco/casa-azbr-lock.png")
casaAzBr_ToDo = pygame.image.load("casas/azulbranco/casa-azbr-to-do.png")
casaAzBr_Done = pygame.image.load("casas/azulbranco/casa-azbr-done.png")
casaAzBr_Fail = pygame.image.load("casas/azulbranco/casa-azbr-fail.png")
seloAzBr_Vazio = pygame.image.load("selos/azbr-sem-selo.png")
seloAzBr_Feito = pygame.image.load("selos/azbr-selo.png")

# casas brancas e azuis
casaBrAz_Travada = pygame.image.load("casas/brancoazul/casa-braz-lock.png")
casaBrAz_ToDo = pygame.image.load("casas/brancoazul/casa-braz-to-do.png")
casaBrAz_Done = pygame.image.load("casas/brancoazul/casa-braz-done.png")
casaBrAz_Fail = pygame.image.load("casas/brancoazul/casa-braz-fail.png")
seloBrAz_Vazio = pygame.image.load("selos/braz-sem-selo.png")
seloBrAz_Feito = pygame.image.load("selos/braz-selo.png")

# casas laranjas e brancas
casaLarBr_Travada = pygame.image.load("casas/laranjabranco/casa-larbr-lock.png")
casaLarBr_ToDo = pygame.image.load("casas/laranjabranco/casa-larbr-to-do.png")
casaLarBr_Done = pygame.image.load("casas/laranjabranco/casa-larbr-done.png")
casaLarBr_Fail = pygame.image.load("casas/laranjabranco/casa-larbr-fail.png")
seloLarBr_Vazio = pygame.image.load("selos/larbr-sem-selo.png")
seloLarBr_Feito = pygame.image.load("selos/larbr-selo.png")

# casas brancas e laranjas
casaBrLar_Travada = pygame.image.load("casas/brancolaranja/casa-brlar-lock.png")
casaBrLar_ToDo = pygame.image.load("casas/brancolaranja/casa-brlar-to-do.png")
casaBrLar_Done = pygame.image.load("casas/brancolaranja/casa-brlar-done.png")
casaBrLar_Fail = pygame.image.load("casas/brancolaranja/casa-brlar-fail.png")
seloBrLar_Vazio = pygame.image.load("selos/brlar-sem-selo.png")
seloBrLar_Feito = pygame.image.load("selos/brlar-selo.png")

mauaBase = pygame.image.load("imagens/maua.png")

# inicialização
pygame.init() # necessário para inicialização
pygame.mixer.init() # inicializa player de audio
janela = pygame.display.set_mode((jan_larg, jan_alt)) # criar janela e definir tamanho
pygame.display.set_caption("Mauá Virtual Tabletop") # título da janela
pygame.display.set_icon(mauaBase) # ícone da janela
clock = pygame.time.Clock() # usado para framerate

# textos gerais
mauaTextoLogin = textGen("BAHNSCHRIFT", 32)
textoLoginReq = textGen("BAHNSCHRIFT", 14)
textoAbaSup = textGen("BAHNSCHRIFT", 32)
textoPadrao = textGen("BAHNSCHRIFT", 16)

# mensagens de erro e acerto
errorTextLogin = textGen("bell mt", 32)

# imagem Maua
imagemMaua = imgGen(mauaBase, 1)

# tabuleiro e tarefas
tabuleiroBase = tab(640, 420)

# variavel para loops
# 1 = Login
# 2 = Tabuleiro
# 3 = Perfil
    # 3.1 = Adm Tarefas (PROF ONLY)
# 4 = Tarefa Aberta
    # 4.1 = Add User (PROF ONLY)
# 100 = Aba de Desempenho
# 777 = Sucesso na Ação
# 999 = Erro Login
# 1000 = Erro Tarefa já Existe
# 1001 = Erro Aluno já Existe no BD
    # 1000.1 e 1001.1 = Erro Curso Inválido
# 1002 = Erro Não Há Tarefa
    # 1002.1 = Aba Aluno não Respondeu
janelaNumber = 1
lastJanela = 2

# variavel abas
abaLogado = 1
abaTarefas = 1

# botões
botaoEnter = Button(jan_larg/2, (jan_alt - jan_alt//4), imagemBotaoEntrar, 1)
botaoExit = Button(55, 500, imagemBotaoSair, 1)
botaoOkLogin = Button(jan_larg/2, jan_alt/1.66, imagemBotaoOk, 1)
botaoNewTarefa = Button(597.5, 440, imagemNewTarefa, 1.33)
botaoConcTarefa = Button(597.5, 440, imagemFinishTarefa, 1.33)
botaoAnaliseEfic = Button(597.5, 440, imagemAnaliseDesemp, 1.33)
botaoCopyResposta = Button(597.5, 440, imagemCopyResposta, 1.33)

botaoSetaE = Button(130, 25, imagemSetaEsq, 2)
botaoSetaD = Button(jan_larg-15, 25, imagemSetaDir, 2)

# botão tabuleiro
botaoTabuleiro = Button(55, 150, imagemAbaTab, 3)
botaoTabuleiroFora = Button(55, 150, imagemAbaTabOut, 3)

# botão perfil
botaoPerfil = Button(55, 250, imagemAbaPerf, 3)
botaoPerfilFora = Button(55, 250, imagemAbaPerfOut, 3)

# botão exibirSenha
botaoSenha = Button(jan_larg/1.575, (jan_alt - (jan_alt//2.5)), imagemSenha, 2)
botaoSenhaOff = Button(jan_larg/1.575, (jan_alt - (jan_alt//2.5)), imagemSenhaOff, 2)

# botão Adm de Tarefa
botaoTarefa = Button(55, 250, imagemTarefa, 3)
botaoTarefaFora = Button(55, 250, imagemTarefaFora, 3)

# botão Adicionar Usuario
botaoNewUser = Button(55, 350, imagemAdd, 3)
botaoNewUserFora = Button(55, 350, imagemAddFora, 3)

botaoAddAluno = Button(597.5, 400, imagemNewAluno, 1.33)

# input de texto
textoEmail = ""
textoSenha = ""
caixaUser = TextBox(False, (0, 69, 135), (0, 0, 0), 16)
caixaSenha = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

descTarefa = ""
caixaDescTarefa = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

dateEntrega = ""
caixaDataEntrega = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

idCasaTarefa = ""
caixaIdCasa = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

cursoTarefa = ""
caixaCurso = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

# caixas de texto - criar aluno
nomeAluno = "" 
caixaNomeAluno = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

emailAluno = ""
caixaEmailAluno = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

senhaAluno = ""
caixaSenhaAluno = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

cursoAluno = ""
caixaCursoAluno = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

raAluno = ""
caixaRaAluno = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

# info usuário
idUsuario = 0
nomeUsuario = ""
raUsuario = ""
curso = 0
isProfessor = 0

# info casa
idCasa = 0
nomeCasa = ""
descCasa = ""

# info tarefa casa
idTarefa = 0
descTarefaAluno = ""
dataEntregaTarefa = ""

respostaTarefa = ""
caixaRespTarefa = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

# info buscas
casaBuscada = ""
caixaCasaBuscada = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

cursoBuscado = ""
caixaCursoBuscado = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

raBuscado = ""
caixaRaBuscado = TextBox(False, (0, 69, 135), (0, 0, 0), 16)

# casa do tabuleiro
    # x, y, sprite base, escala, modulo, numero da casa
casa1_1 = CasaTab(517.5, jan_alt/2, casaAzBr_Travada, 4, 1, 1)
casa1_2 = CasaTab(597.5, jan_alt/2, casaAzBr_Travada, 4, 1, 2)
casa1_3 = CasaTab(677.5, jan_alt/2, casaAzBr_Travada, 4, 1, 3)
selo1 = Selo(seloAzBr_Vazio, seloAzBr_Feito, 3)

casa2_1 = CasaTab(437.5, jan_alt/2, casaBrAz_Travada, 4, 2, 4)
casa2_2 = CasaTab(517.5, jan_alt/2, casaBrAz_Travada, 4, 2, 5)
casa2_3 = CasaTab(597.5, jan_alt/2, casaBrAz_Travada, 4, 2, 6)
casa2_4 = CasaTab(677.5, jan_alt/2, casaBrAz_Travada, 4, 2, 7)
casa2_5 = CasaTab(757.5, jan_alt/2, casaBrAz_Travada, 4, 2, 8)
selo2 = Selo(seloBrAz_Vazio, seloBrAz_Feito, 3)

casa3_1 = CasaTab(517.5, jan_alt/2, casaBrLar_Travada, 4, 3, 9)
casa3_2 = CasaTab(597.5, jan_alt/2, casaBrLar_Travada, 4, 3, 10)
casa3_3 = CasaTab(677.5, jan_alt/2, casaBrLar_Travada, 4, 3, 11)
selo3 = Selo(seloBrLar_Vazio, seloBrLar_Feito, 3)

casa4_1 = CasaTab(517.5, jan_alt/2, casaLarBr_Travada, 4, 4, 12)
casa4_2 = CasaTab(677.5, jan_alt/2, casaLarBr_Travada, 4, 4, 13)
selo4 = Selo(seloLarBr_Vazio, seloLarBr_Feito, 3)

casa5_1 = CasaTab(437.5, jan_alt/2, casaLarBr_Travada, 4, 5, 14)
casa5_2 =  CasaTab(517.5, jan_alt/2, casaLarBr_Travada, 4, 5, 15)
casa5_3 = CasaTab(677.5, jan_alt/2, casaLarBr_Travada, 4, 5, 16)
casa5_4 = CasaTab(757.5, jan_alt/2, casaLarBr_Travada, 4, 5, 17)
selo5 = Selo(seloAzBr_Vazio, seloAzBr_Feito, 3)

casa6_1 = CasaTab(357.5, jan_alt/2, casaBrAz_Travada, 4, 6, 18)
casa6_2 = CasaTab(437.5, jan_alt/2, casaBrAz_Travada, 4, 6, 19)
casa6_3 = CasaTab(517.5, jan_alt/2, casaBrAz_Travada, 4, 6, 20)
casa6_4 = CasaTab(597.5, jan_alt/2, casaBrAz_Travada, 4, 6, 21)
casa6_5 = CasaTab(677.5, jan_alt/2, casaBrAz_Travada, 4, 6, 22)
casa6_6 = CasaTab(757.5, jan_alt/2, casaBrAz_Travada, 4, 6, 23)
casa6_7 = CasaTab(837.5, jan_alt/2, casaBrAz_Travada, 4, 6, 24)
selo6 = Selo(seloBrAz_Vazio, seloBrAz_Feito, 3)

casas = [
        casa1_1, casa1_2, casa1_3,
        casa2_1, casa2_2, casa2_3, casa2_4, casa2_5,
        casa3_1, casa3_2, casa3_3,
        casa4_1, casa4_2,
        casa5_1, casa5_2, casa5_3, casa5_4,
        casa6_1, casa6_2, casa6_3, casa6_4, casa6_5, casa6_6, casa6_7
        ]

# função Leave
def leave(evento):
    if evento.type == pygame.QUIT: # usuário fecha com o X da janela
        pygame.quit()
        exit()

# criação menu lateral - tem os botões do Tab, do Perfil e das Tarefas
def menuLat():
    # barra lateral
    retangMenu = pygame.Rect(0, 0, 120, 540)
    retangMenu.center = (52, jan_alt/2)
    pygame.draw.rect(janela, (255, 255, 255), retangMenu)

    # imagem Mauá
    imagemMaua.criarImagem(janela, 55, 55)

    if isProfessor == 0:
        textoLoginReq.gerarTexto("Tabuleiro", janela, 55, 180, (0, 69, 135))
        textoLoginReq.gerarTexto("Perfil", janela, 55, 280, (0, 69, 135))

    # botões menu aluno
        if janelaNumber == 2:
            botaoTabuleiro.draw(janela)
            botaoPerfilFora.draw(janela)
        elif janelaNumber == 3:
            botaoTabuleiroFora.draw(janela)
            botaoPerfil.draw(janela)
        elif janelaNumber == 4:
            botaoTabuleiroFora.draw(janela)
            botaoPerfilFora.draw(janela)
    else:
        textoLoginReq.gerarTexto("Tabuleiro", janela, 55, 180, (0, 69, 135))
        textoLoginReq.gerarTexto("Tarefas", janela, 55, 280, (0, 69, 135))
        textoLoginReq.gerarTexto("Aluno", janela, 55, 380, (0, 69, 135))
        if janelaNumber == 2:
            botaoTabuleiro.draw(janela)
            botaoTarefaFora.draw(janela)
            botaoNewUserFora.draw(janela)
        elif janelaNumber == 3.1:
            botaoTabuleiroFora.draw(janela)
            botaoTarefa.draw(janela)
            botaoNewUserFora.draw(janela)
        elif janelaNumber == 4.1:
            botaoTabuleiroFora.draw(janela)
            botaoTarefaFora.draw(janela)
            botaoNewUser.draw(janela)

    # botão saída
    botaoExit.draw(janela)

# criação menu erro
def menuErro(texto):
    # aba focada
    retangMenu = pygame.Rect(0, 0, 400, 180) # x, y, larg, alt
    retangMenu.center = (jan_larg/2, jan_alt/2) # posição a partir do centro
    pygame.draw.rect(janela, (255, 255, 255), retangMenu, border_radius=10) # criação do retangulo

    # texto do erro
    errorTextLogin.gerarTexto(texto, janela, jan_larg/2, jan_alt/2, (255, 50, 50))

    # botão para sair
    botaoOkLogin.draw(janela)

def menuRight(texto):
    # aba focada
    retangMenu = pygame.Rect(0, 0, 400, 180) # x, y, larg, alt
    retangMenu.center = (jan_larg/2, jan_alt/2) # posição a partir do centro
    pygame.draw.rect(janela, (255, 255, 255), retangMenu, border_radius=10) # criação do retangulo

    # texto do erro
    errorTextLogin.gerarTexto(texto, janela, jan_larg/2, jan_alt/2, (50, 255, 50))

    # botão para sair
    botaoOkLogin.draw(janela)

def menuInfo(texto):
    # aba focada
    retangMenu = pygame.Rect(0, 0, 400, 180) # x, y, larg, alt
    retangMenu.center = (jan_larg/2, jan_alt/2) # posição a partir do centro
    pygame.draw.rect(janela, (255, 255, 255), retangMenu, border_radius=10) # criação do retangulo

    # texto do erro
    errorTextLogin.gerarTexto(texto, janela, jan_larg/2, jan_alt/2, (0, 0, 0))

    # botão para sair
    botaoOkLogin.draw(janela)

# preenchimento de janela/imagem
def draw(valor):
    janela.fill(valor) # funciona com cor predefinida, codigo hexadecimal e rgb

def drawAba(corFundo):
    draw(corFundo)
    menuLat()

def desenharAbaTab(tela, tituloAba, pagina, corFundo, corTab, haveSetas=True):
    drawAba(corFundo)

    if haveSetas:
        # setas menu
        botaoSetaE.draw(tela)
        botaoSetaD.draw(tela)

    tabuleiroBase.criarTabuleiro(tela, 597.5, 270, corTab, 10)

    textoAbaSup.gerarTexto(tituloAba, tela, 597.5, 25, (corTab))
    textoAbaSup.gerarTexto(pagina, tela, 597.5, 515, (corTab))

def casaTabCriar(tela, aba, spriteTravado, spriteFazer, spriteFeito, spriteFalha, casaTabuleiro):
    casaTabDraw(tela, aba, casaTabuleiro, spriteTravado, spriteFazer, spriteFeito, spriteFalha)
    casaTabClick(casaTabuleiro)

def casaTabDraw(tela, abaAtual, casaTab, spriteLock, spriteToDo, spriteDone, spriteFalha):
    if casaTab.tarefaData == 0:
        casaTab.draw(tela, spriteFalha, abaAtual)
    else:
        if casaTab.trava == 0:
            if casaTab.done == 0:
                casaTab.draw(tela, spriteToDo, abaAtual)
            else:
                casaTab.draw(tela, spriteDone, abaAtual)
        elif casaTab.trava == 1 or casaTab.travaLocal == 1:
            casaTab.draw(tela, spriteLock, abaAtual)

def casaTabClick(casaTab):
    if casaTab.entrar():
        global janelaNumber, idCasa, nomeCasa, descCasa
        global curso, idTarefa, descTarefaAluno, dataEntregaTarefa
        
        print(casaTab.tarefaData)

        idCasa = casaTab.casaNumero

        if isProfessor == 0:
            if casaTab.trava == 0:
                janelaNumber = 4
                
                x = SQL.retrieveCasa(idCasa)
                nomeCasa = x[0]
                descCasa = x[1]

                i = SQL.retrieveTarefa(idCasa, curso)
                idTarefa = i[0]
                descTarefaAluno = i[1]
                dataEntregaTarefa = i[2]
                audio.playSeta()
        else:            
            if casaTab.trava == 0:
                SQL.mudarLibCasa(1, idCasa)
                casaTab.checarStatus(idCasa)
                audio.playSeta()
            else:
                SQL.mudarLibCasa(0, idCasa)
                casaTab.checarStatus(idCasa)
                audio.playSeta()

# game loop
while True:
    if janelaNumber == 1: # tela inicial (tela de login)
        draw((0, 69, 135))

        # retangulo do menu
        retangMenu = pygame.Rect(0, 0, 400, 360) # x, y, larg, alt
        retangMenu.center = (jan_larg/2, jan_alt/2) # posição a partir do centro
        pygame.draw.rect(janela, (255, 255, 255), retangMenu, border_radius=10) # criação do retangulo

        imagemMaua.criarImagem(janela, (jan_larg/2 - 100), 180)

        mauaTextoLogin.gerarTexto("Mauá Virtual", janela, (jan_larg/2 + 60), 160, (0, 69, 135))
        mauaTextoLogin.gerarTexto("Tabletop", janela, (jan_larg/2 + 30), 200, (0, 69, 135))

        textoLoginReq.gerarTexto("E-Mail", janela, (jan_larg/2 - 100), 245, (0, 69, 135))
        textoLoginReq.gerarTexto("Senha", janela, (jan_larg/2 - 100), 299, (0, 69, 135))

        caixaUser.draw(janela, jan_larg/2, jan_alt/2)
        caixaSenha.draw(janela, jan_larg/2, (jan_alt - (jan_alt//2.5)))

        if caixaSenha.textHidden == True:
            botaoSenhaOff.draw(janela)
        elif caixaSenha.textHidden == False:
            botaoSenha.draw(janela)
        
        botaoEnter.draw(janela)

        if botaoEnter.click():
            textoEmail = caixaUser.escritaTexto()
            textoSenha = caixaSenha.escritaTexto()
            if all([textoEmail, textoSenha]):
                busca = SQL.validarLogin(textoEmail, textoSenha)
                if busca != None:
                    idUsuario = busca[0]
                    nomeUsuario = busca[1]
                    isProfessor = busca[4]
                    curso = busca[5]
                    audio.playAcerto()
                    if isProfessor == 0:
                        infoUser = SQL.puxarInfoAluno(idUsuario)
                        idAluno = infoUser[0]
                        raUsuario = infoUser[2]
                        progUsuario = infoUser[3]
                        avatar = infoUser[4]
                    janelaNumber = 2
                else:
                    janelaNumber = 999
                    audio.playErro()

        if caixaSenha.textHidden == True:
            if botaoSenhaOff.click():
                caixaSenha.textHidden = False
        else:
            if botaoSenha.click():
                caixaSenha.textHidden = True

        for event in pygame.event.get():
            caixaUser.select(event)
            caixaUser.digitando(event)
            caixaUser.textHidden = False

            caixaSenha.select(event)
            caixaSenha.digitando(event)

            leave(event)
    
    if janelaNumber == 2: # tela do tabuleiro
        if abaLogado == 1:
            desenharAbaTab(janela, "Explorador", "1/6", (15, 117, 187), (254, 246, 237))
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa1_1)
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa1_2)
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa1_3)
            selo1.gerarBase(janela, 597.5, jan_alt/1.5)

            casa1_1.tarefaData = SQL.checarData(1, curso)
            casa1_2.tarefaData = SQL.checarData(2, curso)
            casa1_3.tarefaData = SQL.checarData(3, curso)

            if casa1_3.done == 1:
                selo1.moduloConc()

        elif abaLogado == 2:
            desenharAbaTab(janela, "Conector", "2/6", (254, 246, 237), (15, 117, 187))
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa2_1)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa2_2)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa2_3)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa2_4)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa2_5)
            selo2.gerarBase(janela, 597.5, jan_alt/1.5)
            
            casa2_1.tarefaData = SQL.checarData(4, curso)
            casa2_2.tarefaData = SQL.checarData(5, curso)
            casa2_3.tarefaData = SQL.checarData(6, curso)
            casa2_4.tarefaData = SQL.checarData(7, curso)
            casa2_5.tarefaData = SQL.checarData(8, curso) 

            if casa2_5.done == 1:
                selo2.moduloConc()
        
        elif abaLogado == 3:
            desenharAbaTab(janela, "Transformador", "3/6", (247, 148, 29), (254, 246, 237))
            casaTabCriar(janela, abaLogado, casaBrLar_Travada, casaBrLar_ToDo, casaBrLar_Done, casaBrLar_Fail, casa3_1)
            casaTabCriar(janela, abaLogado, casaBrLar_Travada, casaBrLar_ToDo, casaBrLar_Done, casaBrLar_Fail, casa3_2)
            casaTabCriar(janela, abaLogado, casaBrLar_Travada, casaBrLar_ToDo, casaBrLar_Done, casaBrLar_Fail, casa3_3)
            selo3.gerarBase(janela, 597.5, jan_alt/1.5)

            casa3_1.tarefaData = SQL.checarData(9, curso)
            casa3_2.tarefaData = SQL.checarData(10, curso)
            casa3_3.tarefaData = SQL.checarData(11, curso)

            if casa3_3.done == 1:
                selo3.moduloConc()

        elif abaLogado == 4:
            desenharAbaTab(janela, "Conhecedor", "4/6", (254, 246, 237), (247, 148, 29))
            casaTabCriar(janela, abaLogado, casaLarBr_Travada, casaLarBr_ToDo, casaLarBr_Done, casaLarBr_Fail, casa4_1)
            casaTabCriar(janela, abaLogado, casaLarBr_Travada, casaLarBr_ToDo, casaLarBr_Done, casaLarBr_Fail, casa4_2)
            selo4.gerarBase(janela, 597.5, jan_alt/1.5)

            casa4_1.tarefaData = SQL.checarData(12, curso)
            casa4_2.tarefaData = SQL.checarData(13, curso)

            if casa4_2.done == 1:
                selo4.moduloConc()

        elif abaLogado == 5:
            desenharAbaTab(janela, "Planejador", "5/6", (15, 117, 187), (254, 246, 237))
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa5_1)
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa5_2)
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa5_3)
            casaTabCriar(janela, abaLogado, casaBrAz_Travada, casaBrAz_ToDo, casaBrAz_Done, casaBrAz_Fail, casa5_4)
            selo5.gerarBase(janela, 597.5, jan_alt/1.5)

            casa5_1.tarefaData = SQL.checarData(14, curso)
            casa5_2.tarefaData = SQL.checarData(15, curso)
            casa5_3.tarefaData = SQL.checarData(16, curso)
            casa5_4.tarefaData = SQL.checarData(17, curso)

            if casa5_4.done == 1:
                selo5.moduloConc()

        elif abaLogado == 6:
            desenharAbaTab(janela, "Realizador", "6/6", (254, 246, 237), (15, 117, 187))
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_1)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_2)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_3)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_4)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_5)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_6)
            casaTabCriar(janela, abaLogado, casaAzBr_Travada, casaAzBr_ToDo, casaAzBr_Done, casaAzBr_Fail, casa6_7)

            casa6_1.tarefaData = SQL.checarData(18, curso)
            casa6_2.tarefaData = SQL.checarData(19, curso)
            casa6_3.tarefaData = SQL.checarData(20, curso)
            casa6_4.tarefaData = SQL.checarData(21, curso)
            casa6_5.tarefaData = SQL.checarData(22, curso)
            casa6_6.tarefaData = SQL.checarData(23, curso)
            casa6_7.tarefaData = SQL.checarData(24, curso)

            selo6.gerarBase(janela, 597.5, jan_alt/1.5)
            if casa6_7.done == 1:
                selo6.moduloConc()

        if botaoExit.click():
            janelaNumber = 1
            audio.playSaida()

        if botaoSetaE.click():
            audio.playSeta()
            if abaLogado>1:
                abaLogado -= 1
            else:
                abaLogado = 6
        if botaoSetaD.click():
            audio.playSeta()
            if abaLogado<6:
                abaLogado += 1
            else:
                abaLogado = 1
        if isProfessor == 0:
            if botaoPerfilFora.click():
                audio.playSeta()
                janelaNumber = 3
        else:
            if botaoTarefaFora.click():
                audio.playSeta()
                janelaNumber = 3.1
            if botaoNewUserFora.click():
                audio.playSeta()
                janelaNumber = 4.1
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # se apertar Q
                    audio.playSeta()
                    if abaLogado>1:
                        abaLogado -= 1
                    else:
                        abaLogado = 6
                if event.key == pygame.K_e:
                    audio.playSeta()
                    if abaLogado<6:
                        abaLogado += 1
                    else:
                        abaLogado = 1
                if event.key == pygame.K_DELETE:
                    progUsuario = (SQL.atualizarProgresso(raUsuario, 0.0))
                    print(f"{progUsuario}%")

            leave(event)
    
    if janelaNumber == 3: # perfil
        drawAba((0, 69, 135))
        textoAbaSup.gerarTexto(nomeUsuario, janela, 597.5, 25, (254, 246, 237))
        textoAbaSup.gerarTexto(raUsuario, janela, 477.5, 65, (254, 246, 237))
        textoAbaSup.gerarTexto(f"Progresso: {progUsuario:.2f}%", janela, 717.5, 65, (254, 246, 237))

        if botaoTabuleiroFora.click():
            audio.playSeta()
            janelaNumber = 2

        if botaoExit.click():
            janelaNumber = 1
            audio.playSaida()
        
        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 3.1: # adm tarefas (PROFESSOR ONLY)
        if abaTarefas == 1: # criar tarefa
            drawAba((0, 69, 135))
            desenharAbaTab(janela, "Administração de Tarefas", "Criação de Tarefas", (0, 69, 135), (254, 246, 237))

            caixaDataEntrega.draw(janela, 597.5, 110, larguraMax=400)
            textoLoginReq.gerarTexto("Data da Entrega (dd/mm/aaaa)", janela, 597.5, 80, (0, 69, 135))

            caixaIdCasa.draw(janela, 597.5, 170, larguraMax=400)
            textoLoginReq.gerarTexto("Número da Casa", janela, 597.5, 140, (0, 69, 135))

            caixaCurso.draw(janela, 597.5, 230, larguraMax=400)
            textoLoginReq.gerarTexto("Abreviação do Curso", janela, 597.5, 200, (0, 69, 135))

            caixaDescTarefa.drawLong(janela, 597.5, 330, 120, larguraMax=400)
            textoLoginReq.gerarTexto("Descrição da Tarefa", janela, 597.5, 260, (0, 69, 135))

            botaoNewTarefa.draw(janela)

            if botaoNewTarefa.click():
                dateEntrega = caixaDataEntrega.escritaTexto()
                idCasaTarefa = caixaIdCasa.escritaTexto()
                cursoTarefa = caixaCurso.escritaTexto()
                descTarefa = caixaDescTarefa.escritaTexto()
                if all([dateEntrega, idCasaTarefa, cursoTarefa, descTarefa]):
                    dataTarefa = datetime.strptime(dateEntrega, "%d/%m/%Y").strftime("%Y-%m-%d")
                    criacao = SQL.criarTarefa(descTarefa, dataTarefa, idCasaTarefa, cursoTarefa)
                    if criacao == 0:
                        janelaNumber = 1000.1
                    elif criacao == 1:
                        janelaNumber = 1000
                    else:
                        audio.playAcerto()
                        lastJanela = 3.1
                        janelaNumber = 777
            
        elif abaTarefas == 2: # visualizar desemp
            drawAba((0, 69, 135))
            desenharAbaTab(janela, "Administração de Tarefas", "Visualização de Desempenho", (0, 69, 135), (254, 246, 237))

            caixaCasaBuscada.draw(janela, 597.5, 200, larguraMax=400)
            textoLoginReq.gerarTexto("Casa a ser Analisada", janela, 597.5, 170, (0, 69, 135))
        
            caixaCursoBuscado.draw(janela, 597.5, 300, larguraMax=400)
            textoLoginReq.gerarTexto("Curso a ser Analisado", janela, 597.5, 270, (0, 69, 135))
            botaoAnaliseEfic.draw(janela)

            if botaoAnaliseEfic.click():
                casaBuscada = caixaCasaBuscada.escritaTexto()
                cursoBuscado = caixaCursoBuscado.escritaTexto()

                if all([cursoBuscado, casaBuscada]):
                    t = SQL.contagemRespostas(cursoBuscado, casaBuscada)
                    if t != -1:
                        m = SQL.totalAlunosCurso(cursoBuscado)
                    else:
                        janelaNumber
                    desempenho = (t/m)*100
                    janelaNumber = 100

        elif abaTarefas == 3: # ver resposta individual
            drawAba((0, 69, 135))
            desenharAbaTab(janela, "Administração de Tarefas", "Aba de Respostas", (0, 69, 135), (254, 246, 237))

            caixaCasaBuscada.draw(janela, 597.5, 200, larguraMax=400)
            textoLoginReq.gerarTexto("Casa da Tarefa", janela, 597.5, 170, (0, 69, 135))

            caixaRaBuscado.draw(janela, 597.5, 300, larguraMax=400)
            textoLoginReq.gerarTexto("RA do Aluno", janela, 597.5, 270, (0, 69, 135))

            botaoCopyResposta.draw(janela)

            if botaoCopyResposta.click():
                casaBuscada = caixaCasaBuscada.escritaTexto()
                raBuscado = caixaRaBuscado.escritaTexto()
                t = SQL.checarResposta(raBuscado, casaBuscada)
                if t == -1: # erro: sem tarefa nessa casa
                    audio.playErro()
                    janelaNumber = 1002
                elif t == 0: # sem resposta
                    audio.playErro()
                    janelaNumber = 1002.1
                else: # resposta copiada
                    audio.playAcerto()
                    lastJanela=3.1
                    pyperclip.copy(t)
                    janelaNumber = 777

        else:
            abaTarefas = 1

        if botaoTabuleiroFora.click():
            audio.playSeta()
            janelaNumber = 2

        if botaoNewUserFora.click():
            audio.playSeta()
            janelaNumber = 4.1

        if botaoSetaE.click():
            audio.playSeta()
            if abaTarefas>1:
                abaTarefas -= 1
            else:
                abaTarefas = 3
        if botaoSetaD.click():
            audio.playSeta()
            if abaTarefas<3:
                abaTarefas += 1
            else:
                abaTarefas = 1
        
        if botaoExit.click():
            janelaNumber = 1
            audio.playSaida()
        
        for event in pygame.event.get():
            caixaDescTarefa.select(event)
            caixaDescTarefa.digitando(event)
            caixaDescTarefa.textHidden = False

            caixaDataEntrega.select(event)
            caixaDataEntrega.digitando(event)
            caixaDataEntrega.textHidden = False

            caixaIdCasa.select(event)
            caixaIdCasa.digitando(event)
            caixaIdCasa.textHidden = False

            caixaCurso.select(event)
            caixaCurso.digitando(event)
            caixaCurso.textHidden = False

            caixaCasaBuscada.select(event)
            caixaCasaBuscada.digitando(event)
            caixaCasaBuscada.textHidden = False

            caixaCursoBuscado.select(event)
            caixaCursoBuscado.digitando(event)
            caixaCursoBuscado.textHidden = False

            caixaRaBuscado.select(event)
            caixaRaBuscado.digitando(event)
            caixaRaBuscado.textHidden = False

            if event.type == pygame.KEYDOWN:
                if not any([caixaCurso.ativo, caixaIdCasa.ativo, caixaDataEntrega.ativo, caixaDescTarefa.ativo]):
                    if event.key == pygame.K_q: # se apertar Q
                        audio.playSeta()
                        if abaTarefas>1:
                            abaTarefas -= 1
                        else:
                            abaTarefas = 3
                    if event.key == pygame.K_e: # se apertar E
                        audio.playSeta()
                        if abaTarefas<3:
                            abaTarefas += 1
                        else:
                            abaTarefas = 1

            leave(event)

    if janelaNumber == 4: # casa (tarefa)
        drawAba((0, 69, 135))


        textCasa = f"Casa {idCasa}: {nomeCasa}"
        desenharAbaTab(janela, textCasa, descCasa, (0, 69, 135), (254, 246, 237), haveSetas=False)
        textoPadrao.gerarTextoQuebrado(descTarefaAluno, janela, 300, 80, (0, 0, 0), 600)
        
        if SQL.checarResposta(raUsuario, idTarefa) == 0:
            botaoConcTarefa.draw(janela)
            caixaRespTarefa.draw(janela, 597.5, 300, larguraMax=400)

            if botaoConcTarefa.click():
                respostaTarefa = caixaRespTarefa.escritaTexto()
                x = SQL.responderTarefa(respostaTarefa, idAluno, idTarefa)
                if x == 1:
                    audio.playAcerto()
                    lastJanela = 4
                    for casaTab in casas:
                        if casaTab.casaNumero == idCasa:
                            casaTab.done = 1
                    progUsuario = SQL.atualizarProgresso(raUsuario, progUsuario+4.16667)
                    janelaNumber = 777
        else:
            botaoCopyResposta.draw(janela)

            if botaoCopyResposta.click():
                casaBuscada = idCasa
                raBuscado = raUsuario
                t = SQL.checarResposta(raBuscado, casaBuscada)
                if t == 0: # sem resposta
                    audio.playErro()
                    janelaNumber = 1003.1
                else: # resposta copiada
                    audio.playAcerto()
                    lastJanela=2
                    pyperclip.copy(t)
                    janelaNumber = 777

        if botaoTabuleiroFora.click():
            audio.playSeta()
            janelaNumber = 2

        if botaoPerfilFora.click():
            audio.playSeta()
            janelaNumber = 3

        if botaoExit.click():
            janelaNumber = 1
            audio.playSaida()
        
        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 4.1: # aba add user (PROFESSOR ONLY)
        drawAba((0, 69, 135))
        desenharAbaTab(janela, "Adição de Aluno", "", (0, 69, 135), (254, 246, 237), haveSetas=False)

        caixaNomeAluno.draw(janela, 597.5, 110, larguraMax=400)
        textoLoginReq.gerarTexto("Nome", janela, 597.5, 80, (0, 69, 135))

        caixaRaAluno.draw(janela, 597.5, 170, larguraMax=400)
        textoLoginReq.gerarTexto("RA", janela, 597.5, 140, (0, 69, 135))

        caixaEmailAluno.draw(janela, 597.5, 230, larguraMax=400)
        textoLoginReq.gerarTexto("E-Mail", janela, 597.5, 200, (0, 69, 135))

        caixaSenhaAluno.draw(janela, 597.5, 290, larguraMax=400)
        textoLoginReq.gerarTexto("Senha", janela, 597.5, 260, (0, 69, 135))

        caixaCursoAluno.draw(janela, 597.5, 350, larguraMax=400)
        textoLoginReq.gerarTexto("Abreviação do Curso", janela, 597.5, 320, (0, 69, 135))

        botaoAddAluno.draw(janela)

        if botaoAddAluno.click():
            nomeAluno = caixaNomeAluno.escritaTexto()
            raAluno = caixaRaAluno.escritaTexto()
            emailAluno = caixaEmailAluno.escritaTexto()
            senhaAluno = caixaSenhaAluno.escritaTexto()
            cursoAluno = caixaCursoAluno.escritaTexto()
            if all([nomeAluno, raAluno, emailAluno, senhaAluno, cursoAluno]):
                criacao = SQL.adicionarAluno(nomeAluno, emailAluno, senhaAluno, cursoAluno, raAluno)
                if criacao == 0:
                    janelaNumber = 1001
                elif criacao == -1:
                    janelaNumber = 1001.1
                else:
                    audio.playAcerto()
                    lastJanela = 4.1
                    janelaNumber = 777


        if botaoTabuleiroFora.click():
            audio.playSeta()
            janelaNumber = 2

        if botaoTarefaFora.click():
            audio.playSeta()
            janelaNumber = 3.1

        if botaoExit.click():
            janelaNumber = 1
            audio.playSaida()
        
        for event in pygame.event.get():
            caixaNomeAluno.select(event)
            caixaNomeAluno.digitando(event)
            caixaNomeAluno.textHidden = False

            caixaRaAluno.select(event)
            caixaRaAluno.digitando(event)
            caixaRaAluno.textHidden = False

            caixaEmailAluno.select(event)
            caixaEmailAluno.digitando(event)
            caixaEmailAluno.textHidden = False

            caixaSenhaAluno.select(event)
            caixaSenhaAluno.digitando(event)
            caixaSenhaAluno.textHidden = False

            caixaCursoAluno.select(event)
            caixaCursoAluno.digitando(event)
            caixaCursoAluno.textHidden = False

            leave(event)

    if janelaNumber == 100: # aba desempenho
        draw((0, 5, 30))
        menuInfo(f"Desempenho: {desempenho:.2f}%")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 3.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1000.1: # erro curso inexistente
        draw((0, 5, 30))
        menuErro(f"Erro: Abreviação {cursoBuscado} não existe!")
        
        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 3.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 777: # aba ação sucesso
        draw((0, 5, 30))
        menuRight("Ação Concluida")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = lastJanela

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 999: # erro de login
        draw((0, 5, 30))

        menuErro("Erro: Email e/ou Senha Incorreto(s)")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1000: # erro tarefa já existe
        draw((0, 5, 30))

        menuErro(f"Erro: Há tarefa no curso e na casa")


        if botaoOkLogin.click():
            janelaNumber = 3.1

        for event in pygame.event.get():
            leave(event)
    
    if janelaNumber == 1000.1: # erro curso inexistente
        draw((0, 5, 30))
        menuErro(f"Erro: Abreviação {cursoTarefa} não existe!")
        
        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 3.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1001: # erro aluno já existe
        draw((0, 5, 30))

        menuErro(f"Erro: Aluno {nomeAluno} já existe no sistema!")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 4.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1001.1: # erro curso inexistente
        draw((0, 5, 30))
        menuErro(f"Erro: Abreviação {cursoAluno} não existe!")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 4.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1002: # erro tarefa inexistente
        draw((0, 5, 30))
        menuErro(f"Erro: Não há tarefa na casa {casaBuscada}!")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 3.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1002.1: # não há resposta desse aluno
        draw((0, 5, 30))
        menuErro(f"Erro: O aluno não respondeu!")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 3.1

        for event in pygame.event.get():
            leave(event)

    if janelaNumber == 1003.1: # você não respondeu (por garantia, existe)
        draw((0, 5, 30))
        menuErro(f"Você não respondeu essa tarefa!")

        if botaoOkLogin.click():
            audio.playSeta()
            janelaNumber = 2

        for event in pygame.event.get():
            leave(event)

    # game tick
    pygame.display.update() # atualiza informações
    clock.tick(60) # colocar 60 fps