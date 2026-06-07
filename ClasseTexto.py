import pygame

class TextMessage():
    def __init__(self, fonte, tamanho):
        self.fonte = pygame.font.SysFont(fonte, tamanho)
    
    def gerarTexto (self, texto, tela, posX, posY, cor):
        self.color = cor
        self.textoUser = texto
        self.textoTela = self.fonte.render(self.textoUser, True, (self.color))
        self.rectTexto = self.textoTela.get_rect()
        self.rectTexto.center = (posX, posY)
        tela.blit(self.textoTela, self.rectTexto)

    def gerarTextoQuebrado(self, texto, tela, posX, posY, cor, larguraMax):
        palavras = texto.split(" ")
        linhas = []
        linhaAtual = ""

        for palavra in palavras:
            teste = linhaAtual + palavra + " "
            larguraTeste, _ = self.fonte.size(teste)

            if larguraTeste <= larguraMax:
                linhaAtual = teste
            else:
                if linhaAtual:
                    linhas.append(linhaAtual.rstrip())
                linhaAtual = palavra + " "

        if linhaAtual:
            linhas.append(linhaAtual.rstrip())

        alturaLinha = self.fonte.get_linesize()

        for i, linha in enumerate(linhas):
            superficie = self.fonte.render(linha, True, cor)
            tela.blit(superficie, (posX, posY + i * alturaLinha))