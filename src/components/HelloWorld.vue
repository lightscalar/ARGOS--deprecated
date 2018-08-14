<template>

  <v-container fluid>
    <v-layout row>

      <v-flex xs9 @click.native='clicked' pa-2>
        <div id='zoombox' style='position: relative'>
          <img id='image' src='static/images/dji_00001.png'
               style='border: 4px solid #888888'
               width='100%'>
        </div>
      </v-flex>

      <v-flex xs3 pa-2>
        <v-card>
          <v-card-text>
          </v-card-text>
          <v-card-text class='text-xs-left'>
            Location: St. John's Marsh
          </v-card-text>
          <v-card-actions>
            <v-tooltip bottom>
              <v-btn slot='activator'
                @click.native='undoAnnotation'
                class='mr-1'
                icon
                style='background-color:#008066; color: white'>
                <v-icon>undo</v-icon></v-btn>
              <span>Undo last annotation</span>
            </v-tooltip>

            <v-tooltip bottom>
              <v-btn slot='activator' icon style='background-color:#008066; color: white'>
                <v-icon>navigate_next</v-icon></v-btn>
              <span>Move to next image</span>
            </v-tooltip>

            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <v-btn slot='activator'
                     @click='dialog=true'
                     icon style='background-color:#008066; color: white'>
                <v-icon>add</v-icon></v-btn>
              <span>Add a new species</span>
            </v-tooltip>
          </v-card-actions>
        </v-card>
      </v-flex>

    </v-layout>


    <v-layout row justify-center>
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
        selectedX: 0,
        selectedY: 0,
        boxWidth: 50,
        dialog: false,
        targetSpecies: null,
        annotations: []
      }
    },

    watch: {

    },

    methods: {

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

    },

    mounted () {
      $('#image').elevateZoom({scrollZoom: true, tint: true, tintOpacity: 0.1})
      $(document).bind('click', '#zoomPicture', this.imageClicked)
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
