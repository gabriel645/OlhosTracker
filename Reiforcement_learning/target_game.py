import pygame
import random
from enum import Enum
from collections import namedtuple
import math

pygame.init()
# font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (0,200,0)
YELLOW = (200,200,0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def __init__(self, w=1920, h=1080):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        # pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        # self.direction = Direction.RIGHT
        
        # self.head = Point(self.w/2, self.h/2)
        # self.snake = [self.head, 
        #               Point(self.head.x-BLOCK_SIZE, self.head.y),
        #               Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.cursor = Point(*pygame.mouse.get_pos())
        
        self.score = 0
        # self.food = None
        # self._place_food()

        self.frame_iteration = 0

        self.boundary = 2000
        self.boundaryMinimum = 100
        self.target = None
        self.targetCenter = None
        self._place_target()


    def _place_target(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.target = Point(x, y)
        self.targetCenter = Point(self.target.x + BLOCK_SIZE//2, self.target.y + BLOCK_SIZE//2)
        # if self.food in self.snake:
        #     self._place_target()

    # def _place_food(self):
    #     x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
    #     y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
    #     self.food = Point(x, y)
    #     if self.food in self.snake:
    #         self._place_food()
        
    def play_step(self):
        self.frame_iteration += 1000//math.dist(self.cursor, self.targetCenter)


        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_UP:
            #         self.direction = Direction.UP
            #     elif event.key == pygame.K_DOWN:
            #         self.direction = Direction.DOWN
        
        # 2. move
        self._move_cursor() # update the cursor
        # self._move(self.direction) # update the head
        # self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        # if self.head == self.food:
        #     self.score += 1
        #     self._place_food()
        # # else:
        #     self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(60)

        try:
            self.score = 2000 // math.dist(self.cursor, self.targetCenter) - self.frame_iteration
        except:
            self.score = 4000 - self.frame_iteration
        # 6. return game over and score
        return game_over, self.score
    
    # def _is_collision(self):
    #     # hits boundary
    #     if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
    #         return True
    #     # hits itself
    #     if self.head in self.snake[1:]:
    #         return True
        
    #     return False

    def _is_collision(self):
        # hits boundary        
        if math.dist(self.cursor, self.targetCenter) > self.boundary:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        pygame.draw.circle(self.display, WHITE, self.targetCenter, self.boundary)        
        pygame.draw.circle(self.display, BLACK, self.targetCenter, self.boundary - 3)    
        pygame.draw.circle(self.display, RED, self.targetCenter, 80)
        pygame.draw.circle(self.display, YELLOW, self.targetCenter,40)
        pygame.draw.circle(self.display, GREEN, self.targetCenter,10)
        
        
        pygame.draw.circle(self.display, GREEN, [self.cursor.x, self.cursor.y],5)

        if self.boundary > self.boundaryMinimum:
            self.boundary -= self.frame_iteration//300
        else:
            self.boundary -= self.frame_iteration//600



        # for pt in self.snake:
        #     pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        #     pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))


        # pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        

        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    # def _move(self, direction):
    #     x = self.head.x
    #     y = self.head.y
    #     if direction == Direction.RIGHT:
    #         x += BLOCK_SIZE
    #     elif direction == Direction.LEFT:
    #         x -= BLOCK_SIZE
    #     elif direction == Direction.DOWN:
    #         y += BLOCK_SIZE
    #     elif direction == Direction.UP:
    #         y -= BLOCK_SIZE
            
    #     self.head = Point(x, y)

    def _move_cursor(self):        
        self.cursor = Point(*pygame.mouse.get_pos())


if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()