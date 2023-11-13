import pygame
import random
import sys

pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 36
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
HITBOX_HEIGHT = 40
FIRE_HITBOX_WIDTH = 23
WATER_HITBOX_WIDTH = 25
OFFSET_X = 2
OFFSET_Y = 5

# Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Erupção na Vila")
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)
font = pygame.font.Font("PixelGameFont.ttf", FONT_SIZE)
orange = pygame.Color(ORANGE)
red = pygame.Color(RED)
fire_extinguish_sound = pygame.mixer.Sound("fire_extinguish.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

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


def draw_gradient_text(screen, text, x, y, start_color, end_color):
    global font
    text_surface = font.render(text, True, pygame.Color("white"))

    text_surface_copy = text_surface.copy()

    height = text_surface_copy.get_height()
    delta_r = (end_color.r - start_color.r) / height
    delta_g = (end_color.g - start_color.g) / height
    delta_b = (end_color.b - start_color.b) / height

    pixel_array = pygame.PixelArray(text_surface_copy)

    for py in range(height):
        r = int(start_color.r + delta_r * py)
        g = int(start_color.g + delta_g * py)
        b = int(start_color.b + delta_b * py)
        for px in range(text_surface_copy.get_width()):
            if text_surface_copy.get_at((px, py))[3] > 0:
                pixel_array[px, py] = (r, g, b)

    del pixel_array

    screen.blit(text_surface_copy, (x, y))


def final_lives_display():
    lives_width, lives_height = font.size(f"Vidas: {lives}")
    clear_rect = pygame.Rect(
        SCREEN_WIDTH - lives_width - 20, 5, lives_width + 10, lives_height + 5
    )
    screen.blit(background_image, clear_rect.topleft, clear_rect)
    draw_gradient_text(
        screen, f"Vidas: {lives}", SCREEN_WIDTH - lives_width - 10, 10, orange, red
    )
    pygame.display.update(clear_rect)


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
            water[0] + (water_image.get_width() - WATER_HITBOX_WIDTH) // 2,
            water[1] + OFFSET_Y,
            WATER_HITBOX_WIDTH,
            HITBOX_HEIGHT,
        )

        for fire in fire_list[:]:
            fire_rect = pygame.Rect(
                (fire[0] + (fire_image.get_width() - FIRE_HITBOX_WIDTH) // 2)
                + OFFSET_X,
                fire[1] + OFFSET_Y,
                FIRE_HITBOX_WIDTH,
                HITBOX_HEIGHT,
            )
            if water_rect.colliderect(fire_rect) and fire[2]:
                fire[2] = False
                score += 1
                fire_list.remove(fire)
                water_list.remove(water)
                fire_extinguish_sound.play()
                create_fire()
                break


def update_screen():
    screen.blit(background_image, (0, 0))
    for fire in fire_list:
        if fire[2]:
            screen.blit(fire_image, (fire[0], fire[1]))

    screen.blit(hose_image, (hose_x, SCREEN_HEIGHT - hose_rect.height))

    for water in water_list:
        screen.blit(water_image, (water[0], water[1]))

    draw_gradient_text(screen, f"Pontos: {score}", 10, 10, orange, red)
    if lives > 0:
        lives_width, _ = font.size(f"Vidas: {lives}")
        draw_gradient_text(
            screen, f"Vidas: {lives}", SCREEN_WIDTH - lives_width - 10, 10, orange, red
        )

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
                [
                    hose_x + (hose_rect.width - water_image.get_width()) // 2,
                    SCREEN_HEIGHT - hose_rect.height,
                ]
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
                        final_lives_display()
                        game_over_text = "Game Over"
                        text_width, text_height = font.size(game_over_text)
                        text_x = (SCREEN_WIDTH - text_width) // 2
                        text_y = (SCREEN_HEIGHT - text_height) // 2
                        draw_gradient_text(
                            screen, game_over_text, text_x, text_y, orange, red
                        )
                        pygame.display.update()
                        pygame.time.wait(3000)
                        running = False
                        break
                    create_fire()

        update_screen()
        clock.tick(60)


if __name__ == "__main__":
    water_image = pygame.image.load("water.png")
    main()
