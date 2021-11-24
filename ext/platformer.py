import pygame, time

##Lien avec main.py
##Appeler une fonction dans ce script qui interagit avec pygame terminate la fenetre du main et la remplace par celle d'ici.
##Quand la fonction fini on revient à la fenetre de main de la ou la fonction est appelée

pygame.init()

screen = pygame.display.set_mode([700, 500])

def test():
  screen.fill((0,0,0))
  return 'Platformer connected'
    