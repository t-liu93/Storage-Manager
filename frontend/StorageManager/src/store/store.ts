import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'


// Create a new store instance.
const store = createStore({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state() {
    return {
      scannedResult: '',
      isScanned: false,
      isScanning: false,
      scanningMode: '',
      isEditing: false,
    }
  },
  mutations: {
    updateScannedResult(state: any, barcode: string) {
      state.scannedResult = barcode
    },
    updateIsScanned(state: any, isScanned: boolean) {
      state.isScanned = isScanned
    },
    updateIsScanning(state: any, isScanning: boolean) {
      state.isScanning = isScanning
    },
    updateScanningMode(state: any, scanningMode: string) {
      state.scanningMode = scanningMode
    },
    updateIsEditing(state: any, isEditing: boolean) {
      state.isEditing = isEditing
    }
  }
})

export default store