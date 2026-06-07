from BibliotecaImagemGerador import GerarImagem as SeloIm

class Selo():
    def __init__(self, vazia, selo, escala):
        self.imagemSelo = selo
        self.imagemVazia = vazia
        self.selo = SeloIm(self.imagemVazia, escala)
    
    def gerarBase(self, tela, x, y):
        self.selo.criarImagem(tela, x, y)
    
    def moduloConc(self):
        self.selo.mudarImagem(self.imagemSelo)