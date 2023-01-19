import math
import sys
from db_scripts import extract_existencia
import datetime


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
            self.height_cm = cm/100
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


class Gee:
    def __init__(self, name: str, location: str, horametro: str, autonomia: int) -> None:
        self.name = name
        self.location = location
        self.horametro = horametro
        self.autonomia = autonomia

    def operacion(self, tipo: str, hora_inicial: str, consumo: int, horametro_roto: bool, hora_final: str = '00:00', horametro_final: str = '0'):
        try:
            hora_inicial_formateada = datetime.datetime.strptime(
                hora_inicial, '%H:%M')

        except ValueError:
            return f'La entrada {hora_inicial} no es una hora valida'

        if horametro_roto:
            try:
                hora_final_formateada = datetime.datetime.strptime(
                    hora_final, '%H:%M')

            except ValueError:
                return f'La entrada {hora_final} no es una hora valida'

            segundos_trabajados = hora_final_formateada - hora_inicial_formateada

        else:
            horametro_inicial_parseado = self.horametro.split('.')
            horametro_final_parseado = horametro_final.split('.')

            horametro_final_formateado = datetime.timedelta(hours=int(
                horametro_final_parseado[0]), minutes=int(horametro_final_parseado[1]))

            horametro_inicial_formateado = datetime.timedelta(hours=int(
                horametro_inicial_parseado[0]), minutes=int(horametro_inicial_parseado[1]))

            segundos_trabajados = horametro_final_formateado - horametro_inicial_formateado

        hora_final = hora_inicial_formateada + segundos_trabajados

        tiempo_horas = round(segundos_trabajados.total_seconds()/3600, 2)
        if tiempo_horas < 0:
            return 'La entrada que define el tiempo trabajado es menor que la marca inicial'

        consumo_por_hora = consumo / tiempo_horas

        if consumo_por_hora > self.autonomia:
            sobreconsumo = True

        else:
            sobreconsumo = False

        if tipo == 'PS':
            energia_generada = 0
            demanda_liberada = 0

        else:
            energia_generada = consumo * 3
            demanda_liberada = round(energia_generada / tiempo_horas, 2)

        dicc = {
            'tipo': tipo,
            'tiempo_horas': tiempo_horas,
            'hora_final': hora_final.time().isoformat(timespec='minutes'),
            'energia_generada': energia_generada,
            'demanda_liberada': demanda_liberada,
            'consumo': consumo,
            'sobreconsumo': sobreconsumo,
        }
        return dicc

    def __str__(self) -> str:
        return self.name
