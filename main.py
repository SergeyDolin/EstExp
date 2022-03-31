import os
from pymongo import MongoClient




def MongoDriver(post):
    client = MongoClient('mongodb://localhost:27017/')
    db =  client.exp_database
    posts = db.posts
    result = posts.insert_one(post).inserted_id


def ParsPoints():
    tupl_buff = {}
    points_Sol = {}
    points_Name = []
    buff = []
    tuple_pkg = []
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
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))
                    elif float(u.split()[2]) > 0.0 and float(u.split()[5]) < 0.0:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))
                    elif float(u.split()[2]) < 0.0 and float(u.split()[5]) > 0.0:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))
                    else:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))    
                MongoDriver(tupl_buff)
                tupl_buff.clear()
            with open(solfile[1]) as readFile:
                content = list(filter(None, readFile.read().split('\n')))
                for u in content[1:]:
                    if float(u.split()[2]) > 0.0 and float(u.split()[5]) > 0.0:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))
                    elif float(u.split()[2]) > 0.0 and float(u.split()[5]) < 0.0:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])+(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))
                    elif float(u.split()[2]) < 0.0 and float(u.split()[5]) > 0.0:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])+(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))
                    else:
                        tupl_buff[str(u.split()[1][0:7])] = (float(u.split()[2])-(float(u.split()[3])+float(u.split()[4])/60.0)/60.0, float(u.split()[5])-(float(u.split()[6])+float(u.split()[7])/60.0)/60.0, float(u.split()[8]))    
                MongoDriver(tupl_buff)
                tupl_buff.clear()
                # print(tupl_buff['09:59:31.000'])
                # MongoDriver(tupl_buff)
                # for elm in content[1:]:

                #     if elm[0].isalpha():
                #         key = elm
                #         tupl_buff.update({key: []})
                #     else:
                #         tupl_buff[key].append(elm)
            
            # dict = {k: ' '.join(v) for k, v in tupl_buff.items()}
            
            # with open(solfile[1], 'r') as readFile:
            #     for str in readFile:
            #         print(str)
        except IOError:
            print("Error file")
        post = {
            "point": point

        }
    

#     try:
#         with open(file, 'r') as readFile:
#         reader = csv.DictReader(readFile)
#         for row in reader:
#                 currentuple.append(row)
#     except IOError:
#         print("Error file")
ParsPoints()
