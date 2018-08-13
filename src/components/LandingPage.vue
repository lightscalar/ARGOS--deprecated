<template>

  <v-container fluid>
    <v-layout row>

      <h1>Where Are You?</h1>

      <input
        style='height: 50px; width: 75px; text-align: center'
        type='color'
        v-model='selectedColor'>

    </v-layout>
  </v-container>

</template>

<script>
  // import Component from "../component_location"

  export default {

    components: {},

    props: [],

    data () {
      return {
        selectedColor: '#ffcc33'
      }
    },

    watch: {

    },

    methods: {

    },

    computed: {

    },

    mounted () {
    }
  }

</script>

<style>

</style>\
