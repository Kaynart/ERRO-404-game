import pygame
# from sys import exit

# pygame.init()

# largura = 640
# altura = 480

# PRETO = (0, 0, 0)

# tela = pygame.display.set_mode((largura, altura))
# pygame.display.set_caption("Sprites")


class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner, atk_speed=1, damage=1):
        super().__init__()
        self.owner = owner
        self.damage = damage
        self.atk_speed = atk_speed
        self.attacking = False  # pra testar, deixei True
        self.sprites = []

        for i in range(0, 9):
            self.sprites.append(pygame.image.load(fr"asset\images\weapon\sabre{i}.png").convert_alpha())

        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.rotate(self.image, 20)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.midtop = (self.owner.rect.right + 24, self.owner.rect.centery - self.image.get_height() // 2)

        self.flip_horizontal = False

    def update(self):
        # ANIMAÇÃO ENQUANTO ATACA
        if self.attacking:
            self.atual += self.atk_speed
            if self.atual >= len(self.sprites):
                self.atual = 0
                self.attacking = False
                
                for alvo in self.owner.target_group:
                    alvo.dano_sofrido = False # reseta a variável de dano sofrido de cada robô alcançado, pra que possam sofrer novo ataque

            img = self.sprites[int(self.atual)]
        else:
            img = self.sprites[0]  # sprite "neutra"

        # INVERSÃO DA IMAGEM E DA POSIÇÃO DA ARMA DE ACORDO COM A POSIÇÃO DO PLAYER
        if self.flip_horizontal: # se tiver virado o player
            img = pygame.transform.flip(img, True, False) # vira a imagem da espada
    
        # transformação básica da imagem da arma
        img = pygame.transform.scale(img, (70, 70)) # escala
        if self.flip_horizontal:
            img = pygame.transform.rotate(img, -20) # rotaciona ao contrário
        else:
            img = pygame.transform.rotate(img, 20) # rotaciona normal

        self.image = img # pega a imagem oficialmente

        if self.flip_horizontal:
            self.rect.midtop = (self.owner.rect.left - 30, self.owner.rect.centery - self.image.get_height() // 2)
        else:
            self.rect.midtop = (self.owner.rect.right + 24, self.owner.rect.centery - self.image.get_height() // 2)

        # APLICAÇÃO DOS EFEITOS DA ESPADADA
        if self.attacking:
            for alvo in self.owner.target_group:
                if self.rect.colliderect(alvo.rect) and not alvo.dano_sofrido: # se houver colisão e o robõ ainda não tiver sofrido nenhum dano desse ataque
                    alvo.image = alvo.imagedano1
                    alvo.levar_dano(self.damage)
                    alvo.empurrar() # ativa o empurrão
                    alvo.iniciar_animacao_dano() # ativa a animação de tomar dano
                if alvo.empurrando:
                    alvo.empurrar()

# class Dummy(pygame.sprite.Sprite):
#     def __init__(self, pos=(100, 200)):
#         super().__init__()
#         self.image = pygame.Surface((40, 80))
#         self.image.fill((255, 255, 255))
#         self.rect = self.image.get_rect(topleft=pos)
#         self.hp = 100 # vida total do boneco
        # self.dano_sofrido = False
        # self.empurrando = False
        # self.knockback = 0 # quantidade de knockback sofrido
        # self.knockback_dir = 0 # direção em que é empurrado

#     def levar_dano(self, quantidade):
#         # Desconto de pontos de vida pelo dano
#         self.hp -= quantidade
#         print(f"Dummy levou {quantidade} de dano! Vida restante: {self.hp}")
#         self.dano_sofrido = True

#         # Checagem se morreu
#         if self.hp <= 0:
#             print("Dummy Derrotado")
#             self.kill()
    

#     def empurrar(self, direcao = 1, forca = 30):
#         # Empurrar
#         if self.empurrando == False:
#             self.knockback = forca
#             self.empurrando = True
#         if self.knockback > 0: # se ainda não tiver na posição nova depois do empurrão, continua sofrendo
#             self.rect.x += self.knockback * 0.3 # recebe o empurrão
#             self.knockback = int(self.knockback - (self.knockback * 0.3)) # diminui o próximo knockback
#         elif self.knockback < 1: # se já foi empurrado bastante
#             self.knockback = 0
#             self.empurrando = False # retorna a variável
#             self.image.fill((255,255,255))
        

# # APENAS PARA TESTE COM PERSONAGENS (ROBÔ E PLAYER PRINCIPAL)
# class Player(Dummy):
#     def __init__(self, pos=(100, 200)):
#         super().__init__(pos)
#         self.velocidade = 5
#         self.image.fill((0, 255, 0))  # cor diferente pra identificar o player

#     def update(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_LEFT]:
#             self.rect.x -= self.velocidade
#         if keys[pygame.K_RIGHT]:
#             self.rect.x += self.velocidade
#         if keys[pygame.K_UP]:
#             self.rect.y -= self.velocidade
#         if keys[pygame.K_DOWN]:
#             self.rect.y += self.velocidade


# player = Player() # player principal
# espada = Weapon(player)
# inimigo = Dummy() # inimigo
# inimigo.rect.topleft = (300, 250) # mudando a posição do inimigo

# # grupo de inimigos (targets possíveis pros ataques)
# inimigos = pygame.sprite.Group()
# inimigos.add(inimigo)

# # define como o grupo de target do dono da arma
# espada.owner.target_group = inimigos # declara os inimigos como targets

# # sprites a serem processadas e updateadas
# todas_as_sprites = pygame.sprite.Group()
# todas_as_sprites.add(player)
# todas_as_sprites.add(espada)
# todas_as_sprites.add(inimigo)

# clock = pygame.time.Clock()

# # looping do jogo principal
# while True:
#     tela.fill(PRETO)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
        
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 espada.attacking = True

#     todas_as_sprites.update()
#     todas_as_sprites.draw(tela)

#     pygame.display.flip()
#     clock.tick(10)  # reduz a velocidade da animação
