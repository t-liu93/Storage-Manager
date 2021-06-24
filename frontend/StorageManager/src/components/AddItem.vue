<template>
  <h1>添加物品</h1>
  <div class='slots'>
    <n-form
      :model="formValue"
      :rules="rules"
    >
      <n-form-item label="条码" path="uuid">
        <n-input :disabled="true" :placeholder=scannedResult />
      </n-form-item>
      <n-form-item label="名称" path="name">
        <n-input placeholder="这是一个物品" v-model:value="formValue.name"/>
      </n-form-item>
      <n-form-item label="数量" path="amount">
        <n-space>
          <n-input-number placeholder="数量" v-model:value="formValue.amount"/>
          <p>现有数量: {{existingAmount}}</p>
        </n-space>
      </n-form-item>
      <n-form-item label="类别" path="checked">
        <n-space>
          <n-tree-select multiple checkable :options="categories" v-model:value="formValue.checked" style="min-width:150px"/>
          <n-button text @click="addCategory">没有合适的类别？点这里添加</n-button>
        </n-space>
      </n-form-item>
      <n-form-item label="保质期" path="expire">
        <n-space>
          <n-date-picker placeholder="2000-01-01" v-model:value="formValue.expire" type="date" :disabled="noExpire"/>
          <n-switch v-model:value="noExpire" />
        </n-space>
      </n-form-item>
    </n-form>
  </div>
  <div class='mainButton'>
    <n-space>
      <n-button type="primary" @click="submit">提交</n-button>
      <n-button type="info" @click="backToHome">返回首页</n-button>
    </n-space>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { mapState } from 'vuex'
import { NButton, NSpace, NSwitch } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { NForm, NFormItem, NInput, NInputNumber, NDatePicker } from 'naive-ui'
// @ts-ignore: Module '"naive-ui"' has no exported member 'NTreeSelect'.
import { NTreeSelect } from 'naive-ui'
import Scanner from './Scanner.vue';
import ServerResult from '../backendDatatype'
import ax from 'axios'
export default defineComponent({
  components: {
    Scanner,
    NButton,
    NSpace,
    NForm,
    NFormItem,
    NInput,
    NInputNumber,
    NDatePicker,
    NSwitch,
    NTreeSelect,
  },
  name: 'AddItemComponent',
  props: {

  },
  mounted () {
    this.getCategory()
    this.getExistingItem()
  },
  setup () {
    const message = useMessage()
    return  {
      formValue: ref({
        name: '',
        amount: 1,
        expire: Date.now(),
        checked: [],
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
        }
      },
      success () {
        message.success("提交成功")
      },
      error () {
        message.error("提交失败")
      }
    }
  },
  data () {
    return {
      noExpire: false,
      categories: [],
      existingAmount: 0,
    }
  },
  computed: mapState([
    'scannedResult',
    'date',
    'isEditing',
  ]),
  methods: {
    backToHome() {
      this.$router.push('/')
    },
    addCategory() {
      this.$router.push('/addcategory')
    },
    getCategory() {
      ax.post(document.location.origin + '/get', {
        type: 'category',
        body: ''
      })
      .then(response => {
        var categories = []
        categories = response.data
        this.buildCategoriesChoice(categories)
      })
    },
    buildCategoriesChoice(categories: [any]) {
      for (let i = 0; i < categories.length; i++) {
        var catDict = {'key' : categories[i].name, 'label' : categories[i].name}
        // @ts-ignore: Argument of type '{ key: any; label: any; }' is not assignable to parameter of type 'never'.
        this.categories.push(catDict)
      }
    },
    getExistingItem() {
      ax.post(document.location.origin + '/get', {
        type: 'item',
        body: {
          uuid: this.scannedResult
        }
      })
      .then(response => {
        if (response.data != null) {
          this.existingAmount = response.data.amount;
          this.formValue.name = response.data.name;
          if (response.data.expireDate === '2099-12-31') {
            this.noExpire = true
          }
          for (let i = 0; i < response.data.category.length; i++) {
            // @ts-ignore: Argument of type 'any' is not assignable to parameter of type 'never'.
            this.formValue.checked.push(response.data.category[i])
          }
        }
      })
    },
    submit() {
      var categories: string[];
      categories = [];
      for (let i = 0; i < this.formValue.checked.length; i++) {
        categories.push(this.formValue.checked[i])
      }
      var date = new Date(this.formValue.expire)
      let expireDate = (this.noExpire) ? '2099-12-31' : date.getFullYear() + '-' + (date.getMonth()+1) + '-' + date.getDate()
      ax.post(document.location.origin + '/set', {
        type: 'item',
        body: {
          uuid: this.scannedResult,
          name: this.formValue.name,
          amount: this.formValue.amount,
          category: categories,
          expireDate: [{
            date: expireDate,
            amount: this.formValue.amount,
          }],
          lastModifiedDate: ''
        }
      })
      .then(response => {
        let serverResult = response.data[0]
        if (serverResult === ServerResult.OK) {
          this.success()
          this.$router.push('/')
        } else if (serverResult === ServerResult.RESULTS_UNKNOWN) {
          this.error()
        }
      })
    },
  },
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
