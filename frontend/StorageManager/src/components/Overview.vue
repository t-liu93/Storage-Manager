<template>
  <h1>物品概览</h1>
  <div class='slot'>
    <n-data-table
      :columns="columns"
      :data="data"
      :pagination="pagination"
      :single-line="false"
      @update:filters="handleFiltersChange"
    />
  </div>
  <div class='mainButton'>
    <n-space>
      <n-button type="info" @click="back">返回</n-button>
    </n-space>
  </div>
</template>

<script lang="ts">
import { defineComponent, h } from 'vue'
import { mapState } from 'vuex'
import { NButton, NSpace } from 'naive-ui'
import { useMessage } from 'naive-ui'
import { NDataTable, NTag } from 'naive-ui'
import ax from 'axios'

const tagColumn = {
  title: '类别',
  key: 'category',
  filterMultiple: true,
  filterOptionValue: null,
  filterOptions: [],
  filter (value: any, row: any) {
    return ~row.category.indexOf(value)
  },
  // @ts-ignore: 'render' implicitly has return type 'any' because it does not have a return type annotation and is referenced directly or indirectly in one of its return expressions.
  render (row: any) {
    const tags = row.category.map((tagKey: string) => {
      return h(
        NTag,
        {
          style: {
            // marginRight: '6px'
          },
          type: 'info'
        },
        {
          default: () => tagKey
        }
      )
    })
    return tags
  }
}

export default defineComponent({
  components: {
    NButton,
    NSpace,
    NDataTable,
    NTag
  },
  name: 'Overview',
  props: {

  },
  mounted () {
    this.retrieveAll()
  },
  setup () {
    const message = useMessage()
    return  {
    }
  },
  data () {
    return {
      columns: [
        {
          title: '名称',
          key: 'name',
        },
        {
          title: '总数量',
          key: 'amount'
        },
        tagColumn,
        {
          title: '详细信息',
          key: 'detail',
          // @ts-ignore: 'render' implicitly has return type 'any' because it does not have a return type annotation and is referenced directly or indirectly in one of its return expressions.
          render (row: any) {
            return h(
              NButton,
              {
                size: 'small',
                onClick: () => {
                  console.log(row.uuid)
                }
              },
              { default: () => '详细信息' }
            )
          }
        },
      ],
      pagination: {
        pagSize: 10
      },
      data: [],
      filterOptions: [],
      tagColumn,
    }
  },
  computed: mapState([
  ]),
  methods: {
    back() {
      this.$router.go(-1)
    },
    retrieveAll() {
      ax.post(document.location.origin + '/get', {
        type: 'allitem',
        body: ''
      })
      .then(response => {
        this.data = response.data;
      })
      ax.post(document.location.origin + '/get', {
        type: 'category',
        body: ''
      })
      .then(response => {
        for (let i = 0; i < response.data.length; i++) {
          this.tagColumn.filterOptions.push({
            // @ts-ignore: Type 'any' is not assignable to type 'never'.
            label: response.data[i].name,
            // @ts-ignore: Type 'any' is not assignable to type 'never'.
            value: response.data[i].name
          })
        }
      })
    },
    handleFiltersChange(filters: any, sourceColumn: any) {
      this.tagColumn.filterOptionValue = filters[sourceColumn.key]
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
