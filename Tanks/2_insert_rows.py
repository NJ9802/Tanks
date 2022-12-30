import sqlite3
try:
	bd = sqlite3.connect("combustible.db")
	cursor = bd.cursor()
	tanks = [
		"""
		INSERT INTO tanks
		(location, existencia)
		VALUES
		('Villa Cuba', 10602.4),
		('Las Casas', 1546.6),
		('Las Morlas', 5293.4);
		"""
	]
	for sentencia in tanks:
		cursor.execute(sentencia);
	bd.commit() #Guardamos los cambios al terminar el ciclo
	print("Tanques insertados correctamente")
except sqlite3.OperationalError as error:
	print("Error al abrir:", error)