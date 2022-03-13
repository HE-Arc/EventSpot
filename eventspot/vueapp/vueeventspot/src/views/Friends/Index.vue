<template>
    <div class="friends">
        <NavBar></NavBar>
        <main class="container">
            <h1>Friends</h1>
            <h2>Add a new friend</h2>
            <div class="mb-4 row">
                <h2>My friends</h2>
                <CardFriends v-for="friend in APIData[0].friends" :key="friend.id" :username="friend.username" :id="friend.id"/>
            </div>
        </main>
        <MyFooter></MyFooter>
    </div>
</template>

<script>
import { getAPI } from '../../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import MyFooter from '../../components/Footer.vue'
import CardFriends from '../../components/CardFriends.vue'
export default {
    name: "friendsIndex",
    components: {
        NavBar,
        MyFooter,
        CardFriends
    },
    computed: mapState(['APIData']),
    created () {
        getAPI.get('/friends/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
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
    h1{
        margin-top:3rem!important;
    }
    h2{
        margin-top:3rem!important;
    }
</style>
