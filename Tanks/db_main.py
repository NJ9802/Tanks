from db import *
from models import Tank, Gee, Darkmode


def ingresar_data():
    villa_cuba = Tank('Villa Cuba', 1.8969469/2, 7.558, 21359, 5000, 90.00, 189)
    casas = Tank('Las Casas', 0.707, 6.068, 9529, 5000, 90.00, 141)
    morlas = Tank('Las Morlas', 0.707, 6.108, 9592, 5000, 90.00, 141)
    mt_487 = Gee('MT-487', 'Villa Cuba', '1112.30', 58, 16, False)
    mt_488 = Gee('MT-488', 'Villa Cuba', '197.30', 58, 16, False)
    mt_489 = Gee('MT-489', 'Villa Cuba', '1212.30', 58, 16, False)
    mt_443 = Gee('MT-443', 'Las Casas', 'Roto', 70, 24, True)
    mt_452 = Gee('MT-452', 'Las Morlas', 'Roto', 65, 12, True)

    session.add(Darkmode(on=False))

    all_gee = [mt_487, mt_488, mt_489, mt_443, mt_452]

    villa_cuba.gees.extend(all_gee[:3])
    casas.gees.append(mt_443)
    morlas.gees.append(mt_452)

    session.add_all(all_gee)
    session.add_all([villa_cuba, casas, morlas])

    session.commit()


def update_darkmode(state: bool):
    session.query(Darkmode).filter_by(id=1).update({Darkmode.on: state})
    session.commit()


def update_stock(tank: Tank):
    session.add(tank)

    session.commit()

def update_gee(gee: Gee):
    session.add(gee)
    session.commit()
    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("¡Creación exitosa de la tabla productos!\n")
    ingresar_data()

darkmode = session.query(Darkmode).filter_by(id=1).first()
all_gee = session.query(Gee).all()
all_tanks = session.query(Tank).all()
