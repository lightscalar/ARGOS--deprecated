import Vue from 'vue'
import Vuex from 'vuex'
import api from '../api/index'
Vue.use(Vuex)

var phragmites = {
      scientificName: 'Phragmites australis subsp americanus',
      commonName: 'Reed',
      gpsCode: 'PA',
      speciesStatus: 'Invasive',
      codeColor: 'Pink',
      notes: 'About twelve feet tall by August.'
    }

var buckthorn = {
      scientificName: 'Frangula alnus',
      commonName: 'Glossy Buckthorn',
      gpsCode: 'FA',
      speciesStatus: 'Invasive',
      codeColor: 'Indigo',
      notes: 'Clumpy, in bushes.'
    }


export default new Vuex.Store ({

  state: {

    targetSpecies: phragmites.scientificName,

    targetSpeciesObj: phragmites,

    codeColor: phragmites.codeColor,

    speciesList: [phragmites, buckthorn],

    colors: {
      'Red':'#F44336',
      'Pink': '#e91e63',
      'Purple': '#9c27b0',
      'Indigo': '#3f51b5',
      'Blue': '#2196f3',
      'Cyan': '#00bcd4',
      'Teal': '#009688',
      'Green': '#4caf50',
      'Lime': '#cddc39',
      'Yellow': '#ffeb3b',
      'Orange': '#ff9800',
      'Deep-Orange': '#ff5722',
      'Brown': '#795548',
      'Blue-Grey': '#607d8b',
    }
  },

  mutations: {

    setSpeciesList(state, speciesList) {
     state.speciesList = speciesList
    },

    setTargetSpecies (state, speciesScientificName) {
        for (var i=0; i<state.speciesList.length; i++) {
            if (state.speciesList[i].scientificName == speciesScientificName) {
                state.targetSpeciesObj = state.speciesList[i]
                state.targetSpecies = speciesScientificName
                state.codeColor = state.targetSpeciesObj.codeColor
            }
        }
    }

  },

  actions: {

    saveAnnotation (context, annotations) {
      console.log(annotations)
      api.postResource('annotations', annotations).then(function (resp) {
        console.log(resp.data)
      })
    },

    getSentence (context, sentence_id) {
      api.getResource('sentence', sentence_id).then( function (resp) {
        context.commit('setSentence', resp.data)
      })
    },

    getNumberAnnotations (context) {
      api.listResource('number').then( function (resp) {
        context.commit('setNumber', resp.data)
      })
    },

    getAnalysis (context) {
      var data = {}
      data['text'] = context.state.currentSentence['text']
      api.postResource('analysis', data).then( function (resp) {
        context.commit('setAnalysis', resp.data)
      })
    },

    submitCommand (context, command) {
      var data = {}
      data['command'] = command
      api.postResource('command', data).then( function (resp) {
        context.commit('setStatus', resp.data)
      })
    },

    getAccuracies (context) {
      api.listResource('accuracies').then( function (resp) {
        context.commit('setAccuracies', resp.data)
      })
    },

    getStatus (context) {
      api.listResource('command').then( function (resp) {
        console.log(resp.data.train)
        context.commit('setStatus', resp.data)
      })

    },

    getRandomReview (context) {
      api.listResource('reviews').then( function (resp) {
        console.log(resp.data)
        context.commit('setReviewText', resp.data.text)
      })

    },

    submitReview (context, reviewText) {
      api.postResource('reviews', {'text':reviewText}).then( function (resp) {
        context.commit('setReview', resp.data)
        console.log(resp.data)
      })
    },

  },

})



