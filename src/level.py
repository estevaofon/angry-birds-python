from characters import Pig
from polygon import Polygon


class Level():
    def __init__(self, pigs, columns, beams, space):
        self.pigs = pigs
        self.columns = columns
        self.beams = beams
        self.space = space
        self.number = []
        self.number_of_birds = 5
        #lower limit
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000
        self.no_more_level = False

    def build_0(self):
        """ Set up level 1"""
        pig1 = Pig(980, 100, self.space)
        pig2 = Pig(985, 182, self.space)
        self.pigs.append(pig1)
        self.pigs.append(pig2)
        p = (950, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1010, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 150)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (950, 200)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1010, 200)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 240)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 5
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000

    def build_1(self):
        """level 2"""
        pig1 = Pig(1000, 100, self.space)
        self.pigs.append(pig1)
        p = (900, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (850, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (850, 150)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1050, 150)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1105, 210)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4

    def build_2(self):
        """level 3"""
        pig1 = Pig(880, 180, self.space)
        self.pigs.append(pig1)
        pig2 = Pig(1000, 230, self.space)
        self.pigs.append(pig2)
        p = (880, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (880, 150)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1000, 80)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1000, 180)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1000, 210)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4

    def build_3(self):
        """level 3"""
        pig = Pig(950, 320, self.space)
        pig.life = 25
        self.pigs.append(pig)
        pig = Pig(885, 225, self.space)
        pig.life = 25
        self.pigs.append(pig)
        pig = Pig(1005, 225, self.space)
        pig.life = 25
        self.pigs.append(pig)
        p = (1100, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1070, 152)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1040, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (920, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (950, 152)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1010, 180)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (860, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (800, 100)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (830, 152)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (890, 180)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (860, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (920, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (1040, 223)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (890, 280)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (1010, 280)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (950, 300)
        self.beams.append(Polygon(p, 85, 20, self.space))
        p = (920, 350)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (980, 350)
        self.columns.append(Polygon(p, 20, 85, self.space))
        p = (950, 400)
        self.beams.append(Polygon(p, 85, 20, self.space))
        self.number_of_birds = 4
    def load_level(self, number):
        try:
            build_name = "build_"+str(number)
            getattr(self, build_name)()
        except AttributeError:
            self.no_more_level = True
