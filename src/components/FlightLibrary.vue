<template>

  <v-card class='sidebar'>
    <v-card-actions>
      <v-tooltip bottom>
        <v-btn
          @click='undoAnnotation'
          slot='activator'
          icon dark
          style="background-color: #008066; color=white; margin-right:5px"
          class='text--white'>
          <v-icon>undo</v-icon>
        </v-btn>
        <span>Undo the last annotation.</span>
      </v-tooltip>
      <v-tooltip bottom>
        <v-btn
          slot='activator'
          @click='deleteAll'
          icon dark style="background-color: #008066; color=white" class='text--white'>
          <v-icon>delete_forever</v-icon>
        </v-btn>
        <span>Delete all annotations on this image.</span>
      </v-tooltip>
      <v-spacer></v-spacer>
      <v-btn
        @click.native='prevImage'
        icon dark style="background-color: #008066; color=#ffffff">
        <v-icon>keyboard_arrow_left</v-icon>
      </v-btn>
      <v-btn
        @click.native='nextImage'
        icon dark style="background-color: #008066; color=white" class='text--white'>
        <v-icon>keyboard_arrow_right</v-icon>
      </v-btn>
    </v-card-actions>
    <v-divider></v-divider>

    <v-card-text>
      <v-select
        label='Collection Date'
        :items="availableFlights"
        item-text="date"
        item-value='flights'
        v-model='selectedDate'
        outline
        >
      </v-select>

        <v-select
          label='Flight Location'
          :disabled='selectedDate.length<1'
          :items="selectedDate"
          item-text="flight_name"
          item-value='images'
          outline
          v-model='selectedFlight'
          >
        </v-select>

          <v-select
            label='Available Images'
            :disabled='selectedDate.length<1'
            :items="selectedFlight"
            item-text="image_loc_short"
            item-value='_id'
            outline
            v-model='selectedImage'
            @change='updateImageData'
            >
          </v-select>

    </v-card-text>

    <info-dialog></info-dialog>

  </v-card>



</template>

<script>
  // import Component from "../component_location"
import InfoDialog from "./InfoDialog"

  export default {

    components: {InfoDialog},

    props: [],

    data () {
      return {
        selectedDate: [],
        selectedFlight: [],
        selectedImage: [],
      }
    },

    watch: {


    },

    methods: {

      deleteAll () {
        this.$emit('delete')
      },

      undoAnnotation () {
        this.$emit('undo')
      },

      openInfo () {
        this.$store.commit('openInfo')
      },

      updateImageData () {
        this.$store.dispatch('getImage', this.selectedImage)
      },

      nextImage () {
        var len = this.selectedFlight.length
        for (var k=0; k < len; k++) {
          if (this.selectedFlight[k]._id == this.selectedImage) {
            if (k < len-1) {
              this.selectedImage = this.selectedFlight[k+1]._id
              return
            } else {
              this.selectedImage = this.selectedFlight[0]._id
              return
            }
          }
        }
      },

      prevImage () {
        var len = this.selectedFlight.length
        for (var k=0; k < len; k++) {
          if (this.selectedFlight[k]._id == this.selectedImage) {
            if (k > 0) {
              this.selectedImage = this.selectedFlight[k-1]._id
              return
            } else {
              this.selectedImage = this.selectedFlight[len-1]._id
              return
            }
          }
        }
      },

    },

    computed: {

      availableFlights () {
        return this.$store.state.imageList
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
        return []
        return this.$store.state.sampleImages
      },

      image () {
        return this.$store.state.image
      }

    },

    mounted () {
      this.$store.dispatch('listImages')
    }
  }

</script>

<style>
    .sidebar {
      margin-top: 8px;
    }
</style>
