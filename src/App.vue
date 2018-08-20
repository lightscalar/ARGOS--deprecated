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

      <!-- <v-tooltip bottom> -->
      <!--   <v-btn slot='activator' -->
      <!--          @click.native='openNewSpecies' -->
      <!--          class='mr-1' -->
      <!--          icon -->
      <!--          style='background-color:#ffffff; color: #008066'> -->
      <!--     <v-icon>add</v-icon></v-btn> -->
      <!--   <span>Add a new species</span> -->
      <!-- </v-tooltip> -->

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
      color: '#ffcc33'
    }
  },

  computed: {

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
