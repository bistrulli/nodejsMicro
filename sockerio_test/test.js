var express = require('express')
var sleep = require('sleep');

var responseTime = require('response-time')
var StatsD = require('node-statsd')

var app = express()
var stats = new StatsD()

stats.socket.on('error', function (error) {
  console.error(error.stack)
})

app.use(responseTime(function (req, res, time) {
  var stat = (req.method + req.url).toLowerCase()
    .replace(/[:.]/g, '')
    .replace(/\//g, '_')
  stats.timing(stat, time)
  console.log(time)
}))

app.get('/', function (req, res) {
  sleep.msleep(20000)
  res.send('hello, world!')
})

var server = app.listen(8080, function() {
	var host = server.address().address
	var port = server.address().port
	console.log("Example app listening at http://%s:%s", host, port)
})