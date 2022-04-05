import pymap3d as pm
from mongodriver import *


refPointsXYZ = {
    "ABMF00GLP" : (2919785.7977, -5383744.9262, 1774604.8863),
    "ALGO00CAN" : (918129.1005, -4346071.3337, 4561977.9236),
    "BAIE00CAN" : (1546823.0264, -3879765.2041, 4804185.1756),
    "LMMF00MTQ" : (2993387.4100, -5399363.7884, 1596748.1929),
    "NRC100CAN" : (1112776.9240, -4341475.9121, 4522955.8899),
    "POVE00BRA" : (2774265.5691, -5662060.1792, -959415.7214),
    "SALU00BRA" : (4566947.8447, -4443098.5640, -286674.5228),
    "SAMO00WSM" : (-6129702.4462, -890028.4135, -1516806.6849),
    "VALD00CAN" : (919075.5264, -4167766.3696, 4724323.6674),
    "WSRT00NLD" : (3828735.5956, 443305.2299, 5064884.8718),
    "ZIM200CHE" : (4331299.6382, 567537.6304, 4633133.9190),
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

def RMS():
    rmsN = []
    rmsE = []
    rmsU = []
    req = []
    for point in refPointsXYZ:
        req.append(MongoDriverGet(diff, {"name":point, "method":"PPP"}))
        
# ApproxPoins()
