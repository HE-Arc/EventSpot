<template>
    <div class="EventsShow">
        <NavBar></NavBar>
        <main class="container">
            <h1>{{APIData.title}}</h1><br>
            <div class="form-group mb-3">
                <a class="btn btn-success">Update</a>&nbsp;
                <a href="#" data-toggle="modal" data-target="#confirm-delete" class="btn btn-danger">Delete</a><br>
            </div>
            <small>Author : {{APIData.user.username}}</small><br>
            <strong>Date : {{this.$moment(APIData.date).format('YYYY-MM-DD HH:mm:ss')}}</strong>
            <img style="max-height: 33vh;" :src="'http://localhost:8000'+ APIData.image" class="mb-5 mp-5 img-responsive center-block d-block mx-auto"  alt="image event">
            <p class="text-justify">{{APIData.description}}</p>
        </main>
        <MyFooter></MyFooter>
    </div>
</template>

<script>
import { getAPI } from '../../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import MyFooter from '../../components/Footer.vue'
export default {
    name: "EventsShow",
    components: {
        NavBar,
        MyFooter
    },
    computed: mapState(['APIData']),
    created () {
        getAPI.get('/events/' +this.$route.params.id, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            this.$store.state.APIData = response.data;
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
