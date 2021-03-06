<template>
    <div class="friends">
        <NavBar></NavBar>
        <main class="container">
            <h1>Friends</h1>
            <FlashMessage v-if="this.type != null" :type="this.type" :message="this.message"></FlashMessage>
            <h2>Add a new friend</h2>
            <form v-on:submit.prevent="submitForm">
                <div class="card-box">
                    <div class="col-12 col-md-6 input-group-pers">
                        <div class="input-group">
                            <input v-model="form.username" required type="text" class="w-75 form-control" id="username" aria-describedby="username" placeholder="Enter username">
                            <button class="w-25 btn btn-success" type="submit">Send</button>
                        </div>
                    </div>
                    <div class="w-50 input-group-pers">
                        <ul class="w-75 list-group" v-if="results.length > 0 && form.username">
                            <a v-for="result in results" :key="result.id" class="text-decoration-none" href="#" @click="addValueToInput(result.username)">
                                <li class="list-group-item list-group-item-action">
                                    {{result.username}}
                                </li>
                            </a>
                        </ul>
                        <span class="w-25"></span>
                    </div>
                </div>
            </form>

            <div class="row">
                <h2>My friends</h2>
                <CardFriends v-for="friend in this.friends" 
                    :key="friend.id" 
                    :username="friend.username" 
                    :id="friend.id"
                    :profileImage="friend.profile.profile_image"
                    :pending="false" 
                    @messageUpdate="message = $event" 
                    @typeUpdate="type = $event" 
                    @dataUpdate="getData"
                />
            </div>

            <div class="mb-4 row">
                <h2>Friends request</h2>
                <CardFriends v-for="friend_request in this.friends_requests" 
                    :key="friend_request.sender.id" 
                    :username="friend_request.sender.username" 
                    :id="friend_request.sender.id"
                    :profileImage="friend_request.sender.profile.profile_image"
                    :pending="true" 
                    @messageUpdate="message = $event"
                    @typeUpdate="type = $event"
                    @dataUpdate="getData"
                />   
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
import FlashMessage from '../../components/FlashMessage.vue'

export default {
    name: "friendsIndex",
    components: {
        NavBar,
        CardFriends,
        FlashMessage,
        MyFooter
    },
    data() {
        return {
            friends : [],
            friends_requests : [],
            form: {
                username : null
            },
            results: [],
            message : null,
            type: null
        }
    },
    watch:{
        // watch if field username change to retrieve username
        'form.username': function (){
            this.searchMembers();
        },
    },
    computed: mapState(['APIData']),
    methods: {
        /**
         * Send friend request
         */
        submitForm(){
            let formData = new FormData()
            formData.append('username', this.form.username)

            getAPI.post('/friends/', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(response => {
                    if(response.status == 201)
                    {
                        this.message = response.data['message']
                        this.type = "success"
                        this.form.username = ""
                    }
                })
                .catch(err => {
                    //if error show flashmesage
                    switch(err.response.status){
                        case 409: this.type = 'warning'; break;
                        case 400: this.type = 'danger'; break;
                    }
                    this.message = err.response.data['message']
                })
        },
        /**
         * Search first 5 user which start with form.username
         */
        searchMembers() {
            if(this.form.username == '')
                return;
                
            getAPI.get('/friends/search', { params: {username:this.form.username},headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(response => {
                    this.results = response.data
                })
                .catch(() => {
                })
        },
        /**
         * When user click on a proposal username
         */
        addValueToInput(username) {
            this.form.username = username;
        },
        /**
         * Retrieve friends and friends request
         */
        getData(){
            getAPI.get('/friends/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
                .then(response => {
                    this.$store.state.APIData = response.data
                    this.friends_requests = this.APIData.friends_requests
                    if(this.APIData.friends != undefined){
                        this.friends = this.APIData.friends[0].friends
                    }
                })
                .catch(() => {
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
