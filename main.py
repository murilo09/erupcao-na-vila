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
hose_image = pygame.image.load("hose.png")
hose_rect = hose_image.get_rect()
hose_x = SCREEN_WIDTH // 2 - hose_rect.width // 2
hose_speed = 5

# Água
water_speed = 5
water_list = []

# Fogo
fire_image = pygame.image.load("fire.png")
fire_rect = fire_image.get_rect()
fire_speed = 2
fire_x = random.randint(0, SCREEN_WIDTH - fire_rect.width)
fire_y = 0
fire_on_fire = True

# Jogo
score = 0
safety_line = SCREEN_HEIGHT - 50


def draw_text(text, x, y):
    text_surface = font.render(text, True, FONT_COLOR)
    screen.blit(text_surface, (x, y))


def update_water_shots():
    global score, fire_on_fire
    for water in water_list:
        water[1] -= water_speed
        water_rect = pygame.Rect(
            water[0], water[1], water_image.get_width(), water_image.get_height()
        )

        if (
            water_rect.colliderect(
                pygame.Rect(fire_x, fire_y, fire_rect.width, fire_rect.height)
            )
            and fire_on_fire
        ):
            fire_on_fire = False
            score += 1
            water_list.remove(water)
            break


def update_screen():
    screen.fill(WHITE)
    if fire_on_fire:
        screen.blit(fire_image, (fire_x, fire_y))
    screen.blit(hose_image, (hose_x, SCREEN_HEIGHT - hose_rect.height))
    for water in water_list:
        screen.blit(water_image, (water[0], water[1]))
    pygame.draw.rect(screen, RED, (0, safety_line, SCREEN_WIDTH, 10))
    draw_text(f"Pontuação: {score}", 10, 10)
    pygame.display.update()


def main():
    global fire_x, fire_y, fire_on_fire, hose_x, score, water_list

    clock = pygame.time.Clock()
    running = True

    while running:
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
        if keys[pygame.K_SPACE]:
            water_list.append(
                [hose_x + hose_rect.width // 2, SCREEN_HEIGHT - hose_rect.height]
            )

        hose_x = max(0, min(hose_x, SCREEN_WIDTH - hose_rect.width))

        update_water_shots()

        fire_y += fire_speed
        if fire_y > safety_line or not fire_on_fire:
            fire_x = random.randint(0, SCREEN_WIDTH - fire_rect.width)
            fire_y = 0
            fire_on_fire = True

        update_screen()
        clock.tick(60)


if __name__ == "__main__":
    water_image = pygame.image.load("water.png")
    main()
