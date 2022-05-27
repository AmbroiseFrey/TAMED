from ext.Core import variables as varia
from ext.Core import operations as Opr

#Voir Dev Info.md pour infos sur le format des 'codes'

unlockable_messages = {
  2000 : {
    "Mission 2":[
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
    "Mission 3":[
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
    "Mission 3 validée":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Merci beaucoup pour votre aide.",
      "Continuez d'explorer la map et rends au prochain checkpoint.",
      "Une fois au checkpoint une analyse de l'air va etre fais automatiquement par le robot.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  4000 : {
    "Mission 4 ":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "L'analyse de l'air est terminée. Le but de cette prochaine analyse est de voir si l'air est ",
      "respirable pour l'humain, ainsi nous vérifions si la présence de molécules cyanures ",
      "d'hydrogène est acceptable pour l'humain. A vous de trouver dans les fichiers où se situent ",
      "les résultats et de compter combien de molécules de cyanure d'hydrogène sont  ",
      "présent dans l'analyse. Cette molécule est constiué dans l'ordre suivant: un atome ",
      " d'azote (en bleue), un atome de carbone (en noir), un atome d'hydrogène (en blanc). Une molécule ",
      "peut etre horizontale, verticale et on ne peut pas compter un même atome dans deux molécules.",
      "Envoiez nous le nombre le molécules par mail !",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  4010 : {
    "Mission 4 validée":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Merci pour votre analyse. D'après nos espères l'air est respirable!",
      "Votre prochaine mission est de determiner le nombre de cristaux de pyrite mais.",
      "je reviendrais vers vous sur ça plus tard. Continuez d'explorer la planète jusqu'au prochain checkpoint.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  5000 : {
    "Mission 5":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Pour pouvoir potentiellement habiter la planète il nous faut imperativement",
      "de la matière première, surtout du fer (pour construire une première base",
      "sur la planète). D'après les analyses faites par le Colonel Thompson, il",
      "n'a trouvé aucune trace de fer à l'état brut. Mais nous avons remarqué grace à",
      "une photo aérienne la présence de crystaux de Pyrite. Ce crystal à la ",
      "particuliarité d'avoir une forme cubique, mais surtout de contenir du fer. Nous",
      "vous demandons de chercher dans les fichiers la photo prise par le robot, et de",
      "compte le nombre de bloc de crystal de Pyrite (et de nous l'envoyer).",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  5010 : {
    "Mission 5 réussi":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Merci pour vos résultat! Continuez de te balader vers le prochain checkpoint.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  6000 : {
    "Alert !!! - Mission 6":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Nous avons reçue un message d'alerte venant du robot.",       "Un fichier système vital pour piloter le robot est corrompu !",
      "Cherchez dans les fichiers le ficher decodevirus.exe et ouvrez le.",
      "Normalement le fichier va directement s'ouvrir en mode récuperation.",
      "La lettre E montre un bloc saint et la lettre F un bloc corrompu.",
      "Vous devez donc compter le nombre de F présent dans le fichier et nous l'envoyer par mail.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  6010 : {
    "Mission 6 réussi":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Le fichier est réparé !!! Baladez vous encore jusqu'au dernier checkpoint.",
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  },
  7000 : {
    "Mission terminé":[
      "from: Gen. Michael Fredlyn ",
      "to: Group:TAMED",
      "Bonjour Mr. Doe,",
      "Merci beaucoup pour votre participation. Après analyse, la planète est habitable.",
      "Vous avez fait un excellent travail Mr John Doe"
      "Cordialement,",
      "Gen. Michael Fredlyn"
    ],
  }
}
  

scans = {
  (1010,2000):( #premier email a envoyer quand l'on retrouve le disque dur
    ("Group:TAMED" or "gen. michael Fredlyn",),
    ("NONE",),
    ('disque', 'dur')
  ),
  (1010,10):( #deuxieme mail Des documents suspects dans le disque dur retrouvé
    ("charlotte.coulson@kryptkorp.org",),
    ("NONE",),
    ("document",)
  ),
  (4000,4010):( # 4 eme mail a envoyer
  ("Group:TAMED",),
  ("NONE",),
  ("9",)
  ),
  (5000,5010):( # 5 eme mail a envoyer
  ("Group:TAMED",),
  ("NONE",),
  ("90",)
  ),
  (6000,6010):( # 6 eme mail a envoyer
  ("Group:TAMED",),
  ("NONE",),
  ("16",)
  )
}


def check_message(message_content:list):
  message_content = message_content[1:4] # garde les parties importantes
  print(message_content)
  for lock in scans.keys():
    if lock[0] in varia.unlocked: #si on a unlock le message
      i = 0
      for contents in scans[lock]: # pour chaque partie du message que l'on veut
        print(lock, contents)
        print(Opr.textData_str(message_content[i]).lower().split())
        if i == 2: #si c'est le message content
          for word in contents: #si les mots que l'on veut
            if word.lower() in Opr.textData_str(message_content[i]).lower().split(): #son dans le content
              return lock[1] #alors c'est bon 
            break # failed
        else:
          for word in contents: #si les mots que l'on veut
            if word.lower() in Opr.textData_str(message_content[i]).lower().split() or word == "NONE": #son dans le titre ou ne sont pas necessaire
              i+= 1 #alors c'est bon
            else:
              break # failed
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