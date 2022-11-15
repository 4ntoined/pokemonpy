#here we go
#companion to pokemon.py
#Antoine
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
# import some packages
import numpy as np
# import the pokemon from database
dats = np.loadtxt("somemons.dat",delimiter=",",dtype='U20')
# make it a list
datl = dats.tolist()
# make it a list of tuples not list of lists
datt = [ tuple(i) for i in datl ]
dtyp = np.dtype( [('index','i4'),('name','U20'),('hp','i4'),('at','i4'),('de','i4'),('sa','i4'),('sd','i4'),('sp','i4'),('type1','i4'),('type2','i4')  ] )
dex = np.array( datt, dtype=dtyp )
# type table, useless I think
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
dtip = np.dtype( [('type','U12'),('index','i4') ] )
types=np.array(moretype,dtype=dtip)
if __name__ == '__main__':
    np.save('saved_dexpoke.npy', dex)
else:
    pass
