import sqlite3
try:
	bd = sqlite3.connect("combustible.db")
	cursor = bd.cursor()
	tablas = [
		"""
			CREATE TABLE IF NOT EXISTS tanks(
				location TEXT NOT NULL,
				existencia REAL NOT NULL
			);
		"""
	]
	for tabla in tablas:
		cursor.execute(tabla);
	print("Tablas creadas correctamente")
except sqlite3.OperationalError as error:
	print("Error al abrir:", error)