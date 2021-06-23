<template>
  <!-- <StorageManager msg="一个库管" /> -->
  <n-message-provider>
    <router-view />
  </n-message-provider>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { NMessageProvider } from 'naive-ui'

export default defineComponent({
  name: 'App',
  components: {
    NMessageProvider
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
