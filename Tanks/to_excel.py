import pandas as pd
from datetime import datetime
import os
import shutil
import locale
from db_main import update_gee


def write_to_excel(data: dict):

    print(locale.getlocale())

    data['gee'].horametro = data['horametro_final']
    update_gee(data['gee'])

    fecha = datetime.strptime(data['fecha'], '%d/%m/%y')
    month = fecha.strftime('%B')
    year = fecha.strftime('%Y')

    if not os.path.isdir(f'./exports/{year}/'):
        os.mkdir(f'./exports/{year}')

    PATH = f'./exports/{year}/anexo 1 {month} Las Morlas-Villa Cuba.xlsx'


    if not os.path.isfile(PATH):
        shutil.copy2('excel/anexo 1 plantilla.xlsx', PATH)


    sheet = data['gee'].location

    df = pd.DataFrame(pd.read_excel(PATH,
                                    sheet_name=sheet))

    row_to_append = {
        'D': fecha.day,
        'M': fecha.month,
        'A': fecha.year,
        'TIPO': data['tipo'],
        'HORA INICIAL': data['hora_inicial'],
        'HORA FINAL': data['hora_final'],
        'HORAMETRO INICIAL': data['horametro_inicial'],
        'HORAMETRO FINAL': data['horametro_final'],
        'Tiempo trabajado HORAS': data['tiempo_horas'],
        'Demanda Liberada (KW)': data['demanda_liberada'],
        'Energía Generada (KW-h)': data['energia_generada'],
        'Combustible Consumido (Lts)': data['consumo'],
        'Existencia final': data['gee'].tank.stock,
        'Observaciones': 'Reporte No.'
    }

    if sheet == 'Villa Cuba':
        row_to_append['GEE'] = data['gee']

    serie = pd.Series(row_to_append)

    new_df = pd.concat([df, serie.to_frame().T])

    with pd.ExcelWriter(
        PATH,
        engine='openpyxl',
        mode='a',
        if_sheet_exists='replace',
    ) as writer:
        new_df.to_excel(writer, sheet_name=sheet, index=False)
