let map;

async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");

    map = new Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var userLocation = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            // Set the map center to the user's location
            map.setCenter(userLocation);

            // Add a marker for the user's location
            var marker = new google.maps.Marker({
                position: userLocation,
                map: map,
                title: 'Your Location'
            });
        }, function () {
            // Handle geolocation error
            console.error('Error: The Geolocation service failed.');
        });
    } else {
        // Browser doesn't support geolocation

    }
}

initMap();


function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                var userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                showMap(userLocation);
            },
            function (error) {
                console.error('Error getting user location:', error);
                showMap();  // Show map without user location
            }
        );
    } else {
        console.error('Geolocation is not supported by this browser.');
        showMap();  // Show map without user location
    }
}
function showMap(userLocation) {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: userLocation || { lat: 0, lng: 0 },  // Default to center of the world if user location is not available
        zoom: 12  // Adjust the zoom level as needed
    });

    // Add markers for nearby locations
    addNearbyMarkers(map, userLocation);
}
function addNearbyMarkers(map, userLocation) {
    var nearbyLocations = [
        { lat: 38.44871609429781, lng: 27.191855058374102, name: 'Test' },
        { lat: 38.426016522455186, lng: 27.137292873180375, name: 'Alsancak' },
        { lat: 38.449564914809464, lng: 27.179649304353735, name: 'Bornova' },
        { lat: 37.84032814580038, lng: 27.845446238235144, name: 'Aydın' },

        // Add more locations as needed
    ];

    // Filter locations within 30 km proximity
    var filteredLocations = nearbyLocations.filter(function (location) {
        return calculateDistance(userLocation, location) <= 30;
    });

    filteredLocations.forEach(function (location) {
        var marker = new google.maps.Marker({
            position: { lat: location.lat, lng: location.lng },
            map: map,
            title: location.name
        });

        // Add additional information or actions when a marker is clicked
        marker.addListener('click', function () {
            // Add your logic here (e.g., show details, navigate to a page, etc.)
            console.log('Marker clicked:', location.name);
        });
    });
}

// Function to calculate distance between two sets of coordinates using Haversine formula
function calculateDistance(coord1, coord2) {
    var R = 6371; // Radius of the Earth in kilometers
    var dLat = degToRad(coord2.lat - coord1.lat);
    var dLng = degToRad(coord2.lng - coord1.lng);
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(degToRad(coord1.lat)) * Math.cos(degToRad(coord2.lat)) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var distance = R * c; // Distance in kilometers
    return distance;
}

// Function to convert degrees to radians
function degToRad(degrees) {
    return degrees * (Math.PI / 180);
}

document.addEventListener('DOMContentLoaded', function () {
    getUserLocation();
});

function validatePassword() {
    var password = document.getElementById('password').value;

    // Password must be at least 8 characters, include 1 number, and 1 non-alphanumeric character
    var passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$/;

    if (!passwordRegex.test(password)) {
        alert("Password must be at least 8 characters, include 1 number, and 1 non-alphanumeric character.");
        return false;
    }

    return true;
}

fetch('https://run.mocky.io/v3/2d6ea01e-0e7a-4130-a3f1-423ff5ea5114')
    .then(response => response.json())
    .then(data => {
        var dropdown = document.getElementById('city');
        data.areaCodes.forEach(item => {
            var option = document.createElement('option');
            option.value = item.city;
            option.text = item.city;
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching data:', error));

fetch('https://run.mocky.io/v3/ca3a5003-3878-403b-a32d-81fb08fd16c4')
    .then(response => response.json())
    .then(data => {
        var dropdown = document.getElementById('country');
        data.countries.forEach(item => {
            var option = document.createElement('option');
            option.value = item.country;
            option.text = item.country;
            dropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching data:', error));


function onSignIn(googleUser) {
    // Retrieve profile information, including name and email
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId());
    console.log('Name: ' + profile.getName());
    console.log('Email: ' + profile.getEmail());
    window.location.href = '/';  

    // You can also perform additional actions here, such as sending the user's information to the server
    // using AJAX to authenticate the user on the server side.
}   