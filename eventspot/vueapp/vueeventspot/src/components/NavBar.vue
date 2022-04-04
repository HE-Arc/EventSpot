<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-light" id="navbar">
      <router-link class="ms-3 me-2 d-none d-md-inline-block" :to="{ name: 'events' }" exact>
        <img id="img-logo" alt="EventSpot Logo" width="50" height="50" src="../assets/mylogo.png">
      </router-link>
      <a class="navbar-brand ms-2" href="/">EventSpot</a>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggle">
        <span class="navbar-toggler-icon text-primary"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarToggle">
        <ul class="navbar-nav ms-2">
          <li v-show="username" class="nav-item">
            <router-link class="nav-link text-dark" active-class="active" :to="{ name: 'events' }" exact>Events</router-link>
          </li>
          <li v-show="username" class="nav-item">
            <router-link class="nav-link text-dark" active-class="active" :to="{ name: 'friends' }" exact>Friends</router-link>
          </li>
        </ul>
        <ul v-if="username" class="navbar-nav ms-2 ms-md-auto me-3">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle text-dark" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" data-bs-toggle="dropdown" aria-expanded="true">
            {{username}}
            </a>
            <div class="dropdown-menu" id="dropdown" aria-labelledby="navbarDropdownMenuLink">
              <router-link class="dropdown-item dropdown-link border-bottom" active-class="active" :to="{ name: 'profilePage' }" exact>My profile</router-link>
              <router-link class="dropdown-item dropdown-link" :to="{ name: 'logout' }" exact>Logout</router-link>
            </div>
          </li>
          <li class="nav-item ms-1 d-none d-md-inline-block">
            <router-link :to="{ name: 'profilePage' }" exact>
              <div id="img-profil-container">
                <img v-if="profile_image" id="img-profil" width="40" height="40" alt="Profile image" :src="profile_image">
                <img v-else id="img-profil" width="40" height="40" alt="Profile image" src="../assets/default_profile.png">
              </div>
            </router-link>
          </li>
        </ul>
        <ul v-else class="navbar-nav ms-auto me-3">
          <li class="nav-item">
            <router-link class="nav-link text-dark" :to="{ name: 'login' }">Login</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>


<script>
import { getAPI,baseURL } from '../axios-api.js'
export default {
  name: "NavBar",
  data () {
    return {
      username: '',
      profile_image: ''
    }
  },
  created () {
    if(this.$store.state.accessToken != null)
    {
      getAPI.get('/profile/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
      .then(response => {
      this.username = response.data.username;
      this.profile_image = baseURL + response.data.profile_image;
      console.log(response);
      })
    }
  }
};
</script>

<style scoped>
#navbar {
  background-color: white;
}

#dropdown {
  min-width: 7em!important;
}

.dropdown-link:hover {
  background-color: #CECECE!important;
}

#img-logo {
  width: 100%;
}

#img-profil {
  width: 100%;
  border-radius: 50%;
}

#img-profil-container {
  width: 40px;
  height: 40px;
}

.active {
  color: black!important;
  font-weight: bold!important;

}
</style>
