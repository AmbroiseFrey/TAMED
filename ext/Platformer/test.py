dictMap = { 1:[
  ['000000000000000000000000000'],
  ['000000000000000000100000000'],
  ['000000000000000011111000000'],
  ['000000000000011111111110000'],
  ['111111111111111111111111111'],
]
}

def decode(map):
  '''
  Le sol est un carré de 10*10 px 1 represente un carré, 0 le vide
  '''
  x = 0
  y = 0
  for el in map:
    x += 600
    environment = map[el]
    for el1 in environment:
      y += 10
      line = environment[el1]
      for c in line:
        if c == '0':
          x += 10
        elif c == '1':
          #ici on rajoute le sprite du sol en 10*10
          x +=10


    
    