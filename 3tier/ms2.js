var express = require('express');
var sleep = require('sleep');
const params = require('params-cli');
const { MongoClient } = require('mongodb');
var exponential = require('@stdlib/random-base-exponential');
const cluster = require('node:cluster');
const process = require('node:process');
var app = express();

mongoInit = async function(ms_name) {
	let db = await MongoClient.connect("mongodb://localhost:27017/${ms_name}")
	if (db.err) { console.log('error'); }
	else { console.log('conneted to mongo'); }
	let dbo = db.db(ms_name)
	try {
		await dbo.collection("rt").drop()
	} catch (e) {
	}
	let rtCol = await dbo.createCollection("rt")
	if (rtCol.err) {
		console.log("error while creating rt collection")
	} else {
		console.log("db init success")
	}
	return dbo
}

getMSHRtime= function(){
	let hrTime = process.hrtime();
	return (hrTime[0] * 1000 + hrTime[1] / 1000000.0);
}

doWork=function (delay){
	let stime=getMSHRtime()
	let i=0;
	while((getMSHRtime()-stime)<=delay){
		i=i+1;
	}
}

var ms_name = null
var port = null
var stime=33.33
ncore=4

if (params.has('ms_name')) {
	ms_name = params.get('ms_name')
} else {
	throw new Error("ms_name required");
}
if (params.has('port')) {
	port = params.get('port')
} else {
	throw new Error("port required");
}


app.get('/:st([0-9]+)', async function(req, res) {
	let st=parseInt(req.params["st"])
	let delay = exponential(1.0 / stime);
	sleep.msleep(Math.max(Math.round(delay),0))
	//doWork(delay);
	let et=(new Date().getTime())
	msdb.collection("rt").insertOne({ "st": st, "end":et})
	res.send('Hello World ' + ms_name);
})

app.get('/mnt', function(req, res) {
	res.send('running ' + ms_name);
})

if (cluster.isPrimary) {
  console.log(`Primary ${process.pid} is running`);

  // Fork workers.
  for (let i = 0; i < ncore; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`worker ${worker.process.pid} died`);
  });
} else {
	var server = app.listen(port,"localhost",100000,async function() {
		var host = server.address().address
		var port = server.address().port
		global.msdb = await mongoInit(ms_name)
		console.log("Example app listening at http://%s:%s", host, port)
	})
  console.log(`Worker ${process.pid} started`);
}