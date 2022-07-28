const { StaticPool } = require('node-worker-threads-pool');
var express = require('express');
const params = require('params-cli');
const { MongoClient } = require('mongodb');
var app=express()

mongoInit = async function(ms_name) {
	let db = await MongoClient.connect(`mongodb://localhost:27017/${ms_name}`)
	if (db.err) { console.log('error'); }
	else { console.log('conneted to mongo'); }
	let dbo = db.db(ms_name)
	return dbo
}

initRtColl=async function(ms_name){
	let db = await MongoClient.connect(`mongodb://localhost:27017/${ms_name}`)
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
	db.close()
}

var ms_name = null
var port = null
ncore=3
stime=100

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

var staticPool = new StaticPool({
  size: ncore,
  task: "./thread.js",
  workerData: ""
});

app.get('/:st([0-9]+)', async function(req, res) {
	let st=parseInt(req.params["st"])
	let result = await staticPool.exec(stime); 
	let et=(new Date().getTime())
	msdb.collection("rt").insertOne({ "st": st, "end":et})
	res.send('Hello World ');
})

app.get('/mnt', function(req, res) {
	res.send('running ');
})

// init db
initRtColl(ms_name)

var server = app.listen(port,"localhost",async function() {
	var host = server.address().address
	var port = server.address().port
	global.msdb = await mongoInit(ms_name)
	console.log("Example app listening at http://%s:%s", host, port)
})
console.log(`Worker ${process.pid} started`);