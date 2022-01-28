import random
from ext.Core import variables as varia
from ext.Core import operations as Opr
Websites = ["www.cia.gov","www.twitter.com", "www.test.com","www.repl.it","www.binaire.it"]

Pages = {"www.cia.gov":[
    "Central Intelligence Agency",
    "Welcome to the Central Intelligence Agency's Website",],
  "www.twitter.com":[
    "Twitter"],
  "www.test.com":[
    "Test Page"],
  "www.repl.it":[
    "Replit"],
  "www.binaire.it": 'binaire.it'
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
  y = 10*varia.resolution[1]/100 # le texte a imprimer commence a cette position
  if page in Pages.keys(): # si la page est dans les clés des urls
    if type(Pages[page]) == str: #si c'est le convertisseur binaire
      varia.sub_page = Pages[page] # on initialise le convertisseur binaire
    else: #sinon, si c'est du texte
      for el in Pages[page]: #pour chaque ligne
        Opr.render_text(el, (1.66*varia.resolution[0]/100,y), varia.WHITE, 3.75*varia.resolution[1]/100) #on l'imprime sur l'ecran
        y += 5*varia.resolution[1]/100 #on fait un "saut à la ligne"
  else:
    pass