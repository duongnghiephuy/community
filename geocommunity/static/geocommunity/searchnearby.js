
class searchNearby {
    constructor(address, lat, long, distance, map) {
        this.address = address;
        this.lat = lat;
        this.long = long;
        this.distance = distance;
        this.map = map;
    }

    getNearby() {
        const url = `http://127.0.0.1:8000/geocommunity/searchnearby/${this.address}/${this.lat}/${this.long}/${this.distance}`;
        fetch(url).then(response => this.mapNearby(response)).catch(error => {
            console.error(`Could not get nearby locations: ${error}`);
        });;
    }

    mapNearby(response) {


        if (typeof (this.markers) !== "undefined") {
            this.map.removeLayer(this.markers);

        }
        let positions = [];
        const data = response.json().features;
        positions.push(L.marker([this.lat, this.long]).bindPopup("<strong>Current Location</strong>"));
        if (typeof (data) !== "undefined" && data.length > 0) {
            for (const feature of data) {
                let marker = L.marker([feature.coordinates[1], feature.coordinates[0]]);
                let popup = `<p><strong>${feature.properties.name}</strong></p>
                        <p>${feature.properties.description}</p>
                        <button type="button" value="join" hx-get="/join/${feature.properties.pk}" hx-trigger="click" hx-swap="delete">Join</button>`;
                marker.bindPopup(popup);
                positions.push(marker)

            }
        }
        this.markers = L.layerGroup(positions);
        this.markers.addTo(this.map);
        this.map.setView(new L.LatLng(this.lat, this.long), 15);
        console.log("Finish");
    }
}



function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (navigator && navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(resolve, reject);
        } else {
            reject(new Error('Geolocation is not supported by this environment'));
        }
    });
}

async function resolveParam1(e) {

    console.log("Here");
    const position = await getCurrentLocation();
    res.address = "No";
    res.lat = position.coords.latitude;
    res.long = position.coords.longitude;
    res.distance = document.querySelector("#distance").value;
    res.getNearby();
}

async function resolveParam2(e) {
    if (e.key === "Enter" || clickAddress.contains(e.target)) {
        const address = inputAddress.value;
        res.address = address;
        res.lat = 999;
        res.long = 999;
        res.distance = document.querySelector("#distance").value;
        res.getNearby();
    }

}

currentLoc = document.querySelector(".current-location");
currentLoc.addEventListener("click", resolveParam1);

inputAddress = document.querySelector(".searchTerm");
inputAddress.addEventListener("keypress", resolveParam2);

clickAddress = document.querySelector(".searchButton");
clickAddress.addEventListener("click", resolveParam2);


map = L.map("map").setView([0, 0], 15);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors', tileSize: 512, zoomOffset: -1

}).addTo(map);
res = new searchNearby("No", 999, 999, 2, map);