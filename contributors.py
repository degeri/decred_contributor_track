from database import Base, engine, session
import csv

a = session.execute('SELECT DISTINCT github_username FROM event_log WHERE datetime >  "2019-02-01" and datetime < "2019-02-28" and type_id = 1;')

before_list = []
feb_list = []

for b in a:

    feb_list.append(b[0])
    c = session.execute('SELECT * FROM event_log WHERE datetime <  "2019-02-01" and github_username = "'+str(b[0])+'" and type_id = 1;')
    #print(b)
    for d in c:
        print(d['github_username'])
        before_list.append(d['github_username'])


before_list = list(set(before_list))

print(before_list)
print(feb_list)


temp3 = [x for x in feb_list if x not in before_list]

print(temp3) 