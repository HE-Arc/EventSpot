<template>
    <div class="EventsCreate">
        <NavBar></NavBar>
        <main class="container">
            <h1 class="mb-4">{{this.pageTitle}}</h1>
            <form v-on:submit.prevent="submitForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group mb-2">
                            <label for="title">Title</label>
                            <input required v-model="form.title" type="text" class="form-control" id="title" aria-describedby="title" placeholder="Enter title">
                            <small v-if="errors.title == null" class="form-text text-muted">Enter a title to identify your event</small>
                            <small v-else class="form-text text-danger ">{{errors.title[0]}}</small>
                        </div>
                        <div class="form-group mb-2">
                            <label required for="title">Description</label>
                            <textarea  rows="4"  v-model="form.description"  class="form-control" id="description" aria-describedby="description"></textarea>
                            <small v-if="errors.description == null" class="form-text text-muted">Enter a description to talk about your event</small>
                            <small v-else class="form-text text-danger ">{{errors.description[0]}}</small>
                        </div>
                        <div class="form-group mb-2">
                            <label for="date">Date</label>
                            <input required v-model="form.date" type="datetime-local" :min="Date.now()" class="form-control" id="date" aria-describedby="date">
                            <small  v-if="errors.date == null" class="form-text text-muted">Enter a title to identify your event</small>
                            <small v-else class="form-text text-danger ">{{errors.date[0]}}</small>
                        </div>
                        <div class="form-group mb-2" >
                            <img v-if="form.image" :src="'http://localhost:8000'+form.image" alt="img event" class="img-thumbnail" style="height:15vh;">
                            <input @change="onChange($event)" class="form-control" type="file" id="formFile" accept="image/*">
                            <small v-if="errors.image == null" for="formFile" class="form-text form-label">Import a picture for you event</small>
                            <small v-else class="form-text text-danger ">{{errors.image[0]}}</small>
                        </div>
                        <div class="form-check form-switch mb-2">
                            <input v-model="form.is_private" class="form-control form-check-input" type="checkbox" id="private" >
                            <label class="form-text form-check-label" for="private">Private event</label>
                            <small v-if="errors.is_private != null" class="form-text text-danger ">{{errors.is_private[0]}}</small>
                        </div>
                    </div>
                    <div class="col-md-6">
                         <div id="mapContainer" class="mb-2"></div>
                         <small v-if="errors.lattitude != null" class="form-text text-danger ">{{errors.lattitude[0]}}</small>
                         <small v-if="errors.longitude != null" class="form-text text-danger ">{{errors.longitude[0]}}</small>
                         <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                    <div class="mb-3">&nbsp;</div>

                </div>
            </form>
        </main>
        <MyFooter class="d-none d-md-block"></MyFooter>
    </div>
</template>

<script>
import { getAPI } from '../../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import MyFooter from '../../components/Footer.vue'
import L from "leaflet";
import 'leaflet/dist/leaflet.css';

// eslint-disable-next-line no-unused-vars
import LeafletSearch from "leaflet-search";
import 'leaflet.awesome-markers';

L.AwesomeMarkers.Icon.prototype.options.prefix = 'fa';


export default {
    name: "EventsCreate",
    components: {
        NavBar,
        MyFooter
    },
    data() {
    return {
      requestApi : getAPI.post, //method ref
      targetApi : '/events/create',
      pageTitle : 'Create a new event',
      map: null,
      homeMarker: null,
      clickMarker: null,
      homeMarkerIcon : new L.AwesomeMarkers.icon({
        icon: 'home',
        markerColor: 'red',
      }),
      clickMarkerIcon : new L.AwesomeMarkers.icon({
        icon: 'map-pin',
        markerColor: 'green',
      }),

      form: {
        title : '',
        description : '',
        date: null,
        is_private : false,
        lattitude : null,
        longitude : null,
        image : null
      },
      errors: {
        title : '',
        description : null,
        date: null,
        is_private : null,
        lattitude : null,
        longitude : null,
        image : null
      }
    };
  },
  created () 
  {
    if(this.$route.params.id != undefined)
    {
        this.pageTitle = "Update event";
        getAPI.get('/events/' +this.$route.params.id, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
        .then(response => {
        this.$store.state.APIData = response.data;
        this.form.title = this.APIData.title;
        this.form.description = this.APIData.description;
        this.form.date = this.$moment(this.APIData.date).format('YYYY-MM-DDTHH:mm');
        this.form.is_private = this.APIData.is_private;
        this.form.image = this.APIData.image;
        this.form.lattitude = this.APIData.lattitude;
        this.form.longitude = this.APIData.longitude;

        this.requestApi = getAPI.put;
        this.targetApi = `events/${this.APIData.id}/update`;

        this.map.setView([this.form.lattitude,this.form.longitude], 10);
        this.clickMarker = L.marker([this.form.lattitude,this.form.longitude], {
                icon: this.clickMarkerIcon,
             }).addTo(this.map);


        })
        .catch(err => {
        console.log(err);
        })
    }
    
  },
  mounted() {
    // initialize Leaflet
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

    const self = this;
    //if the user have the geolcation
      if (navigator.geolocation) {
          //find the curent position
        navigator.geolocation.getCurrentPosition((position) => {
             self.form.lattitude = position.coords.latitude.toFixed(4);
             self.form.longitude = position.coords.longitude.toFixed(4);
             self.map.setView([self.form.lattitude,self.form.longitude], 10);
             self.homeMarker = L.marker([self.form.lattitude,self.form.longitude], {
                icon: this.homeMarkerIcon,
             }).addTo(this.map);
        });

      }
    
    this.map.on("click", (ev) => {
        self.form.lattitude = ev.latlng.lat.toFixed(4);
        self.form.longitude = ev.latlng.lng.toFixed(4);
        if (self.clickMarker == null) {
            self.clickMarker = L.marker([self.form.lattitude,self.form.longitude], {
                icon: this.clickMarkerIcon,
             }).addTo(this.map);
        }
        else {
          self.clickMarker.setLatLng([self.form.lattitude,self.form.longitude]).update(); //if the marker already exist update its pos
        }

    });
  },
  onBeforeUnmount() {
    if (this.map) {
      this.map.remove();
    }
  },
    methods: {
        onChange(event) {
            console.log(event.target.value);
            this.form.image = event.target.files[0]
        },
        submitForm(){
          
          let formData = new FormData();
          const self = this;
          
          Object.entries(this.form).forEach(([key, value]) => {
            formData.append(key, value);
           });

           if(this.form.image == null)
            formData.delete('image');

          this.requestApi(this.targetApi, formData,
          { headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`}
          })
          .then(response => {
            this.$router.push({ name: 'eventsShow', params: { id: response.data.id , state:"success"} })
          })
          .catch(error => {
              if(error.response.status == '400')
              {
                  self.errors = error.response.data;
              }
            console.log(error.response.data);  
            console.log(error.response.status);  
            console.log(error.response.headers);
          })
        }
    },
    computed: mapState(['APIData']),
}
</script>

<style scoped>
    h1{
        margin-top:1rem!important;
    }
    #mapContainer {
        width: 100%;
        height: 50vh;
        padding-bottom: 10em;
    }
    textarea {
        resize: none;
    }

    @import "~leaflet-search/src/leaflet-search.css";
    @import "~leaflet.awesome-markers/dist/leaflet.awesome-markers.css";
    
</style>

<style>
 .fa-map-pin
  {
        margin-top: 15px;
  }
 .fa-house
 {
      margin-top: 12px;
 }
</style>