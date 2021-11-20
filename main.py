from os_run import OperatingSystem
import web_search

user = input('User: ')
password = input('Password: ')
logged_in = False

s=web_search

while True:
  if not(logged_in):
    os = OperatingSystem(user, password)
    logged_in = True
  action = input('Command:')
  if action == '-randompage':
    s.load_page(s.random_page())
  if action == '-search':
    page = input('Search:')
    s.load_page(page)
    break
  
  
  