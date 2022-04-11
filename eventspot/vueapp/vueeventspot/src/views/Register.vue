<template>

  <div class="container-fluid mt-5">
    <div class="row col-lg-6 col-md-8 col-sm-12 col-xs-12 m-auto d-flex text-center" id="main-container">
      <div class="col-md-4 d-none d-md-flex flex-column justify-content-center text-center" id="logo">
        <span><img id="img-logo" alt="EventSpot Logo" src="../assets/mylogo.png"></span>
      </div>
      <div class="col-md-8 col-xs-12 col-sm-12" id="login">
        <div class="container-fluid ml-3">
          <div class="row">
            <h1 class="mt-3">Register</h1>
          </div>
          <div class="row">
            <form v-on:submit.prevent="register" class="form-group px-2">
              <div class="row">
                <input type="text" name="username" id="user" v-model="username" required class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Username">
              </div>
              <div class="row">
                <input type="email" name="emailusername" id="email" v-model="email" required class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Email">
              </div>
              <div class="row">
                <input type="password" name="password" id="pass" v-model="password" required class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Password">
              </div>
              <div class="row">
                <input type="password" name="confirm" id="confirm" v-model="confirm" required class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Password confirmation">
              </div>
              <div class="row mt-3">
                <input type="submit" value="Submit" class="btn btn-primary">
              </div>
              <div v-if="incorrectAuth" class="mt-2">
                <small id="error">{{incorrectAuth}}</small>
              </div>
            </form>
          </div>
          <div class="row mt-3">
            <p>Back to <router-link :to="{ name: 'login' }" exact>Login</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  import { getAPI } from '../axios-api.js'
  export default {
    name: 'register-vue',
    data () {
      return {
        username: '',
        email: '',
        password: '',
        confirm: '',
        incorrectAuth: false
      }
    },
    methods: {
          /**
           * Send register request
           */
          register () { 

            this.incorrectAuth = false;

            if(this.password != this.confirm) {
              this.incorrectAuth = "password confirmation does not match";
              return;
            }
        
            const user = {
              username: this.username,
              email: this.email,
              password: this.password,
              confirm: this.confirm
            };

            getAPI.post('/profiles/', user)
            .then(

              setTimeout(() => {
                 
                if(this.incorrectAuth == false) {
                    this.$store.dispatch('userLogin', {
                    username: this.username,
                    password: this.password
                  })
                  .then(() => {
                    this.$router.push({ name: 'events' })
                  })
                }

              }, 1000)

            )
            .catch(err => {
              if(err.response.data['email']) {
                this.incorrectAuth = err.response.data['email'][0];
              }
              else if(err.response.data['username']) {
                this.incorrectAuth = err.response.data['username'][0];
              }
              else if(err.response.data['password']) {
                this.incorrectAuth = err.response.data['password'][0];
              }

              return 0;
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
  background-color: #ffffff!important;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  border-top:1px solid #ccc;
  border-right:1px solid rgb(235, 235, 235);
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
  min-width: 300px;
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