horario = []
horario1 = 10
horario2 = 15
l = 1
for r in range(horario1, horario2):
    r0 = str(r) + ":00"
    r1 = str(r) + ":30"
    horario.append(r0)
    horario.append(r1)

print(len(horario))