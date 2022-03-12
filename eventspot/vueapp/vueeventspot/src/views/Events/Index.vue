<template>
    <div class="events">
        <NavBar></NavBar>
        <main class="container">
            <h1 class="mt-3">Events list</h1>
            <table class="table table-hover">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="event in APIData" :key="event.id">
                        <td>{{event.title}}</td>
                        <td>
                            <a class="btn btn-primary"><i class="fa fa-eye"></i></a>
                            <a class="btn btn-success"><i class="fa fa-pencil"></i></a>
                            <a href="#" data-toggle="modal" data-target="#confirm-delete" class="btn btn-danger"><i class="fa fa-trash"></i></a>
                        </td>
                    </tr>
                </tbody>
            </table>
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
    name: "eventsIndex",
    components: {
        NavBar,
        MyFooter
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

            if (err.response.status === 401) {
                this.$router.push({ name: 'logout' })
            }
          })
    }
}
</script>

<style scoped>

</style>
