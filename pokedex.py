#here we go
#companion to pokemon.py
#Antoine Washington
import astropy.table as tbl
import numpy as np

poke1=('Bulbasaur',45,49,49,65,65,45,3,7)
poke2=('Ivysaur',60,62,63,80,80,60,3,7)
pokedex=tbl.Table(rows=(poke1,poke2),names=('name','hp','at','de','sa','sd','sp','type1','type2'))

print(pokedex)
