from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('localhost', 27017)
    db = client.test_database
    collection = db.test_collection

    post = {"author": "Mike",
            "age": 43}

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id


    print(posts.find_one())