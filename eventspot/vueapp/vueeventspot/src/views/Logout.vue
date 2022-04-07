<template>
  <div class="log">
  </div>
</template>

<script>
import { getAPI } from '../axios-api.js'
export default {
  name: 'logout-vue',
  
  /**
   * Send logout request and ban token
   */
  created () {
    this.$store.dispatch('userLogout')
    .then(() => {
      getAPI.post('/token/logout/', this.$store.state.refreshToken)
      .then(() => { 
        this.$router.push({ name: 'login' })
      })
      .catch()
    })
  }
}
</script>

<style>
</style>