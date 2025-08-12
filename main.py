# A SEREM FEITAS ALTERAÇÕES PARA FUNCIONAMENTO

# jogo principal.py
import pygame
import sys
import random
import math
from pygame.math import Vector2

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
fundo_menu = pygame.image.load(r"asset\images\tela_inicial\fundo_menu.png").convert_alpha()
fundo_menu = pygame.transform.smoothscale(fundo_menu, (largura_tela, altura_tela))
botao_start_imagem = pygame.image.load(r"asset\images\tela_inicial\botao_start.png").convert_alpha()
botao_exit_imagem  = pygame.image.load(r"asset\images\tela_inicial\botao_exit.png").convert_alpha()
imagem_tela_derrota = pygame.transform.smoothscale(pygame.image.load(r"asset\images\tela_inicial\tela_derrota.png").convert_alpha(), (largura_tela, altura_tela))
imagem_tela_vitoria = pygame.transform.smoothscale(pygame.image.load(r"asset\images\tela_inicial\tela_vitoria.png").convert_alpha(), (largura_tela, altura_tela))

# Retângulos dos botões
botao_start_retangulo = botao_start_imagem.get_rect(topleft=(900, 20))
botao_exit_retangulo  = botao_exit_imagem.get_rect(topleft=(975, 170))

# gente tive que adicionar isso no codigo, isso eh uma mascara que funciona por pixel, impedindo que houvesse bugs no botoes como deu anteriormente
mask_botao_start = pygame.mask.from_surface(botao_start_imagem)
mask_botao_exit  = pygame.mask.from_surface(botao_exit_imagem)

# essa eh a funcao do ponto de pixel invisivel para evitar o bug
def ponto_em_pixel_visivel(pos, rect, mask):
    rx, ry = pos[0] - rect.x, pos[1] - rect.y
    if 0 <= rx < mask.get_size()[0] and 0 <= ry < mask.get_size()[1]:
        return mask.get_at((rx, ry))
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
def tela_derrota():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "quit"
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "menu"
    tela.blit(imagem_tela_derrota, (0, 0))
    pygame.display.flip()
    return None

def tela_vitoria():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return "quit"
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return "menu"
    tela.blit(imagem_tela_vitoria, (0, 0))
    pygame.display.flip()
    return None

# jogo a partir daqui
WIDTH, HEIGHT = 1280, 720
FPS = 60
GROUND_Y = HEIGHT - 80

# cores
WHITE = (255,255,255)
BG = (60, 40, 40)
PLAYER_COLOR = (40, 140, 200)
ROBOT_COLOR = (180, 50, 50)
HP_BG = (30,30,30)
HP_FG = (200,30,30)
HP_FG_ROBOT = (30,200,30)
SWORD_COLOR = (80,200,255)

# ----------------- Jogo -----------------
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Batalha: Espada vs Robôs")
        self.clock = pygame.time.Clock()
        # grupos
        self.all_sprites = pygame.sprite.Group()
        self.robots = pygame.sprite.Group()
        self.swords = pygame.sprite.Group()

        # player
        self.player = Player(WIDTH//2, GROUND_Y)
        self.all_sprites.add(self.player)

        # spawn
        self.spawn_timer = 0.0
        self.spawn_interval = 1.4
        self.running = True

        # fonte
        self.font = pygame.font.SysFont(None, 28)

        # mudem aqui a condicao de vitoria
        self.victory_score = 1500
        self.result = None  # vai ser tirado provavelmente

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        # aqui gente, inves de sair do jogo diretamente, fiz voltar ao menu sem fechar o jogo
        # por isso tirei o pygame quit
        return

# essa parte controla quando o jogo vai pra tela ou o jogo mesmo, basicamente a cola entro o meu codigo e de kaynan
def main():
    estado = "menu"
    resultado = None 
    executando = True

    while executando:
        dt = clock_fps.tick(60) / 1000.0

        if estado == "menu":
            acao = menu()
            if acao == "quit":
                estado = "sair"
            elif acao == "start":
                jogo = Game()
                jogo.run()
                resultado = jogo.result
                # ajusta a tela para o menu se algum bug acontecer
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "vitoria" if resultado == "vitoria" else "derrota"

        elif estado == "derrota":
            acao = tela_derrota()
            if acao == "quit":
                estado = "sair"
            elif acao == "menu":
                # garante que o menu esteja no tamanho certo
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "menu"

        elif estado == "vitoria":
            acao = tela_vitoria()
            if acao == "quit":
                estado = "sair"
            elif acao == "menu":
                pygame.display.set_mode((largura_tela, altura_tela))
                estado = "menu"

        elif estado == "sair":
            executando = False

    pygame.quit()
    sys.exit()
