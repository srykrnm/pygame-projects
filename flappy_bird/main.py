### IMPORTS ###

import pygame
import datetime
import os
import random

### INIT & CONSTANTS ###

pygame.init()
HIT_WAV = pygame.mixer.Sound("audio/hit.wav")
POINT_WAV = pygame.mixer.Sound("audio/point.wav")
WING_WAV = pygame.mixer.Sound("audio/wing.wav")
CURR_HR = datetime.datetime.now().hour
WIDTH, HEIGHT = 400, 600
FPS = 60
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Flappy Bird")
START_PNG = pygame.transform.scale2x(pygame.image.load("sprites/start.png"))
FLPY_BRD = pygame.image.load("sprites/flappy_bird.png")
TAP =   pygame.transform.scale(pygame.image.load("sprites/tap.png").convert_alpha(), (150, 150))
ICON = pygame.image.load("favicon.ico")
if CURR_HR > 18:
    BG = pygame.transform.scale(pygame.image.load("sprites/background-night.png"), (WIDTH, HEIGHT))
    PIPE = pygame.image.load("sprites/pipe-red.png")
else:
    BG = pygame.transform.scale(pygame.image.load("sprites/background-day.png"), (WIDTH, HEIGHT))
    PIPE = pygame.image.load("sprites/pipe-green.png")
GROUND = pygame.transform.scale(pygame.image.load("sprites/base.png"), (WIDTH, 100))
pygame.display.set_icon(ICON)
SPAWN_PIPE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE_EVENT, 1000)
SCROLL_SPEED = 4

### CLASSES ###

class Pipe(pygame.sprite.Sprite):
    def __init__(self, pos, orientation):
        super().__init__()
        if orientation == "up":
            self.image = PIPE
            self.rect = self.image.get_rect(midbottom = pos)
        elif orientation == "down":
            self.image = pygame.transform.flip(PIPE, False, True)
            self.rect = self.image.get_rect(midtop = pos)
    def destroy(self):
        if self.rect.right < 0:
            self.kill()
    def update(self):
        self.rect.x -= SCROLL_SPEED
        self.destroy()
    def draw(self, win):
        win.blit(self.image, self.rect)

class Birdy(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.frames = self.get_frames(random.choice(["bluebird", "redbird", "yellowbird"]))
        self.frame_index= 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.hit_ground = False
        self.up_dn_num = 2
        self.tilt = 0
        self.up_dn_lim = 0

    def animate(self):
        self.frame_index += 0.1
        if int(self.frame_index) >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        self.frame_index += 0.1
        if int(self.frame_index) >= len(self.frames):
            self.frame_index = 0
        if self.direction.y < 0:
            self.tilt = 20 
        else:
            self.tilt -= 2 
        if self.tilt < -90:
            self.tilt = -90
        elif self.tilt > 30:
            self.tilt = 30
        self.image = pygame.transform.rotate(self.frames[int(self.frame_index)], self.tilt)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_frames(self, bird_color):
        frames = []
        for frame in os.listdir("sprites"):
            if frame.split("-")[0] == bird_color:
                new_frame = pygame.transform.scale(pygame.image.load(os.path.join("sprites", frame)).convert_alpha(), (50, 40))
                frames.append(new_frame)
        return frames

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def after_landing(self):
        self.rect.x -= SCROLL_SPEED

    def flap(self):
        self.direction.y = -12

    def up_down(self):
        self.rect.y += self.up_dn_num
        self.up_dn_lim += self.up_dn_num
        if self.up_dn_lim > 5:
            self.up_dn_num = -1
        if self.up_dn_lim < -5:
            self.up_dn_num = 1

    def update(self):
        if self.gravity == 0 and not self.hit_ground:
            self.up_down()
            self.animate()
        else:
            if not self.hit_ground:
                self.rotate()
            self.apply_gravity()
        if self.hit_ground:
            self.after_landing()

class Ground(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH * 2, 100))
        self.image.blit(GROUND, (0, 0))
        self.image.blit(GROUND, (WIDTH, 0))
        self.rect = self.image.get_rect(topleft = (0, HEIGHT - 100))
        self.mask = pygame.mask.from_surface(self.image)

    def scroll_ground(self):
        if self.rect.centerx == WIDTH // 2:
            self.rect.x = 0
        else:
            self.rect.x -= SCROLL_SPEED

    def update(self):
        self.scroll_ground()

class Score(pygame.sprite.Sprite):

    def __init__(self, birdy, pipes):
        super().__init__()
        self.birdy_grp = birdy
        self.pipes_grp = pipes
        self.score = 0
        self.frames = self.get_frames()
        self.image = self.frames["0"]
        self.rect = self.image.get_rect(center = (WIDTH // 2 , 50))
        self.start_counting = False

    def update(self):
        if self.start_counting:
            self.score += 0.1
        if int(self.score) in [100, 1000, 1000, 10000]:
            POINT_WAV.play()
        score_str = str(int(self.score))
        self.image = self.combine_images(score_str)
        self.rect = self.image.get_rect(center = (WIDTH // 2 , 50))

    def combine_images(self, score_str):
        digit_width = 30 
        digit_height = 40 
        total_width = len(score_str) * digit_width 
        combined_image = pygame.Surface((total_width, digit_height), pygame.SRCALPHA) 
        x_offset = 0 
        for digit_char in score_str:
            digit_image = self.frames[digit_char] 
            combined_image.blit(digit_image, (x_offset, 0)) 
            x_offset += digit_width
        return combined_image
        
    def get_frames(self):
        frames = {}
        for frame in os.listdir("sprites"):
            if (frame.split(".")[0]).isdigit():
                new_frame = pygame.transform.scale(pygame.image.load(os.path.join("sprites", frame)).convert_alpha(), (30, 40))
                frames[frame.split(".")[0]] = new_frame
        return frames

### VVI FN ###

def draw(ground, birdy, score, pipes):
    WIN.blit(BG, (0, 0))
    pipes.draw(WIN)
    ground.draw(WIN)
    birdy.draw(WIN)
    score.draw(WIN)
    if not birdy.sprite.hit_ground and birdy.sprite.gravity == 0:
        tap_rect = TAP.get_rect(center = (WIDTH // 2, HEIGHT - 200))
        WIN.blit(TAP, tap_rect)
        pygame.display.update()
        return True
    pygame.display.update()

    return False

def collisions(ground, birdy, pipes, score):
    if pygame.sprite.collide_rect(birdy.sprite, ground.sprite):
        birdy.sprite.gravity = 0
        birdy.sprite.rect.bottom = ground.sprite.rect.top
        birdy.sprite.direction.y = 0
        birdy.sprite.hit_ground = True
        score.sprite.start_counting = False
        if not pygame.mixer.get_busy():
            HIT_WAV.play()
    if pygame.sprite.spritecollide(birdy.sprite, pipes, False):
        birdy.sprite.hit_ground = True
        if birdy.sprite.gravity == 0:
            birdy.sprite.gravity = 0.8
        if not pygame.mixer.get_busy():
            HIT_WAV.play()
        score.sprite.start_counting = False




def start_(ground, birdy, score, pipes):
    WIN.blit(BG, (0, 0))
    ground.draw(WIN)
    birdy.draw(WIN)
    flpy_rect = FLPY_BRD.get_rect(center = (WIDTH // 2, 60))
    start_rect = START_PNG.get_rect(center = (WIDTH // 2, HEIGHT // 2 + 100))
    WIN.blit(FLPY_BRD, flpy_rect)
    WIN.blit(START_PNG, start_rect)
    pygame.display.update()
    key_pressed = pygame.key.get_pressed()
    button_pressed = pygame.mouse.get_pressed()
    if key_pressed[pygame.K_SPACE] or button_pressed[0]:
        birdy.sprite.gravity = 0
        score.sprite.score = 0
        pipes.empty()
        birdy.sprite.rect.center = (WIDTH // 2, HEIGHT // 2 - 50)
        birdy.sprite.direction = pygame.math.Vector2(0, 0)
        return False
    else:
        return True

def spawn_pipes(pipes):
    height = PIPE.get_height()
    x = WIDTH
    while True:
        y_1, y_2 =  random.randint(-300, 0), random.randint(HEIGHT - 100, HEIGHT + 200)
        up_height = (height - (y_2 - (HEIGHT - 100)))
        down_height = (height + y_1)
        gap = HEIGHT - (up_height + down_height)
        if gap >= 250 and gap <= 300:
            break
    pipes.add(Pipe((x, y_1), "down"))
    pipes.add(Pipe((x, y_2), "up"))


def main():
    clock = pygame.time.Clock()
    ground = pygame.sprite.GroupSingle()
    ground.add(Ground())
    birdy = pygame.sprite.GroupSingle()
    birdy.add(Birdy((WIDTH // 2, HEIGHT // 2 - 50)))
    pipes = pygame.sprite.Group()
    score = pygame.sprite.GroupSingle()
    score.add(Score(birdy, pipes))
    tap_visible = False
    game_is_on = True
    game_ended = True
    while game_is_on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_is_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_is_on = False
            if not game_ended and not birdy.sprite.hit_ground:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        birdy.sprite.flap()
                        WING_WAV.play()
                        birdy.sprite.gravity = 0.8
                        score.sprite.start_counting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        birdy.sprite.flap()
                        WING_WAV.play()
                        birdy.sprite.gravity = 0.8
                        score.sprite.start_counting = True
            if event.type == SPAWN_PIPE_EVENT and not game_ended and not tap_visible:
                spawn_pipes(pipes)

        ground.update()
        birdy.update()
        pipes.update()
        score.update()
        if birdy.sprite.rect.right < 0:
            birdy.sprite.kill()
            birdy.add(Birdy((WIDTH // 2, HEIGHT // 2 - 50)))
            game_ended = True

        if game_ended:
            game_ended = start_(ground, birdy, score, pipes)
        else:
            collisions(ground, birdy, pipes, score)
            tap_visible = draw(ground, birdy, score, pipes)
 
    pygame.quit()

### MAIN ###

if __name__ == "__main__":
    main()

### END ###

