   <template>
    <div v-if="this.typeData == 'success'" class="alert alert-success row">
        <div class="col-6"><strong>Success!</strong> {{this.message}}</div>
        <div v-on:click="close" class="col-6 "><button class="btn-close float-end"></button></div>
    </div>
    <div v-else-if="this.typeData == 'danger'" class="alert alert-danger row">
        <div class="col-6"><strong>Error!</strong> {{this.message}}</div>
        <div v-on:click="close" class="col-6 "><button class="btn-close float-end"></button></div>
    </div>
    <div v-else-if="this.typeData == 'warning'" class="alert alert-warning row">
        <div class="col-6"><strong>Warning!</strong> {{this.message}}</div>
        <div v-on:click="close" class="col-6 "><button class="btn-close float-end"></button></div>
    </div>
</template>

<script>
export default {
     props: ["type","message"],
     data()
     {
         return {
             typeData : this.type
         }
     },
     methods:
     {
         /**
          * Close flash message
          */
         close(){
             this.typeData = null;
         },
     },
      watch: { 
      	type: function(newVal, oldVal) { // watch if the flashmessage must change (new data)
          this.typeData = this.type;
        }
      }
}
</script>