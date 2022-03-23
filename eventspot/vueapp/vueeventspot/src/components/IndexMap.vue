<template>
  <div class="row soft-padding margin-zero">
    <div class="container border-solid-black" id="mapContainer"></div>
    <div class="container border-solid-black">
        Legend :
        Current position : &nbsp;<i class="fa fa-home"></i>&nbsp;,&nbsp;
        My memories : &nbsp;<i class="fa fa-user"></i>&nbsp;,&nbsp;
        Friends : &nbsp;<i class="fa fa-users"></i>&nbsp;,&nbsp;
        Public : &nbsp;<i class="fa fa-globe"></i>
     </div>

  </div>
</template>

<script>
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// eslint-disable-next-line no-unused-vars
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
        //https://github.com/pointhi/leaflet-color-markers
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
    },
    methods: {
        initMap() {
            this.map = L.map('mapContainer').setView({lon: 0, lat: 0}, 2);
            this.map.addControl(
                new L.Control.Search({
                url: "https://nominatim.openstreetmap.org/search?format=json&q={s}",
                jsonpParam: "json_callback",
                propertyName: "display_name",
                propertyLoc: ["lat", "lon"],
                marker: L.circleMarker([0, 0], { radius: 30 }),
                autoCollapse: true,
                autoType: true,
                minLength: 2,
                })
            );
            // add the OpenStreetMap tiles
            var gl = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
                attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
            }).addTo(this.map);
            this.map.on('zoomend',function(){
                gl._update();
            });

            this.map.on('zoomend',function(){
                gl._update();
            });
        },
        addEvents() {
            //foreach memories
           /* this.events.forEach((event) => {
                //add publicMarker marker
               // this.drawMarker(event, event.user, this.publicMarker);
            });*/
            const self = this;
            this.events.forEach(event => {
                    self.drawMarker(event, this.homeMarker);
                });

        },
        /*
        * draw a marker on the map
        */
        drawMarker(event, icon) {
            console.log(event);
        },

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
  height: 45vh;
}
@import "~leaflet-search/src/leaflet-search.css";
@import "~leaflet.awesome-markers/dist/leaflet.awesome-markers.css";
</style>