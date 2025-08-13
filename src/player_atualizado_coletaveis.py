
class Jogo:
    def __init__(self):
        self.result = None  # deixa vazio para poder ganhar ou perder
# criei uma funcao do jogo rodando, para poder retornar no menu e ele nao aparecer antes do menu, coisa que tava acontecendo
    def run(self):
        #Importando
        import pygame
        from sys import exit
        import random
        from random import randint
        from weapon import Weapon

        pygame.init()
        pygame.mixer.init()

        #Definições gerais da tela (vai ser substituído)
        screen = pygame.display.set_mode((1280,720)) #Define a tela e eu tamanho (largura, altura) aumenta a resolucao
        background_image = pygame.image.load(r"asset\images\background\backimage.jpg").convert()  # IMAGEM DE FUNDO PROVISÕRIA
        background_image = pygame.transform.scale(background_image, (1280,720)) # IMAGEM DE FUNDO PROVISÕRIA  aumentei a resolucao
        screen.blit(background_image,(0,0))
        
        # efeito de quando o player leva dano
        efeito_tela_dano = pygame.image.load(r"asset\images\background\tela_dano.png").convert_alpha()
        efeito_tela_dano.set_alpha(50) # muda a opacidade

        pygame.display.set_caption('Mise') #Define o nome do jogo
        clock = pygame.time.Clock() #sozinho não faz nada
        texto_font = pygame.font.Font(None, 50) #(nome, tamanho)
        texto_pixel = pygame.font.Font(r"asset\font\Pixeltype.ttf", 40)
        #contadores de coletáveis zerados
        contador_cafe = 0
        contador_powerup = 0  

        # Carregando músicas e efeitos sonoros
        # EFEITOS SONOROS
        # coletáveis
        som_collect_atkspeed = pygame.mixer.Sound(r"asset\sounds\som_atkspeed.mp3")
        som_collect_atkspeed.set_volume(0.5)
        som_collect_dano = pygame.mixer.Sound(r"asset\sounds\som_buffdano.mp3")
        som_collect_dano.set_volume(0.5)
        som_collect_vida = pygame.mixer.Sound(r"asset\sounds\som_vida.mp3")
        som_collect_vida.set_volume(0.5)
        # dano do player
        som_dano_player = pygame.mixer.Sound(r"asset\sounds\som_dano_jogador.mp3")
        som_dano_player.set_volume(0.5)
        


        # MÚSICA PRINCIPAL
        pygame.mixer.music.load(r"asset\sounds\musica_fundo.mp3") # carregando ela
        pygame.mixer.music.set_volume(0.3) # volume para ela
        pygame.mixer.music.play(-1) # faz ela tocar infinitamente


        game_active = True #Condicional de andamento do jogo
        start_time = 0
        start_time = pygame.time.get_ticks()

        #Função para calcular o tempo atual
        def ver_tempo(start_time):
            tempo_atual = (pygame.time.get_ticks() - start_time)//1000 #Dá o tempo atual em segudos
            minutos = int(tempo_atual // 60) # pega apenas os minutos, já que divide a contagem de segundos pro 60
            segundos = int(tempo_atual % 60) # pega o resto da divisão por 60, que sobra os segundos
            tempo_surface = texto_font.render(f"{minutos:02}:{segundos:02}",False,'White')
            tempo_rect = tempo_surface.get_rect(topleft = (1170,10))
            screen.blit(tempo_surface,tempo_rect)


        class Coletaveis(pygame.sprite.Sprite):
            def __init__(self, tipo=None):
                super().__init__()
                self.active = True

                if tipo is None:
                    tipo = {1: "coração", 2: "café", 3: "espadinha"}[randint(1, 3)]
                self.tipo = tipo

                if self.tipo == "coração":
                    self.image = pygame.image.load(r'asset\images\coletaveis\coração_vermelho.png').convert_alpha()
                    self.image = pygame.transform.scale(self.image, (50,50))
                
                elif self.tipo == "café":
                    self.image = pygame.image.load(r'asset\images\coletaveis\café.png').convert_alpha()     
                    self.image = pygame.transform.scale(self.image, (50,50))   
                
                elif self.tipo == "espadinha":
                    self.image = pygame.image.load(fr'asset\images\coletaveis\powerup_sabre.png').convert_alpha()
                    self.image  = pygame.transform.scale(self.image, (70,70))

                self.rect = self.image.get_rect(midbottom=(640, 600))
                self.tempo_nascimento = pygame.time.get_ticks()
                self.tempo_de_vida = 8000 #8 segundos

            def efeito_coletavel(self,jogador):
                    if self.tipo == "coração":
                        som_collect_vida.play()
                        jogador.curar(1) #cura 1 ponto de vida
                        print(f"CURA REALIZADA. Vida atual: {jogador.vida}") # print genérico pra analisar os atributos e suas modaificações
                    elif self.tipo == "café":
                        som_collect_atkspeed.play()
                        jogador.aumenta_atk_speed(0.1) # aumenta o atk speed do player
                        print(f"ATAQUE VELOZ. Velocidade de ataque atual: {jogador.weapon.atk_speed}") # print genérico pra analisar os atributos e suas modaificações
                    elif self.tipo == "espadinha":
                        som_collect_dano.play()
                        jogador.aumenta_dano(0.1) #aumenta o dano em 10%
                        print(f"DANO AUMENTADO. Dano atual: {jogador.weapon.damage}") # print genérico pra analisar os atributos e suas modaificações
                    
            def update(self): #Faz o coletável desaparecer após um tempo
                    if pygame.time.get_ticks() - self.tempo_nascimento > self.tempo_de_vida:
                        self.kill()
                        
        class Jogador(pygame.sprite.Sprite):
            def __init__(self):
                super().__init__()
                self.image_original = pygame.image.load(
                    r'asset\images\player\player-removebg-preview.png'
                ).convert_alpha()
                self.image_original = pygame.image.load(
                    r'asset\images\player\player-removebg-preview.png'
                ).convert_alpha()

                self.image_original = pygame.transform.scale(self.image_original, (90, 130))
                self.image = self.image_original

                self.image_original = pygame.transform.scale(self.image_original, (90, 130))
                self.image = self.image_original

                self.rect = self.image.get_rect(midbottom=(400, 660))  # aumento para 660 para se ajustar a nova resolucao
                self.vida = 10
                self.velocidade = 5
                self.dano = 1 
                self.gravidade = 0

                self.weapon = Weapon(self, 0.5)
                self.hitbox = pygame.Rect(self.rect.x + 5, self.rect.y, 20, 50)

                self.levando_dano = False # variável pra ativar o efeito de levar dano
                self.tempo_efeito_dano = 0

                self.facing_right = True  # Direção inicial

            def curar (self, qtd=1):
                if self.vida < 10:
                    self.vida += qtd
            
            def aumenta_dano(self, porcentagem=0.1):
                self.weapon.damage += self.weapon.damage * porcentagem
            
            def aumenta_atk_speed(self, porcentagem=0.1):
                self.weapon.atk_speed += self.weapon.atk_speed * porcentagem
                # limite de atk speed
                if self.weapon.atk_speed > 1.25:
                    self.weapon.atk_speed = 1.25


            def update(self):
                # movimentação
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.rect.x -= self.velocidade # movimento em si
                    self.facing_right = False
                    self.weapon.flip_horizontal = True # ativa a condição de inversão da arma
                if keys[pygame.K_RIGHT]:
                    self.rect.x += self.velocidade # movimento em si
                    self.facing_right = True
                    self.weapon.flip_horizontal = False # destiva a condição de inversão da arma

                # flip do personagem
                if self.facing_right:
                    self.image = self.image_original
                else:
                    self.image = pygame.transform.flip(self.image_original, True, False)

                # Efeito de dano do player
                if self.levando_dano == True:
                    self.tempo_efeito_dano += 1
                    screen.blit(efeito_tela_dano, (0,0))

                    if self.tempo_efeito_dano > 20:
                        self.tempo_efeito_dano = 0
                        self.levando_dano = False
        #Definindo a classe inimiga
        class Robo_assassino(pygame.sprite.Sprite):
            def __init__(self,velocidade_robo,direcao, alvo):
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
                    self.robo_x = 1280  # ajustado a nova resolucao
                self.robo_y = 660      
                self.rect = self.image.get_rect(midbottom = ((self.robo_x,self.robo_y)))
                self.lado = 1

                #Características com aplicação no jogo
                self.vida_robo = 3
                self.velocidadebase_robo = velocidade_robo # velocidade originak
                self.velocidade_robo = velocidade_robo # velocidade atual
                self.dano_robo = 1
                self.tempo_cooldown_robo = 300 #milissegundos

                self.ultimo_ataque_robo = 0
                self.primeiro_contato = False

                # Para o funcionamento base com a espada
                self.alvo = alvo
                self.dano_sofrido = False
                self.empurrando = False
                self.knockback = 0 # quantidade de knockback sofrido
                self.knockback_dir = 0 # direção em que é empurrado
                self.flip_definido_no_empurrao = False # para o empurrão


            #Definindo função para caso haja ataque do robô
            def checando_ataque_robo(self,jogador): #Definir anteriormente esse último ataque #Substituir pelas informações do jogador corretas
                agora = pygame.time.get_ticks()
                if ((agora - self.ultimo_ataque_robo) >= self.tempo_cooldown_robo) and self.rect.colliderect(jogador.rect) and not self.primeiro_contato: #Se já deu o intervalo de ataque e colidiram pela primeira vez
                    jogador.levando_dano = True
                    som_dano_player.play()
                    jogador.vida = jogador.vida - self.dano_robo #Dando dano
                    self.ultimo_ataque_robo = agora
                    self.primeiro_contato = True
                
                if self.primeiro_contato and not self.rect.colliderect(jogador.rect):
                    self.primeiro_contato = False

            #Essa função só acontece se houver ataque do jogador
            def levar_dano(self, jogador):
                quantidade = jogador.weapon.damage
                # Desconto de pontos de vida pelo dano
                self.vida_robo -= quantidade # vida do robô perde o dano recebido
                print(f"Dummy levou {quantidade} de dano! Vida restante: {self.vida_robo}") # print geral de dano recebido
                self.dano_sofrido = True # variável pra evitar dano contínuo em um mesmo ataque

                # Checagem se morreu
                if self.vida_robo <= 0:
                    print("Dummy Derrotado")
                    self.kill()
                    cont_robos_mortos.append(0)

            def empurrar(self, forca = 80):
                # mudança da direção do empurrão caso necessário
                self.lado = -1 if self.move_direita else 1
                # Empurrar
                if self.empurrando == False:
                    self.velocidade_robo = 0
                    self.knockback = forca
                    self.empurrando = True

                if self.knockback > 1: # se ainda não tiver na posição nova depois do empurrão, continua sofrendo
                    self.rect.x += self.knockback * 0.03 * self.lado # recebe o empurrão
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
                    if self.move_direita: # se o alvo estiver do lado esquerdo
                        self.image = self.imagedano1  #  imagem do robo Vermelho
                    else:
                        self.image = pygame.transform.flip(self.imagedano1, True, False)

                elif self.tempoanimacao < 30:
                    if self.move_direita: # se o alvo estiver do lado esquerdo
                        self.image = self.imagedano2
                    else:
                        self.image = pygame.transform.flip(self.imagedano2, True, False)  # imagem do robo Branco

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
            robo_inimigo = Robo_assassino(velocidade,direcao,jogador)
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
        #Colocar os coletáveis no grupo de sprites
        grupo_coletaveis = pygame.sprite.Group()
        contador_coletaveis = 0
        opcoes_coletaveis = ["coração", "café", "espadinha"]

        vidas_max = 10
        vidas_atuais = jogador.vida

        # CONTADORES COLETÁVEIS
        #imagem do coração pra barra de vida
        imagem_coração = pygame.image.load(fr'asset\images\coletaveis\coração_vermelho.png').convert_alpha()
        imagem_coração = pygame.transform.scale(imagem_coração, (30, 30))
        #imagem do café pro contador
        imagem_cafe = pygame.image.load(fr'asset\images\coletaveis\café.png').convert_alpha()
        imagem_cafe = pygame.transform.scale(imagem_cafe, (40, 40)) 
        #imagem dos sabres pro contador
        imagem_espadinha = pygame.image.load(fr'asset\images\coletaveis\powerup_sabre.png').convert_alpha()
        imagem_espadinha = pygame.transform.scale(imagem_espadinha, (40, 40))

        # ATRIBUTOS
        # imagem do ícone de atk speed
        imagem_atkspeed = pygame.image.load(r"asset\images\atributos\imagem_atkspeed.png").convert_alpha()
        imagem_atkspeed = pygame.transform.scale(imagem_atkspeed, (40, 40))
        # imagem do ícone de dano atual
        imagem_dano = pygame.image.load(r"asset\images\atributos\imagem_dano.png").convert_alpha()
        imagem_dano = pygame.transform.scale(imagem_dano, (40, 40))

        #Função de dropar coletáveis
        def dropar_coletavel():
            objeto = random.choice(opcoes_coletaveis) # Escolhe um tipo de coletável aleatoriamente
            coletavel = Coletaveis(tipo = objeto) # Cria o coletável com o tipo escolhido
            grupo_coletaveis.add(coletavel)
            todas_as_sprites.add(coletavel) 
        ultimo_drop = 0

        #função para desenhar a barra de vida do jogador
        def desenhar_barra_vidas(tela, vidas_atuais, vidas_max):
            for i in range(vidas_max):
                x = 10 + (i * 27)
                y = 10
                if i < vidas_atuais:
                    tela.blit(imagem_coração, (x, y))

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
                    if event.key == pygame.K_UP and jogador.rect.bottom == 660:  # ajustei a nova resolucao
                        jogador.gravidade = -15

                    # Ataque com a espada
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            espada.attacking = True

                if not game_active: #Reiniciando
                    # tela de derrota
                    self.result = "derrota"
                    return
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

                        #reset coletáveis
                        grupo_coletaveis.empty()
                        contador_coletaveis = 0
                        ultimo_drop = 0

                        # Reseta vida do jogador
                        jogador.vida = 10

                        # contadores de coletavies
                        contador_cafe = 0
                        contador_powerup = 0


            if game_active:
                #screen.fill('Beige')
                screen.blit(background_image, (0,0))  # IMAGEM DE FUNDO PROVISÕRIA
                ver_tempo(start_time)

                # vitoria aos 60 segundos
                if (pygame.time.get_ticks() - start_time) >= 60000:
                    self.result = "vitoria"
                    return

                c_robo = len(cont_robos_mortos)-1
                cont_surface = texto_font.render(f'{c_robo}',False,'Black')
                cont_rect = cont_surface.get_rect(center = (300,50))
                # screen.blit(cont_surface,cont_rect) # retirada da contagem de robôs mortos

                # desenhar a imagem do contador café
                screen.blit(imagem_cafe, (1190, 50))  
                texto_cafe = texto_pixel.render(str(contador_cafe), True, 'Yellow')
                screen.blit(texto_cafe, (1235, 60))  

                # desenhar a imagem do contador de espadinha
                screen.blit(imagem_espadinha, (1190, 90))
                texto_espadinha = texto_pixel.render(str(contador_powerup), True,'Yellow')
                screen.blit(texto_espadinha, (1235, 100))

                # desenhar a imagem do indicador do atributo ataque speed
                screen.blit(imagem_atkspeed, (10, 50))
                texto_atkspeed = texto_pixel.render(f"{jogador.weapon.atk_speed:.2f}", True,'White')
                screen.blit(texto_atkspeed, (55, 60))

                # desenhar a imagem do indicador do atributo dano atual
                screen.blit(imagem_dano, (10, 90))  
                texto_danoatual = texto_pixel.render(f"{jogador.weapon.damage:.2f}", True,'White')
                screen.blit(texto_danoatual, (55, 105))

                #O jogo acontece aqui            
                # Desenhando as sprites básicas da arma e personagem principal
                todas_as_sprites.update()
                todas_as_sprites.draw(screen)

                #Pulo do jogador
                jogador.gravidade += 0.7 #"Valor que torna a queda exponencial"
                jogador.rect.y += jogador.gravidade #A queda
                if jogador.rect.bottom >= 660:      # [COLA] era 320
                    jogador.rect.bottom = 660        # [COLA] era 320
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

                #Funcionamento dos coletáveis
                momento_de_dropar = c_robo % 3
                drop = c_robo // 3
                if momento_de_dropar == 0 and c_robo > 0 and drop > ultimo_drop:
                    for item in grupo_coletaveis.sprites():
                        item.kill()
                    dropar_coletavel()
                    ultimo_drop = drop
                    
                #Definir momento de coleta
                coletados = pygame.sprite.spritecollide(jogador, grupo_coletaveis, dokill=True)
                for item in coletados:
                    item.efeito_coletavel(jogador)

                    # atualização dos contadores
                    if item.tipo == "café":
                        contador_cafe += 1
                    elif item.tipo == "espadinha":
                        contador_powerup += 1

                # derrota na hora
                if jogador.vida <= 0:
                    game_active = False
                    self.result = "derrota"
                    return

            #Desenhar a barra de vida do jogador
            desenhar_barra_vidas(screen, jogador.vida, 10)

            # Funcionamento base
            pygame.display.update()
            clock.tick(60) #O jogo roda a 60fps, altera a velocidade_robo do loop

# o jogo roda em arquivo separado tambem, nao precisa diretamente do main
if __name__ == "__main__":
    Jogo().run()
