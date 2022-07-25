var express = require('express');
var sleep = require('sleep');
const params = require('params-cli');
const { MongoClient } = require('mongodb');
var exponential = require('@stdlib/random-base-exponential');
var app = express();
const superagent = require('superagent');
var Agent = require('agentkeepalive');
var rwc = require("random-weighted-choice");

const cluster = require('node:cluster');
const process = require('node:process');


getMSHRtime = function() {
	let hrTime = process.hrtime();
	return (hrTime[0] * 1000 + hrTime[1] / 1000000.0);
}

doWork = function(delay) {
	let stime = getMSHRtime()
	let i = 0;
	while ((getMSHRtime() - stime) <= delay) {
		i = i + 1;
	}
}

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

slowDown = function(mu, so, st) {
	return mu * (1 - (so - Math.min(so, st)) / so)
}

var ms_name = null
var port = null
var ncore = 4
var stime = 200.0

stime = (1.0 / slowDown(1.0 / stime, ncore, ncore))

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


	//invece di predere il tempo di riposta in questo modo
	//faccio un proxy lato ricevete che mi aggiunge il tempo di arrivo della richiesta e 
	//considero quello come tempo di risposta
	//se il proxy non fa nulla ed e molto veloce non dovrebbe aggiungere contesa
	//let reqTime = new Date().getTime()
	//resp = await axios.get(`http://localhost:${tierPort}`,{"proxy":false, "agent": httpAgent})
	resp = await superagent.get(`http://localhost:${tierPort}`);
	//console.log(response.latency)

	let delay = exponential(1.0 / stime);
	sleep.msleep(Math.max(Math.round(delay),0))
	//doWork(delay);

	let et = (new Date().getTime())
	msdb.collection("rt").insertOne({ "st": st, "end": et })

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
	var server = app.listen(port,"localhost",100000, async function() {
		var host = server.address().address
		var port = server.address().port
		global.msdb = await mongoInit(ms_name)
		console.log("Example app listening at http://%s:%s", host, port)
	})
  console.log(`Worker ${process.pid} started`);
}