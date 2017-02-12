var router = require('express').Router()
var DataQuery = require('./DataQuery');

function dev(req, res, next) {
  //var data = dataDb.collection("lobs").find({"data.CZ.GSM":{$exists: true}},{_id:1,"data.CZ.GSM.sum":1}).sort({_id:-1}).toArray()
  var data = dataDb.collection('lobs').aggregate(
    [
      {
        "$match": { _id: { $gt: new Date("2016-09-01T08:15:00.000Z"), $lt: new Date("2016-09-02T08:15:00.000Z") } }
      },
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
          "sumx": {"$sum": "$data.CZ.GSM.sum"},
          "sum": {"$sum": "$data.CZ.MMS.sum"},
          "dataCZGSMsum": {
            "$sum": "$data.CZ.GSM.sum"
          },
          "dataCZMMSsum": {
            "$sum": "$data.CZ.MMS.sum"
          }
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
          sumx: 1,
          count: 1,
          "a":"$sum",
          "dataCZGSMsum": 1,
          "dataCZMMSsum": 1,
        }
      }
    ]
  ).toArray()
    .then(result => res.send(result))
}
function devPost(req, res, next) {
  console.log(req.body)
  DataQuery.getData(req.body)
    .then(a => {
      res.send(a);
    }).catch(e => {
    next(e);
  })

}
function getLobs(req, res, next) {
  CZ_LOBS = ["SIS",
    "DWA",
    "MWB",
    "DAR",
    "SMS",
    "PCF",
    "PPC",
    "TCF",
    "GSM",
    "TPP",
    "XTC",
    "PST",
    "WHS",
    "TAP",
    "SBC",
    "SCF",
    "LAS",
    "MMS",
    "ATS",
    "RRA",
    "VMS",
    "MTS",
    "OTA",
    "BVS",
    "VOP",
    "WEL",
    "CIR",
    "SMG",
    "LTP",
    "M2M",
    "EWG",
    "TIT",
    "RES",
    "KPI",
    "EPC",
    "MNT",
    "TOC",
    "EWH",
    "ACI"];
  const lobs = {CZ:CZ_LOBS};
  res.send(lobs);
}

router.get("/data/dev", dev);
router.get("/lobs", getLobs);
router.post("/data/lobs/raw", devPost);


module.exports = router;