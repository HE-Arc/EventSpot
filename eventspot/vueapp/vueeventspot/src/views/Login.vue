<template>

  <div class="container-fluid mt-5">
    <div class="row col-lg-6 col-md-8 col-sm-12 col-xs-12 m-auto d-flex text-center" id="main-container">
      <div class="col-md-4 d-none d-md-flex flex-column justify-content-center text-center" id="logo">
        <span><img id="img-logo" alt="EventSpot Logo" src="../assets/mylogo.png"></span>
      </div>
      <div class="col-md-8 col-xs-12 col-sm-12" id="login">
        <div class="container-fluid ml-3">
          <div class="row">
            <h1 class="mt-3">Login</h1>
          </div>
          <div class="row">
            <form v-on:submit.prevent="login" class="form-group px-2">
              <div class="row">
                <input type="text" name="username" id="user" v-model="username" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Username">
              </div>
              <div class="row">
                <input type="password" name="password" id="pass" v-model="password" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Password">
              </div>
              <div class="row mt-3">
                <input type="submit" value="Submit" class="btn btn-primary">
              </div>
              <div v-if="incorrectAuth" class="mt-2">
                <small id="error">username or password invalid</small>
              </div>
            </form>
          </div>
          <div class="row mt-3">
            <p>Don't have an account? <router-link :to="{ name: 'register' }" exact>Register Here</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  export default {
    name: 'login-vue',
    data () {
      return {
        username: '',
        password: '',
        incorrectAuth: false
      }
    },
    methods: {
      login () { 
        this.$store.dispatch('userLogin', {
          username: this.username,
          password: this.password
        })
        .then(() => {
          this.$router.push({ name: 'events' })
        })
        .catch(err => {
          console.log(err)
          this.incorrectAuth = true
        })
        }
      }
  }
</script>

<style>
body { 
  background-color:#f4f4f4;
}

#main-container {
  border-radius: 20px;
  box-shadow: 0 5px 5px rgba(0,0,0,.4);
  padding: 0!important;
}

#logo {
  background-color: #CECECE;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
}

#img-logo {
  width: 100%;
}

#login {
  background-color: #fff;
  border-top:1px solid #ccc;
  border-right:1px solid #ccc;
  border-top-right-radius: 20px;
  border-bottom-right-radius: 20px;
}

.custom-input {
  width: 100% !important;
  border:0px solid transparent !important;
  border-bottom: 1px solid #aaa !important;
}

.custom-input:focus{
	border-bottom-color: #008080 !important;
	box-shadow: 0 0 5px rgba(0,80,80,.4) !important; 
	border-radius: 4px !important;
}

#error {
  color: #FF1C19;
}

@media screen and (max-width: 768px) {

	#login {
		border-top-left-radius:20px;
		border-bottom-left-radius:20px;
	}
}

</style>