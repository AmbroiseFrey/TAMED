import pygame, time, numpy
import ext.Core.operations as Opr
import ext.Core.variables as varia

##Lien avec main.py
##Appeler une fonction dans ce script qui interagit avec pygame terminate la fenetre du main et la remplace par celle d'ici.
##Quand la fonction fini on revient à la fenetre de main de la ou la fonction est appelée

pygame.init()
screen = pygame.display.set_mode(varia.resolution)
screen_rect = screen.get_rect()

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
    super().__init__("Assets/Platformer/Player.png", x, y) #On definit le Player via les parametres de base d'un sprite introduit dans la classe Sprite
    self.stand = self.image #Image de base
    self.jump= pygame.image.load("Assets/Platformer/Player.png") #Image pour sauter
    self.vert_move = 0 #On definit cette varibale comme un objet de player. En effet,elle n'est pas totalement controllable par l'utilisateur puisqu'il y a de la gravité. Elle ne sera donc pas remise a zero dans chaque loop pour checker les touches

  def move(self, x, y,floor):
    dx = x
    dy = y

    while self.check_collision(0, dy, floor): #Si la colision est en haut du joueur
      dy -= numpy.sign(dy) #Si y<0 on change de 1 si y>0 on change de -1

    while self.check_collision(dx, dy, floor): #Si la collision est sur le coté
      dx -= numpy.sign(dx) #Si x<0 on change de 1 si x>0 on change de -1

    self.rect.move_ip([dx, dy]) #Cette methode est differente de .move() puisqu'elle permet de vraiment bouger le rectangle pas de faire apparaitre une nouveau quelque part d'autre

  def update(self, level, floor, flag, lava):
    touch_floor = self.check_collision(0,1,floor) #Detect si on touche le sol
    flag = self.check_collision(0,1,flag)
    lava = self.check_collision(0,1,lava)
    horl_move = 0 #Movement horizental
    # On verifie quelle key est pressée
    move = pygame.key.get_pressed() #Permet de ne pas utiliser une boucle for event in
    if move[pygame.K_LEFT]:
      horl_move -=4
    elif move[pygame.K_RIGHT]:
      horl_move +=4

    if move[pygame.K_UP] and touch_floor:
      self.vert_move = -20 # oui, mais ça ne marchera pas si le floor est plus haut ou plus bas
      
    elif self.vert_move < 10: #Si le joueur ne saute pas (valeur toujours egale ou plus petite que la capacité de sauter en un loop) et ne touche pas le sol
      self.vert_move += 1 # on le fait descendre

    if touch_floor and self.vert_move >= 0:
      self.vert_move = 0

    if flag:
      print("Flag")
      return 'Flag'
      

    if lava:
      print("Lava")
      return 'Lava'

    self.move(horl_move, self.vert_move, floor) # On update la character
    self.rect.clamp_ip(screen_rect) # Permet d'empecher le character de sortir de lecran

  def check_collision(self, x, y, environment):
    self.rect.move_ip([x, y]) #On fait boujer le sprite
    collide = pygame.sprite.spritecollideany(self, environment) #On check si il touche le sol
    self.rect.move_ip([-x, -y]) #On le renvoit d'ou il vient
    return collide


#On definit le sol
class Floor(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Floor_(Test).png", x, y)


class Level_Flag(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Flag.png", x, y)

class Lava(Sprite):
  def __init__(self, x, y):
    super().__init__("Assets/Platformer/Lava.png", x, y)


def load_level(level):
  if level == 0:
    floor = pygame.sprite.Group()
    #Un groupe de sprites (des classes donc) qui peuvent etre déplacés ensemble
    #Tests, peut etre pas la methode finale !
    for tile in range(0,650,50): #On ajoute les sprites du sol
      floor.add(Floor(tile,380))

    floor.add(Floor(300,220))
    flag = pygame.sprite.Group()
    flag.add(Level_Flag(550,340))
    lava = pygame.sprite.Group()
    lava.add(Lava(300, 340))

  elif level == 1: # en fait le bug avec le bouton pour revenir a lordi c'est parce que on a une boucle while j'essaye de rtouver un moyen tu m'as fait peur, j'ai cru qu'on m'avait hacké# ah, le bug qui s'est passé hier? celui qui a tout enlevé? non j'ai creer lissue sur le github tu peux aller voir si tu veux ok
    floor = pygame.sprite.Group()
    for tile in range(0,650,50): 
      floor.add(Floor(tile,380))
    floor.add(Floor(300,380))
    lava = pygame.sprite.Group()
    flag = pygame.sprite.Group()
    flag.add(Level_Flag(550,340))
  
  return floor, flag, lava

#Boucle du jeu platformer
def play_game(level = 0):
  varia.RUN_plat == True
  clock = pygame.time.Clock()
  player = Player(100, 200)

  floor, flag, lava = load_level(level)

  #Boucle de jeu
  while varia.RUN_plat:
    #Ici on check les events autre que les touches fleches
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        varia.RUN_plat = False

      #Si la souris est pressée
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          print(event.pos)

          #On check si l'utilisateur veut quitter le jeu
          if Opr.check_interaction(event.pos, (0,50,0,50),['plat'], 'plat') == True:
            return 'home'

    pygame.event.pump()
    screen.fill((0,0,0))
    Opr.render_image('Assets/Icons/Home_Button_(Test).png',(0,0),(50,50))
    
    floor.draw(screen) #On dessine la map
    flag.draw(screen)
    lava.draw(screen)
    player.render() #On render le jouer
    action = player.update(level, floor, flag, lava) #On update par rapport au touches et interactions
    if action == 'Lava':
      action = ''
      return level
      break
    elif action == 'Flag':
      action = ''
      return level+1
      break
    clock.tick(60) #permet de s'adapter à nos boucles, les animations et même les mouvements sont beacoup plus 'smooth'

    pygame.display.flip()