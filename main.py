import os


def pars_points():
    Points_Name = []
    Points_Sol = {}
    buff = []
    sol_count = 0
    point_count = 0
    for root, dirs, files in os.walk("./Points", topdown = True):
        for name in dirs:
            if name != 'PPP' and name != 'PPPDCB' and name != "AMERICA" and name != "EUROPE":
                Points_Name.append(name)
        for name in files:
            buff.append(f'{root}/{name}')
            sol_count+=1
            if sol_count == 2:
                Points_Sol[Points_Name[point_count]] = (buff[0], buff[1])
                point_count += 1
                sol_count = 0
                buff.clear()
    
    for point, solfile in Points_Sol.items():
        
    print(Points_Name)
    print(len(Points_Sol))

#     try:
#         with open(file, 'r') as readFile:
#         reader = csv.DictReader(readFile)
#         for row in reader:
#                 currentuple.append(row)
#     except IOError:
#         print("Error file")
pars_points()
