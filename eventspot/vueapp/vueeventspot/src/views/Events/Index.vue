<template>
    <div class="events">
        <NavBar></NavBar>
        <main class="container">
            <h1 class="mb-3">Events list</h1>
            <p v-if="this.$route.params.state == 'success'">SUCCESS</p>
            <div class="mb-4">
                <h2>My events</h2>
                <router-link class="btn btn-primary" :to="{ name: 'events.create'}">Create an event</router-link>
                <div class="row">
                    <CardEvent v-for="event in APIData.results" :key="event.id" :event="event"/>
                </div><br>
            </div>
            <MyPagination class="mt-6" :links="'events'" />
            <span v-if="this.loaded">
                <IndexMap :events="APIData.results"></IndexMap>
            </span>
        </main>
        <MyFooter></MyFooter>
    </div>
    
</template>


<script>
import { getAPI } from '../../axios-api.js'
import { mapState } from 'vuex'
import MyFooter from '../../components/Footer.vue'
import NavBar from '../../components/NavBar.vue'


import CardEvent from '../../components/CardEvent.vue'
import IndexMap from '../../components/IndexMap.vue'

import MyPagination from '../../components/MyPagination.vue'


export default {
    name: "eventsIndex",
    components: {
        NavBar,
        MyFooter,
        CardEvent,
        MyPagination,
        IndexMap
    },
    data() {
    return { 
        loaded : false, 
        }
    },
    computed: mapState(['APIData']),
        created () {
        getAPI.get('/events/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log('Post API has recieved data');
            this.$store.state.APIData = response.data;
            console.log(this.$store.state.APIData);
            this.loaded=true;
          })
          .catch(err => {
            console.log(err)
          })
    }
}
</script>

<style scoped>

</style>
