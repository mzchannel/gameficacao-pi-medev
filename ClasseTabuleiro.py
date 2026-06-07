import pygame

class Tabuleiro():
    def __init__(self, larg, alt):
        self.x = larg
        self.y = alt
    
    def criarTabuleiro(self, tela, posX, posY, cor, corner):
        self.tabuleiroCriado = pygame.Rect(0, 0, self.x, self.y)
        self.tabuleiroCriado.center = (posX, posY)
        pygame.draw.rect(tela, cor, self.tabuleiroCriado, border_radius=corner)