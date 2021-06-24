<template>
  <h1>详细信息</h1>
  <div class='slots'>
    <n-form
      :model="formValue"
      :rules="rules"
    >
      <n-form-item label="条码" path="uuid">
        <n-input :disabled="true" :placeholder=uuid />
      </n-form-item>
      <n-form-item label="名称" path="name">
        <n-input placeholder="这是一个物品" v-model:value="formValue.name"/>
      </n-form-item>
      <n-form-item label="数量" path="amount">
        <n-space>
          <n-input-number placeholder="数量" v-model:value="formValue.amount"/>
        </n-space>
      </n-form-item>
      <n-form-item label="类别" path="category">
        <n-space>
          <n-tree-select multiple checkable :options="categoryChoices" v-model:value="formValue.category" style="min-width:150px"/>
        </n-space>
      </n-form-item>
      <n-form-item label="备注" path="comments">
        <n-input type="textarea" placeholder="写点备注吧" v-model:value="formValue.comments"/>
      </n-form-item>
    </n-form>
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
import { defineComponent, ref } from 'vue'
import { mapState } from 'vuex'
import { useMessage } from 'naive-ui'
import { NButton, NSpace, NPopconfirm, NForm, NFormItem, NTable, NInput, NInputNumber, NTreeSelect } from 'naive-ui'
import ax from 'axios'
import ServerResult from '../backendDatatype'

export default defineComponent({
  components: {
    NButton,
    NSpace,
    NPopconfirm,
    NForm,
    NTable,
    NInput,
    NFormItem,
    NInputNumber,
    NTreeSelect
  },
  name: 'ItemDetail',
  props: {
    uuid: String
  },
  mounted () {
    this.getExistingItem()
  },
  setup () {
    const message = useMessage()
    return  {
      formValue: ref({
        name: '',
        amount: 1,
        category: [],
        comments: ''
      }),
      rules: {
        uuid: {
          required: true
        },
        name: {
          required: true
        },
        amount: {
          required: true
        },
        comments: {
          required: false
        }
      },
      success () {
        message.success("删除成功")
      },
    }
  },
  data () {
    const router = this.$router
    return {
      categoryChoices: [],
      expireDates: [],
      lastModified: '',
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
    getExistingItem() {
      ax.post(document.location.origin + '/get', {
        type: 'item',
        body: {
          uuid: this.uuid
        }
      })
      .then(response => {
        if (response.data != null) {
          this.formValue.amount = response.data.amount;
          this.formValue.name = response.data.name;
          // @ts-ignore: Parameter 'o' implicitly has an 'any' type.
          if (response.data.expireDate.some(o => o.date == '2099-12-31')) {
            // this.noExpire = true
          }
          for (let i = 0; i < response.data.category.length; i++) {
            var catDict = {'key': response.data.category[i], 'label': response.data.category[i]}
            // @ts-ignore: Argument of type 'any' is not assignable to parameter of type 'never'.
            this.categoryChoices.push(catDict)
            // @ts-ignore: Argument of type 'any' is not assignable to parameter of type 'never'.
            this.formValue.category.push(response.data.category[i])
          }
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
