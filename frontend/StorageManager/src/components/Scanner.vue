<template>
  <StreamBarcodeReader @decode="onDecode" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'
import StreamBarcodeReader from "../../node_modules/vue-barcode-reader/src/components/StreamBarcodeReader.vue";
export default defineComponent({
  components: {
    StreamBarcodeReader,
  },
  name: 'Scanner',
  props: {
  },
  beforeUnmount() {
    this.disableCamera()
  },
  data () {
    return {
    }
  },
  computed: mapState([
    'scanningMode',
  ]),
  methods: {
    disableCamera () {
      const video = document.querySelector('video');
      if (video != null) {
        const mediaStream = video.srcObject;
        if (mediaStream != null) {
          // @ts-ignore: Property 'getTracks' does not exist on type 'MediaProvider'.
          const tracks = mediaStream.getTracks();
          tracks[0].stop();
        }
      }
    },
    onDecode (result: any) {
      this.$store.commit('updateScannedResult', result)
      switch ( this.scanningMode ) {
        case 'add':
          this.$router.push('/additem')
          break;
        default:
          this.$router.push('/')
          break;
      }
    },
  }
})
</script>

<style scoped>

</style>
