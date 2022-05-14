import pygame
from screeninfo import get_monitors

for monitor in get_monitors():
  resolution = (int(monitor.width)-int(0.33*monitor.width/100), int(monitor.height)-int(10*monitor.height/100))
mid_screen = tuple(map(lambda i:i*.5, resolution))

screen = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

class Vector:
  @classmethod
  def add(cl,*v):
    return tuple(map(lambda *a: sum(a), *v))

def prevent(obj, key, callback = lambda e:e):
  if key in obj.keys():
    return callback(obj[key])


mi, ma = sorted(resolution)
def understandValue(s, op:1|0=0):
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
    return float(s[:-1])/100 * resolution[op]
  if s[-2:] == 'vw':
    return float(s[:-2])/100 * resolution[0]
  if s[-2:] == 'vh':
    return float(s[:-2])/100 * resolution[1]
  if s[-4:] == 'vmin':
    return float(s[:-4])/100 * mi
  if s[-4:] == 'vmax':
    return float(s[:-4])/100 * ma
  return float(s)

def renderImage(name, rect):
  rect = tuple(map(understandValue, rect))
  screen.blit(
    pygame.transform.scale(
      pygame.image.load(name),
      tuple(map(int, rect[2:]))
    ),
    rect
  )

class Window:
  def __init__(self, apps, *pages):
    self.focus = None
    self.pages = pages
    self.apps = apps
    self.tools_bar_height = understandValue('5.556vh')
    self.apps_height =  understandValue('5vh')
    self.apps_dist =  understandValue('2vh')
    self.page_rect = 0,0,resolution[0],resolution[1]-self.tools_bar_height
    self.tools_bar = Box(
      (0,self.page_rect[3],self.page_rect[2],self.tools_bar_height),
      *(
        Button(
          (self.apps_dist,(self.tools_bar_height-self.apps_height)/2,self.apps_height,self.apps_height),
          action = eval('lambda **i: Page.open({})'.format(j)),
          background = i
        ) for i,j in zip(apps, range(len(apps)))
      ),
      background= 0xffffff, rel_display = 'horizontal'
    )
    # print(tuple(map(lambda e: e.rect, self.tools_bar.children)))
    self.request_display = True
    self.displayed = []
  def display(self):
    # if self.request_display:
    self.displayed = []
    #display pages
    Page.disp()
    #display toolsbar
    self.tools_bar.display()
    self.request_display = False

def applyChildren(children, obj, rel_display=None):
  for i,j in zip(children,range(len(children))):
    i.parent = obj
    i.index = j
    i.precedes = None if j == len(children)-1 else children[j+1]
    i.subsides = None if j == 0 else children[j-1]
    if rel_display != None:
      i.rect= Vector.add(
        i.rect[:2],
        *((
            (i.subsides.rect[0],0) if rel_display == 'horizontal' else (0, i.subsides.rect[1]),
            (i.subsides.rect[2],0) if rel_display == 'horizontal' else (0, i.subsides.rect[3])
          ) if j != 0 else ()
        ),
        obj.rect[:2] if not isinstance(obj, Page) else (0,0)
      ) + i.rect[2:]

class Page:
  All = []
  opened = 0
  @classmethod
  def disp(cl):
    cl.All[cl.opened].display()
  @classmethod
  def open(cl,link):
    cl.opened = link
    window.request_display = True
  def __init__(self, *children, **style):
    Page.All.append(self)
    self.style = style
    self.analysed = {}
    v = prevent(self.style, 'background')
    if v:
      self.analysed['background'] = (lambda :renderImage(v, window.page_rect)) if type(v) is str else (lambda :pygame.draw.rect(screen, v, window.page_rect))
      self.children = children
      applyChildren(children, self, prevent(style, 'rel_display'))
  def display(self):
    # window.displayed.append(self)
    for i in self.analysed:
      self.analysed[i]()
    for i in self.children:
      i.display()

class Box:
  def __init__(self, rect, *children, events={}, **style):
    self.rect = tuple(map(understandValue, rect))
    self.style = style
    self.analysed = {}
    self.events = events
    self.v = prevent(self.style, 'background')
    if self.v:
      if type(self.v) is str:
        self.analysed['background'] = lambda : renderImage(self.v,self.rect)
      else:
        self.analysed['background'] = lambda : pygame.draw.rect(screen,self.v,self.rect)
    self.children = children
    applyChildren(children, self, prevent(style, 'rel_display'))
  def display(self):
    window.displayed.append(self)
    for i in self.analysed:
      self.analysed[i]()
    for i in self.children:
      i.display()

class Button(Box):
  def __init__(self, rect, action=lambda **i:None, **style):
    super().__init__(rect, events={'onmousedown': action}, **style)
pygame.font.init()

class TextBox(Box):
  def __init__(self, rect, text:str="", **style):
    super().__init__(rect,**style)
    self.value = text
    self.display_value = ('',)
    self.style['font_size'] = round((prevent(self.style,'font_size') or .02*resolution[1]))
    self.style['font_family'] = prevent(self.style,'font_family') or "Assets/FreeSansBold.ttf"
    self.style['color'] = prevent(self.style,'color') or 0
    print(self.style['color'])
    self.font = pygame.font.Font(self.style['font_family'], self.style['font_size'])
    self.edit()
  def edit(self):
    self.display_value = ('',)
    for i in self.value:
      try:
        img = self.font.render(self.display_value[-1]+i, True, self.style['color'])
        if img.get_width()>self.rect[2]:
          l = self.display_value[-1].rfind(' ')
          if l == -1:
            self.display_value = self.display_value[:-1]+ (self.display_value[-1], i)
            continue
          ls = self.display_value[-1][l+1:]
          b = (i,) if ls == '' else (ls+i,)
          self.display_value = self.display_value[:-1]+(self.display_value[-1][:l],)+b
        else:
          self.display_value = self.display_value[:-1]+(self.display_value[-1]+i,)
      except ValueError:
        self.display_value = ("Un de ces characters n'existe pas!",)
        break
  def display(self):
    window.displayed.append(self)
    for i,j in zip(self.display_value,range(len(self.display_value))):
      screen.blit(self.font.render(i, True, self.style['color']), (self.rect[0], self.rect[1]+j*self.style['font_size']))
      self.rect = self.rect[:3]+(len(self.display_value)*self.style['font_size'],)

class Editable(TextBox):
  def __init__(self, *a, **b):
    super().__init__(*a, events={'onkeydown': self.keydown}, **b)
  def keydown(self, event):
    if event.key == pygame.K_BACKSPACE:
      keys = pygame.key.get_pressed()
      if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
        l = self.value.rfind(' ')
        if l == -1:
          self.value = ""
        else:
          self.value = self.value[:l]
      else:
        self.value = self.value[:-1]
    else:
      self.value += event.unicode
    self.edit()


window = Window(
  ('Assets/Icons/App Icons/Home_Button.png',
   'Assets/Icons/App Icons/Folder.png',
   'Assets/Icons/App Icons/Platformer_Button.png',
   'Assets/Icons/App Icons/Internet.png',
   'Assets/Icons/App Icons/Messages.png',
   'Assets/Icons/App Icons/Notes.png'),
  Page(
    Box((10,0,100,100), background=0xff0000),
    Box((0,10,100,50), background=0x00ff00),
    Button((0,0,50,100), action=lambda **i:print(i), background=0xffffff),
    Editable((0,0,300,20),"Hello, my name is Robert and one thing I like in life is to eat bananas.", color = (255,255,255)),
    background='Assets/Backgrounds/Mars-Wallapaper.jpg', rel_display = 'horizontal'),
  Page(
    Box((0,0,'100vw', '4vh'),
    Button(('100vw-3.8vh','.2vh', '3.6vh', '3.6vh'), lambda **i:Page.open(0), background='Assets/Icons/cross.png'), background=0xffffff),
    background=0xff0000, rel_display = 'vertical'),
  Page(background=0x00ff00),
  Page(background=0x0000ff),
  Page(background=0xffff00),
  Page(background=0xffaa00)
)


RUN = True
while RUN:
  window.display()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      RUN = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_presses = pygame.mouse.get_pressed()
        if mouse_presses[0]:
          pos = event.pos
          for j in range(len(window.displayed)-1,-1,-1):
            i = window.displayed[j]
            if pos[0]>=i.rect[0] and pos[0]<=i.rect[0]+i.rect[2] and pos[1]>=i.rect[1] and pos[1]<=i.rect[1]+i.rect[3]:
              window.focus = i
              print(i)
              if 'onmousedown' in i.events.keys():
                i.events['onmousedown'](x = pos[0], y = pos[1])
                break
    if event.type == pygame.KEYDOWN:
      if 'onkeydown' in window.focus.events.keys():
        window.focus.events['onkeydown'](event)
  pygame.display.flip()
  clock.tick(60)

pygame.quit()