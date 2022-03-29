<template>
    <div class="col-md-4">
        <router-link class="card myCard" :to="{ name: 'events.show', params: {id: event.id } }">
            <div class="card-body">
                <img v-if="event.image" class="myImg  img-responsive" :src="`http://localhost:8000${event.image}`" >
                <img v-else class="myImg  img-responsive" src="@/assets/default.jpg" alt="default" >
                <h3 class="card-title">{{ event.title }}</h3>
            </div>
        </router-link>
    </div>
</template>

<script>
export default {
    props:['event']
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