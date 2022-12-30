import math
import sys


class Tank:
    def __init__(self, location, radio, large, capacity):
        self.location = location
        self.radio = radio
        self.large = large
        self.capacity = capacity
        self.stock = 0


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

        volume = area * self.large * 1000

        self.stock = round(volume, 1)
        return self.stock
    
    def percent(self):
        percent = self.stock/self.capacity
        return percent*100
        
    def __str__(self):
        return self.location