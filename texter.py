#gonna use this for my text-printing functions
#
def copyrigh(prespace = True):
    if prespace:    print('\nCopyright (C) 2024 Adarius')
    else:           print('Copyright (C) 2024 Adarius')
    print('This program comes with ABSOLUTELY NO WARRANTY.\n'+\
        'This is free software, and you are welcome to\n'+\
        'redistribute it under certain conditions.')
    return
def magic_head(txt='text',cha='=',long=32,spacing=' ',cha2=''):
    if not cha2: cha2 = cha
    oddd = long%2 == 1
    midline = magic_text(txt=txt,cha=cha,long=long,spacing=spacing,cha2=cha2)
    haf = long // 2
    lineL = genborder(num=haf,cha=cha)
    if oddd: lineR = genborder(num=haf+1,cha=cha2)
    else: lineR = genborder(num=haf,cha=cha2)
    line1 = lineL+lineR
    #line1 = genborder(num=long)
    ans = f"{line1}\n{midline}\n{line1}"
    return ans
def magic_text(txt='text',cha='=',long=32,spacing=' ',cha2=''):
    if not cha2: cha2 = cha
    summ = long-len(txt)-len(spacing) * 2
    od = summ % 2 == 1
    sidel = summ // 2
    if od: sider = sidel + 1
    else: sider = sidel
    border_l = genborder(num=sidel,cha=cha)
    border_r = genborder(num=sider,cha=cha2)
    ans = f"{border_l}{spacing}{txt}{spacing}{border_r}"
    return ans
def genborder(num=24,cha='='):
    star = ''
    inst = num // len(cha)
    for i in range(inst): star+=cha
    return star
#hey
if __name__ == '__main__':
    pass
else:
    pass

