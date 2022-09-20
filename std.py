from audioop import rms
from cProfile import label
import pymap3d as pm
from mongodriver import *
import math
import pandas as pd
import matplotlib.pyplot as plt


# refPointsXYZ = {
#     "ABMF00GLP" : (2919785.7977, -5383744.9262, 1774604.8863),
#     "ALGO00CAN" : (918129.1005, -4346071.3337, 4561977.9236),
#     "BAIE00CAN" : (1546823.0264, -3879765.2041, 4804185.1756),
#     "LMMF00MTQ" : (2993387.4100, -5399363.7884, 1596748.1929),
#     "NRC100CAN" : (1112776.9240, -4341475.9121, 4522955.8899),
#     "POVE00BRA" : (2774265.5691, -5662060.1792, -959415.7214),
#     "SALU00BRA" : (4566947.8447, -4443098.5640, -286674.5228),
#     "SAMO00WSM" : (-6129702.4462, -890028.4135, -1516806.6849),
#     "VALD00CAN" : (919075.5264, -4167766.3696, 4724323.6674),
#     "WSRT00NLD" : (3828735.5956, 443305.2299, 5064884.8718),
#     "ZIM200CHE" : (4331299.6382, 567537.6304, 4633133.9190),
# }
refPointsXYZ = {
    "ABMF00GLP" : (2919785.8091, -5383744.9349, 1774604.8964),
    "BAIE00CAN" : (1546823.0219, -3879765.2132, 4804185.1866),
    "LMMF00MTQ" : (2993387.4220, -5399363.7995, 1596748.2023),
    "POVE00BRA" : (2774265.5748, -5662060.1888, -959415.7180),
    "SAMO00WSM" : (-6129702.5021, -890028.3633, -1516806.6998),
    "VALD00CAN" : (919075.5203, -4167766.3715, 4724323.6668),
    "KARL00DEU" : (4146524.1164, 613138.3688, 4791517.3659),
    "TERS00NLD" : (3798580.3493, 346994.3534, 5094781.1715),
    "WSRT00NLD" : (3828735.5972, 443305.2412, 5064884.8897),
}


refPointsENU = {}
new_diff = {}

def xyzblh2enu(refX,refY,refZ,obsB,obsL,obsH):
    B,L,H = pm.ecef2geodetic(refX,refY,refZ)
    e,n,u = pm.geodetic2enu(B,L,H,B-obsB,L-obsL,H-obsH)
    return e,n,u

def refxyz2enu(refX,refY,refZ):
    B,L,H = pm.ecef2geodetic(refX,refY,refZ)
    e,n,u = pm.geodetic2enu(B,L,H,B-B,L-L,H-H)
    return e,n,u

def ApproxPoins():
    e_buff = []
    n_buff = []
    u_buff = []

    for point, coor in refPointsXYZ.items():
        rE, rN, rU = refxyz2enu(coor[0], coor[1], coor[2])
        refPointsENU[point] = (rE, rN, rU)
    
    for point, coor in refPointsENU.items():
        req = MongoDriverGet(points, {"name": point, "method":"PPP"})
        for i in range(0, len(req["time"])):      
            e,n,u = xyzblh2enu(refPointsXYZ[point][0],refPointsXYZ[point][1],refPointsXYZ[point][2],req["B"][i],req["L"][i],req["H"][i])  
            e_buff.append(refPointsENU[point][0]-e)
            n_buff.append(refPointsENU[point][1]-n)
            u_buff.append(refPointsENU[point][2]-u)
            
        new_diff["name"] = point
        new_diff["method"] = "PPP" 
        new_diff["date"] = req["date"]
        new_diff["time"] = req["time"]
        new_diff["dE"] = e_buff
        new_diff["dN"] = n_buff
        new_diff["dU"] = u_buff
        MongoDriverPost(diff, new_diff)
        new_diff.clear()
        e_buff.clear()
        n_buff.clear()
        u_buff.clear()
    
    for point, coor in refPointsENU.items():
        req = MongoDriverGet(points, {"name": point, "method":"PPPDCB"})
        for i in range(0, len(req["time"])):      
            e,n,u = xyzblh2enu(refPointsXYZ[point][0],refPointsXYZ[point][1],refPointsXYZ[point][2],req["B"][i],req["L"][i],req["H"][i])  
            e_buff.append(refPointsENU[point][0]-e)
            n_buff.append(refPointsENU[point][1]-n)
            u_buff.append(refPointsENU[point][2]-u)
            
        new_diff["name"] = point
        new_diff["method"] = "PPPDCB" 
        new_diff["date"] = req["date"]
        new_diff["time"] = req["time"]
        new_diff["dE"] = e_buff
        new_diff["dN"] = n_buff
        new_diff["dU"] = u_buff
        MongoDriverPost(diff, new_diff)
        new_diff.clear()
        e_buff.clear()
        n_buff.clear()
        u_buff.clear()

def AVG(method):
    avgN = []
    avgE = []
    avgU = []
    req = []
    post = {}
    for point in refPointsXYZ:
        req.append(MongoDriverGet(diffk, {"name":point, "method":method}))
    for _ in range(0, 85000):
        avgN.append(0)
        avgE.append(0)
        avgU.append(0)
    for i in range(0, len(req)):
        for j in range(0, len(req[i]["dN"])):
            avgN[j]+=req[i]["dN"][j]
            avgE[j]+=req[i]["dE"][j]
            avgU[j]+=req[i]["dU"][j]

    
    for dn in range(0, len(avgN)):
        avg = avgN[dn]/len(req)
        avgN[dn] = avg
    for de in range(0, len(avgE)):
        avg = avgE[de]/len(req)
        avgE[de] = avg
    for du in range(0, len(avgU)):
        avg = avgU[du]/len(req)
        avgU[du] = avg
    
    post["method"] = method 
    post["avgN"]=avgN
    post["avgE"]=avgE
    post["avgU"]=avgU


    MongoDriverPost(avgK, post)

def RMS(method):
    rmsN = []
    rmsE = []
    rmsU = []
    req = []
    post = {}
    for point in refPointsXYZ:
        req.append(MongoDriverGet(diff, {"name":point, "method":method}))
    for _ in range(0, 85000):
        rmsN.append(0)
        rmsE.append(0)
        rmsU.append(0)
    for i in range(0, len(req)):
        for j in range(0, len(req[i]["dN"])):
            rmsN[j]+=pow(req[i]["dN"][j],2)
            rmsE[j]+=pow(req[i]["dE"][j],2)
            rmsU[j]+=pow(req[i]["dU"][j],2)

    
    for dn in range(0, len(rmsN)):
        rms = math.sqrt(rmsN[dn]/len(req)) 
        rmsN[dn] = rms
    for de in range(0, len(rmsE)):
        rms = math.sqrt(rmsE[de]/len(req)) 
        rmsE[de] = rms
    for du in range(0, len(rmsU)):
        rms = math.sqrt(rmsU[du]/len(req)) 
        rmsU[du] = rms
    
    post["method"] = method 
    post["rmsN"]=rmsN
    post["rmsE"]=rmsE
    post["rmsU"]=rmsU


    MongoDriverPost(rmsdb, post)

def panda_mongo():

    # rmsBD_PPP = MongoDriverGet(rmsdb, {"method":"PPP"})
    # rmsBD_PPPDCB = MongoDriverGet(rmsdb, {"method":"PPPDCB"})
    # rmsBD_PPPk = MongoDriverGet(rmsdbk, {"method":"PPP"})
    # rmsBD_PPPDCBk = MongoDriverGet(rmsdbk, {"method":"PPPDCB"})

    avgBD_PPP = MongoDriverGet(avgS, {"method":"PPP"})
    avgBD_PPPDCB = MongoDriverGet(avgS, {"method":"PPPDCB"})
    avgBD_PPPk = MongoDriverGet(avgK, {"method":"PPP"})
    avgBD_PPPDCBk = MongoDriverGet(avgK, {"method":"PPPDCB"})


    plt.figure()

    plt.subplot(221)
    plt.plot(avgBD_PPP["avgU"], label='PPP U')
    plt.plot(avgBD_PPPDCB["avgN"], label='PPP(DCB) U')
    plt.xlabel('Время, с')
    plt.ylabel('Среднее, м')
    plt.grid(True)
    # plt.title('Static')
    plt.legend()

    plt.subplot(222)
    plt.plot(avgBD_PPPk["avgU"], label='PPP U')
    plt.plot(avgBD_PPPDCBk["avgU"], label='PPP(DCB) U')
    plt.xlabel('Время, с')
    plt.ylabel('Среднее, м')
    plt.grid(True)
    # plt.title('Kinematic')
    plt.legend()

    # plt.subplot(223)
    # plt.plot(avgBD_PPP["avgE"], label='PPP E')
    # plt.plot(avgBD_PPPDCB["avgE"], label='PPP(DCB) E')
    # plt.xlabel('Время, с')
    # plt.ylabel('Среднее, м')
    # plt.grid(True)
    # plt.legend()

    # plt.subplot(224)
    # plt.plot(avgBD_PPPk["avgE"], label='PPP E')
    # plt.plot(avgBD_PPPDCBk["avgE"], label='PPP(DCB) E')
    # plt.xlabel('Время, с')
    # plt.ylabel('Среднее, м')
    # plt.grid(True)
    # plt.legend()

    # plt.subplot(221)
    # plt.plot(rmsBD_PPP["rmsU"], label='PPP U')
    # plt.plot(rmsBD_PPPDCB["rmsU"], label='PPP(DCB) U')
    # plt.xlabel('Время, с')
    # plt.ylabel('СКП, м')
    # plt.grid(True)
    # plt.title('Static')
    # plt.legend()

    # plt.subplot(222)
    # plt.plot(rmsBD_PPPk["rmsU"], label='PPP U')
    # plt.plot(rmsBD_PPPDCBk["rmsU"], label='PPP(DCB) U')
    # plt.xlabel('Время, с')
    # plt.ylabel('СКП, м')
    # plt.grid(True)
    # plt.title('Kinematic')
    # plt.legend()

    plt.show()
    


# ApproxPoins()
# AVG("PPP")
# AVG("PPPDCB")
# RMS("PPP")  
# RMS("PPPDCB")  
panda_mongo()