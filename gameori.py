import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Estilo Sonic")

BLACK = (0, 0, 0)  
GREEN = (0, 255, 0)  # Cor para os anéis
RED = (255, 0, 0)    # Cor para as vidas

# Carregar o background corretamente
try:
    background = pygame.image.load("backgraund.png.webp").convert()
except FileNotFoundError:
    print("Erro: 'background.png.webp' não encontrado.")
    pygame.quit()
    exit()

background = pygame.transform.scale(background, (SCREEN_WIDTH * 3, SCREEN_HEIGHT))  # Ajuste para um fundo maior

# Carregar imagens e garantir que não sejam distorcidas
player_img = pygame.image.load("player1.png").convert_alpha()
enemy_img = pygame.image.load("nuvem player2.png").convert_alpha()
cloud_img = pygame.image.load("mini nuvem dano.png").convert_alpha()
cloud_img = pygame.transform.rotate(cloud_img, 180)

# Configurações do player
player = pygame.Rect(100, 500, player_img.get_width(), player_img.get_height())
player_speed = 5
player_vel_y = 0
gravity = 0.8
is_jumping = False
lives = 3

# Configurações do inimigo
enemy = pygame.Rect(600, 500, enemy_img.get_width(), enemy_img.get_height())
enemy_speed = 2
clouds = []
cloud_speed = 7
enemy_timer = 0

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

    player_vel_y += gravity
    player.y += player_vel_y

    if player.y > 500:
        player.y = 500
        is_jumping = False

# Função para movimentar o inimigo
def update_enemy():
    dx = player.x - enemy.x
    dy = player.y - enemy.y
    dist = math.sqrt(dx ** 2 + dy ** 2)

    if dist != 0:
        enemy.x += int(enemy_speed * dx / dist)
        enemy.y += int(enemy_speed * dy / dist)

# Função para disparar nuvens
def shoot_cloud():
    cloud = pygame.Rect(enemy.x, enemy.y, 30, 30)
    clouds.append(cloud)

# Função para atualizar nuvens
def update_clouds():
    global lives

    for cloud in clouds[:]:
        cloud.x -= cloud_speed
        if cloud.colliderect(player):
            lives -= 1
            clouds.remove(cloud)
        elif cloud.x < 0:
            clouds.remove(cloud)

# Função para verificar colisão com anéis
def check_ring_collision():
    global ring_count
    for ring in rings[:]:
        if player.colliderect(ring):
            rings.remove(ring)
            ring_count += 1

# Função para calcular o deslocamento da câmera
def camera_offset():
    offset_x = min(0, -player.x + SCREEN_WIDTH // 2)
    offset_x = max(offset_x, SCREEN_WIDTH - background.get_width())  # Limite à direita
    return offset_x, 0  # Manter o eixo Y fixo para evitar deslocamento vertical

# Loop principal
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_player()
    update_enemy()
    update_clouds()
    check_ring_collision()

    enemy_timer += 1
    if enemy_timer > 60:
        shoot_cloud()
        enemy_timer = 0

    offset_x, offset_y = camera_offset()

    screen.blit(background, (offset_x, offset_y))

    # Desenhar o player e inimigo com deslocamento
    screen.blit(player_img, (player.x + offset_x, player.y))
    screen.blit(enemy_img, (enemy.x + offset_x, enemy.y))

    # Desenhar as nuvens
    for cloud in clouds:
        screen.blit(cloud_img, (cloud.x + offset_x, cloud.y))

    # Desenhar anéis
    for ring in rings:
        pygame.draw.rect(screen, GREEN, ring.move(offset_x, offset_y))

    # Vidas e pontuação
    for i in range(lives):
        pygame.draw.rect(screen, RED, (10 + i * 30, 10, 20, 20))
    draw_text(f"Anéis: {ring_count}", GREEN, 600, 10)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()


