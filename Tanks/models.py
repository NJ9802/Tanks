import math
import sys


class Tank:
    def __init__(self, location, radio, large):
        self.location = location
        self.radio = radio
        self.large = large

    def volume(self, cm):
        
        try:
            height=float(cm)/100
        except:
            print('La altura debe ser un numero')
            sys.exit(1)

        part1 = ((self.radio-height)/self.radio)
        root = 2*self.radio*height-height**2
        part2 = (self.radio-height)*math.sqrt(root)
        area = math.acos(part1)*self.radio**2-part2

        return area * self.large
    def __str__(self):
        return self.location