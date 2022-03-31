<template>
    <div class="friends">
        <NavBar></NavBar>
        <main class="container">
            <h1>Friends</h1>
            <FlashMessage v-if="this.type != null" :type="this.type" :message="this.message"></FlashMessage>
            <h2>Add a new friend</h2>
            <form v-on:submit.prevent="submitForm">
                <div class="card-box">
                    <div class="w-50 input-group-pers">
                        <div class="input-group">
                            <input v-model="form.username" required type="text" class="form-control" id="username" aria-describedby="username" placeholder="Enter username">
                            <button class="btn btn-success" type="submit">Send</button>
                        </div>
                    </div>
                </div>
            </form>
            
            <div class="row">
                <h2>My friends</h2>
                <CardFriends v-for="friend in this.friends" :key="friend.id" :username="friend.username" :id="friend.id" :pending="false" @messageUpdate="message = $event" @typeUpdate="type = $event" @dataUpdate="getData"/>
            </div>

            <div class="mb-4 row">
                <h2>Friends request</h2>
                <CardFriends v-for="friend_request in this.friends_requests" :key="friend_request.sender.id" :username="friend_request.sender.username" :id="friend_request.sender.id" :pending="true" @messageUpdate="message = $event" @typeUpdate="type = $event" @dataUpdate="getData"/>   
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
            message : null,
            type: null
        }
    },
    computed: mapState(['APIData']),
    methods: {
        submitForm(){
            let formData = new FormData()
            formData.append('username', this.form.username)

            getAPI.post('/friends/create', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(response => {
                    console.log(response)
                    if(response.status == 201)
                    {
                        this.message = response.data['message']
                        this.type = "success"
                    }
                })
                .catch(err => {
                    switch(err.response.status){
                        case 409: this.type = 'warning'; break;
                        case 400: this.type = 'danger'; break;
                    }
                    this.message = err.response.data['message']
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
        },
        getData(){
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
    },
    created () {
        this.getData()
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
.input-group-pers{
    margin:auto;
}
.card-box {
    padding: 20px;
    border-radius: 3px;
    margin-bottom: 30px;
    background-color: #fff;
}
</style>
