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
    enemy_img = pygame.image.load("nuvemori2.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (700, 550))
    cloud_img = pygame.image.load("nuvemmini2.gif").convert_alpha()
    cloud_img = pygame.transform.scale(cloud_img, (365, 320))

    # Classe do jogador com sprites
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.sprites_running = [
                pygame.transform.scale(pygame.image.load('correr 3pra esquerda.png').convert_alpha(), (100, 150)),
                pygame.transform.scale(pygame.image.load('correr pra esquerda.png').convert_alpha(), (100, 150)),
                pygame.transform.scale(pygame.image.load('correr2 pra esquerda.png').convert_alpha(), (100, 150))
            ]
            self.sprites_standing = [
                pygame.transform.scale(pygame.image.load('paradodireita 1.png').convert_alpha(), (100, 150)),
                pygame.transform.scale(pygame.image.load('paradodireita2.png').convert_alpha(), (100, 150)),
                pygame.transform.scale(pygame.image.load('paradodireita3.png').convert_alpha(), (100, 150)),
                pygame.transform.scale(pygame.image.load('paradodireita4.png').convert_alpha(), (100, 150))
            ]
            self.current_sprite = 0
            self.image = self.sprites_standing[0]
            self.rect = self.image.get_rect()
            self.rect.x = 800
            self.rect.y = SCREEN_HEIGHT - 300  # Ajustado para ficar um pouco mais para cima
            self.speed = 5
            self.vel_y = 0
            self.gravity = 0.8
            self.is_jumping = False
            self.is_moving = False  # Para controle de movimento

        def update(self):
            keys = pygame.key.get_pressed()
            self.is_moving = False  # Reseta a movimentação

            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
                self.is_moving = True  # Atualiza para indicar movimento
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.is_moving = True  # Atualiza para indicar movimento
            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.vel_y = -15
                self.is_jumping = True

            # Gravitacional
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.y > SCREEN_HEIGHT - 190:
                self.rect.y = SCREEN_HEIGHT - 190
                self.is_jumping = False
            
            # Atualiza a imagem do jogador
            if self.is_moving:
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites_running)  # Animação enquanto se move
                self.image = self.sprites_running[self.current_sprite]
            else:
                self.image = self.sprites_standing[self.current_sprite % len(self.sprites_standing)]  # Posição parada

except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}")
    pygame.quit()

# Redimensionar o background para a tela
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Configuração da nuvem inimiga
enemy = pygame.Rect(0, SCREEN_HEIGHT // 2 - 300, 700, 400)
enemy_speed = 2
clouds = []
cloud_speed = 7
enemy_timer = 0
can_shoot = True

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
leaves = []
leaf_count = 0

# Função para gerar uma folha no chão
def spawn_leaf():
    x = random.randint(800, SCREEN_WIDTH + 400)
    y = SCREEN_HEIGHT - 100  # No chão visível
    leaf_image = random.choice(leaf_images)  # Escolhe uma imagem aleatória para a folha
    return pygame.Rect(x, y, 60, 60), leaf_image

# Manter a quantidade correta de folhas
def maintain_leaf():
    if len(leaves) < 1:  # Limite de uma folha ativa por vez
        new_leaf, leaf_img = spawn_leaf()
        leaves.append((new_leaf, leaf_img))

# Carregar e redimensionar as folhas
leaf_images = [
    pygame.transform.scale(pygame.image.load(f"folha{i}.png").convert_alpha(), (60, 60))
    for i in range(1, 5)
]

# Função para verificar colisão com a folha
def check_leaf_collision(player):
    global leaf_count, can_shoot
    for leaf, leaf_img in leaves[:]:
        if player.rect.colliderect(leaf):
            leaf_count += 1
            print(f"Folhas coletadas: {leaf_count}")
            leaves.remove((leaf, leaf_img))
            if leaf_count >= 10:
                can_shoot = False

# Função para disparar nuvens se permitido
def shoot_cloud_towards_player():
    if can_shoot:
        cloud = pygame.Rect(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2, 30, 30)
        clouds.append(cloud)

# Atualizar as nuvens disparadas
def update_clouds():
    global lives
    for cloud in clouds[:]:
        dx = player.rect.x - cloud.x
        dy = player.rect.y - cloud.y
        dist = math.sqrt(dx ** 2 + dy ** 2)

        if dist != 0:
            cloud.x += int(cloud_speed * dx / dist)
            cloud.y += int(cloud_speed * dy / dist)

        if cloud.colliderect(player.rect):
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

# Instanciando o jogador
player = Player()

# Iniciar contagem de vidas
lives = 3

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Manter a folha
    maintain_leaf()

    # Atualizar jogador e inimigos
    player.update()
    update_clouds()
    check_leaf_collision(player)

    # Controlar disparo de nuvens
    enemy_timer += 1
    if enemy_timer > 60:
        shoot_cloud_towards_player()
        enemy_timer = 0

    for ground_enemy in ground_enemies:
        ground_enemy.update()
        ground_enemy.draw(screen)

    # Desenhar background
    draw_scrolling_background(player.rect.x)

    # Desenhar player e nuvem inimiga
    player_y_on_screen = player.rect.y
    screen.blit(player.image, (player.rect.x, player_y_on_screen))
    screen.blit(enemy_img, (enemy.x - player.rect.x + SCREEN_WIDTH // 2, enemy.y))

    # Desenhar folhas
    for leaf, leaf_img in leaves:
        screen.blit(leaf_img, (leaf.x - player.rect.x + SCREEN_WIDTH // 2, leaf.y))

    # Desenhar nuvens
    for cloud in clouds:
        screen.blit(cloud_img, (cloud.x - player.rect.x + SCREEN_WIDTH // 2, cloud.y))

    # Desenhar vidas
    for i in range(lives):
        pygame.draw.rect(screen, RED, (10 + i * 30, 10, 20, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

