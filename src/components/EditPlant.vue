<template>
  <v-layout row justify-center>
    <v-dialog v-model="editPlantIsOpen" persistent max-width="500px">
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
                  v-model='targetPlant.physiognomy'
                  ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-select
                  outline
                  :items="['Native', 'Invasive']"
                  label="Category"
                  required
                  v-model='targetPlant.category'
                  ></v-select>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Scientific Name"
                  hint="E.g., Phragmites australis subsp americanus"
                  outline
                  v-model='targetPlant.scientific_name'
                  required>
                </v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Common Name"
                  outline
                  v-model='targetPlant.common_name'
                  hint="E.g., Reed"></v-text-field>
              </v-flex>
              <v-flex xs12>
                <v-text-field
                  label="Species Code"
                  outline
                  v-model='targetPlant.species_codes'
                  hint="E.g., PA (note: case insensitive)">
                </v-text-field>
              </v-flex>
              <v-flex xs6>
                <v-text-field
                  v-model='targetPlant.color_code'
                  outline
                  label='Annotation Color'>
                </v-text-field>
              </v-flex>
              <v-flex xs6>
                <input
                  style='height: 58px; width: 100%'
                  type='color'
                  value = '#ffcc33'
                  v-model='targetPlant.color_code'>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-btn color="red darken-1" flat @click.native="deletePlant">Delete</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click.native="closeDialog()">Close</v-btn>
          <v-btn color="blue darken-1" flat @click.native="updatePlant">Save</v-btn>
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

  },

  methods: {

    closeDialog () {
      this.$store.commit('closeEditPlant')
    },

    updatePlant () {
      this.$store.dispatch('updatePlant', this.targetPlant)
      this.$store.commit('setPlant', this.targetPlant)
      this.closeDialog()
    },

    deletePlant () {
      this.$store.dispatch('deletePlant', this.targetPlant['_id'])
      this.closeDialog()
    }

  },

  computed: {

    editPlantIsOpen () {
      return this.$store.state.editPlantIsOpen
    },

    targetPlant () {
      // Return an empty species object.
      return this.$store.state.targetPlant
    }

  },

  mounted () {

  }

}

</script>

<style>

</style>
