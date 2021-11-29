import pygame, time
import ext.Core.operations as Opr
import ext.Core.variables as varia

##Lien avec main.py
##Appeler une fonction dans ce script qui interagit avec pygame terminate la fenetre du main et la remplace par celle d'ici.
##Quand la fonction fini on revient à la fenetre de main de la ou la fonction est appelée

niveau = 0

pygame.init()
screen = pygame.display.set_mode(varia.resolution)

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
    self.vert_move = 0 #On definit cette varibale comme un objet de player. En effet,elle n'est pas totalement controllable par l'utilisateur puisqu'il y a de la gravité. Elle ne sera donc pas remise a zero dans chaque loop pour checker les touches

  def move(self, x, y):
    self.rect.move_ip([x,y]) #Cette methode est differente de .move() puisqu'elle permet de vraiment bouger le rectangle pas de faire apparaitre une nouveau quelque part d'autre

  def update(self, floor):
    touch_floor = pygame.sprite.spritecollideany(self, floor) #Detect si on touche le sol
    horl_move = 0 #Movement horizental
    # On verifie quelle key est pressée
    move = pygame.key.get_pressed() #Permet de ne pas utiliser une boule for event in
    if move[pygame.K_LEFT]:
      horl_move -=4
    elif move[pygame.K_RIGHT]:
      horl_move +=4

    if move[pygame.K_UP] and touch_floor:
      self.vert_move = -20

    if self.vert_move < 10 and not touch_floor: #Si le joueur ne saute pas (valeur toujours egale ou plus petite que la capacité de sauter en un loop) et ne touche pas le sol
      self.vert_move += 1 # on le fait descendre

    if touch_floor and self.vert_move > 0: #Si on touche le sol
      self.vert_move = 0 #On empeche de tomber

    self.move(horl_move, self.vert_move) # On update la character


#On definit le sol
class Floor(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Floor_(Test).png", x, y)


#Boucle du jeu platformer
def play_game():
  clock = pygame.time.Clock()
  RUN = True
  player = Player(100, 200)
  floor = pygame.sprite.Group() #Un groupe de sprites (des classes donc) qui peuvent etre déplacés ensemble
  #Tests, peut etre pas la methode finale !
  for tile in range(0,650,50): #On ajoute les sprites du sol
    floor.add(Floor(tile,370))
  
  #Boucle de jeu
  while RUN:
    screen.fill((0,0,0))
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,0),(50,50))

    player.update(floor) #On update par rapport au touches et interactions
    player.render() #On render le jouer
    floor.draw(screen) #On dessine la map

    #Ici on check les events autre que les touches fleches
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        RUN = False

      #Si la souris est pressée
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          print(event.pos)

          #On check si l'utilisateur veut quitter le jeu
          if Opr.check_interaction(event.pos, (0,50,0,50),['plat'], 'plat') == True:
            RUN = False
            return 'home'

    clock.tick(60) #permet de s'adapter à nos boucles, les animations et même les mouvements sont beacoup plus 'smooth'

    pygame.display.flip()