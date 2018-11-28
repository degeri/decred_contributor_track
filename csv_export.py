import sqlite3
from pathlib import Path
import sys
from datetime import datetime
import csv

shouldfilter = False
db_file = Path('database.db')
csv_file = 'database.csv'


if len(sys.argv) == 2:
    try:
        date_limit = datetime.strptime(sys.argv[1], '%Y-%m-%d %H:%M')
        shouldfilter = True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD HH(24hrs):MM")
else:
    print("No Date specified dumpingall to csv")

if db_file.is_file():
    CsvFile = csv.writer(open(csv_file, 'w'), 'excel')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    column_names = ['ID', 'LOGIN', 'REPO', 'FIRSTSEEN']
    CsvFile.writerow(column_names)
    for row in cursor.execute('SELECT * FROM contributors'):
        if shouldfilter:
            try:
                db_date = datetime.strptime(row[3], '%Y-%m-%d %H:%M')
                if date_limit < db_date:
                    CsvFile.writerow(row)
                print(db_date)
            except:
                None
        else:
            CsvFile.writerow(row)
else:
    print("No DB or CSV already exists exiting")
    
