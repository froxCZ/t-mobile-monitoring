// load the hot-reload-server module
var express = require('express')
var app = express()

app.get('/api/', function (req, res) {
    res.send('Hello Wxeorasdld!')
})

app.get('/yes/', function (req, res) {
    res.send('Hello Wxeoxxxrasdld!')
})

app.listen(4000, function () {
    console.log('Example app listening on port 3000!')
})