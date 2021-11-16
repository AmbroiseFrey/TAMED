from os_run import OperatingSystem

user = input('User: ')
password = input('Password: ')
logged_in = False

while True:
  if logged_in != True:
    os = OperatingSystem(user, password)
    logged_in = True
  