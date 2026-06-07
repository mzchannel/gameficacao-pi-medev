import pygame

class GerarImagem():
    def __init__(self, imagemBase, escala):
        self.imagemBase = imagemBase
        self.escala = escala
        self.larg = self.imagemBase.get_width()
        self.alt = self.imagemBase.get_height()
    
    def criarImagem(self, tela, posX, posY):
        self.imagem = pygame.transform.scale(
            self.imagemBase,
            (int(self.larg*self.escala), int(self.alt*self.escala))
        )
        self.imagemGerada = self.imagem.get_rect()
        self.imagemGerada.center = (posX, posY)
        tela.blit(self.imagem, self.imagemGerada)
    
    def mudarImagem(self, novaImagem):
        self.imagemBase = novaImagem