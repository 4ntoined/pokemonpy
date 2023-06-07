#what if i made a class that had some functions to look at a pokemon battle in progress
#and make some determinations thereabout

class cpu:
    def __init__(self,battlefield):
        self.party = battlefield.cpus
        self.activemon = battlefield.cpu_mon
        self.enemymon = battlefield.usr_mon
        self.field = battlefield
        return

    def echo(self):
        print('echo')
        return

    def test1(self):
        print(self.activemon.name)
        return
