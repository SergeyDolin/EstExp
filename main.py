import os
from mongodriver import MongoDriverPost, MongoDriverGet, points


def ParsPoints():
    tupl_buff = {}
    points_Sol = {}
    points_Name = []
    buff = []

    a_buff_date = []
    a_buff_time = []
    a_buff_B = []
    a_buff_L = []
    a_buff_H = []

    tupl_coll = []
    sol_count = 0
    point_count = 0
    
    for root, dirs, files in os.walk("./Points", topdown = True):
        for name in dirs:
            if name != 'PPP' and name != 'PPPDCB' and name != "AMERICA" and name != "EUROPE":
                points_Name.append(name)
        for name in files:
            buff.append(f'{root}/{name}')
            sol_count+=1
            if sol_count == 2:
                points_Sol[points_Name[point_count]] = (buff[0], buff[1])
                point_count += 1
                sol_count = 0
                buff.clear()
    
    for point, solfile in points_Sol.items():
        try:
            with open(solfile[0]) as readFile:
                content = list(filter(None, readFile.read().split('\n')))
                for u in content[1:]:
                    if float(u.split()[2]) > 0.0 and float(u.split()[5]) > 0.0:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))
                    elif float(u.split()[2]) > 0.0 and float(u.split()[5]) < 0.0:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))
                    elif float(u.split()[2]) < 0.0 and float(u.split()[5]) > 0.0:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))
                    else:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))

                tupl_buff["name"] = point
                tupl_buff["method"] = "PPP"
                tupl_buff["date"] = a_buff_date
                tupl_buff["time"] = a_buff_time
                tupl_buff["B"] = a_buff_B
                tupl_buff["L"] = a_buff_L
                tupl_buff["H"] = a_buff_H
                MongoDriverPost(points, tupl_buff)
                tupl_buff.clear()
                a_buff_B.clear()
                a_buff_L.clear()
                a_buff_date.clear()
                a_buff_time.clear()
                a_buff_H.clear()

            with open(solfile[1]) as readFile:
                content = list(filter(None, readFile.read().split('\n')))
                for u in content[1:]:
                    if float(u.split()[2]) > 0.0 and float(u.split()[5]) > 0.0:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))
                    elif float(u.split()[2]) > 0.0 and float(u.split()[5]) < 0.0:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))
                    elif float(u.split()[2]) < 0.0 and float(u.split()[5]) > 0.0:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))
                    else:
                        a_buff_date.append(str(u.split()[0]))
                        a_buff_time.append(str(u.split()[1][0:8]))
                        a_buff_B.append(float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0)
                        a_buff_L.append(float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0)
                        a_buff_H.append(float(u.split()[8]))

                tupl_buff["name"] = point
                tupl_buff["method"] = "PPPDCB"
                tupl_buff["date"] = a_buff_date
                tupl_buff["time"] = a_buff_time
                tupl_buff["B"] = a_buff_B
                tupl_buff["L"] = a_buff_L
                tupl_buff["H"] = a_buff_H
                MongoDriverPost(points, tupl_buff)
                tupl_buff.clear()
                a_buff_B.clear()
                a_buff_L.clear()
                a_buff_date.clear()
                a_buff_time.clear()
                a_buff_H.clear()
                
        except IOError:
            print("Error file")

ParsPoints()