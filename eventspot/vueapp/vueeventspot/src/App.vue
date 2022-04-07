<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {
    
  },
}
</script>

<style>
  html {
    position: relative;
    min-height: 100%;
  }

  body {
    margin: 0 0 100px !important;
    padding: 0;
    background-color: #f8f8f8!important;
  }
</style>
