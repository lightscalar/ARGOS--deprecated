<template>

  <v-container fluid>
    <v-layout row>

      <v-flex xs8 @click.native='clicked' pa-2>
        <div id='zoombox' style='position: relative'>
          <!-- <img id='image' src='static/images/dji_00001.png' -->
          <!--      style='border: 4px solid #888888' -->
          <!--      width='100%'> -->
          <img id='image'
               v-if='imageLocation != "NO_IMAGE"'
               :src="imageLocation"
               v-on:load='addZoom'
               width='100%'>
          <div v-else>
            <h2>Please Select an Image.</h2>
            <img src='../assets/arrow.png' width='50%' style='float:right; margin-top:-125px'>
          </div>

        </div>
      </v-flex>

      <v-flex xs4>
        <flight-library></flight-library>
      </v-flex>

    </v-layout>

  </v-container>

</template>


<script>
  // import Component from "../component_location"
  import FlightLibrary from "./FlightLibrary"

  export default {

    components: {FlightLibrary},

    props: [],

    data () {
      return {
        selectedX: 0,
        selectedY: 0,
        boxWidth: 50,
        dialog: false,
        targetSpecies: null,
        annotations: [],
        tagColor: '#8E24AA'
      }
    },

    watch: {

    },

    methods: {

      addZoom() {
        $('#image').elevateZoom({scrollZoom: true, tint: true, tintOpacity: 0.1})
        $(document).bind('click', '#zoomPicture', this.imageClicked)
      },

      clicked (evt) {
      },

      undoAnnotation () {
        if (this.annotations.length>0) {
          var garbage = this.annotations.pop()
          var id = garbage.x + '-' + garbage.y
          $('#'+id).remove()
        }
      },

      changedSpecies (species) {
        this.$store.commit('setTargetSpecies', species)
      },

      addTag() {
        var id = this.selectedX + '-' +  this.selectedY
        $('#zoombox').append('<div id=' + id + '></div>')
        $('#'+id).css({'background-color': this.tagColor})
        $('#'+id).css({'opacity': 0.3})
        $('#'+id).css({'position': 'absolute'})
        $('#'+id).css({'top': this.selectedY-this.boxWidth/2,
          'left': this.selectedX-this.boxWidth/2})
        $('#'+id).css({'width': this.boxWidth, 'height': this.boxWidth})
        console.log(this.selectedX)
        console.log(this.selectedY)
        var annotation = {
          x: this.selectedX,
          y: this.selectedY,
          species: this.targetSpecies
        }
        this.annotations.push(annotation)
      },

      imageClicked(e) {
        if (e.pageX != undefined) {
          var imgHeight = $('#image').height()
          var imgWidth = $('#image').width()
          // Compensate for the image offset!!
          this.selectedX = e.pageX - $('#image').offset().left
          this.selectedY = e.pageY - $('#image').offset().top
          // Ensure we cannot annotate outside of the image.
          if (this.selectedX >0 && this.selectedX<imgWidth && this.selectedY>0 &&
            this.selectedY<imgHeight) {
            this.addTag()
          }
        }
      }
    },

    computed: {

      speciesList () {
        return this.$store.state.plantList
      },

      imageLocation () {
        if (this.$store.state.imageLocation != '') {
          return this.$store.state.imageServerUrl + '/' + this.$store.state.imageLocation
        } else {
          return 'NO_IMAGE'
        }
      }

    },

    mounted () {
      $('#image').elevateZoom({scrollZoom: true, tint: true, tintOpacity: 0.1})
      this.targetSpecies = this.$store.state.targetSpecies
    }
  }

</script>

<style>

#pane: {
  width: 50px;
  float: none;
  height:50px;
}
#zoombox: {
  position: relative
}
.lay: {
  position: absolute;
  left: 100px;
  top: 100px;
  width: 100px;
  height: 100px;
  background-color: red;
}

</style>
