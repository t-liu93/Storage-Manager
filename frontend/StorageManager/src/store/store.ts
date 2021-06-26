import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'


// Create a new store instance.
const store = createStore({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state() {
    return {
      scanning: {
        scannedResult: '',
        scanningMode: '',
      },
      detailUuid: '',
    }
  },
  mutations: {
    updateScannedResult(state: any, barcode: string) {
      state.scannedResult = barcode
    },
    updateScanningMode(state: any, scanningMode: string) {
      state.scanningMode = scanningMode
    },
    updateDetailUuid(state: any, uuid: string) {
      state.detailUuid = uuid
    }
  }
})

export default store