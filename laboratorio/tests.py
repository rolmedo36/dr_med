import json
a = '[{"fecha": "2024-02-03","hora": "10:00","consultorio": "PEDIATRA","cliente": "RODRIGO JOSE TUVAL"},{"fecha": "2024-02-03","hora": "11:00","consultorio": "PEDIATRA","cliente": "RODRIGO JOSE TUVAL"},{"fecha": "2024-02-05","hora": "13:00","consultorio": "PEDIATRA","cliente": "Tuval"},]'
print('len', len(a))
a = a[0:len(a) - 2] + ']'
print(a)
b = json.loads(a)

print(b)

