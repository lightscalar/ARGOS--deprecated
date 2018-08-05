// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import Vuetify from '../node_modules/vuetify'
import '../node_modules/vuetify/dist/vuetify.min.css' // Ensure you are using css-loader
import '../node_modules/material-design-icons-iconfont/dist/material-design-icons.css' // Ensure you are using css-loader
import store from './store'
import { Photoshop } from 'vue-color'


Vue.config.productionTip = false
Vue.use(Vuetify)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App, 'photoshop-picker': Photoshop},
  template: '<App/>'
})
