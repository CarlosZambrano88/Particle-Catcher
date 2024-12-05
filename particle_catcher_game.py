import pygame, sys
import random

class Particle():
    #initialize all the variables, objects and methods
    def __init__(self, pos=(0,0), size=15, life=10000):
        self.pos = pos
        self.size = size
        self.color = pygame.Color(random.randrange(50, 256), random.randrange(50, 256), random.randrange(50, 256))
        self.age = 0.0
        self.life = life 
        self.alpha = 255
        self.surface = self.update_surface()
        self.dead = False

    def update(self, dt):
        self.age += dt
        self.alpha = 255 * (1 - (self.age / self.life))
        if self.age > self.life:
            self.dead = True

    def update_surface(self):
        surf = pygame.Surface((self.size*.8, self.size*.8))
        surf.fill(self.color)
        return surf
    
    def draw(self, surface):
        if self.dead == True:
            pass
        self.surface.set_alpha(self.alpha)
        surface.blit(self.surface, self.pos)
        

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("GameBase")
resolution = (800, 600)
screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("arialBlack", 50)
font = pygame.font.SysFont(None, 30)
button_font = pygame.font.SysFont("Sans", 38)
score_font = pygame.font.SysFont("freesansbold.ttf", 50)

def draw_text(text, font, color, surface, x, y): 
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def main_menu():
    click = False
    while True:

        screen.fill((0,0,0))
        draw_text("Particle Catcher", title_font, (255, 255, 255), screen, 175, 20)

        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(300, 100, 200, 50)
        htp_button = pygame.Rect(300, 250, 200, 50)
        quit_button = pygame.Rect(300, 400, 200, 50)
        if play_button.collidepoint((mx, my)):
            if click:
                game()
        if htp_button.collidepoint((mx, my)):
            if click:
                how_to_play()
        if quit_button.collidepoint((mx, my)):
            if click:
                print("button 3")
                pygame.quit()
        pygame.draw.rect(screen, (255, 0, 0), play_button)
        pygame.draw.rect(screen, (255, 0, 0), htp_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        draw_text("Play", button_font, (255, 255, 255), screen, 360, 100)
        draw_text("How to Play", button_font, (255, 255, 255), screen, 298, 250)
        draw_text("Quit", button_font, (255, 255, 255), screen, 360, 400)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        mainClock.tick(60)

def render_board(squares, size):
    storage = []
    x = int((800 - (size[0] * squares[0])) / 2)
    y = int((800 - (size[1] * squares[1])) / 2)

    for a in range(squares[0]):
        for b in range(squares[1]):
            pygame.draw.rect(screen, (0, 0, 0), (x+(a*size[0]), y + (b*size[1]), size[0], size[1]), 1)
            storage.append((x+(a*size[0]), y + (b*size[1]), size[0], size[1]))
    return storage

def pre_time(counter):
    if counter > 9:
        return "0:"
    else:
        return "0:0"

def game():

    squares = (5, 5)
    size = (50, 50)
    storage = render_board(squares, size)
    reset = True
    running = True
    life = 3
    score = 0
    counter = 30 

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    life_text = font.render("Lives: " + str(life), True, (0, 0, 0))
    timer_text = font.render(pre_time(counter) + str(counter), True, (0, 0, 0))

    while running:
        clock.tick()
        mouse = pygame.mouse.get_pos()
        randint = random.randint(1, 3)
        if reset is True:
            number = random.randint(0, (squares[0] * squares[1]) - 1)
            target = (storage[number][0], storage[number][1])
            if randint == 1:
                color = (0, random.randrange(100,255), 0)
                click = "left"
            elif randint == 2:
                color = (random.randrange(100,255), 0, 0)
                click = "middle"
            else:
                color = (0, 0, random.randrange(100,255))
                click = "right"
            reset = False

        screen.fill((255, 255, 255))
        #draw_text("Game", font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == timer_event:
                counter = counter - 1
                timer_text = font.render(pre_time(counter) + str(counter), True, (0, 0, 0))

            if event.type == MOUSEBUTTONDOWN:
                if mouse[0] > target[0] and mouse[0] < target[0] + 40 and mouse[1] > target[1] and mouse[1] < target[1]+40:
                    if (event.button == 1 and click == "left"):
                        score = score + 1
                        score_text = font.render("Score " + str(score), True, (0, 0, 0))
                    elif (event.button == 2 and click == "middle"):
                        score = score + 1
                        score_text = font.render("Score " + str(score), True, (0, 0, 0))
                    elif (event.button == 3 and click == "right"):
                        score = score + 1
                        score_text = font.render("Score " + str(score), True, (0, 0, 0))
                    else:
                        life = life - 1
                        life_text = font.render("Lives: " + str(life), True, (0, 0, 0))
                    reset = True
            if life == 0 or counter == 0:
                lose_screen()
            if score == 30:
                win_screen()


        #particle.update(dt)
        #particle.draw(screen)
        pygame.draw.rect(screen, color, (target[0], target[1], size[0], size[1]))
        render_board(squares, size)
        screen.blit(score_text, (10, 10))
        screen.blit(life_text, (10, 40))
        screen.blit(timer_text, (10, 70))
        pygame.display.update()
        #dt = mainClock.tick(1)


def how_to_play():

    running = True
    while running:
        screen.fill((0,0,0))
        draw_text("How to play", title_font, (255, 255, 255), screen, 250, 20)
        draw_text("Click on the squares based on their corresponding colors!", font, (255, 255, 255), screen, 10, 150)
        draw_text("In order to win click on 30 squares correctly, but be careful!", font, (255, 255, 255), screen, 10, 180)
        draw_text("The squares will switch up on you, you get 3 lives, and watch the timer!", font, (255, 255, 255), screen, 10, 210)
        draw_text("Left Mouse Button - click green", font, (255, 255, 255), screen, 10, 300)
        draw_text("Middle Mouse Button - click red", font, (255, 255, 255), screen, 10, 330)
        draw_text("Right Mouse Button - click blue", font, (255, 255, 255), screen, 10, 360)
        draw_text("Press Escape to return to the main menu", font, (255, 255, 255), screen, 10, 550)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        

        pygame.display.update()
        mainClock.tick(60)

def lose_screen():
    running = True
    while running:
        screen.fill((0,0,0))

        draw_text("YOU LOSE", title_font, (255, 255, 255), screen, 250, 20)
        draw_text("Press Escape to return to the main menu", font, (255, 255, 255), screen, 10, 550)
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()

def win_screen():
    running = True
    while running:
        screen.fill((0,0,0))

        draw_text("YOU WIN", title_font, (255, 255, 255), screen, 250, 20)
        draw_text("Press Escape to return to the main menu", font, (255, 255, 255), screen, 10, 550)
        for event in pygame.event.get():
            if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()


main_menu()