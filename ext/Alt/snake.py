import pygame, time, random
import ext.Core.variables as varia
pygame.init()

def test():
  return 'Successfully built snake game'
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
resolution = varia.resolution
 
dis = pygame.display.set_mode(resolution)
 
clock = pygame.time.Clock()
 
snake_blocks = 10
snake_speed = 15
 

 
 
def game():
    RUN = True
    x = resolution[0] / 2
    y = resolution[1] / 2
 
    x1 = 0
    y1 = 0
 
    snake = []
    snk_length = 1
 
    foodx = round(random.randrange(0, resolution[0] - snake_blocks) / 10.0) * 10.0
    foody = round(random.randrange(0, resolution[1] - snake_blocks) / 10.0) * 10.0
 
    while RUN:
      clock.tick(snake_speed)
 
    pygame.quit()