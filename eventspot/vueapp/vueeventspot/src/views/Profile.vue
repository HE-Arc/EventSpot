<template>
    <div class="events">
        <NavBar :key="componentKey"></NavBar>
        <main class="container-fluid mt-5">
            <div class="row col-xl-4 col-lg-5 col-md-7 col-sm-12 col-xs-12 m-auto d-flex text-center" id="main-container">
              <div class="col-12" id="login">
                <div class="container-fluid">
                  <div id="img-container" class="row col-lg-6 col-12 mx-auto justify-content-center text-center mt-3">
                    <!-- https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Fusers%2Fsimple-user-icon&psig=AOvVaw398t0oShOe6hE4rClKoMvz&ust=1647189309778000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCMCA5cSAwfYCFQAAAAAdAAAAABAM -->
                    <span v-if="profile_image"><img id="img-logo" width="120" height="120" alt="Profile image" :src="profile_image"></span>
                    <span v-else><img id="img-logo" width="120" height="120" alt="Profile image" src="../assets/default_profile.png"></span>
                  </div>
                  <div class="row col-12 mx-auto justify-content-center text-center">
                    <form v-on:submit.prevent="updateUser" class="px-2 mx-auto justify-content-center text-center">
                      <div class="form-group row mt-3">
                        <input @change="onChange($event)" class="form-control" type="file" id="formFile" accept="image/*">
                        <small for="formFile" class="form-text form-label">Import a picture for you profile image</small>
                      </div>
                      <div class="form-group row mt-3">
                        <input type="text" name="username" id="user" v-model="formUser.username" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-1 shadow-none mx-auto my-2 custom-input" placeholder="Username">
                      </div>
                      <div class="form-group row">
                        <input type="email" name="emailusername" id="email" v-model="formUser.email" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-1 shadow-none mx-auto my-2 custom-input" placeholder="Email">
                      </div>
                      <div class="form-group row mt-3">
                        <input type="submit" value="Update" class="btn btn-primary">
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
                  <div class="row col-12 mx-auto justify-content-center text-center">
                    <form v-on:submit.prevent="changePassword" class="px-2 mx-auto justify-content-center text-center">
                      <div class="form-group row">
                        <input type="password" name="password" id="pass" v-model="formPassword.password" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="New password">
                      </div>
                      <div class="form-group row">
                        <input type="password" name="confirm" id="confirm" v-model="formPassword.confirm" class="form-control rounded-0 pt-2 pb-1 pr-1 pl-4 shadow-none mx-auto my-2 custom-input" placeholder="Confirmation">
                      </div>
                      <div class="form-group row my-3">
                        <input type="submit" value="Change password" class="btn btn-primary">
                      </div>
                      <div v-if="incorrectPassword" class="my-3">
                        <small class="text-danger">{{incorrectPassword}}</small>
                      </div>
                      <div v-if="successPassword" class="my-3">
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
import { getAPI,baseURL } from '../axios-api.js'
import { mapState } from 'vuex'
import NavBar from '../components/NavBar.vue'
import MyFooter from '../components/Footer.vue'
export default {
    name: "profilePage",
    data () {
      return {
        formUser: {
          username: '',
          email: '',
          profile_image: '',
        },

        formPassword: {
          password: '',
          confirm: '',
        },

        id: '',
        profile_image: '',
        incorrectUser: false,
        successUser: false,
        incorrectPassword: false,
        successPassword: false,
      }
    },
    components: {
        NavBar,
        MyFooter
    },
    computed: mapState(['APIData']),
    created () {        
        getAPI.get('/profiles/myprofile/', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log('Post API has recieved data');
            this.$store.state.APIData = response.data;

            this.formUser.username = this.$store.state.APIData.username;
            this.formUser.email = this.$store.state.APIData.email;
            this.id = this.$store.state.APIData.id;

            if(this.$store.state.APIData.profile_image)
              this.profile_image = baseURL + this.$store.state.APIData.profile_image;
          })
          .catch(err => {
            if (err.response.status === 401) {
                this.$router.push({ name: 'logout' })
            }
          })
    },

    methods: {
      onChange(event) {
          this.formUser.profile_image = event.target.files[0];
      },

      updateUser(){
        if(!this.formUser.username) {
          this.incorrectUser = "username is empty";
          return 0;
        }

        if(!this.formUser.email) {
          this.incorrectUser = "email is empty";
          return 0;
        }

        let formData = new FormData();

        Object.entries(this.formUser).forEach(([key, value]) => {
          formData.append(key, value);
        });

        getAPI.patch('/profiles/' + this.id + '/', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
        .then(response => {
          this.successUser = "Profile updated sucessfully"

          this.$store.state.APIData.username = response.data.username;
          this.$store.state.APIData.email = response.data.email;
          this.$store.state.APIData.profile_image = response.data.profile_image;
          
          this.formUser.username = this.$store.state.APIData.username;
          this.formUser.email = this.$store.state.APIData.email;
          this.profile_image = this.$store.state.APIData.profile_image

          this.$store.state.username =  response.data.username;

          // force navbar to re-render
          this.componentKey += 1;
        })
        .catch(err => {
          this.successUser = false;

          if(err.response.data['email']) {
            this.incorrectUser = err.response.data['email']['email'];
            return -1;
          }

          if(err.response.data['username']) {
            this.incorrectUser = err.response.data['username']['username'];
            return -1;
          }

          if(err.response.data['authorize']) {
            this.incorrectUser = err.response.data['authorize'][0];
            return -1;
          }

        })
      },

      changePassword() {

        if(!this.formPassword.password) {
          this.incorrectPassword = "password is empty";
          return 0;
        }

        if(!this.formPassword.confirm) {
          this.incorrectPassword = "password confirmation is empty";
          return 0;
        }

        if(this.formPassword.password != this.formPassword.confirm) {
          this.incorrectPassword = "password confirmation does not match";
          return 0;
        }

        let formData = new FormData();

        Object.entries(this.formPassword).forEach(([key, value]) => {
          formData.append(key, value);
        });

        getAPI.patch('/profiles/' + this.id + '/', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
        .then(
          this.successPassword = "password updated successfully"
        )
        .catch(err => {
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
  border-radius: 50%;
}

#img-container {
  width: 150px;
  height: 120px;
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
