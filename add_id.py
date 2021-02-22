import sys
import csv

filename = sys.argv[1]

data = []

with open(filename) as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

new_data = []

i=1
for row in data:
    row.insert(0, i)
    new_data.append(row)
    i += 1

filename = 'with_id_' + filename 

with open(filename, "w") as f:
    writer = csv.writer(f)
    writer.writerows(new_data)

print(filename, 'を書きました。')
