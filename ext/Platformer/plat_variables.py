import pygame
from ext.Core.variables import resolution

mid_screen = tuple(i/2 for i in resolution)

mi,ma = sorted(resolution)

checkpoints = [
  (2000, (400,425)),
  
  (3000, (1400,400)),
  
  (4000, (2400,375)),
  
  (5000, (3400,350)),
  
  (6000, (4400,300)),
  
  (7000, (4800,325))
  
              ]

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()