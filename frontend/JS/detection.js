const API = "http://127.0.0.1:8000"

const statusText = document.getElementById("status")

// START DETECTION
async function startDetection(){

try{

statusText.innerText = "Starting detection..."

const res = await fetch(API + "/start-detection")

const data = await res.json()

if(data.status === "started"){

statusText.innerText = "Detection Running"

}
else{

statusText.innerText = "Detection already running"

}

}
catch(error){

statusText.innerText = "Error starting detection"

}

}


// STOP DETECTION
async function stopDetection(){

try{

statusText.innerText = "Stopping detection..."

const res = await fetch(API + "/stop-detection")

const data = await res.json()

if(data.status === "stopped"){

statusText.innerText = "Detection Stopped"

}
else{

statusText.innerText = "Detection not running"

}

}
catch(error){

statusText.innerText = "Error stopping detection"

}

}