<template>
  <div class="log">
  </div>
</template>

<script>
import { getAPI } from '../axios-api.js'
export default {
  name: 'logout-vue',
  created () {
    this.$store.dispatch('userLogout')
    .then(() => {
      getAPI.post('/token-logout/', this.$store.state.refreshToken)
      .then(() => { 
        this.$router.push({ name: 'login' })
      })
    })
  }
}
</script>

<style>
</style>