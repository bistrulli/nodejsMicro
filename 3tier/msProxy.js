const express = require('express');
const httpProxy = require('http-proxy');
const params = require('params-cli');

getParam = function(params, pname) {
	if (params.has(`${pname}`)) {
		return params.get(`${pname}`)
	} else {
		throw new Error(`${pname} required`);
	}
}

port = getParam(params,"port")
tgtPort = getParam(params,"tgtPort")

const proxy = httpProxy.createProxyServer({});
const app = express();
app.get('*', function(req, res) {
	let reqTime = new Date().getTime()
	proxy.web(req, res, { target: `${req.protocol}://${req.hostname}:${tgtPort}/${reqTime}` });
});

const server = app.listen(port, function() {
	var host = server.address().address
	var port = server.address().port
	console.log("proxy listening at http://%s:%s", host, port)
});