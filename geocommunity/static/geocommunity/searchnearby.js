
class searchNearby {
    constructor(address, lat, long, distance) {
        this.address = address;
        this.lat = lat;
        this.long = long;
        this.distance = distance;
        this.map = L.map("map").setView([0, 0], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);
    }

    getNearby() {
        const url = `http://127.0.0.1:8000/geocommunity/"${this.address}"/"${this.lat}"/"${this.long}"/${this.distance}`;
        fetch(url).then(response => this.mapNearby(response)).catch(error => {
            console.error(`Could not get nearby locations: ${error}`);
        });;
    }

    mapNearby() {
        return 0;
    }
}



function getCurrentLocation() {
    return Promise(
        (resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        }
    );
}

async function resolveParam(e) {
    if (e.target === "button" && e.target.classList.contains("current-location")) {
        const position = await getCurrentLocation();
        res.address = "";
        res.lat = position.coords.latitude;
        res.long = position.coords.longitude;
        res.distance = document.querySelector("#distance").value;
    }
    else if ((e.target === "input" && e.key === "Enter") || (e.target === "button")) {
        const address = e.target.value;
        res.address = address;
        res.lat = 999;
        res.long = 999;
        res.distance = document.querySelector("#distance").value;
    }
}

currentLoc = document.querySelector(".current-location");
currentLoc.addEventListener("click", resolveParam);

inputAddress = document.querySelector(".searchTerm");
inputAddress.addEventListener("keypress", resolveParam);

clickAddress = document.querySelector(".searchButton");
clickAddress.addEventListener("click", resolveParam);

res = new searchNearby("", 999, 999);