<template>
    <div class="EventsCreate">
        <NavBar></NavBar>
        <main class="container">
            <h1 class="mb-5">Create a new event</h1>
            <form v-on:submit.prevent="submitForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group mb-3">
                            <label for="title">Title</label>
                            <input v-model="form.title" type="text" class="form-control" id="title" aria-describedby="title" placeholder="Enter title">
                            <small v-if="errors.title == null" class="form-text text-muted">Enter a title to identify your event</small>
                            <small v-else class="form-text text-danger ">{{errors.title[0]}}</small>
                        </div>
                        <div class="form-group mb-3">
                            <label for="title">Description</label>
                            <textarea  rows="4"  v-model="form.description"  class="form-control" id="description" aria-describedby="description"></textarea>
                            <small class="form-text text-muted">Enter a description to talk about your event</small>
                        </div>
                        <div class="form-group mb-3">
                            <label for="date">Date</label>
                            <input v-model="form.date" type="datetime-local" :min="Date.now()" class="form-control" id="date" aria-describedby="date">
                            <small class="form-text text-muted">Enter a title to identify your event</small>
                        </div>
                        <div class="form-group mb-3" >
                            <input @change="onChange($event)" class="form-control" type="file" id="formFile" accept="image/*">
                            <small for="formFile" class="form-text form-label">Import a picture for you event</small>
                        </div>
                        <div class="form-check form-switch mb-3">
                            <input v-model="form.is_private" class="form-control form-check-input" type="checkbox" id="private" >
                            <label class="form-text form-check-label" for="private">Private event</label>
                        </div>
                    </div>
                    <div class="col-md-6 ">
                         <div id="mapContainer" class="mb-3"></div>
                         <button type="submit" class="btn btn-primary">Submit</button>
                    </div>
                    <div><br>&nbsp;</div>

                </div>
            </form>
        </main>
        <MyFooter class="d-none d-md-block"></MyFooter>
    </div>
</template>

<script>
//import { getAPI } from '../../axios-api.js'
//import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import MyFooter from '../../components/Footer.vue'
import L from "leaflet";
import 'leaflet/dist/leaflet.css';
import { getAPI } from '../../axios-api';

export default {
    name: "EventsCreate",
    components: {
        NavBar,
        MyFooter
    },
    data() {
    return {
      map: null,
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
        title : null,
        description : null,
        date: null,
        is_private : null,
        lattitude : null,
        longitude : null,
        image : null
      }
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

    const self = this;
    this.map.on("click", (ev) => {
        self.form.lattitude = ev.latlng.lat.toFixed(4);
        self.form.longitude = ev.latlng.lng.toFixed(4);

        console.log(self.form.lattitude);
        console.log(self.form.longitude);
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

          getAPI.post('/events/create', formData,
          { headers: {
              Authorization: `Bearer ${this.$store.state.accessToken}`}
          })
          .then(response => {
            console.log(response)
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
        margin-top:3rem!important;
    }
    #mapContainer {
        width: 100%;
        height: 50vh;
        padding-bottom: 10em;
    }
    textarea {
        resize: none;
    }
    
</style>
