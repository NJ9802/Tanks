from models import Tank, sys

from db_scripts import update_existencia, extract_existencia



villa_cuba = Tank('Villa Cuba', 1.8969469/2, 7.558)
casas =Tank('Las Casas', 0.707, 6.068)
morlas = Tank('Las Morlas', 0.707, 6.108)




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