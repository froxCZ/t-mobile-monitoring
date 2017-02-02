var router = require('express').Router()
function dev(req, res, next) {
  //var data = dataDb.collection("lobs").find({"data.CZ.GSM":{$exists: true}},{_id:1,"data.CZ.GSM.sum":1}).sort({_id:-1}).toArray()
  var data = dataDb.collection('lobs').aggregate(
    [
      {
        "$group": {
          "_id": {
            "year": {"$year": "$_id"},
            "month": {"$month": "$_id"},
            "dayOfMonth": {"$dayOfMonth": "$_id"},
            "hour": {"$hour": "$_id"},
            "interval": {
              "$subtract": [
                {"$minute": "$_id"},
                {"$mod": [{"$minute": "$_id"}, 15]}
              ]
            }
          },
          "anyDate": {"$first": "$_id"},
          "count": {"$sum": 1},
          "sum": {"$sum": "$data.CZ.GSM.sum"}
        }
      },
      {
        "$sort": {
          "_id": 1
        }
      },
      {
        "$project": {
          _id: {$subtract: ["$anyDate", {$multiply: [1000 * 60, {"$mod": [{"$minute": "$anyDate"}, 15]}]}]},
          sum: 1,
          count: 1,
        }
      }
    ]
  ).toArray()
    .then(result => res.send(result))

}
router.get("/data/dev", dev);


module.exports = router;