from ClasseBotao import Button as Botao
import BibliotecaCodigoBD as SQL

class CasaTab():
    def __init__(self, posX, posY, imagem, escala, modulo, casaNum):
        self.casa = Botao(posX, posY, imagem, escala)
        self.modulo = modulo
        self.casaNumero = casaNum
        self.trava = SQL.checarCasa(self.casaNumero) # 0 = To Do; 1 = Travada
        self.travaLocal = 0
        self.done = 0 # 0 = To Do; 1 = Done
        self.tarefaData = 1

    def draw(self, tela, novaImagem, moduloTela):
        if moduloTela == self.modulo:
            self.casa.mudarSprite(novaImagem)
            self.casa.draw(tela)
    
    def entrar(self):
        if self.casa.click():
            return True
        
    def checarStatus(self, idCasa):
        self.trava = SQL.checarCasa(idCasa)
        return self.trava