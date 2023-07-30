import pygame
import random
import sys
from pygame.math import Vector2
import os

### INIT ###
pygame.init()

### CONSTANTS ###
CELL_NUMBER = 20
CELL_SIZE = 30
WIN = pygame.display.set_mode((CELL_NUMBER*CELL_SIZE,CELL_NUMBER*CELL_SIZE))
pygame.display.set_caption("snake")
FPS = 10
APPLE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "apple.png")), (CELL_SIZE, CELL_SIZE))
MUNCH = pygame.mixer.Sound(os.path.join("Assets", "sound_crunch.wav"))
MUNCH.set_volume(0.2)

HEAD_L = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "head_left.png")),  (CELL_SIZE, CELL_SIZE))
HEAD_R = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "head_right.png")),  (CELL_SIZE, CELL_SIZE))
HEAD_U = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "head_up.png")),  (CELL_SIZE, CELL_SIZE))
HEAD_D = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "head_down.png")),  (CELL_SIZE, CELL_SIZE))

TAIL_U =pygame.transform.scale(pygame.image.load(os.path.join("Assets", "tail_up.png")),  (CELL_SIZE, CELL_SIZE)) 
TAIL_R =pygame.transform.scale(pygame.image.load(os.path.join("Assets", "tail_right.png")),  (CELL_SIZE, CELL_SIZE))
TAIL_L =pygame.transform.scale(pygame.image.load(os.path.join("Assets", "tail_left.png")),  (CELL_SIZE, CELL_SIZE))
TAIL_D =pygame.transform.scale(pygame.image.load(os.path.join("Assets", "tail_down.png")),  (CELL_SIZE, CELL_SIZE))

BODY_H = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "block.png")),  (CELL_SIZE, CELL_SIZE))
BODY_V = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "block_v.png")),  (CELL_SIZE, CELL_SIZE))

TL = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "body_tl.png")),  (CELL_SIZE, CELL_SIZE))
TR = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "body_tr.png")),  (CELL_SIZE, CELL_SIZE))
BL = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "body_bl.png")),  (CELL_SIZE, CELL_SIZE))
BR = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "body_br.png")),  (CELL_SIZE, CELL_SIZE))

BG = (175,215,70)
GRASS_PATCH = (167, 209, 61)

FONT = pygame.font.SysFont("verdana", 20)

### FUNCTIONS ###
def draw_grass():
    WIN.fill(BG)
    for i in range(CELL_NUMBER):
        if i % 2 == 0:
            for j in range(CELL_NUMBER):
                if j % 2 == 0:
                    grass_block = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(WIN, GRASS_PATCH, grass_block)
        else:
            for j in range(CELL_NUMBER):
                if j % 2 != 0:
                    grass_block = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(WIN, GRASS_PATCH, grass_block)

def snake_logic(snake_body, direction):
    for index, block in enumerate(snake_body):
        snake_block = pygame.Rect(int(block.x * CELL_SIZE),int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        if index == 0:
            head_relation = snake_body[0] - snake_body[1]
            if head_relation == Vector2(0,-1): head = HEAD_U
            elif head_relation == Vector2(0, 1): head = HEAD_D
            elif head_relation == Vector2(1, 0): head = HEAD_R
            else: head = HEAD_L
            WIN.blit(head, snake_block)
        elif index == len(snake_body) - 1:
            tail_relation = snake_body[-1] - snake_body[-2]
            if tail_relation == Vector2(0,-1): tail = TAIL_D
            elif tail_relation == Vector2(0, 1): tail = TAIL_U
            elif tail_relation == Vector2(1, 0): tail = TAIL_L
            else: tail = TAIL_R
            WIN.blit(tail, snake_block)
        else:
            pre_block = snake_body[index + 1] - block
            nxt_block = snake_body[index - 1] - block
            if pre_block.x == nxt_block.x:
                body = BODY_V
            elif pre_block.y == nxt_block.y:
                body = BODY_H
            else:
                if pre_block.x == -1 and nxt_block.y == -1 or pre_block.y == -1 and nxt_block.x == -1: 
                    body = TL
                elif pre_block.x == -1 and nxt_block.y == 1 or pre_block.y == 1 and nxt_block.x == -1: 
                    body = BL
                elif pre_block.x == 1 and nxt_block.y == -1 or pre_block.y == -1 and nxt_block.x == 1: 
                    body = TR
                elif pre_block.x == 1 and nxt_block.y == 1 or pre_block.y == 1 and nxt_block.x == 1: 
                    body = BR
            WIN.blit(body, snake_block)
    head = snake_body[0]
    snake_body.pop()
    snake_body.insert(0, head + direction )

def food_logic(food_list, snake_body):
    if len(food_list) == 1:
        food = pygame.Rect(int(food_list[0].x * CELL_SIZE), int(food_list[0].y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        WIN.blit(APPLE, food)
    elif len(food_list) == 0:
        while True:
            succ_flag = 0
            for i in snake_body:
                food_chunk = Vector2(random.randint(0,CELL_NUMBER - 1), random.randint(0,CELL_NUMBER - 1))
                new_food = pygame.Rect(int(food_chunk.x * CELL_SIZE), int(food_chunk.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
                body_chunk = pygame.Rect(int(i.x * CELL_SIZE), int(i.y * CELL_SIZE), CELL_SIZE, CELL_SIZE) 
                if new_food.colliderect(body_chunk):
                    pass
                else:
                    succ_flag += 1
            print(succ_flag, len(snake_body))
            if succ_flag == len(snake_body):
                food_list.append(food_chunk)
                break
            else:
                pass

def collision_logic(food_list, snake_body, score, game_over):
    food = pygame.Rect(int(food_list[0].x * CELL_SIZE), int(food_list[0].y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
    head = pygame.Rect(int(snake_body[0].x * CELL_SIZE), int(snake_body[0].y * CELL_SIZE), CELL_SIZE, CELL_SIZE) 
    tail = snake_body[-1]
    if food.colliderect(head):
        MUNCH.play()
        food_list.pop()
        snake_body.append(tail)
        score[0] += 1
    for i in snake_body[1:]:
        block = pygame.Rect(int(i.x * CELL_SIZE),int(i.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        if head.colliderect(block):
            game_over[0] = True
    head_x = head.x//CELL_SIZE
    head_y = head.y//CELL_SIZE
    if head_x >= CELL_NUMBER or head_x < 0 or head_y >= CELL_NUMBER or head_y < 0:
        game_over[0] = True

def draw_score(snake_body):
    WIN.blit(APPLE, (10, 10))
    score = len(snake_body) - 3
    score_text = FONT.render(f"{score}", 1, "black")
    WIN.blit(score_text, (40, 15))

def update():
    pygame.display.update()

def main():
    is_running = True
    clock = pygame.time.Clock()
    snake_body = [Vector2(4,10),Vector2(3,10),Vector2(2,10)]
    score = [0]
    direction = [1, 0]
    food_list = []
    game_over = [False]
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != [0, 1]:
                    direction = [0, -1]
                if event.key == pygame.K_LEFT and direction != [1, 0]:
                    direction = [-1, 0]
                if event.key == pygame.K_RIGHT and direction != [-1, 0]:
                    direction = [1, 0]
                if event.key == pygame.K_DOWN and direction != [0, -1]:
                    direction = [0, 1]

        if game_over[0] == False:
            draw_grass()
            snake_logic(snake_body, direction)
            food_logic(food_list, snake_body)
            collision_logic(food_list, snake_body, score, game_over)
            draw_score(snake_body)
        update()


### MAIN ###
if __name__ == "__main__":
    main()

### END ###