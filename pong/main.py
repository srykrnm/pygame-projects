import pygame
import os
import random

### INIT ###
pygame.init()

### CONSTANTS ###
WIDTH, HEIGHT = 1000, 600
FPS = 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load(os.path.join("Assets", "icon.jpg"))
pygame.display.set_icon(ICON)
pygame.display.set_caption("pong")
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bg.jpg")), (WIDTH, HEIGHT))
FONT = pygame.font.SysFont("OCR A Extended", 50)


### FUNCTIONS ###
def draw(left_paddle, right_paddle, ball, score):
    WIN.blit(BG, (0, 0))
    if score[1] == 10:
        left_paddle.y, right_paddle.y = 260, 260
        win_text = FONT.render(f"YOU WON", 1, "white")
        WIN.blit(win_text, (580, 260))
        score_text = FONT.render(f" {score[0]}  {score[1]}", 1, "white")
    elif score[0] == 10:
        left_paddle.y, right_paddle.y = 260, 260
        win_text = FONT.render(f"YOU WON", 1, "white")
        WIN.blit(win_text, (180, 260))
        score_text = FONT.render(f"{score[0]}  {score[1]}", 1, "white")
    else:
        score_text = FONT.render(f" {score[0]}  {score[1]}", 1, "white")
    WIN.blit(score_text, (410, -3))
    pygame.draw.rect(WIN, "white", left_paddle)
    pygame.draw.rect(WIN, "white", right_paddle)
    pygame.draw.rect(WIN, "blue", ball)       

    pygame.display.update()

def paddle_mov(left_paddle, right_paddle):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w] and left_paddle.y > 65:
        left_paddle.y -= 1
    if key_pressed[pygame.K_s] and left_paddle.y < 446:
        left_paddle.y += 1
    if key_pressed[pygame.K_o] and right_paddle.y > 65:
        right_paddle.y -= 1
    if key_pressed[pygame.K_k] and right_paddle.y < 446:
        right_paddle.y += 1

def ball_mov(left_paddle, right_paddle, ball, ball_direction, score):
    if ball.x == WIDTH//2 - 4 and ball.y == HEIGHT//2 - 13:
        pygame.time.delay(1000)
    ball.x += ball_direction[0]
    ball.y += ball_direction[1]
    if ball.y <= 65 or ball.y >= 500:
        ball_direction[1] = -ball_direction[1]
    if left_paddle.colliderect(ball) or right_paddle.colliderect(ball):
        if left_paddle.collidepoint(ball.midleft):
            ball_direction[0] = abs(ball_direction[0]) 
        elif left_paddle.collidepoint(ball.topleft) or left_paddle.collidepoint(ball.bottomleft):
            ball_direction[1] = -ball_direction[1]  
        if right_paddle.collidepoint(ball.midright):
            ball_direction[0] = -abs(ball_direction[0]) 
        elif right_paddle.collidepoint(ball.topright) or right_paddle.collidepoint(ball.bottomright):
            ball_direction[1] = -ball_direction[1] 
    if ball.x < 0 or ball.x > 1000:
        if ball.x < 0:
            score[1] += 1
        elif ball.x > 1000:
            score[0] += 1
        ball.x = WIDTH//2 - 4
        ball.y = HEIGHT//2 - 13
        ball_direction[0] = -ball_direction[0]

def main():
    is_running = True
    left_paddle = pygame.Rect(104, 260, 20, 70)
    right_paddle = pygame.Rect(WIDTH - 123, 260, 20, 70)
    ball = pygame.Rect(WIDTH//2 - 4, HEIGHT//2 - 13, 10, 10)
    blah = True
    clock = pygame.time.Clock()
    score = [0, 8]
    ball_direction = [random.choice([1, -1]),random.choice([1, -1])]
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
        if max(score) != 10:
            draw(left_paddle, right_paddle, ball, score)
            paddle_mov(left_paddle, right_paddle)
            ball_mov(left_paddle, right_paddle, ball, ball_direction, score)
        else:
            draw(left_paddle, right_paddle, ball, score)

    pygame.quit()

### MAIN ###
if __name__ == "__main__":
    main()

### END ###