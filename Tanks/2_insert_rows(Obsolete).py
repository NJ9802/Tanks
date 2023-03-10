import sqlite3
try:
	bd = sqlite3.connect("combustible.db")
	cursor = bd.cursor()
	tanks = [
		"""
		INSERT INTO tanks
		(location, existencia, height_cm)
		VALUES
		('Villa Cuba', 10602.4, 15),
		('Las Casas', 1546.6, 15),
		('Las Morlas', 5293.4, 15);
		"""
	]
	for sentencia in tanks:
		cursor.execute(sentencia)
	bd.commit() #Guardamos los cambios al terminar el ciclo
	print("Tanques insertados correctamente")
except sqlite3.OperationalError as error:
	print("Error al abrir:", error)

try:
	bd = sqlite3.connect("combustible.db")
	cursor = bd.cursor()
	sentence = [
		"""
		INSERT INTO darkmode
		(dark)
		VALUES
		(1);
		"""
	]
	for sentencia in sentence:
		cursor.execute(sentencia)
	bd.commit() #Guardamos los cambios al terminar el ciclo
	print("dark insertado correctamente")
except sqlite3.OperationalError as error:
	print("Error al abrir:", error)