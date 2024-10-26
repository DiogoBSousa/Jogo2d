import pygame
import random
import math

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 973
SCREEN_HEIGHT = 556
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Estilo Sonic")

# Cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Carregar imagens
try:
    background = pygame.image.load("Fundo 1.webp").convert()
    player_img = pygame.image.load("player1.png").convert_alpha()
    enemy_img = pygame.image.load("nuvem player2.png").convert_alpha()
    cloud_img = pygame.image.load("mini nuvem dano.png").convert_alpha()
    cloud_img = pygame.transform.rotate(cloud_img, 180)

    #Configurar imagem do player
     
     # Carregar e redimensionar a imagem do player para o tamanho desejado (ex: 40x50)
    player_img = pygame.image.load("player1.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (100, 150))


    # Carregar e redimensionar as folhas
    leaf_images = [
        pygame.transform.scale(pygame.image.load(f"folha{i}.png").convert_alpha(), (20, 20))
        for i in range(1, 5)
    ]
except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    pygame.quit()

# Redimensionar o background para a tela
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurações do player
player = pygame.Rect(500, SCREEN_HEIGHT - 100, 30, 38)  # Posição inicial do player ajustada para frente
player_speed = 5
player_vel_y = 0
gravity = 0.8
is_jumping = False
lives = 3

# Configuração da nuvem inimiga (posição fixa vertical na esquerda)
enemy = pygame.Rect(50, SCREEN_HEIGHT // 2, 50, 50)  # Nuvem inimiga na esquerda, atrás do player
enemy_speed = 2
clouds = []
cloud_speed = 7
enemy_timer = 0
can_shoot = True  # A nuvem só dispara enquanto houver folhas

# Configuração dos inimigos terrestres
class GroundEnemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

ground_enemies = [
    GroundEnemy(300, 500, 40, 40, 2),
    GroundEnemy(600, 500, 50, 50, 3)
]

# Folha e contadores
leaves = []  # Lista para folhas individuais
leaf_count = 0

# Função para gerar uma folha no chão
def spawn_leaf():
    x = random.randint(200, SCREEN_WIDTH - 30)
    y = SCREEN_HEIGHT - 100  # No chão visível
    leaf_image = random.choice(leaf_images)  # Escolhe uma imagem aleatória para a folha
    return pygame.Rect(x, y, 60, 60), leaf_image

# Manter a quantidade correta de folhas
def maintain_leaf():
    if len(leaves) < 1:  # Limite de uma folha ativa por vez
        new_leaf, leaf_img = spawn_leaf()
        leaves.append((new_leaf, leaf_img))

# Carregar e redimensionar as folhas para o tamanho desejado (ex: 30x30)
leaf_images = [
    pygame.transform.scale(pygame.image.load(f"folha{i}.png").convert_alpha(), (60, 60))
    for i in range(1, 5)
]


# Função para verificar colisão com a folha
def check_leaf_collision():
    global leaf_count, can_shoot
    for leaf, leaf_img in leaves[:]:
        if player.colliderect(leaf):
            leaf_count += 1
            print(f"Folhas coletadas: {leaf_count}")
            leaves.remove((leaf, leaf_img))  # Remove a folha coletada
            if leaf_count >= 10:
                can_shoot = False  # Desativa os disparos da nuvem

# Função para atualizar o player
def update_player():
    global player_vel_y, is_jumping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_SPACE] and not is_jumping:
        player_vel_y = -15
        is_jumping = True

    player_vel_y += gravity
    player.y += player_vel_y
    if player.y > 455:
        player.y = 455
        is_jumping = False

# Função para disparar nuvens se permitido
def shoot_cloud_towards_player():
    if can_shoot:
        cloud = pygame.Rect(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, 30, 30)
        clouds.append(cloud)

# Atualizar as nuvens disparadas
def update_clouds():
    global lives
    for cloud in clouds[:]:
        dx = player.x - cloud.x
        dy = player.y - cloud.y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist != 0:
            cloud.x += int(cloud_speed * dx / dist)
            cloud.y += int(cloud_speed * dy / dist)

        if cloud.colliderect(player):
            lives -= 1
            clouds.remove(cloud)
        elif cloud.x < 0 or cloud.x > SCREEN_WIDTH:
            clouds.remove(cloud)

# Função para mover o background
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

    # Manter a folha
    maintain_leaf()

    # Atualizar jogador e inimigos
    update_player()
    update_clouds()
    check_leaf_collision()

    # Controlar disparo de nuvens
    enemy_timer += 1
    if enemy_timer > 60:
        shoot_cloud_towards_player()
        enemy_timer = 0

    for ground_enemy in ground_enemies:
        ground_enemy.update()
        ground_enemy.draw(screen)

    # Desenhar background
    draw_scrolling_background(player.x)

    # Desenhar player e nuvem inimiga
    player_y_on_screen = player.y - player_img.get_height() // 2
    screen.blit(player_img, (SCREEN_WIDTH // 2, player_y_on_screen))
    screen.blit(enemy_img, (enemy.x - player.x + SCREEN_WIDTH // 2, enemy.y))

    # Desenhar folhas
    for leaf, leaf_img in leaves:
        screen.blit(leaf_img, (leaf.x - player.x + SCREEN_WIDTH // 2, leaf.y))

    # Desenhar nuvens
    for cloud in clouds:
        screen.blit(cloud_img, (cloud.x - player.x + SCREEN_WIDTH // 2, cloud.y))

    # Desenhar vidas
    for i in range(lives):
        pygame.draw.rect(screen, RED, (10 + i * 30, 10, 20, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

