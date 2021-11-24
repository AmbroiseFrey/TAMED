Files = {'C':{
          'Utilisateurs':{
                    'Agt.Doe':{
                              'Fichiers': [
                                        'Rapport.odt',
                                        'Manuel entretien.pdf'],
                              'Telechargements':[
                                        'Cow_laugh.mp3',
                                        'fake-virus.exe'
                                        '9348-598-g5h9.png'],
                              'Coffre Fort': 'Acces Sécurisé'
                              }
                    },
          'Program Files':[
                    'chrome.exe',
                    'insert-platformer-simulation-name.exe']
          }
        }

def explore_file(file_path:str = 'C:Utilisateurs:Agt.Doe:Fichiers:'):
  '''
  Fonction qui prend en argument un file path.
  Pour signaler un nouveau dossier on utilise : au lieu de \
  '''
  directory = ''
  directory_content= Files
  for i in range(len(file_path)):
    if file_path[i] != ':':
      directory += file_path[i]
    else:
      directory_content = directory_content[directory]
      directory = ''
      print('New folder')
  
  return directory_content

