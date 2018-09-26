import psycopg2
import numpy as np


myDict = [["id", "email", "name", "local"]]
myDict.append(["9", 'hello@dataquest.io', 'Some Name', '123 Fake St.'])
print(myDict[0][0])

conn = psycopg2.connect("host=localhost dbname=Trabalho1Test user=postgres")
cur = conn.cursor()
cur.execute("insert into users values (%s, %s, %s, %s)",(myDict[1][0],myDict[1][1],myDict[1][2],myDict[1][3]))
conn.commit()
