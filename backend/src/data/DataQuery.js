var ErrorStatus = require('../ErrorStatus')
const VALUES_ON_AXIS = 400;

var dataQuery = class DataQuery {

  static getData(searchParam) {
    var fullQuery = createMongoQuery(searchParam);
    return dataDb.collection('lobs').aggregate(fullQuery).toArray()
      .then(arr => {
        var sumParam = arr[0].searchParam.aggregation.sum || [];
        for(let i in sumParam){
          sumParam[i] = objectPathToValidName(sumParam[i]);
        }
        var minMax = {}
        for(let param of sumParam){
          minMax[param] = {min:arr[0][param],max:arr[0][param]}
        }
        for (let row of arr) {
          delete row.searchParam
          for(let param of sumParam){
            minMax[param].min = Math.min(minMax[param].min,row[param]);
            minMax[param].max = Math.max(minMax[param].max,row[param]);
          }
        }
        var response = {};
        response.metadata = minMax;
        response.data = arr;
        var metadata = {};
        return response
      })
    //return Promise.resolve(fullQuery);
  }
};

module.exports = dataQuery;

function createMongoQuery(searchParam) {
  let from = new Date(searchParam.from);
  var to = new Date(searchParam.to);
  if (isNaN(from.getTime()) || isNaN(to.getTime())) {
    throw new ErrorStatus("missing from or to attribute", 400);
  }
  var match = {"$match": {_id: {$gt: from, $lt: to}}};
  var timeGroupAndProjection = createTimeGroupAndProjection(Math.abs(from.getTime() - to.getTime()));
  var dataGroupAndProjection = createDataGroupAndProjection(searchParam.aggregation);
  var group = {"$group": Object.assign(timeGroupAndProjection.group, dataGroupAndProjection.group)};
  var projection = {"$project": Object.assign(timeGroupAndProjection.project, dataGroupAndProjection.project)};
  projection.$project.searchParam = searchParam;
  var sort = {
    "$sort": {
      "_id": 1
    }
  };

  var fullQuery = [match, group, sort, projection];
  return fullQuery;
}

function createDataGroupAndProjection(aggregation) {
  var group = {};
  var project = {};
  if (aggregation.sum) {
    for (let dataPath of aggregation.sum) {
      var validName = objectPathToValidName(dataPath);
      group[validName] = {"$sum": "$" + dataPath}
      project[validName] = "$" + validName;
    }
  }
  return {group: group, project: project};
}

function createTimeGroupAndProjection(timeDiff) {
  timeDiff /= 1000;
  timeDiff /= 60;
  var minutes = Math.max(timeDiff, 60);
  var groupCount = minutes / VALUES_ON_AXIS;
  if (groupCount < 60) {
    var minuteGroups = [1, 5, 15, 30];
    for (let minuteGroup of minuteGroups) {
      if (groupCount < minuteGroup) {
        console.log("expected # of results: " + (minutes / minuteGroup));
        return createMinuteGrouping(minuteGroup);
      }
    }
  }
  throw new Error("unsupported range")
}

function createMinuteGrouping(groupByMinutes) {
  var groupObject = {
    "_id": {
      "year": {"$year": "$_id"},
      "month": {"$month": "$_id"},
      "dayOfMonth": {"$dayOfMonth": "$_id"},
      "hour": {"$hour": "$_id"},
      "interval": {
        "$subtract": [
          {"$minute": "$_id"},
          {"$mod": [{"$minute": "$_id"}, groupByMinutes]}
        ]
      }
    },
    "anyDate": {"$first": "$_id"},
  };
  var project = {_id: {$subtract: ["$anyDate", {$multiply: [1000 * 60, {"$mod": [{"$minute": "$anyDate"}, groupByMinutes]}]}]}}
  return {group: groupObject, project: project};
}

function objectPathToValidName(objectPath){
  return objectPath.replace(/\./g, '')
}
