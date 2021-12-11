from ext.Core import variables as varia

#Voir Dev Info.md pour infos sur le format des 'codes'

unlockable_messages = {
  200 : ['message mission deux'],
  10 : ['1er message charlotte'],
}

scans = {
  (110,200):( #premier email a envoyer quand l'on retrouve le dique dur
    ("Group:TAMED-Command",),
    ("mission", "1" or "1.0"),
    ('disque', 'dur', 'crash' or "accident", 'recupere' or 'trouve')
  ),

  (10,11):( #deuxieme mail "en reponse". Des documents suspects dans le disque dur retrouvé
    ("charlotte.couslon@kryptkorp.org",),
    ("suspects" or 'bizzare', "documents"),
    ("decouvert" or "trouve", "documents", "disque", "dur")
  )
}


def check_message(message_content:list):
  for lock in scans.keys():
    if lock[0] in varia.unlocked: #si on a unlock le message
      i = 1
      for contents in scans[lock]: #on scan le content que l'on veut
        if i == 3: #si c'est le message content
          for word in contents: #si les mots que l'on veut
            if word.lower() in message_content[i].lower().split(): #son dans le content
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
  return None #c'est donc faux



def update_messagerie():
  for lock_needed in unlockable_messages:
    if lock_needed in varia.unlocked and not lock_needed in varia.messages.keys():
      varia.messages[lock_needed] = unlockable_messages[lock_needed]
    else:
      pass
  for lock in varia.messages:
    if lock not in varia.unlocked and lock in varia.messages.keys():
      varia.messages.pop(lock_needed)