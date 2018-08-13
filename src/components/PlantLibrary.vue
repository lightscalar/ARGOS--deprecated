<template>

  <v-layout row justify-center>
    <v-dialog v-model="libraryIsOpen"
      fullscreen hide-overlay
      transition="dialog-bottom-transition">

      <v-card>
        <v-toolbar dark style='background-color: #008066'>
          <v-btn icon dark @click.native="closeLibrary">
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title style=''>Species Library</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-tooltip bottom>
            <v-btn slot='activator'
                   @click.native='openNewSpecies("Tree")'
                   class='mr-1'
                   icon
                   style='background-color:#ffffff; color: #008066'>
              <v-icon>add</v-icon></v-btn>
            <span>Add a new species</span>
          </v-tooltip>
        </v-toolbar>

        <v-container>
        <v-layout row wrap>
          <v-flex xs12>
            <v-expansion-panel>
              <v-expansion-panel-content
                v-for="(item,i) in structuralCategories"
                :key="i"
                style='background-color: #f0f0f0; color: #008066'
                >
                <div slot="header"><h2>{{item.title}}s</h2></div>
                <v-card>
                  <v-card-text>

                    <v-list
                      two-lines
                      v-if="plantsByStructure[item.name.toLowerCase()].length>0">

                      <v-list-tile
                        v-for="(plant,k) in plantsByStructure[item.name.toLowerCase()]"
                        :key="plant.scientificName+k"
                        avatar
                        class='clickable'
                        >
                        <v-list-tile-avatar @click='setPlant(plant)' >
                          <div
                            v-bind:style='{backgroundColor: plant.annotationColor}'
                            style='height:40px; width:40px; background-color: #ffcc33'>
                          </div>
                        </v-list-tile-avatar>

                        <v-list-tile-content >
                          <v-list-tile-title @click='setPlant(plant)' class='clickable'>
                            {{plant.scientificName}} ({{plant.commonName}})
                          </v-list-tile-title>
                        <v-divider></v-divider>
                        </v-list-tile-content>

                        <v-list-tile-action xs6>
                          <v-btn icon ripple @click.native='editPlant(plant)'>
                            <v-icon color="grey lighten-1">edit</v-icon>
                          </v-btn>
                        </v-list-tile-action>
                      </v-list-tile>

                      <v-divider></v-divider>
                      <h3
                        style='fontSize: 18px; fontWeight: normal; color: gray; margin-right: 3px'>
                        <a @click='openNewSpecies(item.title)'>Add another?</a>
                      </h3>
                    </v-list>

                    <h3 v-else style='fontSize: 18px; fontWeight: normal; color: gray'>
                      Sorry, there are no plants of this type yet.
                      <a @click='openNewSpecies(item.title)'>Add one?</a>
                    </h3>

                  </v-card-text>
                </v-card>
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-flex>

        </v-layout>
        </v-container>
      </v-card>

    </v-dialog>

    <edit-plant></edit-plant>

  </v-layout>

</template>

<script>
// import Component from "../component_location"
import EditPlant from "./EditPlant"

export default {

  components: {EditPlant},

  props: [],

  data () {
    return {
      structuralCategories: [
        {name: 'tree', title: 'Tree'},
        {name: 'shrub', title: 'Shrub'},
        {name: 'graminoid', title: 'Graminoid'},
        {name: 'forb', title: 'Forb'}
      ]
    }
  },

  watch: {

    libraryIsOpen: function () {
      this.$store.dispatch('listPlants')
    }

  },

  methods: {

    closeLibrary () {
        this.$store.commit('closeLibrary')
    },

    setPlant (plant) {
      console.log('Setting.')
      this.$store.commit('setPlant', plant)
      this.closeLibrary()
    },

    editPlant (plant) {
      this.$store.commit('setPlant', plant)
      this.$store.commit('openEditPlant')
      console.log('Editing this plant.')
    },

    openNewSpecies (category) {
      this.$store.commit('resetNewSpecies')
      this.$store.commit('setPlantCategory', category)
      this.$store.commit('openNewSpecies')
    }

  },

  computed: {

    libraryIsOpen () {
      return this.$store.state.libraryIsOpen
    },

    plantsByStructure () {
      return this.$store.state.plantsByStructure
    }

  },

  mounted () {
  }
}

</script>

<style>
.clickable {
  cursor: pointer
}
.clickable:hover {
    color: #008066;
    background-color: #efefef
}

</style>
