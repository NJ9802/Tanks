from models import Tank, sys, Gee

from db_scripts import update_existencia, extract_existencia



villa_cuba = Tank('Villa Cuba', 1.8969469/2, 7.558, 21359)
casas =Tank('Las Casas', 0.707, 6.068, 9529)
morlas = Tank('Las Morlas', 0.707, 6.108, 9592)

mt_487 = Gee('MT-487', 'Villa Cuba', '1112.30', 58)
mt_488 = Gee('MT-488', 'Villa Cuba', '197.30', 58)
mt_489 = Gee('MT-489', 'Villa Cuba', '1212.30', 58)
mt_443 = Gee('MT-443', 'Las Casas', 'Roto', 70)
mt_452 = Gee('MT-452', 'Las Morlas', 'Roto', 65)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        
        

        if sys.argv[1] == 'vc':
            existencia_anterior = extract_existencia(villa_cuba)
            volume = round(villa_cuba.volume()*1000, 1)

            
            consumo = round(existencia_anterior-volume)

        
        
            print('-------------------------------------')
            print(f'Quedan {volume} litros')
            print(f'Consumo: {consumo} litros')

            update_existencia(villa_cuba, volume)


        
        elif sys.argv[1] == 'cs':
            existencia_anterior = extract_existencia(casas)
            volume = round(casas.volume()*1000, 1)
            
            consumo = round(existencia_anterior-volume)

        
        
            print('-------------------------------------')
            print(f'Quedan {volume} litros')
            print(f'Consumo: {consumo} litros')

            update_existencia(casas, volume)
        
        elif sys.argv[1] == 'mo':
            existencia_anterior = extract_existencia(morlas)
            volume = round(morlas.volume()*1000,1)

            consumo = round(existencia_anterior-volume,1)

        
        
            print('-------------------------------------')
            print(f'Quedan {volume} litros')
            print(f'Consumo: {consumo} litros')

            update_existencia(morlas, volume)

        else:

            print('El argumento tiene que ser valido')
            sys.exit(1)

    elif len(sys.argv) == 1: 
        print(
'''
Ingrese las letras correspondientes al servicio como argumento:

Ejemplo:

Villa Cuba => "vc"
Las Casas => "cs"
Las Morlas => "mo"
'''             )
        sys.exit(1)

    else:
        print('Ingrese solamente un argumento')