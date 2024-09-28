import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width = 800
height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Avoid the Falling Blocks")

# Player properties
player_size = 40
player_pos = [width // 2, height - 2 * player_size]

# Enemy properties
enemy_size = 50
enemy_list = [[random.randint(0, width - enemy_size), 0]]

# Game speed
speed = 10

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("monospace", 35)

# Function to detect collisions
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

# Function to drop enemies
def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

# Function to update enemy positions
def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

# Function to draw enemies
def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

# Function to update the speed as the score increases
def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 8
    elif score < 60:
        speed = 12
    else:
        speed = 15
    return speed

# Function to reset the game
def reset_game():
    global player_pos, enemy_list, score, speed, game_over
    player_pos = [width // 2, height - 2 * player_size]
    enemy_list = [[random.randint(0, width - enemy_size), 0]]
    score = 0
    speed = 10
    game_over = False

# Function to draw the "Try Again" button
def draw_try_again_button():
    pygame.draw.rect(screen, green, (width // 3, height // 2, width // 3, 50))
    button_text = font.render("Try Again", True, black)
    screen.blit(button_text, (width // 3 + 50, height // 2 + 10))

# Main game loop
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if width // 3 <= mouse_x <= width // 3 + width // 3 and height // 2 <= mouse_y <= height // 2 + 50:
                reset_game()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 10
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += 10

    screen.fill(black)

    if not game_over:
        drop_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score)
        speed = set_level(score, speed)

        text = "Score: " + str(score)
        label = font.render(text, 1, white)
        screen.blit(label, (width - 200, height - 40))

        for enemy_pos in enemy_list:
            if detect_collision(player_pos, enemy_pos):
                game_over = True
                break

        draw_enemies(enemy_list)
        pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))
    else:
        screen.fill(black)
        game_over_text = font.render("Game Over! Score: " + str(score), True, white)
        screen.blit(game_over_text, (width // 4, height // 2 - 50))
        draw_try_again_button()

    clock.tick(30)
    pygame.display.update()
