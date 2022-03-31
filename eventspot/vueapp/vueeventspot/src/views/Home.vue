<template>
    <div class="Home">
        <NavBar></NavBar>
        <main class="container">
            <div class="row justify-content-center px-4">
                    <h1 class="display-1 text-center">Share your events.</h1>
                    <h2 class="text-center">EventSpot is a website for share your events. You can create an event, associate pictures, location, date and write about it  ! Finally, you can share your creations with your friends.</h2>
            </div>
        </main>
        <MyFooter></MyFooter>
    </div>
</template>


<script>
import NavBar from '../components/NavBar.vue'
import MyFooter from '../components/Footer.vue'

export default {
  name: 'home-vue',
  components: {
        NavBar,
        MyFooter
    },
}
</script>

<style scoped>
.container
{
    margin-top: 12em;
}
</style>