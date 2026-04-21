// const API = "http://127.0.0.1:8000"

// async function loadAnalytics(){

// try{

// const res = await fetch(API + "/analytics")

// const data = await res.json()

// const labels = data.data.map(d => d[0])
// const values = data.data.map(d => d[1])

// const ctx = document.getElementById("chart")

// new Chart(ctx,{

// type:"pie",

// data:{
// labels:labels,
// datasets:[{
// label:"Fatigue Events",
// data:values,
// backgroundColor:[
// "#00e5ff",
// "#ffcc00",
// "#ff4444",
// "#33cc33"
//   ]
//  }]
// },

// options:{
// responsive:true,
// plugins:{
// legend:{
// position:"bottom"
//    }
//  }
// }

// })

// }catch(error){

// console.error("Analytics load error",error)

// }

// }

// loadAnalytics()

// const API = "http://127.0.0.1:8000";

// async function loadAnalytics() {
//     try {
//         // =========================
//         // 1. LOAD PIE CHART DATA
//         // =========================
//         const res = await fetch(API + "/analytics");
//         const data = await res.json();

//         const labels = data.data.map(d => d[0]);
//         const values = data.data.map(d => d[1]);

//         const ctx = document.getElementById("chart");

//         new Chart(ctx, {
//             type: "pie",
//             data: {
//                 labels: labels,
//                 datasets: [{
//                     label: "Fatigue Events",
//                     data: values,
//                     backgroundColor: [
//                         "#00e5ff",
//                         "#ffcc00",
//                         "#ff4444",
//                         "#33cc33"
//                     ]
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 plugins: {
//                     legend: {
//                         position: "bottom"
//                     }
//                 }
//             }
//         });

//         // =========================
//         // 2. LOAD DETAILED ANALYTICS
//         // =========================
//         const detailRes = await fetch(API + "/analytics-details");
//         const detailData = await detailRes.json();

//         const rows = detailData.data;

//         let maxScore = 0;
//         let maxTime = "--";
//         let totalScore = 0;
//         let fatigueEvents = 0;

//         const timeline = document.getElementById("timeline");
//         timeline.innerHTML = "";

//         if (rows.length === 0) {
//             document.getElementById("peakFatigue").innerText = "--";
//             document.getElementById("peakTime").innerText = "--";
//             document.getElementById("riskScore").innerText = "--";
//             return;
//         }

//         rows.forEach(row => {
//             const time = row[0];
//             const score = parseFloat(row[1]);
//             const status = row[2];

//             totalScore += score;

//             if (score > maxScore) {
//                 maxScore = score;
//                 maxTime = time;
//             }

//             if (status !== "Alert") {
//                 fatigueEvents++;
//             }

//             // Create timeline segment
//             const div = document.createElement("div");
//             div.classList.add("timeline-segment");

//             if (status === "Alert") {
//                 div.classList.add("alert");
//             } else if (status === "Mild Fatigue") {
//                 div.classList.add("mild");
//             } else {
//                 div.classList.add("drowsy");
//             }

//             div.title = `${status} | Score: ${score.toFixed(2)} | ${time}`;
//             timeline.appendChild(div);
//         });

//         // =========================
//         // 3. PEAK FATIGUE
//         // =========================
//         document.getElementById("peakFatigue").innerText = maxScore.toFixed(2);
//         document.getElementById("peakTime").innerText = maxTime;

//         // =========================
//         // 4. DRIVER RISK SCORE
//         // =========================
//         const avgScore = totalScore / rows.length;
//         const risk = Math.min(100, (avgScore * 70) + (fatigueEvents * 5));

//         document.getElementById("riskScore").innerText = `${risk.toFixed(0)} / 100`;

//     } catch (error) {
//         console.error("Analytics load error", error);
//     }
// }

// loadAnalytics();



const API = "http://127.0.0.1:8000";

async function loadAnalytics() {

    try {

        const res = await fetch(API + "/analytics");
        const data = await res.json();

        const labels = data.data.map(d => d[0]);
        const values = data.data.map(d => d[1]);

        new Chart(document.getElementById("chart"), {
            type: "pie",
            data: {
                labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        "#00e5ff",
                        "#ffcc00",
                        "#ff4444",
                        "#33cc33"
                    ]
                }]
            }
        });

        const detailRes = await fetch(API + "/analytics-details");
        const rows = (await detailRes.json()).data;

        let maxScore = 0, maxTime = "--";
        let total = 0, fatigueEvents = 0;

        const timeline = document.getElementById("timeline");
        timeline.innerHTML = "";

        rows.forEach(r => {

            const score = parseFloat(r[1]);
            const status = r[2];
            const time = r[0];

            total += score;

            if (score > maxScore) {
                maxScore = score;
                maxTime = time;
            }

            if (status !== "Alert") fatigueEvents++;

            const div = document.createElement("div");
            div.classList.add("timeline-segment");

            if (status === "Alert") div.classList.add("alert");
            else if (status === "Mild Fatigue") div.classList.add("mild");
            else div.classList.add("drowsy");

            timeline.appendChild(div);
        });

        document.getElementById("peakFatigue").innerText = maxScore.toFixed(2);
        document.getElementById("peakTime").innerText = maxTime;

        const avg = total / rows.length;
        const risk = Math.min(100, (avg * 70) + (fatigueEvents * 5));

        document.getElementById("riskScore").innerText = risk.toFixed(0) + " / 100";

    } catch (err) {
        console.error(err);
    }
}

loadAnalytics();