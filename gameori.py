import pygame
import os

# Inicializar o Pygame
pygame.init()

# Definições de tamanho da tela
x = 1280
y = 720

# Criar a tela do jogo
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Jogo - sp')

# Carregar a imagem de fundo
bg_path = os.path.join('DALL·E 2024-10-03 11.36.39 - A pixel art background of a polluted futuristic cityscape for a 2D game. The design features simple, geometric skyscrapers, some with neon lights and .webp')  # Substitua com o caminho correto se necessário
bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (x, y))

# Carregar a imagem do jogador
playerImg = pygame.image.load('personagemprc.png').convert_alpha()
playerImg = pygame.transform.scale(playerImg, (50, 50))

# Posição inicial do jogador
pos_player_x = 200
pos_player_y = 660

# Variável de controle do loop do jogo
rodando = True
bg_x = 0  # Posição inicial do fundo

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Limpar a tela
    screen.blit(bg, (0, 0))

    # Lógica de movimentação do jogador
    keys = pygame.key.get_pressed()  # Verifica as teclas pressionadas
    if keys[pygame.K_LEFT]:  # Mover para a esquerda
        pos_player_x -= 5  # Ajuste a velocidade conforme necessário
    if keys[pygame.K_RIGHT]:  # Mover para a direita
        pos_player_x += 5  # Ajuste a velocidade conforme necessário

    # Lógica de movimento do fundo
    bg_x -= 2  # Velocidade de movimento do fundo

    # Reposicionar o fundo
    rel_x = bg_x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width, 0))
    if rel_x < x:
        screen.blit(bg, (rel_x, 0))

    # Desenhar o jogador na tela
    screen.blit(playerImg, (pos_player_x, pos_player_y))
    
    # Atualizar a tela
    pygame.display.update()

# Finalizar o Pygame
pygame.quit()

