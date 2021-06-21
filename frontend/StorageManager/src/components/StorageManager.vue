<template>
  <h1>一个库管</h1>
  <div class='mainButton'>
    <n-space>
      <n-button type="info" @click="onScanningClick('lookup')">查询</n-button>
      <n-button type="primary" @click="onScanningClick('add')">添加</n-button>
      <n-button type="warning" @click="onScanningClick('modify')">改动</n-button>
      <n-button type="error" @click="onScanningClick('delete')">删除</n-button>
    </n-space>
  </div>
  <div v-if="isScanned" class="result">
    Result: {{scannedResult + scanningMode}}
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
  ]),
  methods: {
    preventNav(event: any) {
      if (!this.isEditing) return
      event.preventDefault()
      event.returnValue = ""
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
