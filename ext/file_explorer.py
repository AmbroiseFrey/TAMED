

Files = {'C:':{
          'Utilisateurs':{
                    'Agt.Doe':{
                              'Fichiers': {
                                        'Rapport.odt':[
                                          'Rapport',
                                          'Auteur: Agent Doe',],
                                        'Manuel entretien.pdf':[
                                          'Manuel d\'entretien du robot ____',
                                          'Etape 1: Redemarrer le programme',
                                          'Etape 2: Relancer les tests',
                                          'Etape 3: Donner les instructions'
                                          ]
                                        },
                              'Telechargements':{
                                        'Cow_laugh.mp3':'>',
                                        'fake-virus.exe':'>',
                                        '9348-598-g5h9.png':'>'},
                              'Coffre Fort [KRYPT CORP]': 'Acces Sécurisé',
                              'Musique':{
                                'La Totomobile.mp3':'>'
                              },
                              'Videos':{
                                'Remi - La Totomobile - clip officiel.mp4':'>',
                                'Boss qui tombe dans les escalier lol.mp4':'>',
                                'DeZoom Meeting - Session 124h9t8s Replay.mp4':'>'
                              }
                      }
                    },
          'Program Files':[
                    'chrome.exe',
                    'insert-platformer-simulation-name.exe']
          }
        }

def explore_file(file_path:str = 'C:/Utilisateurs/Agt.Doe/Fichiers:Manuel entretien.pdf/'):
  '''
  Fonction qui prend en argument un file path.
  Pour signaler un nouveau dossier on utilise / au lieu de \
  '''
  directory = ''
  directory_content= Files
  for i in range(len(file_path)):
    try:
      if file_path[i] != '/':
        directory += file_path[i]
      else:
        directory_content = directory_content[directory]
        directory = ''
    except KeyError:
      directory = Files
  
  return directory_content