import xlsxwriter, sqlite3
from constants import *

db = sqlite3.connect(databaseName, check_same_thread=False)
cur = db.cursor()



