<<<<<<< HEAD
# nao coloquei nenhuma outra biblioteca, porem vamos ter que usar algumas, mas vamos colocar com a demanda
import pygame
import sys

# inicializacao do jogo
pygame.init()

# resolucao da tela
largura_tela = 1280
altura_tela = 720
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Erro 404: Humanidade Não Encontrada")

# clock de fps do jogo, deixei vazio  para definir quando o jogo iniciar
clock_fps = pygame.time.Clock()

# carrega todas as imagens, ainda nao coloquei a tela de derrota e vitoria, porem elas vem pra ca depois
fundo_menu = pygame.image.load(r"asset\images\tela_inicial\1.png").convert()
fundo_menu = pygame.transform.scale(fundo_menu, (largura_tela, altura_tela))
botao_start_imagem = pygame.image.load(r"asset\images\tela_inicial\2.png").convert_alpha()
botao_exit_imagem = pygame.image.load(r"asset\images\tela_inicial\3.png").convert_alpha()

# Retângulos dos botões
botao_start_retangulo = botao_start_imagem.get_rect(topleft=(900, 20))
botao_exit_retangulo = botao_exit_imagem.get_rect(topleft=(975, 170))


# galera essa eh a funcao do menu, basicamente ta feita, mas quero colocar animacao nos botoes
def menu():
    while True:
        clock_fps.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if botao_exit_retangulo.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()
                    elif botao_start_retangulo.collidepoint(evento.pos):
                        return  # sai do menu e vai pro jogo aqui
        tela.blit(fundo_menu, (0, 0))
        tela.blit(botao_start_imagem, botao_start_retangulo)
        tela.blit(botao_exit_imagem, botao_exit_retangulo)
        pygame.display.flip()

# essa eh a funcao principal do jogo, onde vamos
def jogo():
    em_jogo = True

    while em_jogo:
        clock_fps.tick(60) # isso aqui limita os fps do jogo , vcs decidem como fica melhor
        # isso aqui eh quando sai, se sair ele sai do sistema, ou seja fecha o jogo, criarei uma interface para sair dentro do jogo ainda
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # galera aqui voces comecam o codigo, so coloquei isso para nao ficar sem nada na hora de clicar, pode tirar toda essa parte
        tela.fill((0, 100, 200))
        fonte = pygame.font.SysFont(None, 72)
        texto = fonte.render("Jogo Iniciado!", True, (255, 255, 255))
        tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, altura_tela // 2 - texto.get_height() // 2))
        pygame.display.flip()

# aqui eh o funcionamento do jogo
def main():
    while True: #enquanto verdade vai rodar o jogo
        menu()   # basicamente inicia e usar o menu
        jogo()   # isso vai iniciar a funcao jogo que voces ja podem ir comppletando
# isso vai fazer o jogo funcionar basicamente
if __name__ == "__main__":
    main()
# se quiserem fazer por classes tambem da, a gente faria uma classe do jogo completo e colocaria todas as funcoes dentro
=======
# jogo principal.py
import pygame
import random
from pygame.math import Vector2

# ----------------- Config -----------------
WIDTH, HEIGHT = 900, 480
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
        pygame.quit()

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
            # reduce interval gradually (optional)
            # self.spawn_interval = max(0.7, self.spawn_interval - 0.02)

        # atualizar sprites
        self.all_sprites.update(dt)

        # colisão espada -> robô
        # iterar por cada espada e checar colisão manualmente para respeitar hit_enemies set
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

    def draw(self):
        self.screen.fill(BG)
        # chão
        pygame.draw.rect(self.screen, (30,20,20), (0, GROUND_Y, WIDTH, HEIGHT-GROUND_Y))

        # sprites
        # desenhar sombras por baixo (opcional)
        for s in self.all_sprites:
            # sombra simples para personagem e robôs
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

# ----------------- Run -----------------
if __name__ == "__main__":
    game = Game()
    game.run()
    print("Game Over! Pontuação:", game.player.score)
>>>>>>> 0911968613201db8f11e0c5a7f548c56440c22a2
