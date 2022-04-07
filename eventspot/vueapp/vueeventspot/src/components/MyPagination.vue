<template>
    <paginate
    v-model="APIData.current"
    :page-count="Math.ceil(APIData.total/APIData.count)"
    :page-range="APIData.count"
    :click-handler="clickCallback"
    :first-last-button="true"
    :prev-text="'Prev'"
    :next-text="'Next'"
    :container-class="'pagination'"
    :page-class="'page-item'"
  >
    </paginate>

</template>

<script>

import { mapState } from 'vuex'
import Paginate from "vuejs-paginate-next";
import { getAPI } from '../axios-api.js'


export default {
    name: "MyPagination",
    computed: mapState(['APIData']),
    components: {
        Paginate
    },
    props: ['links'],
    methods: {
      /**
       * Call next page
       */
      clickCallback: function (pageNum) {
        getAPI.get(`${this.links}?page=${pageNum}`, { headers: {Authorization: `Bearer ${this.$store.state.accessToken}`}})
          .then(response => {
            this.$store.state.APIData = response.data
          })
          .catch(() => {
            //nothing
          })
      },
    }
}
</script>