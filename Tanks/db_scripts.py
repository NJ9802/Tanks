import sqlite3


def update_existencia(tank, existencia_actual, height_cm):

    try:

        # Conectar a la base de datos
        bd = sqlite3.connect("combustible.db")
        cursor = bd.cursor()

        # Sentencia para actualizar
        sentencia1 = "UPDATE tanks SET existencia = ? WHERE location = ?;"
        sentencia2 = "UPDATE tanks SET height_cm = ? WHERE location = ?;"

        location = tank.location

        # Actualizar datos
        cursor.execute(sentencia1, (existencia_actual, location))
        cursor.execute(sentencia2, (height_cm, location))

        bd.commit()

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)


def extract_existencia(tank):

    try:

        # Conectar a la base de datos
        bd = sqlite3.connect("combustible.db")
        cursor = bd.cursor()

        location = (tank.location,)
        cursor.execute('SELECT * FROM tanks WHERE location=?', location)
        row = cursor.fetchone()
        datos = {
            'stock': float(row[1]),
            'height_cm': row[2],
        }
        return datos

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

def check_darkmode():
    try:

        # Conectar a la base de datos
        bd = sqlite3.connect("combustible.db")
        cursor = bd.cursor()

        cursor.execute('SELECT dark FROM darkmode;')
        dark = cursor.fetchone()[0]
        return dark

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

def update_darkmode(dark):
    try:

        # Conectar a la base de datos
        bd = sqlite3.connect("combustible.db")
        cursor = bd.cursor()

        # Sentencia para actualizar
        sentencia1 = "UPDATE darkmode SET dark = ?;"


        # Actualizar datos
        cursor.execute(sentencia1, (str(dark)))

        bd.commit()

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)

