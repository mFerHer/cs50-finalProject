from datetime  import datetime
import requests
import sqlite3


db = sqlite3.connect("data.db")
curs = db.cursor()                 

curs.execute("""DROP TABLE IF EXISTS info""")

db.commit()
db.close()
