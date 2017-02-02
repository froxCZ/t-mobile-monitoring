import mongo
result = mongo.dataDb()["a"].update({'_id':"x"}, {"$inc": {"lob.x.size":1}}, upsert=True)
print(result)