<template>

  <v-container fluid>
    <v-layout row>

      <v-flex xs8 @click.native='clicked' pa-2>
        <div id='zoombox' style='position: relative'>
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
        <flight-library
          v-on:undo='undoAnnotation'
          v-on:delete='deleteAllAnnotations'>
        </flight-library>
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
        groundTruthPoints: []
      }
    },

    watch: {

      image: function () {
        this.updateGroundTruth()
        this.updateAnnotations()
      }

    },

    methods: {

      updateAnnotations () {
        $('.annotation').remove()
        //Insert annotation tag into image.
        console.log('Here is the new image:')
        console.log(this.image)
        for (var k=0; k<this.image.annotations.length; k++) {
          this.plotAnnotation(this.image.annotations[k])
        }
      },

      updateGroundTruth () {
        var truths = this.image.ground_truth
        var width = $('#image').width()
        var height = $('#image').height()
        this.removeAllGroundTruthPoints()
        for (var k=0; k < truths.length; k++) {
          console.log(truths[k])
          var row = parseInt(truths[k].position_in_image[0] * height/3000)
          var col = parseInt(truths[k].position_in_image[1] * width/4000)
          var id = col + 'gt' + row
          var div = '<div id='+id+'></div>'
          //$('#zoombox').append('<div id='+id+' tooltip="'+truths[k].scientific_name+'"></div>')
          $('#zoombox').append(div)
          $('#'+id).css({'background-color': this.colorMap[truths[k].scientific_name]})
          $('#'+id).css({'position': 'absolute'})
          $('#'+id).css({'border-radius': '50%'})
          $('#'+id).css({'height': '20px'})
          $('#'+id).css({'width': '20px'})
          $('#'+id).css({'top': row - 10})
          $('#'+id).css({'left': col - 10})
          this.groundTruthPoints.push(id)
        }

      },

      removeAllGroundTruthPoints () {

        for (var k=0; k < this.groundTruthPoints.length; k++) {
          var id = this.groundTruthPoints[k]
          $('#'+id).remove()
        }
        this.groundTruthPoints = []

      },

      addZoom () {
        $('#image').elevateZoom({scrollZoom: true, tint: true, tintOpacity: 0.1})
        $(document).unbind('click')
        $(document).bind('click', '#zoomPicture', this.imageClicked)
        this.updateGroundTruth()
      },

      clicked (evt) {
      },

      undoAnnotation () {
        if (this.image.annotations.length>0) {
          var garbage = this.image.annotations.pop()
          var id = garbage.col + '-' + garbage.row
          $('#'+id).remove()
          this.saveImage()
        }
      },

      deleteAllAnnotations () {
        for (var k=0; k<this.image.annotations.length; k++) {
          var garbage = this.image.annotations[k]
          var id = garbage.col + '-' + garbage.row
          $('#'+id).remove()
        }
        this.image.annotations = []
        this.saveImage()
      },

      changedSpecies (species) {
        this.$store.commit('setTargetSpecies', species)
      },

      plotAnnotation (annotation) {
        var id = annotation.col + '-' + annotation.row
        var tagColor = this.$store.state.colorMap[annotation.scientific_name]
        $('#zoombox').append('<div id=' + id + ' class="annotation"></div>')
        $('#'+id).css({'background-color': this.colorMap[annotation.plant]})
        $('#'+id).css({'opacity': 0.5})
        $('#'+id).css({'position': 'absolute'})
        $('#'+id).css({'top': annotation.row - this.boxWidth/2,
          'left': annotation.col - this.boxWidth/2})
        $('#'+id).css({'width': this.boxWidth, 'height': this.boxWidth})

      },

      addTag() {
        if (this.$store.state.targetPlantName == 'Click Here to Set Plant Species') {
          // Don't annotate nothin'.
          this.$store.commit('errorOn', 'Please select a plant species to begin annotation.')
          return
        }
        var id = this.selectedX + '-' +  this.selectedY
        $('#zoombox').append('<div id=' + id + ' class="annotation"></div>')
        $('#'+id).css({'background-color': this.tagColor})
        $('#'+id).css({'opacity': 0.5})
        $('#'+id).css({'position': 'absolute'})
        $('#'+id).css({'top': this.selectedY-this.boxWidth/2,
          'left': this.selectedX-this.boxWidth/2})
        $('#'+id).css({'width': this.boxWidth, 'height': this.boxWidth})
        var annotation = {
          col: this.selectedX,
          row: this.selectedY,
          plant: this.$store.state.targetPlantName,
          imageWidth: $('#image').width(),
          imageHeight: $('#image').height(),
        }
        this.image.annotations.push(annotation)
        this.saveImage()
        console.log(this.image)
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
      },

      saveImage () {
        console.log('Saving Image!')
        this.$store.dispatch('updateImage', this.image)
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
      },

      tagColor () {
        return this.$store.state.annotationColor
      },

      image () {
        return this.$store.state.image
      },

      colorMap () {
        return this.$store.state.colorMap
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
