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

        <v-layout>
          <v-flex xs12 ma-3 elevation-2>
            <v-card>
              <v-card-title>
                <h3>Available Plant Species</h3>
                <v-spacer></v-spacer>
                <v-text-field
                  v-model="search"
                  append-icon="search"
                  label="Search"
                  single-line
                  hide-details
                  >
                </v-text-field>
              </v-card-title>
              <v-data-table
                :headers="headers"
                :items="plants"
                :search="search"
                >
                <template slot="items" slot-scope="props">
                  <td class="text-xs-left">
                    <v-btn :style=
                    '{backgroundColor: props.item.color_code,
                    color: textColor(props.item.color_code)}'
                      @click='setPlant(props.item)'
                    style='min-width: 330px'>
                      {{ props.item.scientific_name }}
                    </v-btn>
                  </td>
                  <td class="text-xs-left">{{ props.item.common_name }}</td>
                  <td class="text-xs-left">{{ props.item.physiognomy }}</td>
                  <td class="text-xs-left">{{ props.item.category }}</td>
                  <td class="text-xs-left">{{ props.item.species_codes[0] }}</td>
                  <td class="text-xs-left">{{ props.item.color_code }}</td>
                  <td class="text-xs-left">
                    <v-btn icon @click.native='editPlant(props.item)'>
                      <v-icon>edit</v-icon></v-btn>
                  </td>
                </template>
                <v-alert slot="no-results" :value="true" color="error" icon="warning">
                  Your search for "{{ search }}" found no results.
                </v-alert>
              </v-data-table>
            </v-card>
          </v-flex>
    </v-layout>

        <!-- <v-container>
          <v-layout row wrap>
            <v-flex xs12>
              <v-expansion-panel>
                <v-expansion-panel-content
                  v-for="(item,i) in structuralCategories"
                  :key="i"
                  style='background-color: #f0f0f0; color: #909090'
                  >
                  <div slot="header"><h2>{{item.title}}s</h2></div>
                  <v-card>
                    <v-card-text>

                      <v-list
                        two-lines
                      v-if="plantsByStructure[item.name.toLowerCase()].length>0">

                      <v-list-tile
                        v-for="(plant,k) in plantsByStructure[item.name.toLowerCase()]"
                        :key="plant.scientific_name+k"
                        avatar
                        class='clickable'
                        >
                        <v-list-tile-avatar @click='setPlant(plant)' >
                          <div
                            v-bind:style='{backgroundColor: plant.color_code}'
                            style='height:40px; width:40px; background-color: #ffcc33'>
                          </div>
                        </v-list-tile-avatar>

                        <v-list-tile-content >
                          <v-list-tile-title @click='setPlant(plant)' class='clickable'>
                            {{plant.scientific_name}} ({{plant.common_name}})
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
        </v-container> -->
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
      search: '',
      structuralCategories: [
        {name: 'tree', title: 'Tree'},
        {name: 'shrub', title: 'Shrub'},
        {name: 'graminoid', title: 'Graminoid'},
        {name: 'forb', title: 'Forb'}
      ],
      desserts: [{'scientific_name':'ice cream'}],
      headers: [
        {
          text:'Scientific Name',
          value: 'scientific_name',
          align: 'left',
          sortable: true
        },
        {
          text:'Common Name',
          value: 'common_name',
          align: 'left',
          sortable: true
        },
        {
          text:'Physiognomy',
          value: 'physiognomy',
          align: 'left',
          sortable: true
        },
        {
          text:'Category',
          value: 'category',
          align: 'left',
          sortable: true
        },
        {
          text:'Species Code',
          value: 'species_code[0]',
          align: 'left',
          sortable: true
        },
        {
          text:'Annotation Color',
          value: 'species_code',
          align: 'left',
          sortable: false
        },
        {
          text:'Edit Plant',
          value: '',
          align: 'left',
          sortable: false
        }
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

    textColor (color) {
      if (color) {
        function hexToRgb(hex) {
          var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
          return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
          } : null;
        }
        var rgb = hexToRgb(color)
        var r = rgb.r; var g = rgb.g; var b = rgb.b
        if (r*0.299 + g*0.587 + b*0.114 > 127) {
          return '#000000'
        } else {
          return '#ffffff'
        }
      } else {
        return '#000000'
      }
    },

    setPlant (plant) {
      console.log('Setting.')
      this.$store.commit('setPlant', plant)
      this.$store.dispatch('getSamples', plant.species_codes[0])
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

    plants() {
      return this.$store.state.plantList
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
