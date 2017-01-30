// load the hot-reload-server module
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
const MongoClient = require('mongodb').MongoClient
MongoClient.connect('mongodb://localhost/test', (err, database) => {
  if (err == null) {
    global.db = database;
    app.listen(4000, function () {
      console.log('App listening on port 4000!')
    })
  } else {
    console.error(err);
  }

});

app.use(bodyParser.json());
app.use('', require('./user/router'));

function clientErrorHandler(err, req, res, next) {
  res.status(err.statusCode || 500).send({error: err.message || 'Something failed!'})
}


app.use(clientErrorHandler);
