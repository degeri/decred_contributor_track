
from database import Base, engine, session
import csv

csv_file = 'event_log.csv'
CsvFile = csv.writer(open(csv_file, 'w'), 'excel')

for row in session.execute('SELECT * FROM event_log'):
    print(row)
    CsvFile.writerow(row)

csv_file = 'event_types.csv'
CsvFile = csv.writer(open(csv_file, 'w'), 'excel')

for row in session.execute('SELECT * FROM event_types'):
    print(row)
    CsvFile.writerow(row)

csv_file = 'repository_list.csv'
CsvFile = csv.writer(open(csv_file, 'w'), 'excel')

for row in session.execute('SELECT * FROM repository_list'):
    print(row)
    CsvFile.writerow(row)

