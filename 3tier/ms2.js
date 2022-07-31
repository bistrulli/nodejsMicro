var express = require('express');
//const { StaticPool } = require('node-worker-threads-pool');
//const workerpool = require('workerpool');
const Piscina = require('piscina');
const params = require('params-cli');
const { MongoClient } = require('mongodb');
var app = express();

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
var stime=33.33
ncore=2

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

////initThreadpool
//var staticPool = new StaticPool({
//	  size: ncore,
//	  task: "../msLocalLogic/msThread.js",
//	  workerData: ""
//});

//create a worker pool using an external worker script
//const pool = workerpool.pool("../msLocalLogic/msThread.js",{minWorkers:ncore,
//															maxWorkers:ncore,
//															workerType:"thread"});

const piscina = new Piscina({
	  filename:"../msLocalLogic/msThread.js",
	  minThreads:ncore,
	  maxThreads:ncore
});


app.get('/:st([0-9]+)', async function(req, res) {
	let st=parseInt(req.params["st"])
	//let result = await staticPool.exec(stime);
	//await pool.exec('doWork', [stime])
	await piscina.run({ delay: stime})
	//doWork(delay);
	let et=(new Date().getTime())
	msdb.collection("rt").insertOne({ "st": st, "end":et})
	res.send('Hello World ' + ms_name);
})

app.get('/mnt', function(req, res) {
	res.send('running ' + ms_name);
})

  
//init db
initRtColl(ms_name)
var server = app.listen(port,"localhost",async function() {
	var host = server.address().address
	var port = server.address().port
	global.msdb = await mongoInit(ms_name)
	console.log("Example app listening at http://%s:%s", host, port)
});
console.log(`Worker ${process.pid} started`);