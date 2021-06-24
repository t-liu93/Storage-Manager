<template>
  <h1>详细信息</h1>
  <div class='slot'>
  </div>
  <div class='mainButton'>
    <n-space>
      <n-button type="info" @click="back">返回</n-button>
    </n-space>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'
import { useMessage } from 'naive-ui'
import { NButton, NSpace } from 'naive-ui'
import ax from 'axios'

export default defineComponent({
  components: {
    NButton,
    NSpace,
  },
  name: 'ItemDetail',
  props: {
    uuid: String
  },
  mounted () {
    console.log(this.uuid)
  },
  setup () {
    const message = useMessage()
    return  {
    }
  },
  data () {
    const router = this.$router
    return {

    }
  },
  computed: mapState([
  ]),
  methods: {
    back() {
      this.$router.go(-1)
    },
  }
})
</script>

<style scoped>
.mainButton {
  display: flex;
  justify-content: center;
}
.slots {
  display: flex;
  justify-content: center;
  margin-right: 10%;
}
</style>
