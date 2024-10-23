import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Estilo Sonic")

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Carregar imagens
try:
    background = pygame.image.load("backgraund.png.webp").convert()
    player_img = pygame.image.load("player1.png").convert_alpha()
    enemy_img = pygame.image.load("nuvem player2.png").convert_alpha()
    cloud_img = pygame.image.load("mini nuvem dano.png").convert_alpha()
    cloud_img = pygame.transform.rotate(cloud_img, 180)
except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    pygame.quit()

# Redimensionar background para o tamanho da tela (scroll infinito)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurações do player
player = pygame.Rect(100, 500, 50, 50)
player_speed = 5
player_vel_y = 0
gravity = 0.8
is_jumping = False
lives = 3

# Configurações do inimigo (vilão)
enemy = pygame.Rect(600, 500, 50, 50)
enemy_speed = 2
clouds = []  # Armazena as nuvens disparadas
cloud_speed = 7
enemy_timer = 0  # Controla o tempo entre disparos

# Anéis (colecionáveis)
rings = [pygame.Rect(random.randint(100, 2000), 400, 20, 20) for _ in range(5)]
ring_count = 0

# Função para desenhar texto
font = pygame.font.SysFont(None, 36)
def draw_text(text, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

# Função para atualizar o player
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

    # Aplicar gravidade e evitar que o player caia fora da tela
    player_vel_y += gravity
    player.y += player_vel_y

    if player.y > 500:
        player.y = 500
        is_jumping = False

# Função para o inimigo perseguir o player
def update_enemy():
    dx = player.x - enemy.x
    dy = player.y - enemy.y
    dist = math.sqrt(dx ** 2 + dy ** 2)

    if dist != 0:
        enemy.x += int(enemy_speed * dx / dist)
        enemy.y += int(enemy_speed * dy / dist)

# Função para disparar nuvens em direção ao player
def shoot_cloud_towards_player():
    """Função para disparar nuvens do inimigo para o player"""
    cloud = pygame.Rect(enemy.x, enemy.y, 30, 30)
    clouds.append(cloud)

# Função para atualizar a posição das nuvens disparadas
def update_clouds():
    global lives

    for cloud in clouds[:]:
        dx = player.x - cloud.x
        dy = player.y - cloud.y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist != 0:
            cloud.x += int(cloud_speed * dx / dist)
            cloud.y += int(cloud_speed * dy / dist)

        # Verificar colisão com o player
        if cloud.colliderect(player):
            lives -= 1
            clouds.remove(cloud)
        elif cloud.x < 0 or cloud.x > SCREEN_WIDTH:
            clouds.remove(cloud)

# Função para verificar colisão com anéis
def check_ring_collision():
    global ring_count
    for ring in rings[:]:
        if player.colliderect(ring):
            rings.remove(ring)
            ring_count += 1

# Função para mover o background repetidamente
def draw_scrolling_background(player_x):
    scroll_x = player_x % SCREEN_WIDTH
    screen.blit(background, (-scroll_x, 0))
    screen.blit(background, (SCREEN_WIDTH - scroll_x, 0))

# Loop principal do jogo
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar o player, inimigo e nuvens
    update_player()
    update_enemy()
    update_clouds()
    check_ring_collision()

    # Controlar o disparo do inimigo
    enemy_timer += 1
    if enemy_timer > 60:  # A cada 60 frames, o inimigo dispara
        shoot_cloud_towards_player()
        enemy_timer = 0

    # Desenhar o fundo rolando (scroll infinito)
    draw_scrolling_background(player.x)

    # Desenhar o player e o inimigo
    screen.blit(player_img, (SCREEN_WIDTH // 2, player.y))
    screen.blit(enemy_img, (enemy.x - player.x + SCREEN_WIDTH // 2, enemy.y))

    # Desenhar as nuvens disparadas
    for cloud in clouds:
        screen.blit(cloud_img, (cloud.x - player.x + SCREEN_WIDTH // 2, cloud.y))

    # Desenhar os anéis
    for ring in rings:
        pygame.draw.rect(screen, GREEN, ring.move(-player.x + SCREEN_WIDTH // 2, 0))

    # Desenhar vidas e pontuação
    for i in range(lives):
        pygame.draw.rect(screen, RED, (10 + i * 30, 10, 20, 20))
    draw_text(f"Anéis: {ring_count}", GREEN, 600, 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()



