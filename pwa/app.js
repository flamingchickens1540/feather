let shots = []

let qrcode = new QRCode("qr", {
    width: 512,
    height: 512,
    colorDark: "#000",
    colorLight: "#fff",
    correctLevel: QRCode.CorrectLevel.L
})

function toggleQR() {
    if (document.getElementById("qr").style.display === "none") { // If QR isn"t showing, show it
        document.getElementById("qr-button").innerText = "Back"
        let shotsObj = {}
        for (let i in shots) {
            shotsObj[shots[i]["time"]] = shots[i]["result"];
        }
        jsonBody = JSON.stringify({
            matchNumber: document.getElementById("matchNumber").value,
            shots: shotsObj
        })
        qrcode.makeCode(btoa(jsonBody));
        console.log(jsonBody)
        document.getElementById("qr").style.display = "block"
        document.getElementById("matchButtons").style.display = "none"
    } else { // If QR is showing
        document.getElementById("qr-button").innerText = "QR"
        document.getElementById("qr").style.display = "none"
        document.getElementById("matchButtons").style.display = "flex"
    }
}

function updateCount() {
    document.getElementById("count").innerText = shots.length
}

function logShot(shotResult) {
    shots.push({
        time: Date.now(),
        result: shotResult
    })
    updateCount()
}

function clearShots() {
    if (confirm("Are you sure you want to clear this match?")) {
        shots = []
        updateCount()
    }
}

function undo() {
    shots.pop()
    updateCount()
}

if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
        navigator.serviceWorker
            .register("/sw.js")
            .then(res => console.log("service worker registered"))
            .catch(err => console.log("service worker not registered", err));
    });
}
