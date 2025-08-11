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
fundo_menu = pygame.image.load("fundo_menu.png").convert_alpha()
fundo_menu = pygame.transform.smoothscale(fundo_menu, (largura_tela, altura_tela))
botao_start_imagem = pygame.image.load("botao_start.png").convert_alpha()
botao_exit_imagem  = pygame.image.load("botao_exit.png").convert_alpha()
imagem_tela_derrota = pygame.transform.smoothscale(pygame.image.load("tela_derrota.png").convert_alpha(), (largura_tela, altura_tela))
imagem_tela_vitoria = pygame.transform.smoothscale(pygame.image.load("tela_vitoria.png").convert_alpha(), (largura_tela, altura_tela))

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

# ----------------- Entidades base -----------------
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, size=(40,40), color=(255,255,255)):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect(midbottom=pos)
        self.pos = Vector2(self.rect.topleft)
        self.vel = Vector2(0,0)

    def update(self, dt):
        # mover por velocidade (vel em pixels/seg)
        self.pos += self.vel * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

# ----------------- Player -----------------
class Player(Entity):
    def __init__(self, x, y):
        super().__init__((x,y), size=(48,72), color=PLAYER_COLOR)
        # ajusta o rect para ficar com bottom em y
        self.rect = self.image.get_rect(midbottom=(x,y))
        self.pos = Vector2(self.rect.topleft)
        # física
        self.speed = 250
        self.jump_power = 560
        self.gravity = 1500
        self.on_ground = True
        # saúde e invulnerabilidade
        self.hp = 120
        self.max_hp = 120
        self.invulnerable_timer = 0.0
        self.invulnerable_duration = 0.8
        # ataque
        self.facing_right = True
        self.attack_cooldown = 0.28
        self.attack_timer = 0.0
        # score
        self.score = 0

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel.x = self.speed
            self.facing_right = True

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vel.y = -self.jump_power
            self.on_ground = False

        # atacar com espaço retornando um objeto Sword (ou None)
        if keys[pygame.K_SPACE] and self.attack_timer <= 0:
            self.attack_timer = self.attack_cooldown
            return Sword(self)
        return None

    def take_damage(self, amount):
        if self.invulnerable_timer <= 0:
            self.hp -= amount
            self.invulnerable_timer = self.invulnerable_duration
            # pequeno pushback
            if self.facing_right:
                self.pos.x -= 20
            else:
                self.pos.x += 20
            # clamp
            if self.pos.x < 0:
                self.pos.x = 0
            if self.pos.x + self.rect.width > WIDTH:
                self.pos.x = WIDTH - self.rect.width

    def update(self, dt):
        # gravidade
        if not self.on_ground:
            self.vel.y += self.gravity * dt
        else:
            self.vel.y = 0

        # aplicar movimento
        super().update(dt)

        # check chão
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.pos.y = self.rect.top
            self.on_ground = True
            self.vel.y = 0
        else:
            self.on_ground = False

        # timers
        if self.attack_timer > 0:
            self.attack_timer -= dt
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt

    def draw_hp(self, surface):
        bar_w = 220
        bar_h = 18
        x = 12
        y = 12
        pygame.draw.rect(surface, HP_BG, (x, y, bar_w, bar_h), border_radius=6)
        pct = max(0, self.hp) / self.max_hp
        pygame.draw.rect(surface, HP_FG, (x+4, y+4, int((bar_w-8)*pct), bar_h-8), border_radius=4)

# ----------------- Robô -----------------
class Robot(Entity):
    def __init__(self, spawn_side, player_ref):
        # spawn_side: 'left' or 'right'
        size = (52,72)
        if spawn_side == 'left':
            midbottom = (-10, GROUND_Y)
        else:
            midbottom = (WIDTH+10, GROUND_Y)
        super().__init__(midbottom, size=size, color=ROBOT_COLOR)
        self.player = player_ref
        # stats
        self.speed = random.uniform(70, 120)  # px/s
        self.hp = 60
        self.max_hp = 60
        # avoid rapid repeated hits from sword: not necessary here because Sword tracks hits
        # damage to player cooldown (per robot)
        self.damage = 12
        self.contact_cooldown = 0.8
        self.contact_timer = 0.0

    def update(self, dt):
        # move horizontally toward player
        if self.player.rect.centerx < self.rect.centerx:
            self.vel.x = -self.speed
        else:
            self.vel.x = self.speed

        # update pos
        super().update(dt)

        # keep on ground
        self.rect.bottom = GROUND_Y
        self.pos.y = self.rect.top

        # timers
        if self.contact_timer > 0:
            self.contact_timer -= dt

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0  # retorna True se morreu

    def draw_hp(self, surface):
        # desenha barra acima do robo
        w = self.rect.width
        h = 6
        x = self.rect.x
        y = self.rect.y - 10
        pygame.draw.rect(surface, HP_BG, (x, y, w, h))
        pct = max(0, self.hp) / self.max_hp
        pygame.draw.rect(surface, HP_FG_ROBOT, (x, y, int(w*pct), h))

# ----------------- Sword (ataque) -----------------
class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        # tamanho do hitbox (mais largo na horizontal)
        self.image = pygame.Surface((48, 18), pygame.SRCALPHA)
        self.image.fill(SWORD_COLOR)
        # rect inicial, será posicionado em update
        self.rect = self.image.get_rect()
        self.duration = 0.12  # segundos
        self.hit_enemies = set()
        self.damage = 30

    def update(self, dt):
        self.duration -= dt
        # posiciona a espada dependendo da direção do player
        if self.player.facing_right:
            # encaixa na direita do jogador
            self.rect.midleft = (self.player.rect.midright[0] + 6, self.player.rect.centery)
        else:
            # encaixa na esquerda
            self.rect.midright = (self.player.rect.midleft[0] - 6, self.player.rect.centery)
        # destrói ao expirar
        if self.duration <= 0:
            self.kill()

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

    def spawn_robot(self):
        side = random.choice(['left','right'])
        r = Robot(side, self.player)
        # position slightly offscreen already set in ctor; but ensure initial x
        if side == 'left':
            r.pos.x = -r.rect.width - 8
        else:
            r.pos.x = WIDTH + 8
        r.rect.topleft = (r.pos.x, r.pos.y)
        self.robots.add(r)
        self.all_sprites.add(r)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        # aqui gente, inves de sair do jogo diretamente, fiz voltar ao menu sem fechar o jogo
        # por isso tirei o pygame quit
        return

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        # ataque retorna Sword quando disparado
        new_sword = self.player.handle_input(keys)
        if new_sword:
            self.swords.add(new_sword)
            self.all_sprites.add(new_sword)

        # spawn robots
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_robot()
            self.spawn_timer = 0.0

        # atualizar sprites
        self.all_sprites.update(dt)

        # colisão espada -> robô
        for sword in list(self.swords):
            hits = pygame.sprite.spritecollide(sword, self.robots, False)
            for r in hits:
                if id(r) not in sword.hit_enemies:
                    died = r.take_damage(sword.damage)
                    sword.hit_enemies.add(id(r))
                    if died:
                        r.kill()
                        self.player.score += 150

        # colisão robô -> player (contato)
        for r in list(self.robots):
            if r.rect.colliderect(self.player.rect):
                if r.contact_timer <= 0:
                    self.player.take_damage(r.damage)
                    r.contact_timer = r.contact_cooldown

        # remove robots that wander too far off-screen (safety)
        for r in list(self.robots):
            if r.rect.right < -200 or r.rect.left > WIDTH + 200:
                r.kill()

        # check game over
        if self.player.hp <= 0:
            self.running = False
            # galera aqui eu imprimo a tela de derrota se o player morre (gui)
            self.result = "derrota"

        # aqui foi so para funcionar a tela de vitoria, precisamos saber se ganhamos, eu coloquei 1500 pontos so para testar rapido kk (gui)
        # deixo a criterio de voces as condicoes de vitoria, coloquei isso so para testar, pode tirar se quiser (gui)
        if self.player.score >= self.victory_score and self.running:
            self.running = False
            self.result = "vitoria"

    def draw(self):
        self.screen.fill(BG)
        # chão
        pygame.draw.rect(self.screen, (30,20,20), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))

        # sprites
        for s in self.all_sprites:
            shadow_rect = s.rect.copy()
            shadow_rect.y += 6
            shadow = pygame.Surface((shadow_rect.width, 8), pygame.SRCALPHA)
            shadow.fill((0,0,0,100))
            self.screen.blit(shadow, shadow_rect.topleft)

        self.all_sprites.draw(self.screen)

        # desenhar barras de hp dos robôs acima deles
        for r in self.robots:
            r.draw_hp(self.screen)

        # desenhar vida do player e score
        self.player.draw_hp(self.screen)
        score_surf = self.font.render(f"SCORE: {self.player.score}", True, WHITE)
        self.screen.blit(score_surf, (WIDTH - 160, 14))

        # exibir texto de invulnerável (efeito visual)
        if self.player.invulnerable_timer > 0:
            inv_surf = self.font.render("DANO", True, (255,240,0))
            self.screen.blit(inv_surf, (12, 40))

        pygame.display.flip()

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

# para dar run no jogo
if __name__ == "__main__":

    game = Game()
    game.run()
    print("Game Over! Pontuação:", game.player.score)
    main()

