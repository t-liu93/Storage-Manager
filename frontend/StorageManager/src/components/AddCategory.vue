<template>
  <h1>添加类别</h1>
  <div class='slots'>
    <n-form
      :model="formValue"
      :rules="rules"
    >
      <n-form-item label="类别" path="name">
        <n-input placeholder="这是一个类别" v-model:value="formValue.name"/>
      </n-form-item>
      <n-form-item label="简介" path="description">
        <n-input placeholder="这是类别的简介" v-model:value="formValue.description"/>
      </n-form-item>
    </n-form>
  </div>
  <div class='mainButton'>
    <n-space>
      <n-button type="primary" @click="submit">添加</n-button>
      <n-button type="info" @click="back">返回</n-button>
    </n-space>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { mapState } from 'vuex'
import { NButton, NSpace } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { NForm, NFormItem, NInput } from 'naive-ui'
import ServerResult from '../backendDatatype'
import ax from 'axios'
export default defineComponent({
  components: {
    NButton,
    NSpace,
    NForm,
    NFormItem,
    NInput,
  },
  name: 'AddCategory',
  props: {

  },
  mounted () {
  },
  setup () {
    const message = useMessage()
    return  {
      formValue: ref({
        name: '',
        description: '',
      }),
      rules: {
        name: {
          required: true
        },
        description: {

        }
      },
      success () {
        message.success("提交成功")
      },
      error (error: string) {
        message.error("提交失败！" + error)
      }
    }
  },
  data () {
    return {
      noExpire: false,
      categories: [],
    }
  },
  computed: mapState([
  ]),
  methods: {
    back() {
      this.$router.go(-1)
    },
    submit() {
      ax.post(document.location.origin + '/set', {
        type: 'category',
        body: {
          name: this.formValue.name,
          description: this.formValue.description,
        }
      })
      .then(response => {
        let serverResult = response.data[0]
        if (serverResult === ServerResult.OK) {
          this.success()
        } else if (serverResult === ServerResult.DB_DUPLICATE_ENTRY){
          this.error('类别已存在，请重新输入。')
        } else if (serverResult === ServerResult.RESULTS_UNKNOWN) {
          this.error('未知错误。')
        }
      })
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
}
</style>
