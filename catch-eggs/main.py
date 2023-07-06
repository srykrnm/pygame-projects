import pygame
import time
import random
import os

### INIT ###
pygame.init()

### Sounds ###
fall = pygame.mixer.Sound("Assets/fall.wav")
bgm = pygame.mixer.music.load("Assets/bgm.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

### CONSTANTS ###
WIDTH, HEIGHT  = 1000, 600 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 400
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "farm.jpg")), (WIDTH, HEIGHT))
BASKET = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "basket.png")), (100, 100) )
WH_HIT = pygame.USEREVENT + 1
BR_HIT = pygame.USEREVENT + 2
END_SIG = pygame.USEREVENT + 3
WH_EGG =  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "wh_egg.png")), (50, 50) )
SCORE =  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "score.png")), (100, 50) )
TIME =  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "time.png")), (50, 50) )
HEART =  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "heart.png")), (40, 40) )
BR_EGG =  pygame.transform.scale(pygame.image.load(os.path.join("Assets", "br_egg.png")), (100, 80) )
FONT = pygame.font.SysFont("comicsans", 20)
GAME_OVER = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "game-over.png")), (350, 200))


### FUNCTIONS ###
def draw(basket, eggs, elapsed_time, score, health):
    WIN.blit(BG, (0, 0))
    WIN.blit(TIME, (30, 10))
    time_text = FONT.render(f"{round(elapsed_time)}s", 1, "black")
    WIN.blit(SCORE, (8, 55))
    score_text = FONT.render(f"{round(score)}", 1, "black")
    WIN.blit(HEART, (35, 115))
    health_text = FONT.render(f"{round(health)}", 1, "black")
    WIN.blit(time_text, (110, 20))
    WIN.blit(score_text, (110, 70))
    WIN.blit(health_text, (112, 120))
    WIN.blit(BASKET, (basket.x, basket.y))
    for egg in eggs["white"]:
       WIN.blit(WH_EGG, (egg.x, egg.y)) 
    for egg in eggs["brown"]:
       WIN.blit(BR_EGG, (egg.x, egg.y))
    if health == 0:
        WIN.blit(GAME_OVER, (320, 180))
    pygame.display.update()

def move_basket(key_pressed, basket):
    if key_pressed[pygame.K_LEFT] and basket.x > 0: 
        basket.x -= 2
    elif key_pressed[pygame.K_RIGHT] and basket.x < WIDTH - 100: 
        basket.x += 2

def move_egg(eggs, basket):
    for egg in eggs["white"]:
        egg.y += 1
        if basket.colliderect(egg):
            fall.play()
            eggs["white"].remove(egg)
            pygame.event.post(pygame.event.Event(WH_HIT))
        elif egg.y > HEIGHT:
            eggs["white"].remove(egg)
            pygame.event.post(pygame.event.Event(END_SIG))

    for egg in eggs["brown"]:
        egg.y += 1
        if basket.colliderect(egg):
            fall.play()
            eggs["brown"].remove(egg)
            pygame.event.post(pygame.event.Event(BR_HIT))
        elif egg.y > HEIGHT:
            eggs["brown"].remove(egg)
            pygame.event.post(pygame.event.Event(END_SIG))

def main():
    is_running = True
    basket = pygame.Rect(WIDTH//2, HEIGHT - 100, 50, 50)
    score = 0
    eggs = {"white": [], "brown": []}
    start_time = time.time()
    elapsed_time = 0
    clock = pygame.time.Clock()
    health = 5
    time_list = []
    done_list = []

    while is_running:
        clock.tick(FPS)
        if elapsed_time not in time_list:
            time_list.append(elapsed_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
            if event.type == WH_HIT:
                score+= 1
            if event.type == BR_HIT:
                score+= 2
            if event.type == END_SIG:
                health -=1
        if health == 0:
            draw(basket, eggs, elapsed_time, score, health)
        else:
            elapsed_time = round(time.time() - start_time)
            if time_list[-1] % random.randint(1, 4) == 0  and time_list[-1] not in done_list:
                egg = pygame.Rect(random.randint(120, WIDTH - 100), random.randint(-1000, -100), 50, 50)
                eggs[random.choice(["white","brown"])].append(egg)
                done_list.append(time_list[-1])
            key_pressed = pygame.key.get_pressed()
            move_basket(key_pressed, basket)
            move_egg(eggs, basket)
            draw(basket, eggs, elapsed_time, score, health)

    pygame.quit()

### MAIN ###
if __name__ == "__main__":
    main()

### END ###