<template>
    <div class="events">
        <NavBar></NavBar>
        <main class="container-fluid mt-5">
            <div class="row col-lg-4 col-md-7 col-sm-12 col-xs-12 m-auto d-flex text-center" id="main-container">
              <div class="col-12" id="login">
                <div class="container-fluid">
                  <div class="row col-lg-6 col-12 mx-auto justify-content-center text-center mt-3">
                    <!-- https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Fusers%2Fsimple-user-icon&psig=AOvVaw398t0oShOe6hE4rClKoMvz&ust=1647189309778000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCMCA5cSAwfYCFQAAAAAdAAAAABAM -->
                    <span v-if="profile_image"><img id="img-logo" width="120" height="120" alt="Profile image" :src="profile_image"></span>
                    <span v-else><img id="img-logo" width="120" height="120" alt="Profile image" src="../assets/default_profile.png"></span>
                  </div>
                  <div class="row col-lg-6 col-12 mx-auto justify-content-center text-center">
                    <form v-on:submit.prevent="updateUser" class="form-group px-2 mx-auto justify-content-center text-center">
                      <div class="row">
                        <input type="file" name="profileImage" accept="image/*" />
                      </div>
                      <div class="row mt-3">
                        <input type="text" name="username" id="user" v-model="username" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-1 shadow-none mx-auto my-2 custom-input" placeholder="Username">
                      </div>
                      <div class="row">
                        <input type="email" name="emailusername" id="email" v-model="email" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-1 shadow-none mx-auto my-2 custom-input" placeholder="Email">
                      </div>
                      <div class="row mt-3">
                        <input type="submit" value="Update" class="btn btn-primary rounded-pill">
                      </div>
                      <div v-if="incorrectUser" class="mt-2">
                        <small class="text-danger">{{incorrectUser}}</small>
                      </div>
                      <div v-if="successUser" class="mt-2">
                        <small class="text-success">{{successUser}}</small>
                      </div>
                    </form>
                  </div>
                  <div class="row mt-4">
                    <h3 class="mt-3">Change password</h3>
                  </div>
                  <div class="row col-lg-6 col-12 mx-auto justify-content-center text-center">
                    <form v-on:submit.prevent="changePassword" class="form-group px-2 mx-auto justify-content-center text-center">
                      <div class="row">
                        <input type="password" name="password" id="pass" v-model="password" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="New password">
                      </div>
                      <div class="row">
                        <input type="password" name="confirm" id="confirm" v-model="confirm" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Confirmation">
                      </div>
                      <div class="row mt-3">
                        <input type="submit" value="Change password" class="btn btn-primary rounded-pill">
                      </div>
                      <div v-if="incorrectPassword" class="mt-2">
                        <small class="text-danger">{{incorrectPassword}}</small>
                      </div>
                      <div v-if="successPassword" class="mt-2">
                        <small class="text-success">{{successPassword}}</small>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
        </main>
        <MyFooter></MyFooter>
    </div>
</template>

<script>
import { getAPI } from '../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../components/NavBar.vue'
import MyFooter from '../components/Footer.vue'
export default {
    name: "profilePage",
    data () {
      return {
        username: '',
        email: '',
        password: '',
        confirm: '',
        id: '',
        profile_image: '',
        incorrectUser: false,
        successUser: false,
        incorrectPassword: false,
        successPassword: false
      }
    },
    components: {
        NavBar,
        MyFooter
    },
    computed: mapState(['APIData']),
    created () {
        getAPI.get('/profile/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log('Post API has recieved data')
            this.$store.state.APIData = response.data

            this.username = this.$store.state.APIData.username
            this.email = this.$store.state.APIData.email
            this.id = this.$store.state.APIData.id
            this.profile_image = this.$store.state.APIData.profile_image
          })
          .catch(err => {
            console.log(err)

            if (err.response.status === 401) {
                this.$router.push({ name: 'logout' })
            }
          })
    },

    methods: {
      updateUser(){
        if(!this.username) {
          this.incorrectUser = "username is empty";
          return 0;
        }

        if(!this.email) {
          this.incorrectUser = "email is empty";
          return 0;
        }
      },

      changePassword() {

        if(!this.password) {
          this.incorrectPassword = "password is empty";
          return 0;
        }

        if(!this.confirm) {
          this.incorrectPassword = "password confirmation is empty";
          return 0;
        }

        if(this.password != this.confirm) {
          this.incorrectPassword = "password confirmation does not match";
          return 0;
        }

        const credentials = {
          password: this.password,
          confirm: this.confirm
        };

        getAPI.put('/profiles/password/' + this.id + '/', credentials, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
        .then(
          this.successPassword = "password updated successfully"
        )
        .catch(err => {
          console.log(err);
          this.successPassword = false;

          if(err.response.data['password']) {
            this.incorrectAuth = err.response.data['password'][0];
            return -1;
          }

          if(err.response.data['authorize']) {
            this.incorrectAuth = err.response.data['authorize'][0];
            return -1;
          }
        })

      }
    }
}
</script>

<style scoped>
body { 
  background-color:#f4f4f4;
}

#main-container {
  border-radius: 20px;
  box-shadow: 0 5px 5px rgba(0,0,0,.4);
  padding: 0!important;
}

#login {
  background-color: #fff;
  border-top:1px solid #ccc;
  border-right:1px solid #ccc;
  border-radius: 20px;
}

#img-logo {
  width: 100%;
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

@media screen and (max-width: 768px) {

	#login {
		border-top-left-radius:20px;
		border-bottom-left-radius:20px;
	}
}
</style>
