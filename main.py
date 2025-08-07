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