<template>
  <div class="col-md-4">
    <div class="container justify-content-center align-items-center">
      <div class="friends-card">
        <div class="mt-5 text-center">
          <h4 class="mb-0">{{ username }}</h4>
          <button v-if="pending == true" @click="accept(id)" class="btn btn-success btn-sm btn-custom">Accept</button>
          <button v-if="pending == true" @click="decline(id)" class="btn btn-danger btn-sm btn-custom">Decline</button>
          <button v-if="pending == false" @click="remove(id)" class="btn btn-danger btn-sm btn-custom">Remove</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAPI } from '../axios-api';
export default {
  props: ["username", "id", "pending"],
  components: {
  },
  methods: {
    remove(id){
      const self = this
      getAPI.delete('/friends/' + id + '/delete', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log(response)
            self.$router.go()
          })
          .catch(err => {
            console.log(err)
          })
    },
    decline(id){
      const self = this
      getAPI.delete('/friends/' + id + '/decline', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log(response)
            self.$router.go()
          })
          .catch(err => {
            console.log(err)
          })
    },
    accept(id){
      const self = this
      let formData = new FormData()
      formData.append('id',id)
      getAPI.post('/friends/accept', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log(response)
            self.$router.go()
          })
          .catch(err => {
            console.log(err)
            console.log(err.response.data);
            console.log(err.response.status);
            console.log(err.response.headers);
          })
    },  
  },
};
</script>
<style>
.friends-card {
  width: 380px;
  border: none;
  border-radius: 15px;
  padding: 8px;
  background-color: #fff;
  position: relative;
  height: 250px;
}
</style>