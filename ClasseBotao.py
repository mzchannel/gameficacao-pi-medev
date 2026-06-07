import pygame

# cria a classe do Botão
class Button():
    # define a inicialização e quais variaveis são da classe
    def __init__(self, x, y, imagem, escala):
        self.sprite = imagem
        self.larg = self.sprite.get_width()
        self.alt = self.sprite.get_height()
        self.escala = escala
        self.posX = x
        self.posY = y
        self.pressed = False
    
    def draw(self, tela):
        self.imagem = pygame.transform.scale(
            self.sprite,
            (int(self.larg*self.escala), int(self.alt*self.escala))
        )
        self.rect = self.imagem.get_rect()
        self.rect.center = (self.posX, self.posY)
        # desenha o botão
        tela.blit(self.imagem, (self.rect.x, self.rect.y))

    def mudarSprite(self, novaImagem):
        self.sprite = novaImagem

    def click(self):
        acaoBotao = False
        # pega posição do mouse
        posMouse = pygame.mouse.get_pos()

        # checagem de colisão com o mouse
        if self.rect.collidepoint(posMouse):
            # se o botão esquerdo do mouse clicar no botão (não fica repetindo enquanto estiver clicando)
            if pygame.mouse.get_pressed()[0] == 1 and self.pressed == False:
                self.pressed = True
                acaoBotao = True
            
            # checa se o botão esquerdo do mouse foi solto
            if pygame.mouse.get_pressed()[0] == 0:
                self.pressed = False

        # entrega valor da checagem de ação
        return acaoBotao