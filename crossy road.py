import pygame
import random
import os

pygame.init()

pygame.display.set_caption("EndToper's crossy road")
WHITE = (255,255,255)
BLACK = (0,0,0)
HEIGHT = 465
#кип(НЕ ТРОГАТЬ НЕ В КОИМ СЛУЧАЕ)
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
WIDTH = round(width/4*3)
print(WIDTH)
FPS = 60
g_speed = 1
screen = pygame.display.set_mode((WIDTH,HEIGHT))
run = True
m1,m2 =0,0
scores = 0
game_run =True
best_score = 0


image_adress = os.path.join('car_game_images','car.png')
my_image = pygame.image.load(image_adress).convert_alpha()

image_adress = os.path.join('car_game_images','mc.png')
mc_im = pygame.image.load(image_adress).convert_alpha()
GREEN =(0,255,0)

clock = pygame.time.Clock()


class car(pygame.sprite.Sprite):
    def __init__(self,x,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.x = x
        self.pos = pos
    def update(self,speed):
        y = 0
        if self.pos == 4:
            y = 45
        if self.pos == 3:
            y = 135
        if self.pos == 2:
            y = 255
        if self.pos == 1:
            y = 345
        screen.blit(my_image,(self.x,y))
        if self.pos == 2 or self.pos == 4:
            self.x = self.x+speed
        if self.pos == 1 or self.pos == 3:
            self.x = self.x-speed
        if self.x <= 0 or self.x >= WIDTH:
            self.pos = random.randint(1,4)
            if self.pos == 2 or self.pos == 4:
                self.x = 1
            if self.pos == 1 or self.pos == 3:
                self.x = WIDTH-1
        self.rect.x = self.x
        self.rect.y = y
        #столковения

class mc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.x = WIDTH/2
        self.y = 5
        
    def show(self):
        screen.blit(mc_im,(self.x,self.y))
    def motion(self,m1,m2):
        global scores
        if self.x+m1 < WIDTH-2 and self.x+m1 > 2:
            self.x = self.x + m1
        if self.y+m2 < HEIGHT-2 and self.y+m2 > 2:
            self.y = self.y + m2
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y >= HEIGHT - 15:
            scores = scores + 1
            self.y = 5
            harder(1)
            
def harder(num):
    global cars,g_speed
    if len(cars) <= 16:
        for i in range(num):
            x = random.randint(0,WIDTH)
            pos = random.randint(1,4)
            mashin = car(x,pos)
            cars.append(mashin)
            g_speed = g_speed + 0.1
    if len(cars) > 16:
        g_speed = g_speed + 0.1

mc1 = mc()
def game_map():
    # big save zone 1
    pygame.draw.line(screen, GREEN, [0, 22.5], [WIDTH, 22.5], 35)
    pygame.draw.line(screen, BLACK, [0, 2.5], [WIDTH, 2.5], 5)
    pygame.draw.line(screen, BLACK, [0, 42.5], [WIDTH, 42.5], 5)
    #big save zone 2
    pygame.draw.line(screen, BLACK, [0, 422.5], [WIDTH, 422.5], 5)
    pygame.draw.line(screen, GREEN, [0, 442.5], [WIDTH, 442.5], 35)
    pygame.draw.line(screen, BLACK, [0, 462.5], [WIDTH, 462.5], 5)
    #small save zone 3
    pygame.draw.line(screen, BLACK, [0, 127.5], [WIDTH, 127.5], 15)
    #small save zone 4
    pygame.draw.line(screen, BLACK, [0, 337.5], [WIDTH, 337.5], 15)
    # big save zone 5
    pygame.draw.line(screen, BLACK, [0, 212.5], [WIDTH, 212.5], 5)
    pygame.draw.line(screen, GREEN, [0, 232.5], [WIDTH, 232.5], 35)
    pygame.draw.line(screen, BLACK, [0, 252.5], [WIDTH, 252.5], 5)



cars=[]
for i in range(4):
    x = random.randint(0,WIDTH)
    pos = random.randint(1,4)
    mashin = car(x,pos)
    cars.append(mashin)


def game_reload():
    global game_run,cars,scores
    mc1.__init__()
    scores = 0
    game_run = True
    cars = []
    speed = 1
    for i in range(4):
        x = random.randint(0,WIDTH)
        pos = random.randint(1,4)
        mashin = car(x,pos)
        cars.append(mashin)
    
    
while run:
    if scores > best_score:
        best_score = scores
    for i in range(len(cars)):
        if cars[i].rect.colliderect(mc1.rect):
            game_run=False
    screen.fill(WHITE)
    clock.tick(FPS)
    game_map()
    for i in range(len(cars)):
        cars[i].update(g_speed)
    mc1.show()
    mc1.motion(m1,m2)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if i.type == pygame.KEYDOWN and game_run == True:
            if i.key == pygame.K_ESCAPE:
                run = False
            if i.key == pygame.K_a:
                m1 = m1 -1
                m2 = m2 + 0
            if i.key == pygame.K_s:
                m1 = m1 + 0
                m2 = m2 + 1
            if i.key == pygame.K_d:
                m1 = m1 + 1
                m2 = m2 + 0
            if i.key == pygame.K_w:
                m1 = m1 + 0
                m2 = m2 -1
        elif i.type == pygame.KEYUP and game_run == True:
            if i.key == pygame.K_a:
                m1 = 0
            if i.key == pygame.K_s:
                m2 = 0
            if i.key == pygame.K_d:
                m1 = 0
            if i.key == pygame.K_w:
                m2 = 0
        if i.type == pygame.MOUSEBUTTONDOWN and game_run == False:
            game_reload()
    if game_run == False:
        m1,m2 =0,0
        fontObj = pygame.font.Font('freesansbold.ttf', 25)
        textSurfaceObj = fontObj.render(f'Вы проиграли. Нажмите для рестарта. Ваш результат - {scores}. Ваш рекорд - {best_score}', False, BLACK, WHITE)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (WIDTH/2,HEIGHT/2)
        screen.blit(textSurfaceObj, textRectObj)
    #score
    fontObj = pygame.font.Font('freesansbold.ttf', 25)
    textSurfaceObj = fontObj.render(f'score - {scores}', False, WHITE, GREEN)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (100,20)

    screen.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()


pygame.quit()
