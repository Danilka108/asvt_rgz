import pygame
from random import randint

class Upast(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.file = "Paint/fal/right/1.png"
        self.x = 300

        self.image = pygame.image.load(self.file).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, 350))

        self.vid = False
        self.anim, self.t = 1, 25

    def update(self, direction):
        self.t -= 1

        if self.t == 0:
            self.anim += 1
            self.t = 25

        if self.anim < 6:
            self.file = "Paint/fal/" + direction + "/" + str(self.anim) + ".png"
        if direction == "left":
            self.x = 300
        else:
            self.x = 650

        self.image = pygame.image.load(self.file).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, 350))

class Sound():
    def __init__(self):
        self.egg = pygame.mixer.Sound("Sound/egg.ogg")
        self.catch = pygame.mixer.Sound("Sound/catch.ogg")
        self.pas = pygame.mixer.Sound("Sound/pass.ogg")
        self.gameover = pygame.mixer.Sound("Sound/gameover.ogg")

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.file = ["Paint/score/0.png" for i in range(2)]
        self.s = [0 for i in range(2)]
        self.frame = 0

        self.image = [pygame.image.load(self.file[i]).convert_alpha() for i in range(2)]
        self.rect = [self.image[i].get_rect(center=(670 + 30 * i, 100)) for i in range(2)]

    def update(self):
        if self.frame < 0:
            self.s[1] = self.frame
        else:
            self.s[0] = self.frame // 10
            self.s[1] = self.frame % 10

        #print("s[0]=" + str(self.s[0]) + "; s[1]=" + str(self.s[1]))

        for i in range(2):
            self.file = ["Paint/score/" + str(self.s[i]) + ".png" for i in range(2)]

            self.image = [pygame.image.load(self.file[i]).convert_alpha() for i in range(2)]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.left, self.x = True, 430
        self.up, self.ay, self.engine = True, 0, 0

        self.file = 'Paint/player/left.png'
        self.arm_file = 'Paint/arm/left_up.png'

    def update(self):
        if self.left == True:
            self.file = 'Paint/player/left.png'
            self.x = 430

            if self.up == True:
                self.arm_file = 'Paint/arm/left_up.png'
                self.ay = 250
            else:
                self.arm_file = 'Paint/arm/left_down.png'
                self.ay = 300

            self.arm_image = pygame.image.load(self.arm_file).convert_alpha()
            self.arm_rect = self.arm_image.get_rect(center=(self.x - 80, self.ay))
        else:
            self.file = 'Paint/player/right.png'
            self.x = 560

            if self.up == True:
                self.arm_file = 'Paint/arm/right_up.png'
                self.ay = 250
            else:
                self.arm_file = 'Paint/arm/right_down.png'
                self.ay = 300

            self.arm_image = pygame.image.load(self.arm_file).convert_alpha()
            self.arm_rect = self.arm_image.get_rect(center=(self.x + 80, self.ay))

        if self.left and self.up:
            self.engine = 0
        elif self.left and not (self.up):
            self.engine = 1
        elif not (self.left) and self.up:
            self.engine = 2
        elif not (self.left) and not (self.up):
            self.engine = 3

        self.image = pygame.image.load(self.file).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, 300))

class Lose(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = [pygame.image.load("Paint/lose.png").convert_alpha() for i in range(3)]
        self.rect = [self.image[i].get_rect(center=(400 + 70 * i, 80))  for i in range(3)]

        self.prop = 0

        self.gameover = pygame.image.load("Paint/gameover.png").convert_alpha()
        self.gameover_rect = self.gameover.get_rect(center=(500, 130))

class Egg(pygame.sprite.Sprite):
    def __init__(self, nom):
        pygame.sprite.Sprite.__init__(self)

        self.file = "Paint/egg.png"

        self.x = [0 for i in range(5)]
        self.y = [0 for i in range(5)]

        self.vid = [False for i in range(5)]
        self.t, self.next = False, 0
        self.vid[0] = True

        for i in range(5):
            if nom == 1:
                self.x[i] = 191 + 10 + i * 25
                self.y[i] = 181 - 10 + i * 13
            elif nom == 2:
                self.x[i] = 181 + 10 + i * 25
                self.y[i] = 271 - 10 + i * 13
            elif nom == 3:
                self.x[i] = 811 - (10 + i * 25)
                self.y[i] = 185 - 10 + i * 13
            elif nom == 4:
                self.x[i] = 811 - (10 + i * 25)
                self.y[i] = 275 - 10 + i * 13

        self.image = [pygame.image.load(self.file).convert_alpha() for i in range(5)]
        if nom < 3:
            self.image = [pygame.transform.rotate(self.image[i], 30 * i) for i in range(5)]
        else:
            self.image = [pygame.transform.rotate(self.image[i], -30 * i) for i in range(5)]
        self.rect = [self.image[i].get_rect(center=(self.x[i], self.y[i])) for i in range(5)]

    def update(self):
        if self.t == True:
            self.vid[self.next] = False
            self.next += 1
            if self.next < 5:
                self.vid[self.next] = True

            self.t = False

pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 1000)

def pos(pos, xy):
    pos_x, pos_y = "", ""
    bool_x, bool_y = False, False

    for i in range(len(pos)):
        if pos[i] == "(" and xy == "x":
            bool_x = True
        elif bool_x == True and pos[i] != "," and xy == "x":
            pos_x += pos[i]
        elif pos[i] == "," and xy == "x":
            bool_x = False
        elif pos[i] == " " and xy == "y":
            bool_y = True
        elif bool_y == True and pos[i] != ")" and xy == "y":
            pos_y += pos[i]
        elif pos[i] == ")" and xy == "y":
            bool_y = False

    if xy == "x":
        return int(pos_x)
    elif xy == "y":
        return int(pos_y)

    print("xy should be 'x' or 'y'")
    return 0

width, height = 1000, 500
sc = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

fon = pygame.image.load("Paint/fon.png")

p = Player()
egg = [Egg(i + 1) for i in range(4)]
fal = randint(0, 3)
score = Score()
upast = Upast()
lose = Lose()
sound = Sound()

game = True
direction = "right"
over = False

while True:
    sc.blit(fon, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.USEREVENT:
            for i in range(4):
                if fal == i:
                    egg[i].t = True
                    if game:
                        sound.egg.play()

    pos_x = pos(str(pygame.mouse.get_pos()), "x")
    pos_y = pos(str(pygame.mouse.get_pos()), "y")

    if pos_x < 500:
        p.left = True
    else:
        p.left = False

    if pos_y < 250:
        p.up = True
    else:
        p.up = False

    if game:
        p.update()

    for i in range(4):
        if fal == i:
            if egg[i].next == 5:
                if fal == p.engine:
                    score.frame += 1
                    sound.catch.play()
                else:
                    upast.vid = True
                    game = False
                    sound.pas.play()

                    if fal > 1:
                        direction = "right"
                    else:
                        direction = "left"

                fal = randint(0, 3)
                egg[i].next = 0

            if game:
                egg[i].update()
            else:
                upast.update(direction)

    if not (game) and upast.anim == 6 and not (over):
        lose.prop += 1

        if lose.prop != 3:
            game = True
            upast.anim = 1
        else:
            over = True
            sound.gameover.play()

    score.update()

    sc.blit(p.image, p.rect)
    sc.blit(p.arm_image, p.arm_rect)

    for i in range(5):
        for j in range(4):
            if egg[j].vid[i] and fal == j:
                sc.blit(egg[j].image[i], egg[j].rect[i])

    for i in range(2):
        sc.blit(score.image[i], score.rect[i])

    if upast.vid and not (game):
        sc.blit(upast.image, upast.rect)

    for i in range(lose.prop):
        sc.blit(lose.image[i], lose.rect[i])
    if over == True:
        sc.blit(lose.gameover, lose.gameover_rect)

    pygame.display.flip()
    clock.tick(60)
