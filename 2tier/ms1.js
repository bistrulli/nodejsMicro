var express = require('express');
var sleep = require('sleep');
const params = require('params-cli');
const { MongoClient } = require('mongodb');
var exponential = require('@stdlib/random-base-exponential');
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

app.get('/:st([0-9]+)', function(req, res) {
	st=parseInt(req.params["st"])
	var delay = exponential(1.0 / 300.0);
	sleep.msleep(Math.round(delay))
	res.send('Hello World ' + ms_name);
	et=(new Date().getTime())
	if(st>0)
		msdb.collection("rt").insertOne({ "st": st, "end":et})
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