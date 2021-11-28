import pygame, time
import ext.operations as Opr

##Lien avec main.py
##Appeler une fonction dans ce script qui interagit avec pygame terminate la fenetre du main et la remplace par celle d'ici.
##Quand la fonction fini on revient à la fenetre de main de la ou la fonction est appelée


WHITE = (255, 255, 255)

resolution = (600,400)
niveau = 0

pygame.init()
screen = pygame.display.set_mode(resolution)



#Test des extensions via main.py
def test():
  screen.fill((0,0,0))
  return 'Platformer connected'


class Sprite(pygame.sprite.Sprite): # Cette classe permet de faire un 'blueprint' de base pour chaque sprite. Chaque appel de cette class dans une classe ou varibale permet la creation de sprites different et independants mais suivants le meme 'plan' définit dans cette classe
  def __init__(self, image, x, y): #definitions de base (image de base et position de départ)
    super().__init__()

    self.image = pygame.image.load(image)
    self.rect = self.image.get_rect()

    self.rect.center = [x, y]

  def update(self):
    pass

  def render(self):
    screen.blit(self.image, self.rect)

#On definit le joueur
class Player(Sprite): # Le sprite du jouer est une 'child class' de la class sprite
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Player_(Test).png", x, y) #On definit le Player via les parametres de base d'un sprite introduit dans la classe Sprite
    self.stand = self.image #Image de base
    self.jump= pygame.image.load("Assets/Platformer/Player_(Test).png") #Image pour sauter
    ###ADD## self.walk_animation = pygame.image.load(f'Assets/Platformer/Walk Animation/Player Walk{i for i in range(1,12)}.png') #Serie d'animation de marche

#On definit le sol
class Floor(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Floor_(Test).png", x, y)


#Boucle du jeu platformer
def play_game():
  move_droite = False
  move_gauche = False
  RUN = True
  while RUN:
    screen.fill((0,0,0))
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,350),(50,50))

    player = Player(100, 200)
    floor = pygame.sprite.Group() #Un groupe de sprites (des classes donc) qui peuvent etre déplacés ensemble

    #Tests, peut etre pas la methode finale !
    for tile in range(0,400,70): #On ajoute les sprites du sol
      floor.add(Floor(tile,300))

    player.render() #On render le jouer
    floor.draw(screen) #On dessine la map

    if move_droite:
      print('droite')
    if move_gauche:
      print('gauche')

    #Ici on check les events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        RUN = False
      
      #On check si les touches son utilisés et quand elles sont relachées
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
          move_droite = True
        if event.key == pygame.K_LEFT:
          move_gauche = True
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
          move_droite = False
        if event.key == pygame.K_LEFT:
          move_gauche = False

      #Si la souris est pressée
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          print(event.pos)

          #On check si l'utilisateur veut quitter le jeu
          if Opr.check_interaction(event.pos, (0,50,360,400),['plat'], 'plat') == True:
            RUN = False
            return 'home'

    pygame.display.flip()