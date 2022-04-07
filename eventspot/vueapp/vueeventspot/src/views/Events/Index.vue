<template>
    <div class="events">
        <NavBar></NavBar>
        <main class="container">
            <FlashMessage class="mt-5" v-if="this.$route.params.state == 'success'" :type="'success'" :message="'Operation done with success!'"></FlashMessage>
            <h1 class="mb-3">Events list</h1>
            <div class="mb-4">
                <h2>My events</h2>
                <router-link class="btn btn-primary" :to="{ name: 'events.create'}">Create an event</router-link>
                <div class="row">
                    <CardEvent v-for="event in APIData.results" :key="event.id" :event="event"/>
                </div><br>
            </div>
            <MyPagination class="mt-6" :links="'events'" />
            <span v-if="this.loaded">
                <IndexMap :events="publicEvents"></IndexMap>
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
import FlashMessage from '../../components/FlashMessage.vue'
import MyPagination from '../../components/MyPagination.vue'


export default {
    name: "eventsIndex",
    components: {
        NavBar,
        MyFooter,
        CardEvent,
        MyPagination,
        IndexMap,
        FlashMessage
    },
    data() {
      return { 
          loaded : false, 
          publicEvents : null
          }
    },
    computed: mapState(['APIData']),
        created () {
        //find my events
        getAPI.get('/events/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            this.$store.state.APIData = response.data;
          })
          .catch(() => {
          })
        //find public events
        getAPI.get('/events/public', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            this.publicEvents = response.data;
            this.loaded=true;
          })
          .catch(() => {
          })
    }
}
</script>

<style scoped>

</style>
