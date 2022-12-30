import sqlite3

def update_existencia(tank, existencia_actual):


    try:
    
        #Conectar a la base de datos
        bd = sqlite3.connect("combustible.db")
        cursor = bd.cursor()
    
        #Sentencia para actualizar
        sentencia = "UPDATE tanks SET existencia = ? WHERE location = ?;"

        location = tank.location
        
        #Actualizar datos
        cursor.execute(sentencia, (existencia_actual, location))
        bd.commit()
        
    
    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)


def extract_existencia(tank):


    try:
    
        #Conectar a la base de datos
        bd = sqlite3.connect("combustible.db")
        cursor = bd.cursor()

        location = (tank.location,)
        cursor.execute('SELECT * FROM tanks WHERE location=?', location)
        return float((cursor.fetchone()[1]))

    except sqlite3.OperationalError as error:
        print("Error al abrir:", error)