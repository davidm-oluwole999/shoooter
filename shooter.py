import pygame
import os
import time

pygame.font.init()

pygame.mixer.init()

WIDTH, HEIGHT= 900, 500
WINDOW= pygame.display.set_mode((WIDTH,HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
pygame.display.set_caption("Space Shooter Game")

r_bullets= []
y_bullets= []
bullet_speed= 9
speed= 5

RED_HIT= pygame.USEREVENT+ 1
YELLOW_HIT= pygame.USEREVENT+ 2

ysi= pygame.image.load(os.path.join("images", "spaceship2.png"))#yellow ship image= ysi
rsi= pygame.image.load(os.path.join("images", "spaceship.png"))#red ship image

border= pygame.Rect(WIDTH//2, 0, 10, HEIGHT)
ys= pygame.transform.rotate(pygame.transform.scale(ysi,(50, 40)), 90)
rs= pygame.transform.rotate(pygame.transform.scale(rsi,(50, 40)), 270)
space= pygame.transform.scale(pygame.image.load(os.path.join("images", "space.png")), (WIDTH, HEIGHT))

def draw_window(red, yellow, r_bullets, y_bullets, r_health, y_health):
    WINDOW.blit(space, (0, 0))
    pygame.draw.rect(WINDOW, "green", border)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(r_health), 1,"white" )
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(y_health), 1, 'white')
    WINDOW.blit(yellow_health_text, (10,10))
    WINDOW.blit(red_health_text, (WIDTH- 60, 10))
    WINDOW.blit(ys, (yellow.x, yellow.y))
    WINDOW.blit(rs,(red.x, red.y))
    for r in r_bullets:
        pygame.draw.rect(WINDOW, "red", r)
    for y in y_bullets:
        pygame.draw.rect(WINDOW, "yellow", y, )
    pygame.display.update()

def movement_y(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x- speed> 0:
        yellow.x-= speed
    elif keys_pressed[pygame.K_d] and yellow.x+ speed+ yellow.width< border.x:
        yellow.x+= speed
    if keys_pressed[pygame.K_w] and yellow.y- speed> 0:
        yellow.y-= speed
    elif keys_pressed[pygame.K_s] and yellow.y+ speed+ yellow.height< HEIGHT- 15:
        yellow.y+= speed

def movement_r(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x- speed> border.x+ border.width:
        red.x-= speed
    elif keys_pressed[pygame.K_RIGHT] and red.x+ speed+ red.width< WIDTH:
        red.x+= speed
    if keys_pressed[pygame.K_UP] and red.y- speed> 0:
        red.y-= speed
    elif keys_pressed[pygame.K_DOWN] and red.y+ speed+ red.height< HEIGHT- 15:
        red.y+= speed


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x+= bullet_speed
        if bullet.colliderect(red):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x> WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-= bullet_speed
        if bullet.colliderect(yellow):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x< 0:
            red_bullets.remove(bullet)         
          
def main():
    global r_bullets, y_bullets, winner_text
    red= pygame.Rect(800,250,50,40)
    yellow= pygame.Rect(100,250,50,40)
    r_bullets= []
    y_bullets= []
    r_health= 10
    y_health= 10
    clock= pygame.time.Clock()
    run= True
    while run:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run= False
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LCTRL and len(y_bullets)< 50:
                    bullet= pygame.Rect(yellow.x+ yellow.width, yellow.y+ yellow.height//2, 10, 5)
                    y_bullets.append(bullet)
                if e.key == pygame.K_RCTRL and len(r_bullets)< 50:
                    bullet= pygame.Rect(red.x+ red.width, red.y+ red.height//2, 10, 5)
                    r_bullets.append(bullet)
            if e.type == RED_HIT:
                r_health-= 1
            elif e.type == YELLOW_HIT:
                y_health-= 1
        winner_text=""
        if r_health<= 0:
            winner_text= "YELLOW WINS!!!"
        if y_health<= 0:
            winner_text= "RED WINS!!!"
        if winner_text!= "":
            draw_text= WINNER_FONT.render(winner_text, 1, "white")
            WINDOW.blit(draw_text, (WIDTH//2-100,HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(5000)


        key_pressed= pygame.key.get_pressed()
        movement_y(key_pressed, yellow)
        movement_r(key_pressed, red)
        handle_bullets(y_bullets, r_bullets, yellow, red)
        draw_window(red, yellow, r_bullets, y_bullets, r_health, y_health)

    main()
if __name__ == "__main__":
    main()