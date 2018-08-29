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

var emptySpecies = {
  structuralCategory: 'Tree',
  category: 'Invasive',
  scientificName: '',
  commonName: '',
  codeName: '',
  annotationColor: '#ffcc33'
}

export default new Vuex.Store ({

  state: {

    // Modal control variables.
    newSpeciesOpen: false,
    libraryIsOpen: false,
    editPlantIsOpen: false,
    infoIsOpen: false,
    waiting: false,
    showError: false,
    errorMessage: '',

    // Species variables.
    targetPlant: $.extend(true, {}, emptySpecies),
    imageLocation: '',
    imageServerUrl: 'http://localhost:2007',

    // Image details.
    latitude: 0,
    longitude: 0,
    altitude: 0,
    orientation: 0,

    // emptySpecies: JSON.parse(JSON.stringify(emptySpecies)),
    emptyPlant: $.extend(true, {}, emptySpecies),
    targetPlantName: 'Click Here to Set Plant Species',
    annotationColor: '#f3f3f3',

    plantList: [],

    plantsByStructure: {
      tree: [],
      shrub: [],
      graminoid: [],
      forb: []
    },

    // Flight data/images/etc.
    imageList: [],
    image: {ground_truth:[]},
    colorMap: {},

    // Sample images.
    sampleImages: []

  },

  mutations: {

    errorOn(state, errorMessage) {
      state.errorMessage = errorMessage
      state.showError = true
    },

    errorOff(state) {
      state.errorMessage=''
      state.showError=false
    },

    weWait(state) {
      state.waiting = true
    },

    weReady(state) {
      state.waiting = false
    },

    setPlantList(state, plantList) {
      state.plantList = plantList
      state.plantsByStructure = {tree:[], shrub: [], graminoid:[], forb:[]}
      // Also populate the plantsByStructure object.
      state.colorMap = {}
      for (var i=0; i<state.plantList.length; i++) {
        var plant = plantList[i]
        plantList[i].code = plant.species_codes[0]
        var physiognomy = plant.physiognomy.toLowerCase()
        state.plantsByStructure[physiognomy].push(plant)
        state.colorMap[plantList[i].scientific_name] = plantList[i].color_code
      }
    },

    setPlantSamples(state, samples) {
      // Add all images.
      state.sampleImages = []
      for (var k=0; k<samples.length; k++) {
        var sample = samples[k].split('/')
        var sampleLoc = '/' + sample.slice(-3).join('/')
        state.sampleImages.push(state.imageServerUrl + sampleLoc)
      }
    },

    setImageList(state, imageList) {
      state.imageList = imageList
    },

    setImage(state, image) {
      var img = image.image_loc
      var imgArray = img.split('/')
      state.imageLocation = '/' + imgArray.slice(-4).join('/')
      state.image = image
      state.latitude = Math.floor(image.metadata['Composite:GPSLatitude']*1000)/1000
      state.longitude = Math.floor(image.metadata['Composite:GPSLongitude']*1000)/1000
      state.altitude = Math.floor(image.metadata['XMP:RelativeAltitude']*3.28084*1000)/1000
      state.orientation = Math.floor(image.metadata['MakerNotes:CameraYaw']*1000)/1000
    },

    setPlant(state, plant) {
      state.targetPlantName = plant.scientific_name
      state.targetPlant = plant
      state.annotationColor = plant.color_code
    },

    setTruthPlant(state, plantName) {
      for (var k=0; k<state.plantList.length; k++) {
        if (state.plantList[k].scientific_name == plantName) {
          state.targetPlantName = state.plantList[k].scientific_name
          state.targetPlant = state.plantList[k]
          state.annotationColor = state.targetPlant.color_code
        }
      }
    },

    setPlantName(state, plantName) {
      state.targetPlantName = plantName
    },

    setPlantCategory(state, category) {
      state.emptyPlant['physiognomy'] = category
    },

    openNewSpecies(state) {
      state.newSpeciesOpen = true
    },

    openInfo(state) {
      state.infoIsOpen = true
    },

    closeInfo(state) {
      state.infoIsOpen = false
    },

    closeNewSpecies(state) {
      state.newSpeciesOpen = false
    },

    closeEditPlant(state) {
      state.editPlantIsOpen = false
    },

    openEditPlant(state) {
      state.editPlantIsOpen = true
    },

    openLibrary(state) {
      state.libraryIsOpen = true
    },

    closeLibrary(state) {
      state.libraryIsOpen = false
    },

    resetNewSpecies(state) {
      state.emptyPlant = $.extend(true, {}, emptySpecies)
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

    savePlant (context, plant) {
      api.postResource('plants', plant).then(function (resp) {
        context.commit('setPlant', plant)
        context.dispatch('listPlants')
      })
    },

    listPlants (context) {
      api.listResource('plants').then( function (resp) {
        context.commit('setPlantList', resp.data)
      })
    },

    listImages (context) {
      api.listResource('images').then( function (resp) {
        context.commit('setImageList', resp.data)
      })
    },

    getImage (context, id) {
      context.commit('weWait')
      api.getResource('image', id).then( function (resp) {
        context.commit('setImage', resp.data)
        context.commit('weReady')
      })
    },

    updateImage (context, image) {
      api.putResource('image', image).then(function (resp) {
        console.log('Image updated in database.')
      })
    },

    getSamples (context, plant_code) {
      api.getResource('plantsample', plant_code).then( function (resp) {
        context.commit('setPlantSamples', resp.data)
      })
    },

    updatePlant (context, plant) {
      api.putResource('plant', plant).then (function (resp) {
        // DO STUFF?
        context.dispatch('listPlants')
      })
    },

    deletePlant (context, plant) {
      api.deleteResource('plant', plant).then (function (resp) {
        context.dispatch('listPlants')
        // Set current plant to empty plant.
        var empty = $.extend(true, {}, emptySpecies)
        context.commit('setPlant', empty)
        context.commit('setPlantName', 'Click Here to Set Plant Species')
      })
    }

  },

})



