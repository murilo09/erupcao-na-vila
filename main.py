import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT_SIZE = 36
FONT_COLOR = (0, 0, 0)

# Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Incêndio Florestal")
font = pygame.font.Font(None, FONT_SIZE)

# Mangueira
hose_speed = 5
hose_image = pygame.image.load("hose.png")
hose_rect = hose_image.get_rect()
hose_x = SCREEN_WIDTH // 2 - hose_rect.width // 2

# Água
water_list = []
water_speed = 4

# Fogo
fire_list = []
fire_speed = 2
fire_image = pygame.image.load("fire.png")
fire_rect = fire_image.get_rect()

# Jogo
score = 0
lives = 3
trigger_delay = 1000
safety_line = SCREEN_HEIGHT - 50


def draw_text(text, x, y):
    text_surface = font.render(text, True, FONT_COLOR)
    screen.blit(text_surface, (x, y))


def create_fire():
    fire_x = random.randint(0, SCREEN_WIDTH - fire_rect.width)
    fire_y = 0
    fire_on_fire = True
    fire_list.append([fire_x, fire_y, fire_on_fire])


def set_difficulty():
    global score, hose_speed, trigger_delay, fire_list, fire_speed, water_speed
    if 15 <= score < 25:
        hose_speed = 7
        trigger_delay = 700
    elif 25 <= score < 30:
        fire_speed = 3
        water_speed = 5
        hose_speed = 8
        trigger_delay = 500
    elif score >= 30:
        fire_speed = 4
        water_speed = 6
        hose_speed = 9
        trigger_delay = 300


def update_water_shots():
    global score
    for water in water_list[:]:
        water[1] -= water_speed
        water_rect = pygame.Rect(
            water[0], water[1], water_image.get_width(), water_image.get_height()
        )

        for fire in fire_list[:]:
            fire_rect = pygame.Rect(
                fire[0], fire[1], fire_image.get_width(), fire_image.get_height()
            )
            if water_rect.colliderect(fire_rect) and fire[2]:
                fire[2] = False
                score += 1
                water_list.remove(water)
                fire_list.remove(fire)
                create_fire()
                break


def update_screen():
    screen.fill(WHITE)
    for fire in fire_list:
        if fire[2]:
            screen.blit(fire_image, (fire[0], fire[1]))

    screen.blit(hose_image, (hose_x, SCREEN_HEIGHT - hose_rect.height))

    for water in water_list:
        screen.blit(water_image, (water[0], water[1]))

    pygame.draw.rect(screen, RED, (0, safety_line, SCREEN_WIDTH, 10))
    draw_text(f"Pontuação: {score}", 10, 10)
    lives_width, _ = font.size(f"Vidas: {lives}")
    draw_text(f"Vidas: {lives}", SCREEN_WIDTH - lives_width - 10, 10)

    pygame.display.update()


def main():
    global lives, hose_x, score, water_list, fire_list, trigger_delay, hose_speed
    last_shot_time = pygame.time.get_ticks() - trigger_delay

    clock = pygame.time.Clock()
    running = True

    create_fire()

    while running:
        tempo_atual = pygame.time.get_ticks()

        if score >= 10 and len(fire_list) < 2:
            create_fire()
        if score >= 15 and len(fire_list) < 3:
            create_fire()
        if score >= 25 and len(fire_list) < 4:
            create_fire()
        set_difficulty()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        if keys[pygame.K_a]:
            hose_x -= hose_speed
        if keys[pygame.K_d]:
            hose_x += hose_speed
        if keys[pygame.K_SPACE] and tempo_atual - last_shot_time >= trigger_delay:
            water_list.append(
                [hose_x + hose_rect.width // 2, SCREEN_HEIGHT - hose_rect.height]
            )
            last_shot_time = tempo_atual

        hose_x = max(0, min(hose_x, SCREEN_WIDTH - hose_rect.width))

        update_water_shots()

        for fire in fire_list[:]:
            if fire[2]:
                fire[1] += fire_speed
                if fire[1] > safety_line:
                    lives -= 1
                    fire_list.remove(fire)
                    if lives <= 0:
                        print("Fogo atingiu a linha! Jogo encerrado.")
                        running = False
                        break
                    else:
                        create_fire()

        update_screen()
        clock.tick(60)


if __name__ == "__main__":
    water_image = pygame.image.load("water.png")
    main()
