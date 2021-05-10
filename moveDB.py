import sqlite3
import csv

dbname = 'tfc.sqlite2021-05-09'
dbname2 = 'tfc_cover.sqlite20210509'

connection = sqlite3.connect(dbname)


def make_csv(f_name, connection):
    cursor = connection.cursor()
    cursor.execute("select * from {0}".format(f_name))

    data = []
    for row in cursor.fetchall():
        data.append(row)

    with open('{0}.csv'.format(f_name), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    cursor.close()

def make_poline_csv(f_name, connection):
    cursor = connection.cursor()
    cursor.execute("select id,remark,om,qty,balance,code_id,po_id from {0}".format(f_name))

    data = []
    for row in cursor.fetchall():
        data.append(row)

    with open('{0}.csv'.format(f_name), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    cursor.close()

make_csv('tfc_code', connection)
make_csv('po', connection)
make_poline_csv('poline', connection)
make_csv('inv', connection)
make_csv('invline', connection)

connection.close()

connection = sqlite3.connect(dbname2)
make_csv('condition', connection)
make_csv('po_fabric', connection)
connection.close()
