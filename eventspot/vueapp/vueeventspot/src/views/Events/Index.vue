<template>
    <div class="events">
        <NavBar></NavBar>
        <div v-for="events in APIData" :key="events.id">
            <h1>{{events.title}}</h1>
            <p>{{events.description}}</p>
        </div>
    </div>
</template>

<script>
import { getAPI } from '../../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
export default {
    name: "eventsIndex",
    components: {
        NavBar
    },
    computed: mapState(['APIData']),
    created () {
        getAPI.get('/events/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log('Post API has recieved data')
            this.$store.state.APIData = response.data
          })
          .catch(err => {
            console.log(err)
          })
    }
}
</script>

<style scoped>

</style>
