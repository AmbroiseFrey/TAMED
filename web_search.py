###---------------------------------------###
###Don't mind this just testing things out###
###---------------------------------------###

import random

Websites = ["www.cia.gov","www.twitter.com", "www.test.com","www.repl.it"]
Titles = {"www.cia.gov":"Central Intelligence Agency", "www.twitter.com":"Twitter", "www.test.com":"Test","www.repl.it":"Replit"}

def random_page():
  return random.choice(Websites)

def load_page(page):
  while True:
    print(Titles[page])
    break