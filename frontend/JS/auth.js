const API = "http://127.0.0.1:8000"
// REGISTER USER

async function register(){

try{

const username =
document.getElementById("username").value.trim()

const password =
document.getElementById("password").value.trim()


// validation
if(username === "" || password === ""){

alert("Username and password required")
return

}


const res = await fetch(API + "/register", {

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
username:username,
password:password
})

})

const data = await res.json()


if(data.status === "success"){

alert("User successfully registered")

window.location.href = "login.html"

}
else{

alert("User already exists")

}

}
catch(error){

alert("Server error. Make sure backend is running.")

}

}

// LOGIN USER

async function login(){

try{

const username =
document.getElementById("username").value.trim()

const password =
document.getElementById("password").value.trim()


// validation
if(username === "" || password === ""){

alert("Username and password required")
return

}

const res = await fetch(API + "/login", {

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
username:username,
password:password
})

})

const data = await res.json()


if(data.status === "success"){

// save login state
localStorage.setItem("user", username)

alert("Login successful")

window.location.href = "detection.html"

}
else{

alert("Invalid username or password")

}

}
catch(error){

alert("Server error. Make sure backend is running.")

}

}

// LOGOUT FUNCTION (use later)

function logout(){

localStorage.removeItem("user")

window.location.href = "login.html"

}