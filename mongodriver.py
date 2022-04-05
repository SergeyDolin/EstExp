from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db =  client.exp_database
points = db.obs
diff = db.dEdNdU
def MongoDriverPost(collection,post):
    collection.insert_one(post).inserted_id

def MongoDriverGet(collection,post):
    for point in collection.find(post):
        return point