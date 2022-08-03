var express = require('express');
// const {execSync} = require('child_process');
var sleep = require('sleep');
const exponential = require('@stdlib/random-base-exponential');
const params = require('params-cli');
var app = express();
const axios = require('axios')
var rwc = require("random-weighted-choice");
const { MongoClient } = require('mongodb');
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
	let client = await MongoClient.connect(`mongodb://localhost:27017/`)
	if (client.err) { console.log('error'); }
	else { console.log('conneted to mongo'); }
	return client
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

axios.defaults.headers = {
		  'Cache-Control': 'no-cache',
		  'Pragma': 'no-cache',
		  'Expires': '0',
		};

var ms_name = null
var port = null
var stime = 200.0
global.ms2Port=null
global.ms3Port=null

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
	let st=new Date();
	if(ms2Port==null){
		var client = await mongoInit()
		var db=client.db("sys")
		var ms2obj=await db.collection("ms").findOne({name:"ms2"})
		ms2Port=ms2obj.prxPort
	}
	
	let table = [
		{ weight: 1, id: "tier2", port: ms2Port},
		{ weight: 0, id: "tier3", port: null }
	];
	let tier = rwc(table);

	let tierPort = null
	for (i = 0; i < table.length; i++) {
		if (table[i].id == tier) {
			tierPort = table[i].port
			break
		}
	}
	let response = await axios.get(`http://localhost:${tierPort}`)
	if (response.err) { console.log('error'); }
	else { 
		doWork(stime*1e06)
		//sleep.msleep(stime)
		// d=(exponential(1.0 / delay)/1000.0).toFixed(4)
		// d=(stime)
		// execSync(`sleep ${d}`);
		
		res.send('Hello World ' + ms_name); 
		//end=new Date();
		// console.log(end.getTime()-st.getTime());
	}
})

app.get('/mnt', function(req, res) {
	res.send('running ' + ms_name);
})
  
  
var server = app.listen(port,"localhost", async function() {
	var host = server.address().address
	var port = server.address().port
	console.log("Example app listening at http://%s:%s", host, port)
})
console.log(`Worker ${process.pid} started`);