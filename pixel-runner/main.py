import pygame
import time
import random

# INIT 

pygame.init()

# CONSTANTS 

WIN = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
BG = pygame.image.load("graphics/Sky.png").convert()
GROUND = pygame.image.load("graphics/ground.png").convert()
FONT_1 = pygame.font.Font("font/Pixeltype.ttf", 50)
FONT_2 = pygame.font.Font("font/Pixeltype.ttf", 25)
BGM = pygame.mixer.Sound("audio/music.wav")
BGM.set_volume(0.5)
BGM.play(loops = -1)

# CHARACTERS

player_intro = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()

# USEREVENTS

obstacle_event = pygame.USEREVENT + 1

# TIMERS 

pygame.time.set_timer(obstacle_event, 3000)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk = [pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha(),  pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()]
        self.player_jump =   pygame.image.load("graphics/Player/jump.png").convert_alpha()
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
    def take_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity 
        if self.rect.bottom > 300:
            self.rect.bottom = 300
            self.gravity = 0
    def animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image =  self.player_walk[int(self.player_index)]
        pass
    def update(self):
        self.take_input()
        self.apply_gravity()
        self.animation()

    def obstacle_mech(obstacle_rect_list, obs_vel):
        for i in obstacle_rect_list:
            if i.right < 0:
                obstacle_rect_list.remove(i)
            else:
                i.x -= obs_vel


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            self.frames = [pygame.image.load("graphics/Fly/Fly2.png").convert_alpha(),  pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()]
            y_pos = 210
        elif type == "snail":
            self.frames = [pygame.image.load("graphics/snail/snail1.png").convert_alpha(),  pygame.image.load("graphics/snail/snail2.png").convert_alpha()]
            y_pos = 300

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(800, 1500), y_pos))
        self.vel = 6

    def animation(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image =  self.frames[int(self.frame_index)]

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.animation()
        self.rect.x -= self.vel
        self.destroy()

player_sprite = pygame.sprite.GroupSingle()
player_sprite.add(Player())

obstacle_sprite = pygame.sprite.Group()


# FUNCTIONS 

def welcome_screen(player_intro_rect, time_elapsed):
    WIN.blit(BG, (0,0))
    WIN.blit(GROUND, (0, 300))
    WIN.blit(player_intro, player_intro_rect)
    wm_text = FONT_1.render(f"SPACE: START / ESC: EXIT",False,"#646464")
    wm_rect = wm_text.get_rect(midtop = (400, 365))
    wm_rect.inflate_ip(10 * 2, 10 * 2)
    wm_intro = FONT_1.render(f"PIXEL RUNNER",False,"#646464")
    wm_intro_rect = wm_intro.get_rect(midtop = (400, 30))
    pygame.draw.rect(WIN, "#C0E8EC", wm_intro_rect)
    if time_elapsed != 0:
        pre_score = FONT_2.render(f"PREVIOUS SCORE: {time_elapsed}",False,"#646464")
        pre_score_rect = pre_score.get_rect(midtop = (400, 70))
        WIN.blit(pre_score, pre_score_rect)
    WIN.blit(wm_intro, wm_intro_rect)
    pygame.draw.rect(WIN, "#646464", wm_rect, 2, 5)
    WIN.blit(wm_text, wm_rect.inflate(-20, -30))
    pygame.display.update()

def background():
    WIN.blit(BG, (0,0))
    WIN.blit(GROUND, (0, 300))           

def collision():
    if pygame.sprite.spritecollide(player_sprite.sprite, obstacle_sprite, False):
        obstacle_sprite.empty()
        return False
    else:
        return True

def draw (time_elapsed):
    pre_score = FONT_1.render(f"SCORE: {time_elapsed}",False,"#646464")
    pre_score_rect = pre_score.get_rect(midtop = (400, 30))
    WIN.blit(pre_score, pre_score_rect)
    pygame.display.flip()
 

def main():
    clock = pygame.time.Clock()
    run = True
    game_active = False
    player_intro_rect = player_intro.get_rect(midbottom = (100, 300))
    obstacle_sprite.add(Obstacle("snail"))
    start_time = time.time()
    pre_frame_time = time.time()
    time_elapsed = 0
    while run:
        clock.tick(60)
        dt = time.time() - pre_frame_time
        pre_frame_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_active:
                if event.type == obstacle_event:
                    prob = ["fly", "snail", "snail", "snail"]
                    obstacle_sprite.add(Obstacle(random.choice(prob)))
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        start_time = time.time()
                    elif event.key == pygame.K_ESCAPE:
                        run = False

        if game_active:
            time_elapsed = int(time.time() - start_time)
            background()
            player_sprite.update()
            player_sprite.draw(WIN)
            obstacle_sprite.update()
            obstacle_sprite.draw(WIN)
            game_active = collision()
            draw(time_elapsed)
        else:
            if time_elapsed != 0 :
                pygame.time.delay(1000)
            welcome_screen(player_intro_rect, time_elapsed)
    pygame.quit()

# MAIN 

if __name__ == "__main__":
    main()

# END
