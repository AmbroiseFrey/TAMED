import pygame, time, random
import ext.Core.variables as varia
pygame.init()

def test():
  return 'Successfully built snake game'
 
pygame.init()
 
resolution = varia.resolution
 
screen = pygame.display.set_mode(resolution)
 
clock = pygame.time.Clock()

snake_speed = 15
 
def snake(snake):
  for x in snake:
    if x == 1:
      pygame.draw.rect(screen, varia.BLACK, )
    elif x == 0:
      pygame.draw.rect(screen, varia.WHITE, )
 
 
def game():
    RUN = True
    x = resolution[0] / 2
    y = resolution[1] / 2
 
    snake = [1,0]
    snk_length = 1
 
    while RUN:
      clock.tick(snake_speed)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          RUN = False
        if event.type == pygame.KEYDOWN:
          pass
 
    pygame.quit()