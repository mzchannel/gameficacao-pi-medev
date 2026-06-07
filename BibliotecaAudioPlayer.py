import pygame # para pygame, usar Python 3.13

def playErro():
    erro = pygame.mixer.Sound("Audios/Erro.wav")
    erroExtra = pygame.mixer.Sound("Audios/ErroExtra.wav")
    erro.play()
    erroExtra.play()

def playAcerto():
    acerto = pygame.mixer.Sound("Audios/Acerto.wav")
    acerto.set_volume(.25)
    acerto.play()

def playSeta():
    setaClick = pygame.mixer.Sound("Audios/ArrowClick.wav")
    setaClick.set_volume(.1)
    setaClick.play()

def playSaida():
    saida = pygame.mixer.Sound("Audios/Saida.wav")
    saidaExtra = pygame.mixer.Sound("Audios/SaidaExtra.wav")
    saida.set_volume(.25)
    saidaExtra.set_volume(.25)
    saida.play()
    saidaExtra.play()