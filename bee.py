import pygame, os
from pygame.locals import *
from random import randint

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 600, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images
bee_img = pygame.image.load(os.path.join('images','bee.png'))
flower_img = pygame.image.load(os.path.join('images', 'flower.png'))
background_img = pygame.image.load(os.path.join('images','background.png'))

# Initial positions
bee_pos = [100, 100]
flower_pos = [200, 200]

score = 0
game_over = False
font = pygame.font.Font(None, 36)

# Function to place the flower randomly
def place_flower():
    flower_pos[0] = randint(70, WIDTH - 70)
    flower_pos[1] = randint(70, HEIGHT - 70)

# Function to display text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Main game loop
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

while not game_over:
    window.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        bee_pos[0] -= 2
    if keys[K_RIGHT]:
        bee_pos[0] += 2
    if keys[K_UP]:
        bee_pos[1] -= 2
    if keys[K_DOWN]:
        bee_pos[1] += 2

    # Check collision
    bee_rect = bee_img.get_rect(topleft=(bee_pos[0], bee_pos[1]))
    flower_rect = flower_img.get_rect(topleft=(flower_pos[0], flower_pos[1]))

    if bee_rect.colliderect(flower_rect):
        score += 10
        place_flower()

    # Draw everything
    window.blit(bee_img, bee_pos)
    window.blit(flower_img, flower_pos)
    draw_text("Score: " + str(score), font, (0, 0, 0), window, 10, 10)

    # Check for game over
    if (pygame.time.get_ticks() - start_ticks) / 1000 > 30:
        game_over = True

    pygame.display.flip()
    clock.tick(60)

# Game over screen
window.fill((255, 182, 193))  # pink color
draw_text("Time's up! Your final score: " + str(score), font, (255, 0, 0), window, WIDTH // 2 - 100, HEIGHT // 2 - 20)
pygame.display.flip()
pygame.time.wait(3000)