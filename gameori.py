import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Estilo Sonic")

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Carregar imagens
background = pygame.image.load("backgraund.png.webp")
player_img = pygame.image.load("player1.png").convert_alpha()
enemy_img = pygame.image.load("nuvem player2.png").convert_alpha()
cloud_img = pygame.image.load("mini nuvem dano.png").convert_alpha()
cloud_img = pygame.transform.rotate(cloud_img, 180)

# Configurações do player
player = pygame.Rect(100, 500, 50, 50)
player_speed = 5
player_vel_y = 0
gravity = 0.8
is_jumping = False
lives = 3

# Configurações do inimigo (vilão)
enemy = pygame.Rect(600, 500, 50, 50)
clouds = []
cloud_speed = 7
enemy_timer = 0  # Controla o tempo entre os disparos

# Anéis (colecionáveis)
rings = [pygame.Rect(random.randint(100, 700), 400, 20, 20) for _ in range(5)]
ring_count = 0

# Função para desenhar o texto na tela
font = pygame.font.SysFont(None, 36)
def draw_text(text, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Função para atualizar a posição do player
def update_player():
    global player_vel_y, is_jumping

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        player_vel_y = -15
        is_jumping = True

    # Aplicar gravidade e atualizar a posição vertical
    player_vel_y += gravity
    player.y += player_vel_y

    # Evitar que o player caia fora da tela
    if player.y > 500:
        player.y = 500
        is_jumping = False

# Função para gerar mini nuvens disparadas pelo inimigo
def shoot_cloud():
    cloud = pygame.Rect(enemy.x, enemy.y, 30, 30)
    clouds.append(cloud)

# Função para atualizar as nuvens disparadas
def update_clouds():
    global lives

    for cloud in clouds[:]:
        cloud.x -= cloud_speed
        if cloud.colliderect(player):
            lives -= 1
            clouds.remove(cloud)
        elif cloud.x < 0:
            clouds.remove(cloud)

# Função para verificar a colisão com os anéis
def check_ring_collision():
    global ring_count
    for ring in rings[:]:
        if player.colliderect(ring):
            rings.remove(ring)
            ring_count += 1

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar a posição do player e das nuvens
    update_player()
    update_clouds()

    # Verificar colisão com anéis
    check_ring_collision()

    # Controle do inimigo atirando nuvens
    enemy_timer += 1
    if enemy_timer > 60:  # Dispara uma nuvem a cada 60 frames
        shoot_cloud()
        enemy_timer = 0

    # Desenhar o fundo, personagens e interface
    screen.blit(background, (0, 0))
    screen.blit(player_img, player)
    screen.blit(enemy_img, enemy)
    for cloud in clouds:
        screen.blit(cloud_img, cloud)
    for ring in rings:
        pygame.draw.rect(screen, GREEN, ring)
    for i in range(lives):
        pygame.draw.rect(screen, RED, (10 + i * 30, 10, 20, 20))

    # Exibir pontuação
    draw_text(f"Anéis: {ring_count}", GREEN, 600, 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
