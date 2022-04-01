<template>
  <div class="col-lg-4">
    <div class="text-center card-box">
      <div class="member-card pt-2 pb-2">
        <div class="thumb-lg member-thumb mx-auto">
          <img v-if="profileImage!=null" :src="`http://localhost:8000${profileImage}`" class="rounded-circle img-thumbnail" alt="profile-image">
          <img v-else src="@/assets/default_profile.png" class="rounded-circle img-thumbnail" alt="profile-image">
        </div>
        <div>
          <h4>{{ username }}</h4>
        </div>
        <button v-if="pending == true" @click="accept(id)" class="btn btn-success btn-rounded">Accept</button>
        <button v-if="pending == true" @click="decline(id)" class="btn btn-danger btn-rounded">Decline</button>
        <button v-if="pending == false" @click="remove(id)" class="btn btn-danger btn-rounded">Remove</button>
      </div>
    </div>
  </div>
</template>

<script>
import { getAPI } from '../axios-api';
import VueSimpleAlert from "vue3-simple-alert"
export default {
  props: ["username", "id", "pending", "profileImage"],
  components: {
  },
  methods: {
    remove(id){
      VueSimpleAlert.confirm("Are you sure you want to remove this friend ?").then(() => {
        getAPI.delete('/friends/' + id + '/delete', {headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
            .then(response => {
              console.log(response)
              this.$emit("messageUpdate", 'Successfully removed that friend.')
              this.$emit("typeUpdate", "success")
              this.$emit("dataUpdate", null)
            })
            .catch(err => {
              console.log(err)
              this.$emit("messageUpdate", 'User not found.')
              this.$emit("typeUpdate", "danger")
              this.$emit("dataUpdate", null)
            })
      }).catch(()=>{})
    },
    decline(id){
      VueSimpleAlert.confirm("Are you sure you want to decline the friend request ?").then(() => {
        getAPI.delete('/friends/' + id + '/decline', { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
            .then(response => {
              console.log(response)
              this.$emit("messageUpdate", 'Friend request declined.')
              this.$emit("typeUpdate", "success")
              this.$emit("dataUpdate", null)
            })
            .catch(err => {
              console.log(err)
              this.$emit("messageUpdate", 'User not found.')
              this.$emit("typeUpdate", "danger")
              this.$emit("dataUpdate", null)
            })
      }).catch(()=>{})
    },
    accept(id){
      let formData = new FormData()
      formData.append('id',id)
      getAPI.post('/friends/accept', formData, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            console.log(response)
            this.$emit("messageUpdate", response.data['message'])
            this.$emit("typeUpdate", "success")
            this.$emit("dataUpdate", null)
          })
          .catch(err => {
            console.log(err)
            this.$emit("messageUpdate", err.response.data['message'])
            this.$emit("typeUpdate", "danger")
            this.$emit("dataUpdate", null)
          })
    },  
  },
};
</script>
<style scoped>
.card-box {
    padding: 20px;
    border-radius: 3px;
    margin-bottom: 30px;
    background-color: #fff;
}
.thumb-lg {
    height: 88px;
    width: 88px;
}
.img-thumbnail {
    padding: .25rem;
    background-color: #fff;
    border: 1px solid #dee2e6;
    border-radius: .25rem;
    max-width: 100%;
    height: auto;
}
.btn-rounded {
    border-radius: 2em;
    margin: 1em;
}
.text-muted {
    color: #98a6ad!important;
}
</style>