// load the hot-reload-server module
var express = require('express')
var app = express()

app.post('/login', function (req, res) {
  var a = {name:"Vojtech Udrzal",roles:["admin","user"]};
  res.send(a)
})

app.get('/yes/', function (req, res) {
  res.send('Hello Wxeoxxxrasdld!')
})

app.listen(4000, function () {
  console.log('Example app listening on port 3000!')
})