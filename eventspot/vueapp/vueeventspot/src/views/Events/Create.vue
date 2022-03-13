<template>
    <div class="EventsCreate">
        <NavBar></NavBar>
        <main class="container">
            <h1 class="mb-5">Create a new event</h1>
            <form>
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group mb-3">
                            <label for="title">Title</label>
                            <input required type="text" class="form-control" id="title" aria-describedby="title" placeholder="Enter title">
                            <small class="form-text text-muted">Enter a title to identify your event</small>
                        </div>
                        <div class="form-group mb-3">
                            <label for="date">Date</label>
                            <input required type="datetime-local" :min="Date.now()" class="form-control" id="date" aria-describedby="date">
                            <small class="form-text text-muted">Enter a title to identify your event</small>
                        </div>
                        <div class="form-group mb-3" >
                            <input class="form-control" type="file" id="formFile" accept="image/*">
                            <small for="formFile" class="form-text form-label">Import a picture for you event</small>
                        </div>
                        <div class="form-check form-switch mb-3">
                            <input class="form-control form-check-input" type="checkbox" id="private" >
                            <label class="form-text form-check-label" for="private">Private event</label>
                        </div>
                    </div>
                    <div class="col-md-6 ">
                         <div id="mapContainer" class="mb-3"></div>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </main>
        <MyFooter></MyFooter>
    </div>
</template>

<script>
//import { getAPI } from '../../axios-api.js'
//import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import MyFooter from '../../components/Footer.vue'
import L from "leaflet";
import 'leaflet/dist/leaflet.css';

export default {
    name: "EventsCreate",
    components: {
        NavBar,
        MyFooter
    },
    data() {
    return {
      map: null,
    };
  },
  mounted() {
    // initialize Leaflet
    this.map = L.map('mapContainer').setView({lon: 0, lat: 0}, 2);

    // add the OpenStreetMap tiles
    var gl = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(this.map);
    this.map.on('zoomend',function(){
        gl._update();
    });
  },
  onBeforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },

   // computed: mapState(['APIData']),
}
</script>

<style scoped>
    h1{
        margin-top:3rem!important;
    }
    #mapContainer {
        width: 100%;
        height: 100%;
    }
    
</style>
