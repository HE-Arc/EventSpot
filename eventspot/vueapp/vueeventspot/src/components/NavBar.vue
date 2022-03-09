<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
      <a class="navbar-brand" href="/">EventSpot</a>
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link text-white" :to="{ name: 'eventsIndex' }" exact>Events</router-link>
        </li>
      </ul>

      <div v-if="false" class="navbar-collapse collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item"><a class="nav-link text-white">Username</a></li>
          <li class="nav-item"><a class="nav-link text-white">Logout</a></li>
        </ul>
      </div>

      <!-- ELSE -->
      <div v-else class="navbar-collapse collapse">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item"><a class="nav-link text-white">Login</a></li>
          <li class="nav-item"><a class="nav-link text-white">Sign up</a></li>
        </ul>
      </div>
    </nav>
  </header>
</template>


<script>
export default {
  name: "NavBar",
};
</script>
