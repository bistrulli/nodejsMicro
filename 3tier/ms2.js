var express = require('express');
const params = require('params-cli');
var sleep = require('sleep');
var app = express();
//const { MongoClient } = require('mongodb');
const { hrtime } = require('node:process');

function doWork(delay){
	const start = hrtime.bigint();
	let i=0;
	while(hrtime.bigint()-start<delay){
		i++;
	}
	return i;
}

mongoInit = async function() {
	let client = await MongoClient.connect(`mongodb://localhost:27017`)
	if (db.err) { console.log('error'); }
	else { console.log('conneted to mongo'); }
	return client
}

initRtColl=async function(ms_name){
	let db = await MongoClient.connect(`mongodb://localhost:27017`)
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
var stime=50.0

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

app.get('/', async function(req, res) {
	//d=(stime/1000).toFixed(4)
	//d=(exponential(1.0 / delay)/1000.0).toFixed(4)
	sleep.msleep(stime);
	//doWork(stime*1e06)
	res.send('Hello World ' + ms_name);
})

app.get('/mnt', function(req, res) {
	res.send('running ' + ms_name);
})


var server = app.listen(port,"localhost",async function() {
	var host = server.address().address
	var port = server.address().port
	console.log("Example app listening at http://%s:%s", host, port)
});
console.log(`Worker ${process.pid} started`);