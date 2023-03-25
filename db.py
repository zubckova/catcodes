from peewee import *

conn = SqliteDatabase('catcodes.sqlite')

cursor = conn.cursor()
cursor.execute("SELECT * FROM codes")
results = cursor.fetchall()
print(results)

conn.close()