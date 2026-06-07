import pygame
import pyperclip

class TextBox():
    def __init__(self, ativo, corOn, corOff, tamanho):
        self.fonteTexto = pygame.font.SysFont("BAHNSCHRIFT", tamanho) # fonte do texto
        self.textoUser = "" # variavel que armazena o texto exibido
        self.textOrig = "" # variavel que armazena o texto digitado
        self.ativo = ativo
        self.textHidden = True

        # desenha retângulo
        self.inputRect = pygame.Rect(0, 0, 140, 32)

        self.inputCorAtiva = pygame.Color(corOn)
        self.inputCorPassiva = pygame.Color(corOff)
        self.cor = self.inputCorPassiva

    def mudaFlag(self):
        if self.ativo:
            self.cor = self.inputCorAtiva
        else:
            self.cor = self.inputCorPassiva

    def draw(self, tela, x, y, larguraMax=250):
        # retangulo do input text
        self.mudaFlag()

        # posição retângulo
        self.inputRect.center = (x, y)

        if self.textHidden == True:
            self.letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890@.-"
            segurança = str.maketrans(self.letras, len(self.letras)*"*")
            self.textoUser = self.textOrig.translate(segurança)

            self.texto_tela = self.fonteTexto.render(self.textoUser, True, (0, 0, 0)) # renderização do texto
            self.inputRect.w = max(larguraMax, self.texto_tela.get_width()+20)

            pygame.draw.rect(tela, self.cor, self.inputRect, 2)
            tela.blit(self.texto_tela, (self.inputRect.x+5, self.inputRect.y+6)) # precisa colocar o blit aq pois ele atualiza o texto da tela
        else:
            self.texto_tela = self.fonteTexto.render(self.textOrig, True, (0, 0, 0)) # renderização do texto
            self.inputRect.w = max(larguraMax, self.texto_tela.get_width()+20)

            pygame.draw.rect(tela, self.cor, self.inputRect, 2)
            tela.blit(self.texto_tela, (self.inputRect.x+5, self.inputRect.y+6)) # precisa colocar o blit aq pois ele atualiza o texto da tela

    def drawLong(self, tela, x, y, alturaMin, larguraMax=250):
        self.mudaFlag()

        # Quebra o texto caractere por caractere para garantir o wrap
        linhas = []
        linhaAtual = ""

        for char in self.textOrig:
            teste = linhaAtual + char
            larguraTeste, _ = self.fonteTexto.size(teste)

            if larguraTeste <= larguraMax - 10:  # margem de 10px
                linhaAtual = teste
            else:
                linhas.append(linhaAtual)
                linhaAtual = char  # começa nova linha com o char que excedeu

        if linhaAtual:
            linhas.append(linhaAtual)

        # Se não há texto, garante pelo menos uma linha vazia
        if not linhas:
            linhas = [""]

        # Calcula altura total do retângulo com base nas linhas
        alturaLinha = self.fonteTexto.get_linesize()
        alturaTotal = max(alturaMin, alturaLinha * len(linhas) + 12)

        # Posiciona e redimensiona o retângulo
        self.inputRect.w = larguraMax
        self.inputRect.h = alturaTotal
        self.inputRect.center = (x, y)

        pygame.draw.rect(tela, self.cor, self.inputRect, 2)

        # Renderiza cada linha
        for i, linha in enumerate(linhas):
            superficie = self.fonteTexto.render(linha, True, (0, 0, 0))
            tela.blit(superficie, (self.inputRect.x + 5, self.inputRect.y + 6 + i * alturaLinha))

    def select(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.inputRect.collidepoint(evento.pos):
                self.ativo = True
            else:
                self.ativo = False
    
    def escritaTexto(self):
        return self.textOrig

    def digitando(self, evento):
        if evento.type == pygame.KEYDOWN: # se uma tecla foi clicada
            if self.ativo == True:
                if evento.key == pygame.K_BACKSPACE: # se a tecla foi backspace
                    self.textOrig = self.textOrig[0:-1] # Remove
                elif evento.key == (pygame.K_RETURN or pygame.K_KP_ENTER): # ao apertar Enter
                    self.ativo = False
                elif evento.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.textOrig += pyperclip.paste()
                else:
                    self.textOrig += evento.unicode # adiciona o digito na tela