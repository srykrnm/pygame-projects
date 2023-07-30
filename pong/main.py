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
START_BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "start_bg.jpg")), (WIDTH, HEIGHT))
FONT = pygame.font.Font("font/Pixeltype.ttf", 90)
FONT_1 = pygame.font.Font("font/Pixeltype.ttf", 50)


### FUNCTIONS ###
def draw(left_paddle, right_paddle, ball, score):
    WIN.blit(BG, (0, 0))
    score_text = FONT.render(f"{score[0]}     {score[1]}", 1, "white")
    score_rect = score_text.get_rect(center = (500, 35))
    WIN.blit(score_text, score_rect)
    pygame.draw.rect(WIN, "white", left_paddle)
    pygame.draw.rect(WIN, "white", right_paddle)
    pygame.draw.rect(WIN, "blue", ball)       
    pygame.display.update()

def start_draw(left_paddle, right_paddle, ball, score):
    WIN.blit(START_BG, (0, 0))
    score_text = FONT.render(f"PONG", 1, "white")
    score_rect = score_text.get_rect(center = (500, 35))
    slct_txt = FONT_1.render(f"ENTER A KEY", 1, "white")
    slct_rect = slct_txt.get_rect(center = (500, 200))
    a_txt = FONT_1.render(f"A : PLAY WITH A FRIEND OFFLINE", 1, "white")
    a_rect = slct_txt.get_rect(center = (350, 300))
    b_txt = FONT_1.render(f"B : PLAY WITH AI OFFLINE", 1, "white")
    b_rect = slct_txt.get_rect(center = (400, 400))
    WIN.blit(score_text, score_rect)
    WIN.blit(slct_txt, slct_rect)
    WIN.blit(a_txt, a_rect)
    WIN.blit(b_txt, b_rect)
    pygame.display.update()
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_a]:
        return True, False, None
    elif key_pressed[pygame.K_b]:
        return True, True, None
    else:
        return False, False, None




def left_paddle_mov(left_paddle):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w] and left_paddle.y > 65:
        left_paddle.y -= 1
    if key_pressed[pygame.K_s] and left_paddle.y < 446:
        left_paddle.y += 1

def right_paddle_mov(right_paddle):
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_o] and right_paddle.y > 65:
        right_paddle.y -= 1
    if key_pressed[pygame.K_k] and right_paddle.y < 446:
        right_paddle.y += 1

def ai_paddle_mov(paddle, ball):
    if ball.x < WIDTH // 2:
        if ball.y > paddle.y and paddle.y < 446:
            paddle.y += 1
        elif ball.y < paddle.y and paddle.y > 65:
            paddle.y -= 1
        else:
            pass

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
    ai = True
    side = None
    clock = pygame.time.Clock()
    score = [0, 0]
    game_started = False
    ball_direction = [random.choice([1, -1]),random.choice([1, -1])]
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                    break
        if game_started:
            if max(score) != 10:
                draw(left_paddle, right_paddle, ball, score)
                if ai:
                    right_paddle_mov(right_paddle)
                    ai_paddle_mov(left_paddle, ball)
                else:
                    right_paddle_mov(right_paddle)
                    left_paddle_mov(left_paddle)
                ball_mov(left_paddle, right_paddle, ball, ball_direction, score)
            else:
                draw(left_paddle, right_paddle, ball, score)
        else:
            game_started, ai, side = start_draw(left_paddle, right_paddle, ball, score)

    pygame.quit()

### MAIN ###
if __name__ == "__main__":
    main()

### END ###
