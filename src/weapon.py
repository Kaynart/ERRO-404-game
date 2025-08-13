import pygame

pygame.mixer.init()

som_dano_robo = pygame.mixer.Sound(r"asset\sounds\som_dano_robo.mp3")
som_dano_robo.set_volume(0.05)
som_espada = pygame.mixer.Sound(r"asset\sounds\som_espada.mp3")
som_espada.set_volume(0.2)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner, atk_speed=1, damage=1):
        super().__init__()
        self.owner = owner
        self.damage = damage
        self.atk_speed = atk_speed
        self.attacking = False  # pra testar, deixei True
        self.sprites = []
        self.som_arma = False # ajustar o som

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
            img = pygame.transform.rotate(img, -10) # rotaciona ao contrário
        else:
            img = pygame.transform.rotate(img, 10) # rotaciona normal

        self.image = img # pega a imagem oficialmente

        if self.flip_horizontal:
            self.rect.midtop = (self.owner.rect.left - 15, self.owner.rect.centery - self.image.get_height() // 2 - 10)
        else:
            self.rect.midtop = (self.owner.rect.right + 5, self.owner.rect.centery - self.image.get_height() // 2 - 10)

        # APLICAÇÃO DOS EFEITOS DA ESPADADA
        if self.attacking:
            if not self.som_arma: # booleana para ajustar som
                som_espada.play()
                self.som_arma = True
            for alvo in self.owner.target_group:
                if self.rect.colliderect(alvo.rect) and not alvo.dano_sofrido: # se houver colisão e o robõ ainda não tiver sofrido nenhum dano desse ataque
                    som_dano_robo.play()
                    alvo.image = alvo.imagedano1
                    alvo.levar_dano(self.owner)
                    alvo.empurrar() # ativa o empurrão
                    alvo.iniciar_animacao_dano() # ativa a animação de tomar dano
                if alvo.empurrando:
                    alvo.empurrar()
        else: self.som_arma = False
