import pygame
import sys


# Анимация
current_animation = 'idle'
animation_frame = 0
animation_speed = 0.15
last_direction = 'right'

def update_animation():
    global animation_frame, current_animation
    
    if not on_ground:
        current_animation = 'jump'
    elif player_vel[0] != 0:
        current_animation = 'run_right' if player_vel[0] > 0 else 'run_left'
        animation_frame += animation_speed
    elif keys[pygame.K_DOWN]:
        current_animation = 'crouch'
    else:
        current_animation = 'idle'
    
    if isinstance(player_sprites[current_animation], list):
        if animation_frame >= len(player_sprites[current_animation]):
            animation_frame = 0
    else:
        animation_frame = 0

def get_current_sprite():
    if isinstance(player_sprites[current_animation], list):
        return player_sprites[current_animation][int(animation_frame) % len(player_sprites[current_animation])]
    return player_sprites[current_animation]


# Инициализация
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Платформер")

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# Фон
background_img = pygame.image.load("images/текстуры/фон1.png").convert()  # если хочешь фон
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Игрок
player_size = (50, 50)
# Загрузка спрайтов
player_sprites = {
    'idle': pygame.transform.scale(pygame.image.load("images/игрок/ожидание.png").convert_alpha(), player_size),
    'run_right': [pygame.transform.scale(pygame.image.load(f"images/игрок/вправо.png").convert_alpha(), player_size) for i in range(1, 5)],
    'run_left': [pygame.transform.scale(pygame.image.load(f"images/игрок/влево.png").convert_alpha(), player_size) for i in range(1, 5)],
    'jump': pygame.transform.scale(pygame.image.load("images/игрок/прыжок.png").convert_alpha(), player_size),
    'crouch': pygame.transform.scale(pygame.image.load("images/игрок/приседание.png").convert_alpha(), player_size)
}

player = pygame.Rect(100, 500, *player_size)
player_vel = [0, 0]
speed = 3
jump_power = -15
gravity = 1
on_ground = False

# Платформы
platform_img = pygame.image.load("images/текстуры/платформа.png").convert_alpha()
platform_size = (200, 20)
platform_img = pygame.transform.scale(platform_img, platform_size)

platforms = [
    (pygame.transform.scale(platform_img, (WIDTH, 20)), pygame.Rect(0, HEIGHT-20, WIDTH, 20)),
    (pygame.transform.scale(platform_img, (100, 20)), pygame.Rect(200, HEIGHT-100, 100, 20)),
    (pygame.transform.scale(platform_img, (100, 20)), pygame.Rect(300, HEIGHT-200, 100, 20)),
    (pygame.transform.scale(platform_img, (200, 20)), pygame.Rect(400, HEIGHT-300, 200, 20)),
    (pygame.transform.scale(platform_img, (100, 20)), pygame.Rect(700, HEIGHT-100, 100, 20))
]

# Часы
clock = pygame.time.Clock()
FPS = 60

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    print(player.x, player.y)

    # Управление
    keys = pygame.key.get_pressed()
    player_vel[0] = 0
    if keys[pygame.K_LEFT]:
        player_vel[0] = -speed
    if keys[pygame.K_RIGHT]:
        player_vel[0] = speed
    if keys[pygame.K_SPACE] and on_ground:
        player_vel[1] = jump_power
        on_ground = False

    # Обновление анимации
    update_animation()
    player_img = get_current_sprite()

    # Гравитация
    player_vel[1] += gravity

    # Перемещение по оси X
    player.x += player_vel[0]
    for img, plat in platforms:
        if player.colliderect(plat):
            if player_vel[0] > 0:
                player.right = plat.left
            elif player_vel[0] < 0:
                player.left = plat.right

    # Перемещение по оси Y
    player.y += player_vel[1]
    on_ground = False
    for img, plat in platforms:
        if player.colliderect(plat):
            if player_vel[1] > 0:
                player.bottom = plat.top
                player_vel[1] = 0
                on_ground = True
            elif player_vel[1] < 0:
                player.top = plat.bottom
                player_vel[1] = 0

    # Отрисовка
    screen.blit(background_img, (0, 0))  # фон

    screen.blit(player_img, (player.x, player.y))  # игрок

    for img, plat in platforms:
        screen.blit(img, (plat.x, plat.y))  # платформы

    pygame.display.flip()
    clock.tick(FPS)