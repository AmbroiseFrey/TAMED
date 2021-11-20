import pygame

class OperatingSystem:
  def __init__(self,user,password):
    self.password= password
    self.user = user
    if password == '0000' and user == 'User1':
      print('Welcome back ' + user + '!')
      return
    else:
      print('Wrong !')
      return
  
  def mails():
    return
      
  
  