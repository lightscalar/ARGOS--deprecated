<template>

  <v-app id="app">

    <v-toolbar app class='elevation-0' style='background-color: #008066'>

      <img src='./assets/logo@2x.png' height=100 style='margin-left:32px; margin-top:23px'>
      <h1 class='logo'>ARGOS | Automated RecoGnition Of Species</h1>
      <v-spacer></v-spacer>

      <!-- <h1 class='white--text'>Target Species { &nbsp; </h1> -->

      <v-tooltip bottom>
      <v-chip
        label
        @click.native="openLibrary"
        slot='activator'
        v-bind:style="{backgroundColor: codeColor, color: textColor}">
        {{targetPlantName}}
      </v-chip>
        <span>Current annotation species—click to change</span>
      </v-tooltip>

    </v-toolbar>

    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
      <v-footer app style='background-color: #008066; height:40px'>
        <small class='white--text' style='margin-left:55px; margin-top: 3px'>
          Copyright 2018, Michigan Aerospace Corporatation. Ann Arbor, MI.
        </small>
      </v-footer>
    </v-content>

    <!-- MODALS -->
    <new-plant></new-plant>
  <plant-library></plant-library>

  <v-snackbar top v-model='waiting'>
    <v-icon dark>access_time</v-icon>
    <h3>Please Wait. Loading Image.</h3>
  </v-snackbar>

  <v-snackbar top color='error' v-model='showError'>
    <v-icon dark style='margin-right: 10px'>error_outline</v-icon>
    <h3>{{errorMessage}}</h3>
  </v-snackbar>

  </v-app>




</template>

<script>

import NewPlant from './components/NewPlant'
import PlantLibrary from './components/PlantLibrary'

export default {
  components: {NewPlant, PlantLibrary},
  name: 'App',
  data () {
    return {
      color: '#ffcc33',
      error: true
    }
  },

  computed: {

    showError: {
      get: function () {
        return this.$store.state.showError
      },
      set: function () {
        this.$store.commit('errorOff')
      }
    },

    errorMessage () {
      return this.$store.state.errorMessage
    },

    waiting () {
      return this.$store.state.waiting
    },

    codeColor () {
      return this.$store.state.annotationColor
    },

    textColor () {
      if (this.codeColor) {
        function hexToRgb(hex) {
          var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
          return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
          } : null;
        }
        var rgb = hexToRgb(this.codeColor)
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

    targetPlantName () {
      return this.$store.state.targetPlantName
    },

  },

  methods: {
    openNewSpecies () {
      console.log('Opening!')
      this.$store.commit('openNewSpecies')
    },

    openLibrary () {
        this.$store.commit('openLibrary')
    }

  },

  mounted () {
    this.$store.dispatch('listPlants')
    this.$store.dispatch('listImages')
  }
}
</script>


<style>
html, body {margin: 0; height: 100%; overflow: hidden; margin-top:-18px}
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
.logo {
  color: #ffffff;
  margin-left: 15px;
}
.overlay: {
  opacity: 0.5;
  position: absolute;
  color: blue;
  left: 100px;
  top: 100px;
  width: 100px;
  height: 100px;
}
</style>
