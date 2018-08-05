<template>

  <v-container fluid>
    <v-layout row>

      <v-flex xs9 @click.native='clicked' pa-2>
        <div id='zoombox' style='position: relative'>
          <img id='image' src='static/images/dji_00001.png'
               width='100%'>
        </div>
      </v-flex>

      <v-flex xs3 pa-2>
        <v-card>
          <v-card-text>
            <v-select
              v-model='targetSpecies'
              :items="speciesList"
              item-text= 'scientificName'
              label="Target Species">

            </v-select>
          </v-card-text>
          <v-card-text class='text-xs-left'>
            Location: St. John's Marsh
          </v-card-text>
          <v-card-actions>
            <v-btn style='background-color:#008066; color: white'>
              <v-icon left>navigate_next</v-icon>Next Image</v-btn>
            <v-spacer></v-spacer>
            <v-btn @click='dialog=true' style='background-color:#008066; color: white'>
              <v-icon left>add_circle</v-icon>Add Species</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>

    </v-layout>


    <v-layout row justify-center>
      <v-dialog v-model="dialog" persistent max-width="500px">
        <v-card>
          <v-card-title style='background-color: #008066; color: white'>
            <span class="headline">Add New Species</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 sm6>
                  <v-text-field
                        label="Species Name"
                        required
                        hint='Latin species name'
                        outline
                        persistent-hint>
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm6>
                  <v-text-field
                        label="Shortcut Name"
                        persistent-hint
                        outline
                        hint="Shortcut code used for GPS annotation">
                  </v-text-field>
                </v-flex>
                <v-flex xs12 sm6>
                  <v-select
                    outline
                    :items="['Invasive', 'Native']"
                    label="Species Type"
                    required
                    ></v-select>
                </v-flex>
                <v-flex xs12 sm6>
                  <v-select
                    outline
                    :items="['Red', 'Pink', 'Purple',
                    'Indigo', 'Blue', 'Cyan', 'Teal',
                    'Green', 'Lime', 'Yellow', 'Orange',
                    'Deep-Orange', 'Blue-Grey', 'Brown']"
                    label="Coding Color"
                    required
                    ></v-select>
                </v-flex>
                <v-flex xs12>
                  <v-textarea
                    outline
                    name="input-7-1"
                    label="Species Notes"
                    value=""
                    hint="Anything interesting about this plant?"
                    ></v-textarea>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" flat @click.native="dialog = false">Close</v-btn>
            <v-btn color="blue darken-1" flat @click.native="dialog = false">Save</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
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
        targetSpecies: null
      }
    },

    watch: {

    },

    methods: {

      clicked (evt) {
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
            console.log(this.selectedX)
            this.addTag()
          }
        }
      }
    },

    computed: {

      speciesList () {
        return this.$store.state.speciesList
      },

      speciesDict () {
        // Dictionary version of species list, indexed by scientificName
        var speciesDict = {}
        for (var i=0; i<this.speciesList.length; i++) {
          speciesDict[this.speciesList[i].scientificName] = this.speciesList[i]
        }
        return speciesDict
      },

      tagColor () {
        var codeColor = this.speciesDict[this.targetSpecies].codeColor
        console.log(codeColor)
        return codeColor
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
