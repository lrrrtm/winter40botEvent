import sqlite3
from constants import *

db = sqlite3.connect(databaseName, check_same_thread=False)
cur = db.cursor()


def checkInputName(current):
    try:

        firstname, lastname = current.split(" ")[0], current.split(" ")[1]
        firstname = firstname.replace("ё", "е").replace("Ё", "Е")
        lastname = lastname.replace("ё", "е").replace("Ё", "Е")
        cur.execute(f"select * from school where firstname = \"{firstname}\" and lastname = \"{lastname}\"")
        data = cur.fetchall()
        if len(current.split(" ")) == 2 and len(current.split(" ")[0]) < 20 and  len(current.split(" ")[1]) < 20 and len(data) == 1:
            return True
    except Exception as e:
        print(e)
        return False
    return False
