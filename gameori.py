import pygame
import os  # Importante para lidar com caminhos de arquivos

# Inicializa o Pygame
pygame.init()

# Definir tamanho da tela
x = 1280
y = 720

# Configura a tela do jogo
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Jogo - sp')

# Carregar a imagem de fundo (garantindo que o caminho esteja correto)
bg_path = os.path.join('DALL·E 2024-10-03 11.36.39 - A pixel art background of a polluted futuristic cityscape for a 2D game. The design features simple, geometric skyscrapers, some with neon lights and .webp')  # Substitua com o caminho correto se necessário
bg = pygame.image.load(bg_path)
bg = pygame.transform.scale(bg, (x, y))

# Variável para controlar o loop do jogo
rodando = True

# Loop principal do jogo
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Desenhar o fundo na tela
    screen.blit(bg, (0, 0))
    
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width,0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))

    x-=2    
    # Atualizar a tel
    pygame.display.update()


pygame.quit()
