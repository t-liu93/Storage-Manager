<template>
  <h1>一个库管</h1>
  <div class='mainButton'>
    <n-space>
      <n-button type="info" @click="overview">概览</n-button>
      <n-button type="primary" @click="onScanningClick('add')">添加</n-button>
      <n-button type="warning" @click="onScanningClick('modify')">改动</n-button>
      <n-button type="error" @click="onScanningClick('delete')">删除</n-button>
    </n-space>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'
import { NButton, NSpace } from 'naive-ui'
import Scanner from './Scanner.vue';
export default defineComponent({
  components: {
    NButton,
    NSpace,
    Scanner,
  },
  name: 'StorageManager',
  props: {

  },
  data () {
    return {
    }
  },
  computed: mapState([
    'scannedResult',
    'isScanned',
    'isScanning',
    'scanningMode',
    'isEditing',
    'date'
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
    overview() {
      this.$router.push('/overview')
    },
    onScanningClick (mode: string) {
      this.$store.commit('updateScanningMode', mode)
      this.$store.commit('updateIsScanned', false)
      this.$store.commit('updateIsScanning', true)
      this.$store.commit('updateIsEditing', true)
      this.$router.push('/scan')
    }
  }
})
</script>

<style scoped>
.mainButton {
  display: flex;
  justify-content: center;
}
</style>
