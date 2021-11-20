from os_run import *
from web_search import *

user = input('User: ')
password = input('Password: ')
logged_in = False


while True:
  if not (logged_in):
      os = OperatingSystem(user, password)
      logged_in = True
  action = input('Command:')
  if action == '-randompage':
      load_page(random_page())
  if action == '-search':
      page = input('Search:')
      load_page(page)
      break
