<template>
  <v-layout row justify-center>
    <v-dialog v-model="newSpeciesOpen" persistent max-width="500px">
      <v-card>
        <v-card-title style='background-color: #008066; color=#ffffff'>
          <span class="headline" style='color: white'>Add New Species</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-select
                  outline
                  :items="['Tree', 'Shrub', 'Graminoid', 'Forb']"
                  label="Plant Physiognomy"
                  required
                  v-model='newSpecies.structuralCategory'
                  ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-select
                  outline
                  :items="['Native', 'Invasive']"
                  label="Plant Physiognomy"
                  required
                  v-model='newSpecies.category'
                  ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Scientific Name"
                  hint="E.g., Phragmites australis subsp americanus"
                  outline
                  v-model='newSpecies.scientificName'
                  required>
                </v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Common Name"
                  outline
                  v-model='newSpecies.commonName'
                  hint="E.g., Reed"></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Species Code"
                  outline
                  v-model='newSpecies.codeName'
                  hint="E.g., PA (note: case insensitive)">
                </v-text-field>
              </v-flex>
              <v-flex xs6>
                <v-text-field
                  v-model='newSpecies.annotationColor'
                  outline
                  label='Annotation Color'>
                </v-text-field>
              </v-flex>
              <v-flex xs6>
                <input
                  style='height: 58px; width: 100%'
                  type='color'
                  v-model='newSpecies.annotationColor'>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="closeDialog()">Close</v-btn>
          <v-btn color="blue darken-1" flat @click.native="saveSpecies">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>


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

        newSpeciesOpen: function () {
          if (!this.$store.state.newSpeciesOpen) {
            console.log('Resetting species!')
            this.$store.commit('resetNewSpecies')
          }
        }

    },

    methods: {

      closeDialog () {
        this.$store.commit('closeNewSpecies')
      },

      saveSpecies () {
        this.$store.dispatch('savePlant', this.newSpecies)
        this.$store.dispatch('listPlants')
        this.closeDialog()
      },

    },

    computed: {

      newSpeciesOpen () {
        return this.$store.state.newSpeciesOpen
      },

      newSpecies () {
        // Return an empty species object.
        return this.$store.state.emptyPlant
      }

    },

    mounted () {

    }

  }

</script>

<style>

</style>
