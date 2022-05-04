from ext.Core import variables as varia
from ext.Core import operations as Opr

#Voir Dev Info.md pour infos sur le format des 'codes'

unlockable_messages = {
  10 :{
    'Unlock Charlotte 2':[
      'from: ',
      'to: '
    ]
  },
  2000 : {
    "TAMED Mission - 2":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour,",
      "Merci d'avoir récupéré le disque dur, il va nous etre très utile!",
      "Il faut maintenant que vous récupériez un morceau de la planète pour l'analyser et savoir si elle est",
      "habitable."
    ],
  },
  1010 : {
    "Accident de la Station":[
      "from: Charlotte Coulson",
      "to: John Doe",
      "Bonjour Mr. Doe,",
      "Je suis Charlotte Coulson et j'ai travaillé sur le projet Zeus:",
      "Il consistait à rendre opérationnel une station qui orbitait autour de Kepler-272 Alpha, pour ensuite",
      "verifier si la planète Kepler-272 Alpha est habitable.",
      "Malheuresement tu n'es pas le premier à tenter cette mission, Colonel Tompson l'à lui même tentée,",
      "mais sa station s'est écrasé dans des circonstances inconnues.",
      "Peut tu regaarder les fichiers que tu as recuperé pour verifier s'il n'y a pas quelque chose qui cloche?",
      "Verfie les logs de la station."
    ],
  },
    3000 : {
    "Mission 2":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "En analysant le disque dur de Colonel Thompson nous avons identifié un fichier qui pourrait nous aider. Il y a dedans le résultat d'une de ses analyses.",
      "Ce fichier est sous le format '.bin'.",
      "Trouves le dans les fichiers et décrypte le grace au site 'www.binaire.it'.",
      "Bonne chance, je vous recontacte quand on a du nouveau.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  3010 : {
    "Mission 2 validée":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Merci beaucoup pour votre aide.",
      "Continues d'explorer la map et rends au prochain checkpoint.",
      "Une fois au checkpoint une analyse de l'air va etre fais automatiquement par le robot.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  4000 : {
    "Mission 3 ":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "L'analyse de l'air est temrinée. Le but de cette analytse est de voir si l'air est ",
      "respirable pour l'humain, ainsi nous vérifions si la présence de molécules cyanures ",
      "d'hydrogène est acceptable pour l'humain. A toi de trouver dans les fichiers où se situent ",
      "les résultats et de compter combien de molécules de cyanure d'hydrogène sont  ",
      "présent dans l'analyse. Cette molécule est constiué dans l'ordre suivant: un atome ",
      " d'azote (en bleue), un atome de carbone (en noir), un atome d'hydrogène (en blanc). Une molécule ",
      "peut etre horizontale, verticale, et en diagonal.",
      "Envoies nous de nombre le molécules par mail !!!",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  4010 : {
    "Mission 3 validée":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Merci pour ton analyse. D'après nos espères l'air est respirable!",
      "Ta prochaine mission est de determiner le nombre de cristaux de pyrite mais.",
      "on reviendras vers toi sur ça plus tard. Continues d'explorer la map jusqu'au prochain checkpoint.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  5000 : {
    "Mission 4":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Pour pouvoir potentiellement habiter la planète il nous faut imperativement",
      "de la matière première, surtout du fer (pour construire une première base",
      "sur la planète). D'après les analyses faites par le Colonel Thompson, il",
      "n'a trouvé aucune trace de fer à l'état brut. Mais nous avons remarqué grace à",
      "une photo aérienne la présence de crystaux de Pyrite. Ce crystal à la ",
      "particuliarité d'avoir une forme cubique, mais surtout de contenir du fer. Nous",
      "te demandons de chercher dans les fichiers la photo prise par le robot, et de",
      "compte le nombre de bloc de crystal de Pyrite (et de nous l'envoyer).",
      "Cordialement,",
      "Gen. Michael Fredlyn"
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
    ("charlotte.coulson@kryptkorp.org" or 'Charlotte' or 'coulson',),
    ("documents" or 'document' or 'log',),
    ("documents" or 'document' or 'file' or 'log')
  ),
  (4000,4010):(
  ("Group:TAMED" or "gen. michael Fredlyn",),
  ("NONE"),
  ("10")
  )
}


def check_message(message_content:list):
  message_content = message_content[:2]
  print(message_content)
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
            if word.lower() in Opr.textData_str(message_content[i]).lower().split() or "NONE" in Opr.textData_str(message_content[i]).lower().split(): #son dans le titre ou ne sont pas necessaire
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