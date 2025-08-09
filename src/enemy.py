#Importando
import pygame
from sys import exit
import random
from random import randint

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

        #A hitbox - equivalente ao alcance da arma do jogador
        self.hitbox = pygame.Rect(self.rect.x+5, self.rect.y, 20, 50) #Hitbox um pouco menor que o jogador

    #Movimentação Kaynan
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

jogador = Jogador()

#Definindo a classe inimiga
class Robo_assassino(pygame.sprite.Sprite):
    def __init__(self,velocidade_robo,direcao):
        super().__init__()
        self.image = pygame.Surface((40,80)) #(largura, altura) #Substituir aqui pela imagem
        self.image.fill('Red')
        #O robô será um retângulo vermelho
        self.direcao = direcao #Esquerda ou direita #Ver também o lado da imagem
        if direcao == 'esquerda':
            self.robo_x = 0
        elif direcao == 'direita':
            self.robo_x = 800
        self.robo_y = 320
        self.rect = self.image.get_rect(midbottom = ((self.robo_x,self.robo_y)))

        #Características com aplicação no jogo
        self.vida_robo = 3
        self.velocidade_robo = velocidade_robo
        self.dano_robo = 1
        self.tempo_cooldown_robo = 300 #milissegundos

        self.ultimo_ataque_robo = 0
        self.primeiro_contato = False

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
    def checando_ataque_jogador(self,jogador,cont_robos_mortos,grupo_robos_assassinos):
        if self.rect.colliderect(jogador.hitbox): #È quando colide e o jogador usa a arma
            self.vida_robo = self.vida_robo - jogador.dano
            if self.vida_robo <= 0: 
                self.vida_robo = 0 #Será Excluído depois
                grupo_robos_assassinos.remove(self)
                cont_robos_mortos.append(1) #Contador para aparecer os coletáveis
                #Remover do grupo de robôs no código rodando - excluir todos com vida == 0
                #Implementar código de KAYNAN + BRÍGIDA
    
    #Movimentação de acordo com o jogador
    def movimento_robo(self,jogador):
        if self.rect.x > jogador.rect.x: self.rect.x -= self.velocidade_robo
        elif self.rect.x < jogador.rect.x: self.rect.x += self.velocidade_robo
        
        self.robo_x = self.rect.x

#Função de spawn do robô
def spawn_robo(grupo_robos_assassinos):
    num = random.randint(1,999)
    if num%2 == 0: direcao = 'esquerda'
    else: direcao = 'direita'
    velocidade = 4
    robo_inimigo = Robo_assassino(velocidade,direcao)
    grupo_robos_assassinos.add(robo_inimigo)

#Grupo de Sprites (apenas para organizar melhor cada um dos elementos do grupo)
grupo_robos_assassinos = pygame.sprite.Group()
cont_robos_mortos = [0]

 #Timer
timer_spawn_robo = pygame.USEREVENT + 1
pygame.time.set_timer(timer_spawn_robo, 1500) #(Evento , repetição) #Um robô surge a cada 1,5s -> tempo alterável depois

while True: #Faz o jogo rodar em loop
    pygame.display.update()
    clock.tick(60) #O jogo roda a 60fps, altera a velocidade_robo do loop

    #Eventos importantes:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #Busca se, de todos os eventos que acontece, é de saída
            pygame.quit()
            exit() #Termina o código
        if game_active and event.type == timer_spawn_robo:
            spawn_robo(grupo_robos_assassinos) #Adiciona robôs
            
        if event.type == pygame.KEYDOWN and game_active: #Movimentação
            if event.key == pygame.K_UP and jogador.rect.bottom == 320:  #condicional para o jogador pular
                jogador.gravidade = -15

        if not game_active: #Reiniciando
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #Condicional de restart
                start_time = pygame.time.get_ticks()
                game_active = True
                jogador.gravidade = 0 #O pulo
                grupo_robos_assassinos = pygame.sprite.Group() #Redefine os inimigos
                cont_robos_mortos = [0]
                jogador.vida = 100  # resetar vida do jogador

    if game_active:
        screen.fill('Beige')
        ver_tempo(start_time)
        c_robo = len(cont_robos_mortos)-1
        cont_surface = texto_font.render(f'{c_robo}',False,'Black')
        cont_rect = cont_surface.get_rect(center = (300,50))
        screen.blit(cont_surface,cont_rect)

        #O jogo acontece aqui            
        screen.blit(jogador.image, jogador.rect) #Jogador

        #Pulo do jogador
        jogador.gravidade += 0.7 #"Valor que torna a queda exponencial"
        jogador.rect.y += jogador.gravidade #A queda
        if jogador.rect.bottom >= 320: 
            jogador.rect.bottom = 320
            jogador.gravidade = 0
        jogador.update()

        #Funcionamento dos robôs
        for robo in grupo_robos_assassinos.sprites():
            robo.movimento_robo(jogador)
            robo.checando_ataque_robo(jogador)
            robo.checando_ataque_jogador(jogador, cont_robos_mortos, grupo_robos_assassinos)
            screen.blit(robo.image, robo.rect)

        if jogador.vida <= 0:
            game_active = False

    else: #Tela de restart
        rest_surface = texto_font.render('PRESS SPACE TO CONTINUE', False, 'Black') #(terobo_xto, AA, cor)
        rest_rect = rest_surface.get_rect(center = (400,200))

        screen.fill('Beige')
        screen.blit(rest_surface,rest_rect)
