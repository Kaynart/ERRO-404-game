#Importando
import pygame
from sys import exit
import random
from random import randint
from weapon import Weapon

pygame.init()

#Definições gerais da tela (vai ser substituído)
screen = pygame.display.set_mode((800,400)) #Define a tela e eu tamanho (largura, altura)
screen.fill('Beige')
pygame.display.set_caption('Mise') #Define o nome do jogo
clock = pygame.time.Clock() #sozinho não faz nada
texto_font = pygame.font.Font(None, 50) #(nome, tamanho)

game_active = True #Condicional de andamento do jogo
start_time = 0

#Função para calcular o tempo atual
def ver_tempo(start_time):
    tempo_atual = (pygame.time.get_ticks() - start_time)//1000 #Dá o tempo atual em segudos
    tempo_surface = texto_font.render(f'{tempo_atual}',False,'Black')
    tempo_rect = tempo_surface.get_rect(center = (400,50))
    screen.blit(tempo_surface,tempo_rect)


class Jogador(pygame.sprite.Sprite): #Apenas para testar a interação
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(400, 320))
        self.vida = 5
        self.velocidade = 5
        self.dano = 1 
        self.gravidade = 0

        self.weapon = Weapon(self)

        #A hitbox - equivalente ao alcance da arma do jogador
        self.hitbox = pygame.Rect(self.rect.x+5, self.rect.y, 20, 50) #Hitbox um pouco menor que o jogador

    #Movimentação Kaynan
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade # movimento em si
            self.weapon.flip_horizontal = True # ativa a condição de inversão da arma
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade # movimento em si
            self.weapon.flip_horizontal = False # destiva a condição de inversão da arma
    
    
    #Quando é coletado um coração vermelho, aumenta um coração
    def coracao_vermelho(self):
        if self.vida < 5:
            self.vida += 1
    
    #Quando um coração azul é coletado, chega a vida máxima
    def coracao_azul(self):
        self.vida = 5
    
    #Quando um café é coletado, dano almenta
    def cafe(self):
        self.dano += (self.dano)*0.1



#Definindo a classe inimiga
class Robo_assassino(pygame.sprite.Sprite):
    def __init__(self,velocidade_robo,direcao):
        super().__init__()
        # Declaração de imagnes base do robô
        self.imagebase = pygame.image.load(fr'asset\images\enemy\Robo1.png').convert_alpha()
        self.imagebase = pygame.transform.scale(self.imagebase, (130,130))
        self.imagedano1 = pygame.image.load(fr'asset\images\enemy\Robo2.png').convert_alpha()
        self.imagedano1 = pygame.transform.scale(self.imagedano1, (130,130))
        self.imagedano2 = pygame.image.load(fr'asset\images\enemy\Robo3.png').convert_alpha()
        self.imagedano2 = pygame.transform.scale(self.imagedano2, (130,130))

        self.image =  self.imagebase
        self.imageD = self.image
        self.imageE = pygame.transform.flip(self.image, True, False)
        self.move_direita = False

        self.animando_dano = False # animacao do dano
        self.tempoanimacao = 0 # tempo de ocorrencia da animação

        # Movimentação base
        self.direcao = direcao #Esquerda ou direita #Ver também o lado da imagem
        if direcao == 'esquerda':
            self.robo_x = 0
        elif direcao == 'direita':
            self.robo_x = 800
        self.robo_y = 340
        self.rect = self.image.get_rect(midbottom = ((self.robo_x,self.robo_y)))

        #Características com aplicação no jogo
        self.vida_robo = 3
        self.velocidadebase_robo = velocidade_robo # velocidade originak
        self.velocidade_robo = velocidade_robo # velocidade atual
        self.dano_robo = 1
        self.tempo_cooldown_robo = 300 #milissegundos

        self.ultimo_ataque_robo = 0
        self.primeiro_contato = False

        # Para o funcionamento base com a espada
        self.dano_sofrido = False
        self.empurrando = False
        self.knockback = 0 # quantidade de knockback sofrido
        self.knockback_dir = 0 # direção em que é empurrado


    #Definindo função para caso haja ataque do robô
    def checando_ataque_robo(self,jogador): #Definir anteriormente esse último ataque #Substituir pelas informações do jogador corretas
        agora = pygame.time.get_ticks()
        if ((agora - self.ultimo_ataque_robo) >= self.tempo_cooldown_robo) and self.rect.colliderect(jogador.rect) and not self.primeiro_contato: #Se já deu o intervalo de ataque e colidiram pela primeira vez
            jogador.vida = jogador.vida - self.dano_robo #Dando dano
            self.ultimo_ataque_robo = agora
            self.primeiro_contato = True
        
        if self.primeiro_contato and not self.rect.colliderect(jogador.rect):
            self.primeiro_contato = False

    #Essa função só acontece se houver ataque do jogador
    def levar_dano(self, quantidade):
        # Desconto de pontos de vida pelo dano
        self.vida_robo -= quantidade # vida do robô perde o dano recebido
        print(f"Dummy levou {quantidade} de dano! Vida restante: {self.vida_robo}") # print geral de dano recebido
        self.dano_sofrido = True # variável pra evitar dano contínuo em um mesmo ataque

        # Checagem se morreu
        if self.vida_robo <= 0:
            print("Dummy Derrotado")
            self.kill()
    

    def empurrar(self, direcao = 1, forca = 80):
        # Empurrar
        if self.empurrando == False:
            self.velocidade_robo = 0
            self.knockback = forca
            self.empurrando = True

        if self.knockback > 1: # se ainda não tiver na posição nova depois do empurrão, continua sofrendo
            self.rect.x += self.knockback * 0.03 # recebe o empurrão
            self.knockback = int(self.knockback - (self.knockback * 0.03)) # diminui o próximo knockback
            
        else: # se já foi empurrado bastante
            self.knockback = 0
            self.velocidade_robo = self.velocidadebase_robo
            self.empurrando = False # retorna a variável

    def iniciar_animacao_dano(self):
        self.animando_dano = True
        self.tempoanimacao = 0

    def atualizar_animacao_dano(self): # sempre vai rodar
        if not self.animando_dano: # se não for caso de animação de dano, retorna nada e foge da execução
            return

        self.tempoanimacao += 1  # Incrementa a cada frame

        # TEMPO DA ANIMAÇÃO DE DANO
        if self.tempoanimacao < 20:
            self.image = self.imagedano1  #  imagem do robo Vermelho
        elif self.tempoanimacao < 30:
            self.image = self.imagedano2  # imagem do robo Branco
        else:
            self.image = self.imagebase  # Volta ao normal
            self.animando_dano = False
            self.tempoanimacao = 0

    #Movimentação de acordo com o jogador
    def movimento_robo(self,jogador):
        if self.rect.x > jogador.rect.x: 
            self.rect.x -= self.velocidade_robo
            self.move_direita = False

        elif self.rect.x <= jogador.rect.x: 
            self.rect.x += self.velocidade_robo
            self.image = pygame.transform.flip(self.image, True, False)
            self.move_direita = True

        self.robo_x = self.rect.x
    
    # Update base 
    def update(self, jogador=None):
        # Se passar o jogador, atualiza movimento; senão, só animação
        if jogador:
            if self.empurrando:
                self.empurrar()
            else:
                self.movimento_robo(jogador)

            self.checando_ataque_robo(jogador)

        # Atualiza a animação de dano sempre
        self.atualizar_animacao_dano()

#Função de spawn do robô
def spawn_robo(grupo_robos_assassinos, todas_as_sprites):
    num = random.randint(1,999)
    if num%2 == 0: direcao = 'esquerda'
    else: direcao = 'direita'
    velocidade = 2
    robo_inimigo = Robo_assassino(velocidade,direcao)
    grupo_robos_assassinos.add(robo_inimigo)
    todas_as_sprites.add(robo_inimigo)

grupo_robos_assassinos = pygame.sprite.Group()
cont_robos_mortos = [0]

# Jogador
jogador = Jogador()
# Espada
espada = jogador.weapon

#Grupo de Sprites (apenas para organizar melhor cada um dos elementos do grupo)
todas_as_sprites = pygame.sprite.Group()
todas_as_sprites.add(jogador)
todas_as_sprites.add(espada)

# Declarando os possíveis inimigos pros ataques da espada
espada.owner.target_group = grupo_robos_assassinos

#Timer
timer_spawn_robo = pygame.USEREVENT + 1
pygame.time.set_timer(timer_spawn_robo, 1500) #(Evento , repetição) #Um robô surge a cada 1,5s -> tempo alterável depois

while True: #Faz o jogo rodar em loop

    #Eventos importantes:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #Busca se, de todos os eventos que acontece, é de saída
            pygame.quit()
            exit() #Termina o código
        if game_active and event.type == timer_spawn_robo:
            spawn_robo(grupo_robos_assassinos, todas_as_sprites) #Adiciona robôs
            espada.owner.target_group = grupo_robos_assassinos # atualiza os targets da espada com os novos robôs
            
        if event.type == pygame.KEYDOWN and game_active: # Ativação de teclas
            # Movimentação
            if event.key == pygame.K_UP and jogador.rect.bottom == 320:  #condicional para o jogador pular
                jogador.gravidade = -15

            # Ataque com a espada
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    espada.attacking = True

        if not game_active: #Reiniciando
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #Condicional de restart
                start_time = pygame.time.get_ticks()
                game_active = True
                jogador.gravidade = 0 #O pulo

                # Cria novo grupo de robôs
                grupo_robos_assassinos = pygame.sprite.Group()
                cont_robos_mortos = [0]

                # Limpa e recria o grupo geral de sprites
                todas_as_sprites.empty()
                todas_as_sprites.add(jogador)
                todas_as_sprites.add(espada)

                # Atualiza a referência do grupo de alvos da espada
                espada.owner.target_group = grupo_robos_assassinos

                # Reseta vida do jogador
                jogador.vida = 100

    if game_active:
        screen.fill('Beige')
        ver_tempo(start_time)
        c_robo = len(cont_robos_mortos)-1
        cont_surface = texto_font.render(f'{c_robo}',False,'Black')
        cont_rect = cont_surface.get_rect(center = (300,50))
        screen.blit(cont_surface,cont_rect)

        #O jogo acontece aqui            
        # Desenhando as sprites básicas da arma e personagem principal
        todas_as_sprites.update()
        todas_as_sprites.draw(screen)

        #Pulo do jogador
        jogador.gravidade += 0.7 #"Valor que torna a queda exponencial"
        jogador.rect.y += jogador.gravidade #A queda
        if jogador.rect.bottom >= 320: 
            jogador.rect.bottom = 320
            jogador.gravidade = 0
        jogador.update()

        #Funcionamento dos robôs
        for robo in grupo_robos_assassinos.sprites():
            robo.update(jogador)
            if robo.move_direita:
                robo.image = robo.imageD
            else:
                robo.image = robo.imageE
            
            robo.checando_ataque_robo(jogador)
            # robo.checando_ataque_jogador(jogador, cont_robos_mortos, grupo_robos_assassinos)
            if robo.move_direita: robo.image = robo.imageD
            else: robo.image = robo.imageE

        if jogador.vida <= 0:
            game_active = False

    else: #Tela de restart
        rest_surface = texto_font.render('PRESS SPACE TO CONTINUE', False, 'Black') #(terobo_xto, AA, cor)
        rest_rect = rest_surface.get_rect(center = (400,200))

        screen.fill('Beige')
        screen.blit(rest_surface,rest_rect)

    # Funcionamento base
    pygame.display.flip()
    clock.tick(60) #O jogo roda a 60fps, altera a velocidade_robo do loop
