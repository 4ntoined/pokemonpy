#companion to pokemon.py
"""
Copyright (C) 2023 Adarius
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
#normal 0,fire 1,water 2,grass 3,electric 4,ice 5,fighting 6,poison 7,
#ground 8,flying 9,psychic 10,bug 11, #rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17
# import some packages
import numpy as np


def pokedexer(pokedexpath):
    dats = np.loadtxt(pokedexpath,delimiter=",",dtype='U20')
    # make it a list
    datl = dats.tolist()
    # make it a list of tuples not list of lists
    datt = [ tuple(i) for i in datl ]
    dtyp = np.dtype( [('index','i4'),('name','U20'),('hp','i4'),('at','i4'),('de','i4'),('sa','i4'),('sd','i4'),('sp','i4'),('type1','i4'),('type2','i4')  ] )
    dexx = np.array( datt, dtype=dtyp )
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
    typess=np.array(moretype,dtype=dtip)
    return (dexx, typess)
#dexpath = "./somemons.dat"
#dex, types = pokedexer(dexpath)

if __name__ == '__main__':
    #np.save('saved_dexpoke.npy', dex)
    pass
else:
    pass
