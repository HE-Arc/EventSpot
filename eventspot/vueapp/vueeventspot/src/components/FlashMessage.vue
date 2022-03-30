   <template>
    <div v-if="this.type == 'success'" class="alert alert-success">
        {{this.message}}
    </div>
    <div v-else-if="this.type == 'danger'" class="alert alert-danger">
        {{this.message}}
    </div>
    <div v-else-if="this.type == 'warning'" class="alert alert-warning">
        {{this.message}}
    </div>
</template>

<script>
export default {
     props: ["type","message"],
}
</script>