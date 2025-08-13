# main(jogo_principal)
import pygame
import sys
import random
import math
from pygame.math import Vector2
from player_atualizado_coletaveis import Jogo

# inicializacao do jogo
pygame.init()

# resolucao da tela do menu
largura_tela = 1280
altura_tela = 720
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Erro 404: Humanidade Não Encontrada")

# clock de fps do jogo, deixei vazio  para definir quando o jogo iniciar
clock_fps = pygame.time.Clock()

# carrega todas as imagens, agora coloquei as telas 
fundo_menu = pygame.image.load("asset/images/tela_inicial/fundo_menu.png").convert_alpha()
fundo_menu = pygame.transform.smoothscale(fundo_menu, (largura_tela, altura_tela))
botao_start_imagem = pygame.image.load("asset/images/tela_inicial/botao_start.png").convert_alpha()
botao_exit_imagem  = pygame.image.load("asset/images/tela_inicial/botao_exit.png").convert_alpha()
imagem_tela_derrota = pygame.transform.smoothscale(pygame.image.load("asset/images/tela_inicial/tela_derrota.png").convert_alpha(), (largura_tela, altura_tela))
imagem_tela_vitoria = pygame.transform.smoothscale(pygame.image.load("asset/images/tela_inicial/tela_vitoria.png").convert_alpha(), (largura_tela, altura_tela))

# sons derrota e vitória
musica_derrota = pygame.mixer.Sound(r"asset\sounds\musica_derrota.mp3")
musica_derrota.set_volume(0.7)
musica_vitoria = pygame.mixer.Sound(r"asset\sounds\musica_vitoria.mp3")
musica_vitoria.set_volume(0.7)

# botão de restart para vitoria/derrota
botao_restart_imagem = pygame.image.load("asset/images/tela_inicial/botao_restart.png").convert_alpha()
x = int(largura_tela * 0.80)
y = int(altura_tela * 0.90)
botao_restart_retangulo = botao_restart_imagem.get_rect(center=(x, y))
mask_botao_restart = pygame.mask.from_surface(botao_restart_imagem)

# Retângulos dos botões
botao_start_retangulo = botao_start_imagem.get_rect(topleft=(900, 20))
botao_exit_retangulo  = botao_exit_imagem.get_rect(topleft=(975, 170))

# gente tive que adicionar isso no codigo, isso eh uma mascara que funciona por pixel, impedindo que houvesse bugs no botoes como deu anteriormente
mask_botao_start = pygame.mask.from_surface(botao_start_imagem)
mask_botao_exit  = pygame.mask.from_surface(botao_exit_imagem)

# boolenas de controle do som
som_derrota = False
som_vitoria = False

# essa eh a funcao do ponto de pixel invisivel para evitar o bug
def ponto_em_pixel_visivel(pos, rect, mask):
    rx, ry = pos[0] - rect.x, pos[1] - rect.y
    if 0 <= rx < mask.get_size()[0] and 0 <= ry < mask.get_size()[1]:
        return mask.get_at((rx, ry))
    return False

# funcao do botao da animacao, depois de seculos consegui arrumar o botao resdtart
def hover_restart():
    pos = pygame.mouse.get_pos()
    return (
        botao_restart_retangulo.collidepoint(pos) and
        ponto_em_pixel_visivel(pos, botao_restart_retangulo, mask_botao_restart)
    )

# funcao para o funcionamento perfeito do botao restart, fora do botao ele nao funciona, o clique so vai em cima dele
def click_pixel_perfeito_restart(pos):
    tempo = pygame.time.get_ticks() / 1000.0
    pulso = 1.0 + 0.03 * math.sin(tempo * 6.0)
    escala = 1.06 * pulso if hover_restart() else 1.0

    if escala == 1.0:
        # o clique so vai no retangulo original e na mascara criada
        return (botao_restart_retangulo.collidepoint(pos) and
                ponto_em_pixel_visivel(pos, botao_restart_retangulo, mask_botao_restart))

    # essa funcao calcula o aumento do botao na animacao e faz com que o clique fique mais preciso
    w, h = botao_restart_imagem.get_size()
    w2, h2 = int(w * escala), int(h * escala)
    img_escalada = pygame.transform.smoothscale(botao_restart_imagem, (w2, h2))
    rect_escalado = img_escalada.get_rect(center=botao_restart_retangulo.center)
    if not rect_escalado.collidepoint(pos):
        return False

    mask_escalada = pygame.mask.from_surface(img_escalada)
    rx, ry = pos[0] - rect_escalado.x, pos[1] - rect_escalado.y
    if 0 <= rx < w2 and 0 <= ry < h2:
        return mask_escalada.get_at((rx, ry))
    return False

# galera essa eh a funcao do menu, basicamente ta feita, mas quero colocar animacao nos botoes
# adaptei: mudei como funciona as acoes e coloquei a animacao do botao
def menu():
    acao = None
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            acao = "quit"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # agora o clique so vai se tiver nos botoes, fora dele nao pega 
            if botao_exit_retangulo.collidepoint(evento.pos) and \
                ponto_em_pixel_visivel(evento.pos, botao_exit_retangulo, mask_botao_exit):
                acao = "quit"
            elif botao_start_retangulo.collidepoint(evento.pos) and \
                ponto_em_pixel_visivel(evento.pos, botao_start_retangulo, mask_botao_start):
                acao = "start"  # sai do menu e vai pro jogo aqui

    tela.blit(fundo_menu, (0, 0))

    # animacao do botao, vi um problema ao passar o exit, ent vou ajeitar ja
    # atualizacao: ajeitei ta funcionando certin
    posicao_mouse = pygame.mouse.get_pos()
    tempo = pygame.time.get_ticks() / 1000.0
    pulso = 1.0 + 0.03 * math.sin(tempo * 6.0)

    # a animacao checa pixels invisiveis
    if botao_start_retangulo.collidepoint(posicao_mouse) and \
        ponto_em_pixel_visivel(posicao_mouse, botao_start_retangulo, mask_botao_start):
        desenhar_botao_pulsante(tela, botao_start_imagem, botao_start_retangulo, escala_base=1.06 * pulso)
    else:
        tela.blit(botao_start_imagem, botao_start_retangulo)

    if botao_exit_retangulo.collidepoint(posicao_mouse) and \
        ponto_em_pixel_visivel(posicao_mouse, botao_exit_retangulo, mask_botao_exit):
        desenhar_botao_pulsante(tela, botao_exit_imagem, botao_exit_retangulo, escala_base=1.06 * pulso)
    else:
        tela.blit(botao_exit_imagem, botao_exit_retangulo)

    pygame.display.flip()
    return acao

# funcao da animacao do botao
def desenhar_botao_pulsante(surface, imagem, retangulo, escala_base=1.06):
    w, h = imagem.get_size()
    imagem_escalada = pygame.transform.smoothscale(imagem, (int(w * escala_base), int(h * escala_base)))
    r = imagem_escalada.get_rect(center=retangulo.center)
    surface.blit(imagem_escalada, r.topleft)

# aqui vem a tela de derrota e tela de vitoria apertando esq para voltar para o menu
def tela_derrota(som_derrota):
    if som_derrota:
        musica_derrota.play()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "quit"
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "menu"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # clique continua pixel-perfect, para garantir que nao haja erros no clique do botao
            if click_pixel_perfeito_restart(evento.pos):
                return "restart"
    tela.blit(imagem_tela_derrota, (0, 0))

    # animação do botão restart — sem mudar posição e sem flicker
    tempo = pygame.time.get_ticks() / 1000.0
    pulso = 1.0 + 0.03 * math.sin(tempo * 6.0)
    if hover_restart():
        desenhar_botao_pulsante(tela, botao_restart_imagem, botao_restart_retangulo, escala_base=1.06 * pulso)
    else:
        tela.blit(botao_restart_imagem, botao_restart_retangulo)

    pygame.display.flip()
    return None

def tela_vitoria(som_vitoria):
    if som_vitoria:
        musica_vitoria.play()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "quit"
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "menu"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:  # clique continua pixel-perfect, mesma coisa que anteriormente            
            if click_pixel_perfeito_restart(evento.pos):
                return "restart"
    tela.blit(imagem_tela_vitoria, (0, 0))

    # animação do botão restart — sem mudar posição e sem flicker
    # antes tinha um problema de flipar o botao, por isso isso aqui.
    tempo = pygame.time.get_ticks() / 1000.0
    pulso = 1.0 + 0.03 * math.sin(tempo * 6.0)
    if hover_restart():
        desenhar_botao_pulsante(tela, botao_restart_imagem, botao_restart_retangulo, escala_base=1.06 * pulso)
    else:
        tela.blit(botao_restart_imagem, botao_restart_retangulo)

    pygame.display.flip()
    return None

# essa parte cuida dos estados do jogo
def main():
    estado = "menu"
    resultado = None 
    executando = True

    som_derrota = False
    som_vitoria = False

    while executando:
        dt = clock_fps.tick(60) / 1000.0

        if estado == "menu":
            acao = menu()
            if acao == "quit":
                estado = "sair"
            elif acao == "start":
                jogo = Jogo()
                jogo.run()
                resultado = jogo.result
                # ajusta a tela para o menu se algum bug acontecer
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "vitoria" if resultado == "vitoria" else "derrota"

                # booleanas para ajuste do som
                if estado == 'derrota': som_derrota = True
                else: som_vitoria = True

        elif estado == "derrota":
            acao = tela_derrota(som_derrota)
            som_derrota = False
            if acao == "quit":
                estado = "sair"
            elif acao == "menu":
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "menu"
            elif acao == "restart": 
                som_derrota = True
                som_vitoria = True
                jogo = Jogo()
                jogo.run()
                resultado = jogo.result
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "vitoria" if resultado == "vitoria" else "derrota"

        elif estado == "vitoria":
            acao = tela_vitoria(som_vitoria)
            som_vitoria = False
            if acao == "quit":
                estado = "sair"
            elif acao == "menu":
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "menu"
            elif acao == "restart": 
                som_vitoria = True # reseta o som de vitória
                som_derrota = True
                jogo = Jogo()
                jogo.run()
                resultado = jogo.result
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "vitoria" if resultado == "vitoria" else "derrota"

        elif estado == "sair":
            executando = False

    pygame.quit()
    sys.exit()

# para dar run no jogo
if __name__ == "__main__":
    main()
