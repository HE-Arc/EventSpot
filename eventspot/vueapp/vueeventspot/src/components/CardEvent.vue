<template>
    <div class="col-md-4">
        <router-link class="card myCard" :to="{ name: 'events.show', params: {id: event.id } }">
            <div class="card-body">
                <img v-if="event.image" class="myImg  img-responsive" :src="myImg" >
                <img v-else class="myImg  img-responsive" src="@/assets/default.jpg" alt="default" >
                <h3 class="card-title">{{ event.title }}</h3>
            </div>
        </router-link>
    </div>
</template>

<script>
import { baseURL } from '../axios-api';

export default {
    props:['event'],
    data(){
        return {
        myImg : baseURL + this.event.image
        }
    },
}

</script>

<style scoped>
.card{
    margin-top: 1rem;
    text-decoration: none;
    color: black;
}
.myCard
{
    text-align: center;
}
.card-title
{
    margin-top: 1rem;
}
.myImg
{
    height: 10em;
    width: 100%;
    object-fit: cover;
}
</style>