const API = "http://127.0.0.1:8000"

async function loadAnalytics(){

try{

const res = await fetch(API + "/analytics")

const data = await res.json()

const labels = data.data.map(d => d[0])
const values = data.data.map(d => d[1])

const ctx = document.getElementById("chart")

new Chart(ctx,{

type:"pie",

data:{
labels:labels,
datasets:[{
label:"Fatigue Events",
data:values,
backgroundColor:[
"#00e5ff",
"#ffcc00",
"#ff4444",
"#33cc33"
  ]
 }]
},

options:{
responsive:true,
plugins:{
legend:{
position:"bottom"
   }
 }
}

})

}catch(error){

console.error("Analytics load error",error)

}

}

loadAnalytics()