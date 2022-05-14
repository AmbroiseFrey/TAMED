import pygame, time 
from ext.Core import variables as varia

pygame.init()
pygame.mixer.init()
x,y = varia.resolution
screen = pygame.display.set_mode((int(x),int(y)))
save = None

res0=varia.resolution[0]/100
res1=varia.resolution[1]/100

def ConvertBinarytoDecimal(binary_value):
  decimal_value, i = 0, 0
  while(binary_value != 0):
      print(binary_value)
      dec = binary_value % 10 # on trouve le reste
      decimal_value = decimal_value + dec * pow(2, i)
      binary_value = binary_value//10 # on remet 
      i += 1
  return (decimal_value)

def ConvertDecimaltoText(binary_data):
  print(binary_data)
  text_data = ''
  if binary_data.isdigit():
    for i in range(0, len(binary_data), 7):
      # on sépare le chiffre en binaire en octets
      byte = int(binary_data[i:i + 7]) # on passe chacque octet dans le convertisseur decimal
      decimal_data = ConvertBinarytoDecimal(byte)

      text_data += chr(decimal_data)
    return text_data
  else:
    return "Ce n'est pas un chiffre binaire!" 

def render_text(text:str, pos:tuple, color:tuple=varia.WHITE, size=6*res1):
  '''
  Fonction qui permet d'afficher du texte.
  Prend en argument le texte (str) et sa position (tuple)
  '''
  size = int(size)
  pygame.font.init()
  font = pygame.font.Font("Assets/FreeSansBold.ttf", size) # on definit la font
  try:
    text = font.render(text, True, color) # On definit le text
  except ValueError:
    text = font.render("Un de ces characters n'existe pas!", True, color)
  screen.blit(text,pos) # On affiche

def textInZone(color, zonerect):
  """
  Attention, ça ne marchera pas si le texte est de la même couleur que le background
  """
  pxarray = pygame.PixelArray(screen) # les pixels de l'écran
  value = screen.map_rgb(color) #
  # mat = ()
  for x in range(zonerect[0][0], zonerect[1][0]):
    line = ()
    for y in range(zonerect[0][1], zonerect[1][1]):
      line += ( pxarray[x,y],)
      if pxarray[x,y] == value:
        return True
    # mat += (line,)
    # print(mat, value)
  return False


# to be tried
def textarea(textData:tuple=("",), size:tuple=(0,0), pos:tuple=(0,0), background=(255,255,255), color=(0,0,0), padding:float=0, border=None,  border_width:float=1, font_size:int=23, font_spacing:float=5):
  '''
  Permet de retourner à la ligne automatiquement
  '''
  size = tuple(understandValue(s) for s in size)
  pos = tuple(understandValue(p) for p in pos)
  div(background, size[1],size[0],pos[1],pos[0],border=border, border_width=border_width, padding=padding)
  for i in range(len(textData)):
    s = textData[i]
    p = pos[0]+font_spacing,pos[1]+font_size*i+font_spacing*(i+1)
    render_text(s, p, color, font_size)
  i = len(textData)
  x,y = int(pos[0]+size[0]-font_spacing),int(pos[1]+font_size*(i-1)+font_spacing*i)
  #wait until it displays (if possible)
  if textInZone(color, ((x-5,y),(x,y+font_size))):
    l = textData[-1].rfind(' ')
    if l == -1:
      return textData[:-1]+(textData[-1][:-1],textData[-1][-1])
    ls = textData[-1][l+1:]
    b = () if ls == '' else (ls,)
    return textData[:-1]+(textData[-1][:l],)+b
  return textData

def textData_str(textData, sep=' '):
  if type(textData)!=str:
    return sep.join(textData)
  else:
    return textData


def render_image(image_name:str, pos:tuple, size:tuple, center:bool=False):
  '''
  Fonction qui permet d'afficher une image.
  Prend en argument le nom de l'image (str), sa position (tuple), et sa taille (tuple)'''
  loaded_img= pygame.image.load(image_name) # On load l'image
  size = list(size)
  size[0] = int(size[0])
  size[1] = int(size[1])
  size = tuple(size)
  loaded_img = pygame.transform.scale(loaded_img, size) # On change son échelle
  if center: #si c'st une image centrée
    pos = tuple(
      pos[i]-size[i]/2 +varia.mid_screen[i]
      for i in (0,1)
    )
  screen.blit(loaded_img, pos + size) # On affiche


def render_rectangle(color:tuple, size:tuple, pos:tuple):
  '''
  Fonction qui permet d\'afficher un rectangle.
  Prend en argument la couleur (un tuple), sa taille (tuple), et sa position (tuple)
  '''
  pygame.draw.rect(screen, color, pygame.Rect(pos + size))


mi, ma = sorted(varia.resolution)
def understandValue(s, op:1|0=0): # faire des positions qui dépendent de la résolution
  if type(s) is int or type(s) is float:
    return s
  if '*' in s:
    x = s.split('*',1)
    return understandValue(x[0]) * understandValue(x[1])
  if '/' in s:
    x = s.split('/',1)
    return understandValue(x[0]) / understandValue(x[1])
  if '+' in s:
    x = s.split('+',1)
    return understandValue(x[0]) + understandValue(x[1])
  if '-' in s:
    x = s.split('-',1)
    return understandValue(x[0]) - understandValue(x[1])
  if s[-1] == '%':
    return float(s[:-1])/100 * varia.resolution[op]
  if s[-2:] == 'vw':
    return float(s[:-2])/100 * varia.resolution[0]
  if s[-2:] == 'vh':
    return float(s[:-2])/100 * varia.resolution[1]
  if s[-4:] == 'vmin':
    return float(s[:-4])/100 * mi
  if s[-4:] == 'vmax':
    return float(s[:-4])/100 * ma
  return float(s)

def div(color:tuple=(0,0,0), height=0, width=0, top=0, left=0, bottom=None, right=None, border:tuple=False, border_width=1, padding=0):
  x1,y1 = 0,0
  x2,y2 = 0,0
  h = understandValue(height)
  w = understandValue(width)
  #position along the y-axis
  if bottom != None:
    y2 = understandValue(bottom,1)
    y1 = y2 - h
  else: 
    y1 = understandValue(top, 1)
    y2 = y1 + h
  #position along the x-axis
  if right != None:
    x2 = understandValue(right,0)
    x1 = x2 - w
  else: 
    x1 = understandValue(left,0)
    x2 = x1 + w
  pygame.draw.rect(screen, color, pygame.Rect((x1,y1,x2-x1,y2-y1)))
  if border:
    p = understandValue(padding)
    w = understandValue(border_width)
    render_rectangle_borders(border, (x1-p,y1-p), (x2-x1+p*2, y2-y1+p*2), w, (0,0))


def render_rectangle_relative(color:tuple, p1:tuple, p2:tuple, relativity:tuple=(1,0)):
  '''
  Fonction qui permet d\'afficher un rectangle avec une position relative.
  Prend en argument la couleur (un tuple), et le 2 points qui définissent le rectangle, le point1 `p1` a une position relative à coin en-haut à gauche et le point `p2` a un position relative au point en-bas à droite'''
  p2 = (
    varia.resolution[0] + p2[0] - p1[0] if relativity[0] else p2[0], 
    varia.resolution[1] + p2[1] - p1[1] if relativity[1] else p2[1]
  )
  pygame.draw.rect(screen, color, pygame.Rect(p1 + p2))


def render_rectangle_borders(color:tuple, p1:tuple, p2:tuple, width:float=1, relativity:tuple=(1,0)):
  '''
  Fonction qui permet d\'afficher les bords d\'un rectangle définit par les points `p1` et `p2` avec une coleur `couleur`'''
  p2 = (
    varia.resolution[0] + p2[0] - p1[0] if relativity[0] else p2[0], 
    varia.resolution[1] + p2[1] - p1[1] if relativity[1] else p2[1]
  )
  w2 = width/2
  pygame.draw.rect(screen, color, pygame.Rect((p1[0]-w2,p1[1]-w2,p2[0]+width,width)))
  pygame.draw.rect(screen, color, pygame.Rect((p2[0]+p1[0]-w2,p1[1]-w2,width,p2[1]+w2)))
  pygame.draw.rect(screen, color, pygame.Rect((p1[0]-w2,p2[1]+p1[1]-w2,p2[0]+width,width)))
  pygame.draw.rect(screen, color, pygame.Rect((p1[0]-w2,p1[1]-w2,width,p2[1]+w2)))


def render_circle(color: tuple, radius, pos: tuple):
  '''
  Fonction qui permet d'afficher un cercle.
  Prend en argument la couleur (un tuple), son rayon (int), et sa position (tuple)
  '''
  pygame.draw.circle(screen, color, pos, int(radius))

def check_interaction(clickpos: tuple, wanted_area: tuple, wanted_pages: list, page: str):
  '''
  Fonction qui prend en parametre la position de la souris au moment du click que l'on check et qui la compare avec la zone que l'on veut sous forme de tuple - (x1, x2,y1,y2)
  Compare aussi la page du jeu et les pages dans lesquelles le bouton marche. 
  La fonction renvoi True ou False selon si la souris est bien a l'endroit voulu
  '''
  if page in wanted_pages:
    if wanted_area[0]<=clickpos[0]<=wanted_area[1] and wanted_area[2]<=clickpos[1]<=wanted_area[3]:
      return True
    else:
      return False
  else:
    return False

def render_time():
  '''
  Affiche l'heure
  '''
  hour = time.strftime("%H")
  hour = int(hour) +1
  render_text(str(hour) +':' + time.strftime("%M"),(85.67*varia.resolution[0]/100,87.5*varia.resolution[1]/100),varia.BLACK,7.5*varia.resolution[1]/100)
  render_text(time.strftime("%Y-%m-%d"),(86*varia.resolution[0]/100,95*varia.resolution[1]/100),varia.BLACK,3.75*varia.resolution[1]/100)

def render_file(file_contents: list, file_name: str = 'File', x: float=3.33, y: float=8.33, espacement_ligne : float = 5, size : tuple = (400,266)):
  '''
  Render le content d'un fichier
  '''
  if type(file_contents) == list: # Si c'est du texte en plusieurs lignes
    for el in file_contents:
      render_text(el, (x*res0,y*res1), varia.WHITE,3*res1)
      y += espacement_ligne
  elif type(file_contents) == str: 
    if file_contents[len(file_contents)-3:len(file_contents)] in ['mp3','wav']: #si c'est de la musique
      varia.sound = 'Assets/Directory Files/' + file_contents
    elif file_contents[len(file_contents)-3:len(file_contents)] in ['png','jpg']: #si c'est une image
      render_image('Assets/Directory Files/'+file_contents, (x*res0,y*res1), size)
    elif file_contents[len(file_contents)-3:len(file_contents)] in ['mp4']: #si c'est une video
      render_image('Assets/Directory Files/'+file_contents[:-4]+'.png', (x*res0+6.25*res0,y*res1), (480,240))
    elif file_contents == 'snake.py': #si c'est le snake game
      return 'snake'
    elif file_contents == 'tamed.exe': #si c'est le snake game
      return 'plat'
    else:
      render_text(file_contents, (x*res0,y*res1)) # base, on render le texte
  else:
    pass
  return varia.page