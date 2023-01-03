import math
import sys
from db_scripts import extract_existencia

class TankException(Exception):
    pass

class Tank:
    def __init__(self, location, radio, large, capacity):
        self.location = location
        self.radio = radio
        self.large = large
        self.capacity = capacity
        self.stock = extract_existencia(self)['stock']
        self.height_cm = extract_existencia(self)['height_cm']


    def volume(self, cm):
        
        try:
            self.height_cm=cm/100
        except:
            print('La altura debe ser un numero')
            sys.exit(1)

        part1 = ((self.radio-self.height_cm)/self.radio)
        root = 2*self.radio*self.height_cm-self.height_cm**2
        part2 = (self.radio-self.height_cm)*math.sqrt(root)
        area = math.acos(part1)*self.radio**2-part2

        volume = area * self.large * 1000

        self.stock = round(volume, 1)
        self.height_cm *= 100
        self.height_cm = round(self.height_cm, 2)
        return self.stock
    
    def percent(self):
        percent = self.stock/self.capacity
        return percent*100
        
    def __str__(self):
        return self.location