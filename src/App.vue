<template>

  <v-app id="app">
    <v-toolbar app class='elevation-0' style='background-color: #008066'>
      <img src='./assets/logo@2x.png' height=100 style='margin-left:32px; margin-top:23px'>
      <h1 class='logo'>ARGOS | Automated RecoGnition Of Species</h1>
      <v-spacer></v-spacer>
      <h1 class='white--text'>Target Species { &nbsp; </h1>
      <v-chip
        label
        v-bind:style="{backgroundColor: codeColor, color: textColor}">{{targetSpecies}}</v-chip>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
      <v-footer app style='background-color: #008066; height:60px'>
        <small class='white--text' style='margin-left:55px'>
          Copyright 2018, Michigan Aerospace Corporatation. Ann Arbor, MI.
        </small>
      </v-footer>
    </v-content>

  </v-app>




</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      color: '#ffcc33'
    }
  },

  computed: {

    codeColor () {
      var colorName = this.$store.state.codeColor
      var hexCode = this.$store.state.colors[colorName]
      return hexCode
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
        if (r*0.299 + g*0.587 + b*0.114 > 186) {
          return '#000000'
        } else {
          return '#ffffff'
        }
      } else {
        return '#000000'
      }

    },

    targetSpecies () {
      return this.$store.state.targetSpecies
    }

  }
}
</script>


<style>
#app {
  <!-- font-family: 'Avenir', Helvetica, Arial, sans-serif; -->
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
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
