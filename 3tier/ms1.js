var express = require('express');
var sleep = require('sleep');
const params = require('params-cli');
const axios = require('axios');

const { MongoClient } = require('mongodb');
var exponential = require('@stdlib/random-base-exponential');
const { PerformanceObserver, performance } = require('perf_hooks');
var app = express();

mongoInit = async function(ms_name) {
	var db = await MongoClient.connect("mongodb://localhost:27017/${ms_name}")
	if (db.err) { console.log('error'); }
	else { console.log('conneted to mongo'); }
	dbo = db.db(ms_name)
	try {
		await dbo.collection("rt").drop()
	} catch (e) {
	}

	rtCol = await dbo.createCollection("rt")
	if (rtCol.err) {
		console.log("error while creating rt collection")
	} else {
		console.log("db init success")
	}
	return dbo
}

ms_name = null
port = null
mnt_port = null
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
if (params.has('mnt_port')) {
	mnt_port = params.get('mnt_port')
} else {
	throw new Error("mnt_port required");
}



const obs = new PerformanceObserver((items) => {
	//req_time.push(items.getEntries()[0].duration)
	var myobj = { "st": items.getEntries()[0].startTime, "end": items.getEntries()[0].startTime + items.getEntries()[0].duration }
	msdb.collection("rt").insertOne(myobj)
	performance.clearMarks();
});
obs.observe({ entryTypes: ['measure'] });

app.get('/', async function(req, res) {
	performance.mark('A');
	
	console.log("nested call")
	await axios.get('http://localhost:8083/')
	
	
	var delay = exponential(1.0 / 300);
	sleep.msleep(Math.round(delay))
	performance.mark('B');
	res.send('Hello World '+ms_name);
	performance.measure('rt', 'A', 'B');
})

var server = app.listen(port, async function() {
	var host = server.address().address
	var port = server.address().port

	global.msdb = await mongoInit(ms_name)
	console.log("Example app listening at http://%s:%s", host, port)

})

var server2 = app.listen(mnt_port, async function() {
	var host = server2.address().address
	var port = server2.address().port

	console.log("Example app listening at http://%s:%s", host, port)

})