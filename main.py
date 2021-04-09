import pygame
import time
import random
from pygame.locals import *

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        #super().__init__()
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x,self.y))
        pygame.display.flip()
    
    def move(self):
        self.x = SIZE*random.randint(1,24)
        self.y = SIZE*random.randint(1,19)

class Snake:
    def __init__(self,parent_screen,length):
        #super().__init__()
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        #self.parent_screen.fill((0,255,255))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i],self.y[i]))
        pygame.display.flip()

    def move_down(self):
        self.direction = 'down'
    
    def move_up(self):
        self.direction = 'up'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'
    
    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0]-=SIZE
        if self.direction == 'down':
            self.y[0]+=SIZE
        if self.direction == 'left':
            self.x[0]-=SIZE
        if self.direction == 'right':
            self.x[0]+=SIZE
        self.draw()

class Game:
    def __init__(self):
        #super().__init__()
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000,800))
        self.surface.fill((0,255,255,))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.t = 0.3
        
    def iscollision(self, x1,y1,x2,y2):
        if(x1 >= x2 and x1< x2 + SIZE):
            if(y1 >= y2 and y1< y2 + SIZE):
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/bgm.mp3")
        pygame.mixer.music.play()

    def play_sound(self, get_sound):
        print(get_sound)
        sound = pygame.mixer.Sound(f"resources/{get_sound}.mp3")
        pygame.mixer.Sound.play(sound)
        print("All OK")

    def render_bg(self):
        bg = pygame.image.load("resources/bg1.jpg")
        self.surface.blit(bg, (0,0))
        pygame.display.flip()

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.iscollision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
            self.t-=0.03
            if self.t<=0.1:
                self.t = 0.1
            #print("collision!")
        
        for i in range(3,self.snake.length):
            if self.iscollision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                #print("GAME OVER")
                raise "game over"
        
        if self.snake.x[0]<0 or self.snake.y[0]<0 or self.snake.x[0]>960 or self.snake.y[0]>760:
            print(f"{self.x[0]} {self.y[0]}")
            raise "game over"
    
    def display_score(self):
        font = pygame.font.SysFont('calibri', 30)
        score = font.render(f"Score is : {self.snake.length}", True, (220,220,220))
        self.surface.blit(score, (800,10))
    
    def game_over(self):
        self.surface.fill((255,0,0))
        fontbig = pygame.font.SysFont('comicsansms', 80)
        over = fontbig.render("GAME OVER", True, (255,255,0))
        self.surface.blit(over, (250,300))
        font = pygame.font.SysFont('comicsansms', 30)
        score = font.render(f"Score is : {self.snake.length}", True, (200,200,200))
        self.surface.blit(score, (400,400))
        again = font.render("Press ENTER to Play Again and ESC to exit", True, (200,200,200))
        self.surface.blit(again, (200,450))
        pygame.display.flip()
        pygame.mixer.music.pause()
        #time.sleep(0.5)

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
        self.t = 0.3
    
    def run(self):
        running = True
        pause = False
    
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False 
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                    pass
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            time.sleep(self.t)


if __name__ == "__main__":
    game = Game()
    game.run()
    