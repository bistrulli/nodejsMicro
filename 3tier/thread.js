//const sleep = require('sleep');
const {execSync} = require('child_process');
const exponential = require('@stdlib/random-base-exponential');
const { parentPort, workerData } = require('worker_threads');

// Something you shouldn"t run in main thread
// since it will block.
function doWork(delay) {
	d=(exponential(1.0 / delay)/1000.0).toFixed(4)
	execSync(`sleep ${d}`);
}

// Main thread will pass the data you need
// through this event listener.
parentPort.on('message', (delay) => {
doWork(parseFloat(delay));
// return the result to main thread.
parentPort.postMessage("done");
});