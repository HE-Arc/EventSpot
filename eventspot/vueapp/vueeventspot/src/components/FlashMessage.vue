   <template>
    <div v-if="this.typeData == 'success'" class="alert alert-success row">
        <div class="col-6"><strong>Success!</strong> {{this.message}}</div>
        <div v-on:click="close" class="col-6 "><button class="btn-close float-end" data-dismiss="alert" aria-label="close"></button></div>
    </div>
    <div v-else-if="this.typeData == 'danger'" class="alert alert-danger">
        {{this.message}}
    </div>
    <div v-else-if="this.typeData == 'warning'" class="alert alert-warning">
        {{this.message}}
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
         close(){
             this.typeData = null;
         },
     }
}
</script>