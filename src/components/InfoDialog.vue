<template>
  <div class="text-xs-center">

    <v-divider style='margin-top:-25px'></v-divider>
    <v-card>
      <v-card-text>
        <v-list dense style='margin-top:-0'>
          <v-list-tile>
            <v-list-tile-content>Latitude</v-list-tile-content>
            <v-list-tile-content
              class="align-end">{{latitude}}</v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-content>Longitude</v-list-tile-content>
            <v-list-tile-content
              class="align-end">{{longitude}}</v-list-tile-content>
          </v-list-tile>
          <v-list-tile>
            <v-list-tile-content>Altitude (ft)</v-list-tile-content>
            <v-list-tile-content
              class="align-end">{{altitude}}</v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-card-text>
      <v-divider></v-divider>

      <v-card-text>
        <v-list dense v-if='uniqueGroundTruth.length>0'>

          <v-list-tile v-for='(truth,i) in uniqueGroundTruth' :key='i'
                       @click='setPlant(truth.scientific_name)'
            style='background-color: #fafafa; margin-top: 2px'>
            <v-list-tile-content 
              style='cursor:pointer'>
              <a @click='setPlant(truth.scientific_name)' style='color: black'>
                {{truth.scientific_name}}
              </a>
            </v-list-tile-content>
            <v-list-tile-content
              class="align-end">
              <div style='border-radius:50%; height:25px; width:25px; cursor: pointer'
                   @click='setPlant(truth.scientific_name)'
                   v-bind:style='{backgroundColor: colorMap[truth.scientific_name]}'>
              </div>
            </v-list-tile-content>
          </v-list-tile>

        </v-list>

        <h2 v-else style='color: #9f9f9f'>
          No Ground Truth Present in Image
        </h2>
      </v-card-text>
    </v-card>
  </div>

</template>

<script>
// import Component from "../component_location"

export default {

  components: {},

  props: [],

  data () {
    return {
    }
  },

  watch: {

  },

  methods: {
    closeDialog () {
      this.$store.commit('closeInfo')
    },

    setPlant (plantName) {
      this.$store.commit('setTruthPlant', plantName)
    }

  },

  computed: {

    isOpen () {
      return this.$store.state.infoIsOpen
    },

    latitude () {
      return this.$store.state.latitude
    },

    longitude () {
      return this.$store.state.longitude
    },

    altitude () {
      return this.$store.state.altitude
    },

    orientation () {
      return this.$store.state.orientation
    },

    sampleImages () {
      return this.$store.state.sampleImages
    },

    image () {
      return this.$store.state.image
    },

    colorMap () {
      return this.$store.state.colorMap
    },

    uniqueGroundTruth () {

      console.log(this.image.ground_truth)

      var isIn = function (el, arr) {
        for (var i=0; i<arr.length; i++) {
          if (arr[i] == el) {
            return true
          }
        }
        return false

      }
      var ugt = []
      var uniquePlants = []
      for (var k=0; k<this.image.ground_truth.length; k++) {
        if (!isIn(this.image.ground_truth[k].scientific_name, uniquePlants)) {
          uniquePlants.push(this.image.ground_truth[k].scientific_name)
          ugt.push(this.image.ground_truth[k])
        }
      }
      return ugt
    },

  },

  mounted () {
  }
}

</script>

      <style>

</style>
