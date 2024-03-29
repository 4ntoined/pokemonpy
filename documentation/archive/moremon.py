#
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
#ground 8,flying 9,psychic 10,bug 11,rock 12,ghost 13,dragon 14,
#dark 15,steel 16,fairy 17

import numpy as np
typeStrings=["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy","Typeless"]
index,names,gens,type1,type2,hp,at,de,sa,sd,sp,tot=np.loadtxt("list800.csv",dtype="U140",delimiter=",",skiprows=1,unpack=True,comments="%")
type2=[i.split()[0] for i in type2]
#i need name, stats, and types
for i in range(len(type1)):
    for j in range(len(typeStrings)):
        if type1[i]==typeStrings[j]: #when text matches, take down the type number
            type1[i]=j
        if type2[i]==typeStrings[j]:
            type2[i]=j
    if type2[i]=="Unknown":
        type2[i]=20 #may one day turn this into nan...not today though
ofile=open("somemons.dat","w")
for i in range(len(names)):
    ofile.write(f"{i},{names[i]},{hp[i]},{at[i]},{de[i]},{sa[i]},{sd[i]},{sp[i]},{type1[i]},{type2[i]}\n")
ofile.close()

