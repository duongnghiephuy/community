
class searchNearby {
    constructor(lat, long, distance, map) {
        this.lat = lat;
        this.long = long;
        this.distance = distance;
        this.map = map;
    }

    getNearby() {
        const url = `http://127.0.0.1:8000/geocommunity/searchnearby/${this.lat}/${this.long}/${this.distance}`;
        fetch(url).then(response => this.mapNearby(response)).catch(error => {
            console.error(`Could not get nearby locations: ${error}`);
            errorMessage.innerHTML += "Please check your network";
        });;
    }

    mapNearby(response) {


        if (typeof (this.markers) !== "undefined") {
            this.map.removeLayer(this.markers);

        }

        let positions = [];
        const data = response.json().features;
        positions.push(L.marker([this.lat, this.long]).bindPopup("<strong>Current Location</strong>"));
        if (response.ok) {
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
            else {
                errorMessage.innerHTML += " No nearby communities found";

            }
        }
        else {
            errorMessage.innerHTML += " Please check your network";
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


    errorMessage.innerHTML = "";
    try {
        const position = await getCurrentLocation();
        res.lat = position.coords.latitude;
        res.long = position.coords.longitude;
    }
    catch (error) {
        res.lat = 999;
        res.long = 999;

        errorMessage.innerHTML += error;

    }

    res.distance = document.querySelector("#distance").value;
    res.getNearby();
}

async function resolveParam2(e) {
    errorMessage.innerHTML = "";
    if (e.key === "Enter" || clickAddress.contains(e.target)) {
        const address = inputAddress.value;
        let cur_coordinate = [999, 999];
        try {
            const url = `https://nominatim.openstreetmap.org/search?q=${address}&format=geojson&limit=1`;

            const geores = await fetch(url);

            const geojsondata = await geores.json();

            cur_coordinate = geojsondata.features[0].geometry.coordinates;
            if (typeof (cur_coordinate !== "undefined") && cur_coordinate.length > 0) {

                res.lat = cur_coordinate[1];
                res.long = cur_coordinate[0];
            }
        }
        catch (error) {
            res.lat = 999;
            res.long = 999;
            errorMessage.innerHTML += "Address not valid, please try a more general one";
        }
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

errorMessage = document.querySelector(".error-message");

map = L.map("map").setView([0, 0], 15);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors', tileSize: 512, zoomOffset: -1

}).addTo(map);
res = new searchNearby(999, 999, 2, map);