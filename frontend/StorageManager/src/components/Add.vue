<template>
  <h1>添加物品</h1>
  <div class='mainButton'>
    <n-button type="info" @click="backToHome">返回首页</n-button>
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
  name: 'AddComponent',
  props: {

  },
  data () {
    return {
    }
  },
  methods: {
    backToHome() {
      this.$router.push('/')
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
