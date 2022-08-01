# import the pygame module, so you can use it
from random import randint
from turtle import pos
import pygame
import time



# Temp file


# define a main function
def main():     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")
    #load images
    image = pygame.image.load("img/target.png")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((1920,1080))
    screen.blit(image, (0,0))
    pygame.display.flip()
    # define a variable to control the main loop
    running = True

    # t = time.time() 
    # main loop
    while running:

    # if (time.time()) >= (t + 10):
        screen.fill((0,0,0))
        time.sleep(6)
        cord = (randint(20, 1900),randint(20, 1060))
        position = [cord[0] + 25,cord[1] + 25]

        with open('training_pos.txt', 'w') as f:        
            f.write(str(position))  

        # print(position)
        screen.blit(image, cord)
        pygame.display.flip()
        # t = time.time()
        
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()