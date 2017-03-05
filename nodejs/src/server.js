// load the hot-reload-server module
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var proxy = require('express-http-proxy');

app.use('/proxy', proxy('www.google.com'));
const MongoClient = require('mongodb').MongoClient
MongoClient.connect('mongodb://localhost/dev', (err, database) => {
  if (err == null) {
    global.db = database;
    app.listen(4000, function () {
      console.log('App listening on port 4000!')
    })
  } else {
    console.error(err);
  }

});
MongoClient.connect('mongodb://localhost/dev_data', (err, database) => {
  global.dataDb = database;
})

app.use(bodyParser.json());
app.use('', require('./user/router'));
app.use('', require('./data/router'));

function clientErrorHandler(err, req, res, next) {
  console.log(err);
  res.status(err.statusCode || 500).send({error: err.message || 'Something failed!'})
}

app.use(clientErrorHandler);

app.use('/analyser', proxy('http://localhost:5000/'));