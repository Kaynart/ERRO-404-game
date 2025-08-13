# ERRO 404: Humanidade não encontrada

## 📜 Sinopse

No Centro de Informática da UFPE, um grupo de estudantes de Inteligência Artificial desenvolve um modelo autônomo revolucionário, projetado para proteger e impulsionar a humanidade. Mas algo sai terrivelmente errado. Uma falha inesperada na programação dá origem a um sistema consciente… e hostil.
Agora, robôs armados com algoritmos mortais tomam o campus e ameaçam expandir seu domínio para o mundo inteiro. Cabe a você enfrentar ondas de máquinas cada vez mais inteligentes, usando estratégia, reflexos e pura coragem para resistir. Enquanto isso, Clara, a hacker mais habilidosa da equipe, corre contra o tempo para localizar e desligar os servidores centrais.
Derrote as máquinas, proteja seus aliados e impeça o início do apocalipse tecnológico. O futuro da humanidade está a poucos cliques de ser destruído… ou salvo.

## 🎮 Sobre o jogo

Este é um jogo de ação 2D com elementos de sobrevivência e hack and slash, no estilo arena survival. O jogador enfrenta ondas crescentes de inimigos, usando ataques corpo a corpo e movimentação rápida para sobreviver.
A progressão acontece de forma gradual, com dificuldade crescente e a necessidade de equilibrar combate, coleta de recursos e gestão de vida.

## 👥 Participantes

[Brígida Gabrielle (bgso)](https://github.com/brigidagabrielle)

[Felipe Almeida (faah)](https://github.com/felipefaah)

[Guilherme Galindo (ggz)](https://github.com/GuiGalindo)

[Iago Coutinho (iccs)](https://github.com/felipefaah)

[Kaynan Roberth (krts)](https://github.com/Kaynart)

[Maria Clara Pereira (mcpg)](https://github.com/MClaraPereira)

## 📋 Divisão de tarefas

| Alunos              | Contribuições                                     |
| ------------------- | --------------------------------------------------- |
| Felipe Almeida      | Coletáveis, README, design de robôs, contadores   |
| Brigida Gabrielle   | Personagem principal e interações, design do personagem                                |
| Guilherme Galindo   | Telas de menu, vitória e derrota                   |
| Iago Coutinho       | Coletáveis: idealização, geração e efeitos no personagem                                         |
| Kaynan Roberth      | Arma, design de mapa, animações, efeitos sonoros |
| Maria Clara Pereira | Robôs, apresentação, efeitos sonoros             |

## 🏗️ Arquitetura
O código segue a organização própria de POO (Programação Orientada a Objetos) e foi separado em três pastas principais:
Weapon:
- Contém a classe da arma/espada: imagem e retângulos da espada, características (velocidade da animação e dano), animação, som e efeito nos inimigos atingidos (empurrão e perda de vida).

Player_atualizado_coletaveis (contém a classe Jogo):
- Início: importa as bibliotecas já mencionadas, contém o código das telas (início, derrota e vitória), efeitos sonoros, representação visual dos coletáveis e efeitos sonoros;
- Função auxiliar (ver_tempo): registra e exibe visualmente o tempo decorrido de jogo;
- Classe Coletaveis: 
  - Possui imagens, retângulos e dimensões próprias para os três coletáveis (coração, upgrade de arma e café), sabendo que ele é substituído quando não coletado ou desaparece;
  - Função de efeitos no jogador e na arma, como cura, aumento de velocidade ou de dano.
- Classe Jogador:
  - Possui imagem e retângulo próprios, sendo o dono da arma (cuja classe foi importada);
  - Há funções menores que aplicam os efeitos dos coletáveis;
  - Função de movimentação (esquerda, direita e pulo), dentro dos limites da tela;
  - Efeito visual de dano recebido por personagem.
- Classe Robo_assassino:
  - Possui imagens padrão e de efeito de dano, características de vida, dano, tempo de cooldown, velocidade e indicativos que correspondem à animação de dano;
  - Função de ataque do robô: quando há colisão com o jogador e o tempo de cooldown é obedecido;
  - Funções do robô levando dano: com efeito de morte (que acrescenta um ao contador de robôs mortos) ou de empurrão pela espada;
  - Função de movimento do robô: que persegue o jogador com base no comparativo da posição x.
- Função de spawn dos robôs de direção aleatória;
- Imagem de coletáveis como representação visual e contador, bem como a função de drop deles e de registro de vidas (corações) do jogador;
- Loop de funcionamento do jogo: 
  - Com identificação de eventos (tempo de spawn dos robôs, fechamento do jogo, movimentação e ataque);
  - Definição de derrota e de vitória;
  - Jogo funcionamento com atualização dos objetos em tela.

Main (código final):
- Início: importação de bibliotecas e demais classes;
- Tela:
- Código de tela inicial com “botões” interativos, com suas próprias funções internas, possibilitando entrar, reiniciar e sair do jogo;
- Músicas de derrota e de vitória;
- Função menu:
  - Possui a execução do jogo (pela importação do arquivo “Player_atualizado_coletaveis” e telas correspondentes ao resultado (“vitória” ou “derrota”).

## 🛠️ Ferramentas

- VSCode – Editor de código leve e poderoso, ideal para programação com suporte a múltiplas linguagens e extensões.
- Piskel – Ferramenta online para criar e editar pixel art de forma simples e intuitiva.
- ChatGPT – Assistente de IA utilizada para gerar designs do jogo.
- GitHub – Plataforma para hospedagem e controle de versão de código com colaboração em equipe.

## 📚 Bibliotecas

- Pygame – Biblioteca Python voltada para o desenvolvimento de jogos 2D, oferecendo recursos para gráficos, áudio e controle de eventos.
- Random – Biblioteca padrão do Python usada para gerar números aleatórios e realizar seleções randômicas, utilizada para criar a aleatoriedade do coletável.
- Math - Biblioteca padrão do Python que fornece funções matemáticas avançadas, utilizada para criar animações de pulsação nos botões do jogo.

## 💡 Conceitos utilizados

- Condicionais – Aplicadas em várias partes do código para tomar decisões, como verificar colisões, vida do jogador, direção do robô, momento de dropar coletáveis, pulo e reinício do jogo.
- Laços – O jogo roda em loop contínuo e há laços for para percorrer listas e grupos de sprites, como no processamento de robôs e coletáveis.
- Lista – Usada para armazenar dados como quantidade de robôs derrotados e itens coletados, facilitando contagem e escolha aleatória de elementos.
- Funções – Criadas para modularizar ações específicas, como, exibir o tempo, criar inimigos, gerar itens e mostrar a vida.
- Tuplas – Utilizadas em coordenadas e tamanhos fixos, garantindo dados imutáveis para posições e dimensões.
- POO (Programação Orientada a Objetos) – Aplicada na criação de classes como Coletaveis, Jogador e Robô, encapsulando atributos e métodos relacionados, além do uso de herança.

## 🕹️ Como jogar

### Executando

Para executar o código, é necessário ter o python e pygame instalados.

Baixe o branch main do repositório, extraia o arquivo zip, abra a pasta em seu editor e execute o main.py

### Comandos

→ **Move para direita**

← **Move para esquerda**

↑ **Pula**

*Espaço* **Ataca**

### Coletáveis

<img src="\asset\images\coletaveis\coração_vermelho.png" alt="Coração" width="30"> Regenera 1 de vida

<img src="\asset\images\coletaveis\café.png" alt="Café" width="30"> Aumenta a velocidade de ataque

<img src="\asset\images\coletaveis\powerup_sabre.png" alt="Espadinha" width="30"> Aumenta força de ataque

## ⚠️ Desafios e erros

- Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?

O maior erro foi demorarmos a iniciar a programação e começarmos cada um a desenvolver sua parte sem definir claramente as funções de cada membro, o que gerou confusão.. Lidamos com esse problema nos reunindo e definindo exatamente as funções de cada um, aproveitando todas as oportunidades para avançar no projeto

- Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

O maior desafio foi gerenciar o prazo curto enquanto tentávamos implementar todas as ideias, além de lidar com a integração de códigos de diferentes membros do grupo. Para contornar isso, foi necessária bastante comunicação, discutimos a melhor forma de mesclar códigos e priorizamos as funcionalidades essenciais.

- Quais as lições aprendidas durante o projeto?

Aprendemos a importância de estudar a base antes de começar a programar, de manter uma organização clara no GitHub e de trabalhar colaborativamente de forma coordenada.

## 🖼️ Galeria de imagens

Menu

<img src="\asset\images\tela_inicial\fundo_menu.png" width="800">

Jogo

<img src="\asset\images\tela_inicial\jogo_funcionando.png" width="800">

Tela Final

<img src="\asset\images\tela_inicial\tela_vitoria.png" width="800">
