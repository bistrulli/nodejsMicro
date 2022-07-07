var express = require('express');
var sleep = require('sleep');
const params = require('params-cli');
const { MongoClient } = require('mongodb');
var exponential = require('@stdlib/random-base-exponential');
var app = express();
const axios = require('axios');
var rwc = require("random-weighted-choice");

mongoInit = async function(ms_name) {
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
	return dbo
}

var ms_name = null
var port = null
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
	let st = parseInt(req.params["st"])

	let table = [
		{ weight: 1, id: "tier1", port: 8082 },
		{ weight: 0, id: "tier2", port: 8083 }
	];
	let tier = rwc(table);

	let tierPort = null
	for (i = 0; i < table.length; i++) {
		if (table[i].id == tier) {
			tierPort = table[i].port
			break
		}
	}

	let reqTime = new Date().getTime()
	await axios.get(`http://localhost:${tierPort}/${reqTime}`)


	let delay = exponential(1.0 / 300.0);
	sleep.msleep(Math.round(delay))
	const et = (new Date().getTime())
	msdb.collection("rt").insertOne({ "st": st, "end": et })
	res.send('Hello World ' + ms_name);
})

app.get('/mnt', function(req, res) {
	res.send('running ' + ms_name);
})

var server = app.listen(port, async function() {
	var host = server.address().address
	var port = server.address().port
	global.msdb = await mongoInit(ms_name)
	console.log("Example app listening at http://%s:%s", host, port)
})