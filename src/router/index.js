import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import LandingPage from '@/components/LandingPage'
import FlightLibrary from '@/components/FlightLibrary'

Vue.use(Router)

export default new Router({
  routes: [

    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },

    {
      path: '/landing',
      name: 'LandingPage',
      component: LandingPage
    },

    {
      path: '/flights',
      name: 'FlightLibrary',
      component: FlightLibrary
    }

  ]
})
