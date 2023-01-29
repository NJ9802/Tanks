import math
import datetime

from db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Tank(Base):
    __tablename__ = 'tanks'

    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    radio = Column(Float, nullable=False)
    large = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    stock = Column(Float, nullable=False)
    height_cm = Column(Float)
    max_height = Column(Float, nullable=False)
    gees = relationship('Gee', back_populates='tank')

    def __init__(self, location: str, radio: float, large: float, capacity: float,
                 stock: float, height_cm: float, max_height: int):
        self.location = location
        self.radio = radio
        self.large = large
        self.capacity = capacity
        self.stock = stock
        self.height_cm = height_cm
        self.max_height = max_height

    def volume(self, cm):

        if cm > self.max_height:
            return f'Capacidad maxima excedida\nMedicion maxima {self.max_height} cm'
        
        self.height_cm = cm/100

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

    def __repr__(self):
        return f"Tanque({self.location}, {self.stock}, {self.height_cm})"

    def __str__(self):
        return f'Tanque de {self.location}'


class Gee(Base):

    __tablename__ = 'gee'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    horametro = Column(String, nullable=False)
    autonomia_cc = Column(Integer, nullable=False)
    autonomia_sc = Column(Integer, nullable=False)
    horametro_roto = Column(Boolean, nullable=False)
    tanks_id = Column(Integer, ForeignKey('tanks.id'))
    tank = relationship('Tank', back_populates='gees')

    def __init__(self, name: str, location: str, horametro: str, autonomia_cc: int, autonomia_sc: int, horametro_roto: bool) -> None:
        self.name = name
        self.location = location
        self.horametro = horametro
        self.autonomia_cc = autonomia_cc
        self.autonomia_sc = autonomia_sc
        self.horametro_roto = horametro_roto

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
                horametro_final = 'Roto'

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

        if tipo == 'PS':
            energia_generada = 0
            demanda_liberada = 0
            autonomia = self.autonomia_sc

        else:
            energia_generada = consumo * 3
            demanda_liberada = round(energia_generada / tiempo_horas, 2)
            autonomia = self.autonomia_cc

        consumo_por_hora = consumo / tiempo_horas

        if consumo_por_hora > autonomia:
            sobreconsumo = True

        else:
            sobreconsumo = False

        processed_data = {
            'gee': self,
            'tipo': tipo,
            'horametro_inicial': self.horametro,
            'horametro_final': horametro_final,
            'tiempo_horas': tiempo_horas,
            'hora_inicial': hora_inicial,
            'hora_final': hora_final.time().isoformat(timespec='minutes'),
            'energia_generada': energia_generada,
            'demanda_liberada': demanda_liberada,
            'consumo': consumo,
            'sobreconsumo': sobreconsumo,
        }
        return processed_data

    def __repr__(self):
        return f"GEE({self.name}, {self.location}, {self.horametro}, {self.autonomia})"

    def __str__(self) -> str:
        return self.name


class Darkmode(Base):
    __tablename__ = 'dark'
    id = Column(Integer, primary_key=True)
    on = Column(Boolean, nullable=False)
