import pygame
import os

### INIT ###
pygame.init()
pygame.mixer.init()

### SOUNDS ###
send_hit = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")
recieved_hit = pygame.mixer.Sound("Assets/Grenade+1.mp3")
bgm = pygame.mixer.music.load("Assets/Interstellar+Odyssey.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

### GAME-SETTINGS ###
FPS = 400
MAX_BULLETS = 5

### WINDOW ###
WIDTH, HEIGHT = 1000, 600
pygame.display.set_caption("my game")

### COLORS ###
WHITE = (255, 255, 255)  
RED_COL = (255, 0, 0)  
YELLOW_COL = (255, 255, 0)  
BLACK = (0, 0, 0)  

### VISUAL OBJECTS ###
YELLOW_SPACESHIP = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "game-over.png")), (400, 250))
TROPHY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "trophy.png")), (30, 30))
L_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "left-arrow.png")), (40, 40))
R_ARROW = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "right-arrow.png")), (40, 40))
RED_SPACESHIP = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bg1.jpg")), (WIDTH, HEIGHT))
SP_DIM = (55, 40) 
YELLOW = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP, SP_DIM), 90)
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2
RED = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP, SP_DIM), 270)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 8, HEIGHT)

### FUNCTIONS ###
def display_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health , winner):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(RED, (red.x, red.y))
    WIN.blit(YELLOW, (yellow.x, yellow.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED_COL, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW_COL, bullet)
    draw_health_bar(red_health, 10, 30, 25, 150, 30)
    draw_health_bar(yellow_health, 10, 820, 25, 150, 30, reverse = True)
    disp_winner(winner)
    pygame.display.update()

def disp_winner(winner):
    WIN.blit(TROPHY, (485, 25))
    if winner != "":
        if winner == "red":
            WIN.blit(L_ARROW, (400, 20))
            pass
        elif winner == "yellow":
            WIN.blit(R_ARROW, (550, 20))
            pass
        WIN.blit(GAME_OVER, (300, 180))

def red_mov (keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x > 10:
        red.x -=1
    if keys_pressed[pygame.K_d] and red.x < WIDTH//2 - 47:
        red.x +=1
    if keys_pressed[pygame.K_s] and red.y < 535:
        red.y +=1     
    if keys_pressed[pygame.K_w] and red.y > 81:
        red.y -=1

def yellow_mov (keys_pressed, yellow):
    if keys_pressed[pygame.K_RIGHT] and yellow.x < WIDTH - 48:
        yellow.x +=1
    if keys_pressed[pygame.K_LEFT] and yellow.x > WIDTH//2 + 5:
        yellow.x -=1
    if keys_pressed[pygame.K_UP] and yellow.y > 81:
        yellow.y -=1     
    if keys_pressed[pygame.K_DOWN] and yellow.y < 535:
        yellow.y +=1

def bullets_mov(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x +=1
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            recieved_hit.play()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x > WIDTH - 20:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x -=1
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            recieved_hit.play()
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x < 10:
            yellow_bullets.remove(bullet)

def draw_health_bar(current_health, max_health, x, y, width, height, reverse=False):
    health_ratio = current_health / max_health
    fill_width = health_ratio * width
    if reverse:
        fill_rect = pygame.Rect(x + width - fill_width, y, fill_width, height)
    else:
        fill_rect = pygame.Rect(x, y, fill_width, height)
    outline_rect = pygame.Rect(x, y, width, height)
    border_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
    pygame.draw.rect(WIN, (105, 105, 105), border_rect)
    pygame.draw.rect(WIN, (255, 0, 0), outline_rect)
    pygame.draw.rect(WIN, (0, 255, 0), fill_rect)

def main():
    winner = ""
    red = pygame.Rect(200, 270, SP_DIM[0], SP_DIM[1])
    yellow = pygame.Rect(750, 270, SP_DIM[0], SP_DIM[1])
    clock = pygame.time.Clock()
    health = {"red": 10, "yellow": 10}
    bullets = {"red": [], "yellow": []}
    is_running = True
    while is_running:
        clock.tick(300)
        if health["red"] == 0 or health["yellow"] == 0:
            for i,j in health.items():
                if j != 0:
                    winner = i
                    break 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN and winner == "":
                if event.key == pygame.K_LCTRL and len(bullets["red"]) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    bullets["red"].append(bullet)
                    send_hit.play()
                if event.key == pygame.K_RCTRL and len(bullets["yellow"]) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    bullets["yellow"].append(bullet)
                    send_hit.play()
            if event.type == RED_HIT:
                health["red"]-=1
            if event.type == YELLOW_HIT : 
                health["yellow"]-=1
        keys_pressed = pygame.key.get_pressed()
        red_mov(keys_pressed, red)
        yellow_mov(keys_pressed, yellow)
        bullets_mov(bullets["red"], bullets["yellow"], red, yellow)
        display_window(red, yellow, bullets["red"], bullets["yellow"], health["red"], health["yellow"], winner)        

### MAIN ###

if __name__ == "__main__":
    main()

### END ###
