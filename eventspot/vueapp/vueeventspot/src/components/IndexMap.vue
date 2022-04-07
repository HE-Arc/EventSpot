<template>
  <div class="row soft-padding margin-zero">
    <div class="container border-solid-black" id="mapContainer"></div>
    <div class="container border-solid-black">
        Legend :
        Current position : &nbsp;<i class="fa fa-home"></i>&nbsp;,&nbsp;
        My events : &nbsp;<i class="fa fa-user"></i>&nbsp;,&nbsp;
        Friends : &nbsp;<i class="fa fa-users"></i>&nbsp;,&nbsp;
        Public : &nbsp;<i class="fa fa-globe"></i>
     </div>

  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { baseURL } from '../axios-api';

import LeafletSearch from "leaflet-search";
import 'leaflet.awesome-markers';
L.AwesomeMarkers.Icon.prototype.options.prefix = 'fa';

export default {
     name: "IndexMap",
     props: ["events",],
     data() {
        return {
        map: null,
        currentPosMarker: null,
        latlng: null,
        imgDefault:
            "<img class='miniImg' src='@/assets/default.jpg' alt='default.jpg'/><br><br>",
        imgPath: "",
        //Marker from https://github.com/pointhi/leaflet-color-markers
        myMarker: new L.AwesomeMarkers.icon({
            markerColor: 'black',
            icon : 'user'
        }),
            publicMarker: new L.AwesomeMarkers.icon({
            icon: 'globe',
            markerColor: 'blue',
        }),
        userFriendsMarker : new L.AwesomeMarkers.icon({
            icon: 'users',
            markerColor: 'green',
        }),
        homeMarker : new L.AwesomeMarkers.icon({
            icon: 'home',
            markerColor: 'red',
        }),
        };
    },
    onBeforeUnmount() {
        if (this.map) {
        this.map.remove();
        }
    },
    mounted() {
        this.initMap(); //prepare the map
        this.addEvents();
        this.getCurrentPosition();
    },
    methods: {
        /**
         * build the map
         */
        initMap() {
            this.map = L.map('mapContainer').setView({lon: 7.4474, lat: 46.9480}, 5);
            
            //add controller to the map
            this.map.addControl(
                new L.Control.Search({
                url: "https://nominatim.openstreetmap.org/search?format=json&q={s}",
                jsonpParam: "json_callback",
                propertyName: "display_name",
                propertyLoc: ["lat", "lon"],
                marker: L.circleMarker([0, 0], { radius: 30 }),
                autoCollapse: true,
                zoom: 10,
                autoType: true,
                minLength: 2,
                })
            );
            // add the OpenStreetMap tiles
            var gl = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                minZoom: 5,
                attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
            }).addTo(this.map);
            
            //update gl when zoomed
            this.map.on('zoomend',function(){
                gl._update();
            });
        },
        /**
         * Add events on the map
         */
        addEvents() {
            this.events.forEach(event => {

                 var marker = this.publicMarker; //by default it's a public event

                 if(event.user.username === this.$store.state.username) //if it's my events
                    marker = this.myMarker;
                 else if(event.is_private) //if it's a private event
                    marker = this.userFriendsMarker;

                 this.drawMarker(event, marker);
            });

        },
        /*
        * draw a marker on the map
        */
        drawMarker(event, icon) {
            var mark = L.marker([event.lattitude,event.longitude], {
                icon: icon,
            });

            var imgPth = "";
            
            //add image in picture if exist
            if (event.image != null) {
                imgPth = `<img class='miniImg' src="${baseURL}${event.image}" alt="${event.title}"'/><br><br>`;
            }
            //else default image
            else {
                imgPth = `<img class='miniImg' src="${require("@/assets/default.jpg")}" alt="default"'/><br><br>`;
            }

            //add popup to marker
            //event name
            //user name
            //image
            //link to show event
            mark.bindPopup(
                `<h5>${event.title}</h5>
                <i>Author : ${event.user.username}</i><br>
                ${imgPth}
                <a class="btn btn-info" href="events/${event.id}">See more information</a>
                    `
            );

            mark.addTo(this.map);
        },

        /**
         * find the curent position and add to the map,
         * only if accecpted location
         */
        getCurrentPosition()
        {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    var coords = [position.coords.latitude,position.coords.longitude];
                    L.marker(coords, {
                        icon: this.homeMarker,
                    }).addTo(this.map);

                    this.map.setView(coords,5);
                });

            }
        }

     },


}
</script>


<style>
.leaflet-popup-content-wrapper {
  width: 28em;
  height: 26em;
}
.leaflet-popup-content-wrapper a {
  text-decoration: none;
  color: white;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
img.miniImg {
  height: 15em;
  width: 100%;
  object-fit: cover;
}
#mapContainer {
  width: 100vw;
  height: 60vh;
}

 .fa-globe, .fa-house, .fa-home, .fa-users, .fa-user
  {
        margin-top: 15px;
  }


@import "~leaflet-search/src/leaflet-search.css";
@import "~leaflet.awesome-markers/dist/leaflet.awesome-markers.css";
</style>
