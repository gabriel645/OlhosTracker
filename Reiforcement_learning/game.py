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
Eye_predict = namedtuple('Point', 'x, y')
Eye_real = namedtuple('Point', 'x, y')
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

class TargetGameAI:
    
    def __init__(self, w=1920, h=1080):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()   

        # init game state        
        self.reset()


    def reset(self):
        self.cursor = Point(self.w//2, self.h//2)        
        self.score = 0    
        self.total_reward = 0        
        self.boundaryMinimum = 100
        self.target = None
        self.targetCenter = None
        self.old_ct_dist = 10000
        self.boundary_speed = 60
        self.dist_to_relocate = 200      

        self._place_target()



    def _place_target(self):
        self.boundary = 4000
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.target = Point(x, y)
        self.targetCenter = Point(self.target.x + BLOCK_SIZE//2, self.target.y + BLOCK_SIZE//2)
        self._update_ui()
   
        
    def play_step(self, action):

        game_over = False
        reward = 0       


        # self.frame_iteration += 1000//math.dist(self.cursor, self.targetCenter)



        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()            
        
        # 2. move
        self._move_cursor(action) # update the cursor
        
        # 3. check if game over
        if self._is_collision():
            game_over = True
            return reward, game_over, self.score
                    
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(60)

        ct_dist = math.dist(self.cursor, self.targetCenter)
        print(f"DIST = {ct_dist}")
        
        # dist_score = 1920 - ct_dist

        # reward = dist_score/100

        self.old_ct_dist = ct_dist

        print(f"Reward: {reward}")

        if ct_dist < self.dist_to_relocate:
            reward += 10
            self._place_target()
            if self.dist_to_relocate > 10:
                self.dist_to_relocate -= 10

        if  (ct_dist - self.old_ct_dist < 0) and self.old_ct_dist < 10000:
            reward += 1

        if (ct_dist > 80) and (ct_dist - self.old_ct_dist >= 0):            
            reward = 0


        if action[0] > 1920 or action[0] < 0 or action[1] > 1080 or action[1] < 0:
            reward = 0


        self.score += reward
        # 6. return game over and score
        return reward, game_over, self.score
       

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

        if self.boundary > self.boundaryMinimum + 700:
            self.boundary -= self.boundary_speed//10
        elif self.boundary > self.boundaryMinimum and self.boundary <= self.boundaryMinimum + 700:
            self.boundary -= self.boundary_speed//20
        else:
            self.boundary -= self.boundary_speed//50

        pygame.display.flip()

    def _move_cursor(self, action):        
        self.cursor = Point(*action)


# if __name__ == '__main__':
#     game = SnakeGame()
    
#     # game loop
#     while True:
#         game_over, score = game.play_step()

#         if game_over == True:
#             break
        
#     print('Final Score', score)
        
#     pygame.quit()