Files ={
'C:':{
  'Utilisateurs':{
    'Agent Doe':{
      'Fichiers': {
        'Travail' : {
          'Rapport-Delta056.odt':[
            'Rapport Delta 056',
            'Auteur: Delta',
            'A destination de: Joint Military Technology Department - Europe',
            '[Redacted]',
            '[Redacted]',
            'Niveau : Extremement Elevé'
            ],
          'Manuel entretien.pdf':[
            'Manuel de redémmarage du robot:',
            'Etape 1: Redémarrer le programme',
            'Etape 2: Relancer les tests',
            'Etape 3: Donner les instructions'
            ],
          'codes.bin':[
            '01001111 01110000 01100101 01110010 01100001 01110100',
            '01101001 01101111 01101110 00100000 01000011 01100001',
            '01101100 01111001 01110000 01110011 01101111 00100000',
            '00101101 00100000 01010100 01001111 01010000 00100000',
            '01010011 01000101 01000011 01010010 01000101 01010100',
            '00001010 00101101 00110000 00110011 00111010 00110010',
            '**Error**: Data not found'
            ],
          'Identification_Card.png' : 'Identification_Card.png',
        },
        'Personnel' : {
            'Famille.png' : 'Famille.png',
            'Addresse.odt' : 'Things'}
        },
        'Telechargements':{
          '9348-598-g5h9.jpg':'9348-598-g5h9.jpg',
          'Cow_laugh.mp3':'Cow_laugh.wav',
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
            'The Earth is flat'
            ],
        },
        'Coffre Fort [KRYPT CORP]': [
          'Accès Sécurisé',
          'Veuillez vous reconnecter sur www.kryptcorp.org'
          ],
        'Musique':{
          'La Totomobile.mp3':'>',
          'Chandelier - Sia.mp3':'>',
          'Never Gonna Give You Up - Rick Astley.mp3':'>',
        },
        'Videos':{
          'Personel' : {
            'Boss qui tombe dans les escaliers lol.mp4':'Boss qui tombe dans les escaliers lol.mp4',
          },
          'Clips de Musique' : {
            'Remi - La Totomobile - clip officiel.mp4':'Remi - La Totomobile - clip officiel.mp4',
          },
          'Travail':{
            'DeZoom Meeting - Session 124h9t8s Replay.mp4':'>'
          },
        },
      },
    'Administrateur':{
      'Magma-Wall' : {
        'Magma-Wall.txt':[
          'Magam Wall v3.2.6 - Premium[Max Security]',
          'High performance firewall developped by Krypt Corp',
          'Includes Internet, Files and E-Mail scanners',
          'Note: Your version includes:',
          '- Complex defence, attack and counter-attack hack systems',
          '- Computer lockdown and file auto destruction'
          ],
      'pc-lockdown.exe' : '>',
      'source-code':'This action requires access to Project: Magma Wall',
      }
    },
  },
  'Program Files':{
    'chrome.exe':'<',
    'tamed.exe':'tamed.exe',
    'snake.py': 'snake.py'
  },
},
}

def explore_file(file_path:str = 'PC/C:/Utilisateurs/Agent Doe/Fichiers:Manuel entretien.pdf/'):
  '''
  Fonction qui prend en argument un file path.
  Pour signaler un nouveau dossier on utilise / au lieu de \
  '''
  directory = ''
  directory_content= Files
  for i in range(len(file_path)):
    try:
      assert type(directory_content) == dict, "Directory must be a dictionary"
      if file_path[i] != '/':
        directory += file_path[i]
      else:
        directory_content = directory_content[directory]
        directory = ''
    except:
      directory = Files
      return False
  
  return directory_content