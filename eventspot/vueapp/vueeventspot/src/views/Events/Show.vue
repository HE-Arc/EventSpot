<template>
    <div class="EventsShow">
        <NavBar></NavBar>
        <main class="container">
            <FlashMessage class="mt-5" v-if="this.$route.params.state == 'success'" :type="'success'" :message="'Operation done with success!'"></FlashMessage>
            <h1>{{APIData.title}}</h1><br>
            <div v-if="APIData.user.username == this.$store.state.username" class="form-group mb-3">
                <router-link  v-if="APIData.user != undefined" class="btn btn-success" :to="{ name: 'events.update', params: {id: APIData.id } }">Update</router-link>&nbsp;
                <a href="#" data-toggle="modal" data-target="#confirm-delete" @click="destroy()" class="btn btn-danger">Delete</a><br>
            </div>
            <small v-if="APIData.user != undefined">Author : {{APIData.user.username}}</small><br>
            <strong>Date : {{this.$moment(APIData.date).format('YYYY-MM-DD HH:mm')}}</strong>
            <img style="max-height: 33vh;" :src="this.img" class="mb-5 mp-5 img-responsive center-block d-block mx-auto"  alt="image event">
            <p class="text-justify">{{APIData.description}}</p>
        </main>

        <MyFooter></MyFooter>
    </div>
</template>

<script>
import { getAPI,baseURL } from '../../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import MyFooter from '../../components/Footer.vue'
import FlashMessage from '../../components/FlashMessage.vue'

import VueSimpleAlert from "vue3-simple-alert"

export default {
    name: "EventsShow",
    components: {
        NavBar,
        MyFooter,
        FlashMessage
    },
     data() {
        return {
            img: require("@/assets/default.jpg"),
        }
    },
    computed: mapState(['APIData']),
    methods: {
        destroy() 
        {
            VueSimpleAlert.confirm("Are you sure?").then(() => {
                getAPI.delete('/events/' +this.$route.params.id, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(() => {
                    this.$router.push({ name: 'events', params: { state:"success"} })
                })
                .catch(err => {
                    console.log(err);
                })   
            }).catch(()=>{});
        }
    },
    created () {
        getAPI.get('/events/' +this.$route.params.id, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            this.$store.state.APIData = response.data;

            if(response.data.image != undefined)
            {
                this.img = baseURL + response.data.image;
            }

          })
          .catch(err => {
            console.log(err);
          })
    }
}
</script>

<style scoped>
    h1{
        margin-top:3rem!important;
    }
</style>
