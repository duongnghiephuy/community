
class searchNearby {
    constructor(address, lat, long) {
        this.address = address;
        this.lat = lat;
        this.long = long;
    }

    getNearby() {
        const url = `http://127.0.0.1:8000/geocommunity/$"{this.address}"/$"{this.lat}"/$"{this.long}"`;
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
    if (e.target === "button") {
        const position = await getCurrentLocation();
        const res = new searchNearby("", position.coords.latitude, position.coords.longitude)
    }
    else if (e.target === "input" && e.key === "Enter") {
        const address = e.target.value;
        const res = new searchNearby(address, 999, 999);
    }
}

currentLoc = document.querySelector(".current-location");
currentLoc.addEventListener("click", resolveParam);

inputAddress = document.querySelector(".searchTerm");
inputAddress.addEventListener("keypress", resolveParam)


