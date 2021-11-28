Files = {'C:':{
          'Utilisateurs':{
                    'Agent Doe':{
                              'Fichiers': {
                                        'Travail' : {
                                                  'Rapport-Delta056.odt':[
                                                            'Rapport Delta 056',
                                                            'Auteur: Agent Delta',
                                                            'Sur les dangers du groupement Armadilo',
                                                            'I. Controlle de la chaine Cluster-2',
                                                            'Niveau : Extremement Elevé'
                                                  ],
                                                  'Manuel entretien.pdf':[
                                                            'Manuel de redemmarage du robot:',
                                                            'Etape 1: Redemarrer le programme',
                                                            'Etape 2: Relancer les tests',
                                                            'Etape 3: Donner les instructions']
                                                  },
                                        'Personnel' : {
                                                  'Famille.png' : 'Famille.png'
                                                  }
                                        },
                              'Telechargements':{
                                        '9348-598-g5h9.jpg':'9348-598-g5h9.jpg',
                                        'Cow_laugh.mp3':'Cow_laugh.mp3',
                                        'fake-virus.exe':[
                                          'YOU HAVE BEEN HACKED',
                                          '--------------------',
                                          'Please pay the needed amount or all your files will be deleted',
                                          'Payment methods',
                                          '-Credit Card',
                                          '-Cash',
                                          '-Kidney transfer',
                                          'If you shut down your computer, it will self destruct !'
                                        ],
                                        'flat-earth-manifest.pdf':[
                                          'The Flat Earth Society Manifest',
                                          '------------------------------',
                                          'The earth is flat'
                                          ]},
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
          'Program Files':{
                    'chrome.exe':'<',
                    'insert-platformer-simulation-name.exe':'<'}
          }
        }

def explore_file(file_path:str = 'C:/Utilisateurs/Agent Doe/Fichiers:Manuel entretien.pdf/'):
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
    except KeyError or TypeError:
      directory = Files
  
  return directory_content