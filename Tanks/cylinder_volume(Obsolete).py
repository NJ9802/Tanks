from models import Tank, Gee, Darkmode

from db import *

darkmode = session.query(Darkmode).filter_by(id=1).first()

villa_cuba = session.query(Tank).filter_by(location='Villa Cuba').first()
casas =session.query(Tank).filter_by(location='Las Casas').first()
morlas = session.query(Tank).filter_by(location='Las Morlas').first()

mt_487 = session.query(Gee).filter_by(name='MT-487').first()
mt_488 = session.query(Gee).filter_by(name='MT-488').first()
mt_489 = session.query(Gee).filter_by(name='MT-489').first()
mt_443 = session.query(Gee).filter_by(name='MT-443').first()
mt_452 = session.query(Gee).filter_by(name='MT-452').first()

all_gee = session.query(Gee).all()
all_tanks = session.query(Tank).all()
#[villa_cuba, casas, morlas]
# if __name__ == '__main__':

#     if len(sys.argv) == 2:
        
        

#         if sys.argv[1] == 'vc':
#             existencia_anterior = extract_existencia(villa_cuba)
#             volume = round(villa_cuba.volume()*1000, 1)

            
#             consumo = round(existencia_anterior-volume)

        
        
#             print('-------------------------------------')
#             print(f'Quedan {volume} litros')
#             print(f'Consumo: {consumo} litros')

#             update_existencia(villa_cuba, volume)


        
#         elif sys.argv[1] == 'cs':
#             existencia_anterior = extract_existencia(casas)
#             volume = round(casas.volume()*1000, 1)
            
#             consumo = round(existencia_anterior-volume)

        
        
#             print('-------------------------------------')
#             print(f'Quedan {volume} litros')
#             print(f'Consumo: {consumo} litros')

#             update_existencia(casas, volume)
        
#         elif sys.argv[1] == 'mo':
#             existencia_anterior = extract_existencia(morlas)
#             volume = round(morlas.volume()*1000,1)

#             consumo = round(existencia_anterior-volume,1)

        
        
#             print('-------------------------------------')
#             print(f'Quedan {volume} litros')
#             print(f'Consumo: {consumo} litros')

#             update_existencia(morlas, volume)

#         else:

#             print('El argumento tiene que ser valido')
#             sys.exit(1)

#     elif len(sys.argv) == 1: 
#         print(
# '''
# Ingrese las letras correspondientes al servicio como argumento:

# Ejemplo:

# Villa Cuba => "vc"
# Las Casas => "cs"
# Las Morlas => "mo"
# '''             )
#         sys.exit(1)

#     else:
#         print('Ingrese solamente un argumento')