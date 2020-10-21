#here we go
#companion to pokemon.py
#Antoine Washington
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17

import astropy.table as tbl
#import numpy as np

moremon=[
        ('Bulbasaur',45,49,49,65,65,45,3,7),
        ('Ivysaur',60,62,63,80,80,60,3,7),
        ('Venusaur',80,82,83,100,100,80,3,7),
        ('Charmander',39,52,43,60,50,65,1,20),
        ('Charmeleon',58,64,58,80,65,80,1,20),
        ('Charizard',78,84,78,109,85,100,1,9),
        ('Squirtle',44,48,65,50,64,43,2,20),
        ('Wartortle',59,63,80,65,80,58,2,20),
        ('Blastoise',79,83,100,85,105,78,2,20),
        ('Starmie',60,75,85,100,85,115,2,10),
        ('Lugia',106,90,130,90,154,110,10,9),
        ('Ho-oh',106,130,90,110,154,90,1,9)

        ]

dex=tbl.Table(rows=moremon,names=('name','hp','at','de','sa','sd','sp','type1','type2'),dtype=('U16','i4','i4','i4','i4','i4','i4','i4','i4'))
indie=tbl.Column(range(0,len(dex)),dtype='i4')
dex.add_column(indie,index=0,name='index')

moretype=[
        ('Normal',0),
        ('Fire',1),
        ('Water',2),
        ('Grass',3),
        ('Electric',4),
        ('Ice',5),
        ('Fighting',6),
        ('Poison',7),
        ('Ground',8),
        ('Flying',9),
        ('Psychic',10),
        ('Bug',11),
        ('Rock',12),
        ('Ghost',13),
        ('Dragon',14),
        ('Dark',15),
        ('Steel',16),
        ('Fairy',17),
        ('Typeless',18) #mostly just for struggle, which does neutral damage to everyone
        ]

types=tbl.Table(rows=moretype,names=('type','index'),dtype=('U12','i4'))