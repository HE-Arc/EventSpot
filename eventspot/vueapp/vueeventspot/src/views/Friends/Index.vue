<template>
    <div class="friends">
        <NavBar></NavBar>
        <main class="container">
            <h1>Friends</h1>
            <small v-if="errors != null" class="form-text text-danger ">{{errors}}</small>
            <FlashMessage :type="'success'" :message="'ceci est mon erreur'"></FlashMessage>

            <h2>Add a new friend</h2>
            <form v-on:submit.prevent="submitForm">
                <div class="mb-4 row">
                    <input v-model="form.username" required type="text" class="form-control" id="username" aria-describedby="username" placeholder="Enter username">
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            <div class="mb-4 row">
                <h2>My friends</h2>
                <CardFriends v-for="friend in this.friends" :key="friend.id" :username="friend.username" :id="friend.id" :pending="false"/>
            </div>
            <div class="mb-4 row">
                <h2>Friends request</h2>
                <CardFriends v-for="friend_request in this.friends_requests" :key="friend_request.sender.id" :username="friend_request.sender.username" :id="friend_request.sender.id" :pending="true"/>   
            </div>
        </main>
    </div>
</template>

<script>
import { getAPI } from '../../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../../components/NavBar.vue'
import CardFriends from '../../components/CardFriends.vue'
import FlashMessage from '../../components/FlashMessage.vue'

export default {
    name: "friendsIndex",
    components: {
        NavBar,
        CardFriends,
        FlashMessage
    },
    data() {
        return {
            friends : [],
            friends_requests : [],
            form: {
                username : ""
            },
            results: [],
            errors : ""
        }
    },
    computed: mapState(['APIData']),
    methods: {
        submitForm(){
            const self = this
            let formData = new FormData()
            formData.append('username', this.form.username)

            getAPI.post('/friends/create', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(response => {
                    console.log(response)
                    self.$router.go()
                })
                .catch(err => {
                    self.errors = err.response.data
                    console.log(err)
                })
        },
        async searchMembers() {
            await getAPI.get('/friends/search', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(response => {
                    console.log('Post API has recieved data')
                    this.$store.state.APIData = response.data
                   console.log(response.data)
                })
                .catch(err => {
                    self.errors = err.response.data
                    console.log(err)
                })
        }
    },
    created () {
        getAPI.get('/friends/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log('Post API has recieved data')
            this.$store.state.APIData = response.data
            this.friends_requests = this.APIData.friends_requests
            if(this.APIData.friends != undefined){
                this.friends = this.APIData.friends[0].friends
            }
          })
          .catch(err => {
            self.errors = err.response.data
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
