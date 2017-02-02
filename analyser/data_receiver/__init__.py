from pymongo import MongoClient

client = MongoClient("mongodb://localhost/dev")
db = client["dev"]
result = db.test.insert_one(
  {
    "address": {
      "street": "2 Avenue"
    }
  }
)
print(result.acknowledged)



