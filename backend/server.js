// load the hot-reload-server module
var express = require('express')
var app = express()
var bodyParser = require('body-parser');
app.use(bodyParser.json());

var users = {
  "vojta": {name: "Vojtech Udrzal", roles: ["admin", "user"], password: "asd"}
}
app.post('/login', function (req, res) {
  console.log("body:");
  console.log(req.body);
  var user = users[req.body.username];
  if (user == null || user.password != req.body.password) {
    res.sendStatus(401);
  } else {
    res.send(user);
  }
})

app.get('/yes/', function (req, res) {
  res.send('Hello Wxeoxxxrasdld!')
})

app.listen(4000, function () {
  console.log('Example app listening on port 3000!')
})