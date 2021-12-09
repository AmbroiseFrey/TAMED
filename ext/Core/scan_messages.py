import ext.Core.variables as varia

scans = {
  1:(
    'ambroise',
    'Test',
    ('tres', 'bete', 'je')
  ),

  'Le niveau en int':(
    "Le destinataire (s'il y en a plusieurs faire une liste de liste)",
    "L'objet",
    ('Les mots cles', 'a avoir', 'dans le contenu du mail')
  ),
}


def check_message(message_content:list):
  for lock in scans.keys():
    if lock in varia.unlocked: #si on a unlock le message
      i = 1
      for contents in scans[lock]: #on scan le content que l'on veut
        if i == 3: #si c'est le message content
          for word in contents: #si les mots que l'on veut
            if word in message_content[i].split(): #son dans le content
              return True #alors c'est bon
            break # failed
        elif message_content[i] == contents: # si il est bien egal a celui donné
          i+= 1 #on peu continuer
        else:
         break #sinon c'est automatiquement failed
    else:
      pass
  return False #c'est donc faux