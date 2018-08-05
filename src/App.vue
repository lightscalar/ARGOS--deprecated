<template>

  <v-app id="app">
    <v-toolbar app class='elevation-0' style='background-color: #008066'>
      <img src='./assets/logo@2x.png' height=100 style='margin-left:32px; margin-top:23px'>
      <h1 class='logo'>ARGOS | Automated RecoGnition Of Species</h1>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
      <v-footer app style='background-color: #008066; height:50px'></v-footer>
    </v-content>

  </v-app>




</template>

<script>
export default {
  name: 'App',
  data () {
    return {

      dialog: false
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
