<template>
  <h1>详细信息</h1>
  <p>{{uuid}}</p>
  <div class='slot'>
  </div>
  <div class='mainButton'>
    <n-space>
      <n-popconfirm
        @positive-click="confirmDeletion"
        @negative-click="cancelDeletion"
        positive-text="确认删除"
        negative-text="取消">
        <template #trigger>
          <n-button type="error">删除此物品</n-button>
        </template>
        注意！此操作将从数据库中永久删除此物品，请确认。
      </n-popconfirm>
      <n-button type="info" @click="back">返回</n-button>
    </n-space>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'
import { useMessage } from 'naive-ui'
import { NButton, NSpace, NPopconfirm } from 'naive-ui'
import ax from 'axios'
import ServerResult from '../backendDatatype'

export default defineComponent({
  components: {
    NButton,
    NSpace,
    NPopconfirm,
  },
  name: 'ItemDetail',
  props: {
    uuid: String
  },
  mounted () {
  },
  setup () {
    const message = useMessage()
    return  {
      success () {
        message.success("删除成功")
      },
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
    confirmDeletion() {
      ax.post(document.location.origin + '/set', {
        type: 'deleteitem',
        body: {
          uuid: this.uuid
        }
      })
      .then(response => {
        let serverResult = response.data[0]
        if (serverResult === ServerResult.OK) {
          this.success()
          this.$router.go(-1)
        }
      })
    },
    cancelDeletion() {

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
