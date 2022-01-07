from ext.Core import variables as varia
from ext.Core import operations as Opr

#Voir Dev Info.md pour infos sur le format des 'codes'

unlockable_messages = {
  2000 : {
    "TAMED Mission - 2":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour,",
    ],
  },
  1010 : {
    "Accident de la Station":[
      "from: Charlotte Coulson",
      "to: John Doe",
      "Bonjour Mr. Doe,",
      "Je suis Charlotte Coulson et j'ai travaillé sur le projet Zeus"
    ],
  }
}

scans = {
  (1010,2000):( #premier email a envoyer quand l'on retrouve le disque dur
    ("Group:TAMED" or "gen. michael Fredlyn",),
    ("mission", "1" or "1.0"),
    ('disque', 'dur')
  ),

  (1010,10):( #deuxieme mail Des documents suspects dans le disque dur retrouvé
    ("charlotte.coulson@kryptkorp.org" or 'Charlotte coulson',),
    ("documents" or 'document',),
    ("documents" or 'document' or 'file')
  )
}


def check_message(message_content:list):
  for lock in scans.keys():
    if lock[0] in varia.unlocked: #si on a unlock le message
      i = 1
      for contents in scans[lock]: #on scan le content que l'on veut
        if i == 3: #si c'est le message content
          for word in contents: #si les mots que l'on veut
            if word.lower() in Opr.textData_str(message_content)[i].lower().split(): #son dans le content
              return lock[1] #alors c'est bon 
            break # failed
        else:
          for word in contents: #si les mots que l'on veut
            if word.lower() in message_content[i].lower().split(): #son dans le titre
              i+= 1 #alors c'est bon
            else:
              break # failed
    else:
      pass
  return None #c'est donc un message qui ne correspond a rien



def update_messagerie():
  for lock_needed in unlockable_messages:
    if lock_needed in varia.unlocked and not lock_needed in varia.messages.keys(): #si un nouveau message est débloqué
      varia.popup += 1
      message_add = {lock_needed: unlockable_messages[lock_needed]} # on ajoute le message
      new_messages = varia.messages 
      message_add.update(new_messages)
      varia.messages = message_add
    pass
  for lock in varia.messages:
    if lock not in varia.unlocked and lock in varia.messages.keys():
      varia.messages.pop(lock_needed)
    pass
  return