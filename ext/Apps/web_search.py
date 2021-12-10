import random
from ext.Core import variables as varia
from ext.Core import operations as Opr
Websites = ["www.cia.gov","www.twitter.com", "www.test.com","www.repl.it"]

Pages = {"www.cia.gov":[
    "Central Intelligence Agency",
    "Welcome to the Central Intelligence Agency's Website",],
  "www.twitter.com":[
    "Twitter"],
  "www.test.com":[
    "Test Page"],
  "www.repl.it":[
    "Replit"]
}

def random_page():
  '''
  On choisit une page au hasard de la liste Websites
  '''
  return random.choice(Websites)

def load_page(page):
  
  '''
  On load une page par rapport a son url qui correspond a la clé de Pages
  '''
  y = 40
  if page in Pages.keys(): # si la page est dans les clés des urls
    for el in Pages[page]:
      Opr.render_text(el, (10,y), varia.WHITE, 15)
      y += 20
  else:
    pass