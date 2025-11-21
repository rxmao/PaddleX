<template>
  <div class="customer-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>客户列表</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>新增客户
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="搜索公司名称/联系人/电话"
          clearable
          style="width: 300px;"
          @clear="handleSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>

        <el-select
          v-model="searchForm.taxpayer_type"
          placeholder="纳税人类型"
          clearable
          style="width: 150px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option label="一般纳税人" value="general" />
          <el-option label="小规模纳税人" value="small" />
        </el-select>

        <el-select
          v-model="searchForm.status"
          placeholder="状态"
          clearable
          style="width: 120px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option label="正常" value="1" />
          <el-option label="停用" value="0" />
        </el-select>
      </div>

      <el-table :data="tableData" border style="margin-top: 20px;" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="company_name" label="公司名称" min-width="200" />
        <el-table-column prop="taxpayer_type_text" label="纳税人类型" width="120" />
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="salesman_name" label="业务员" width="100" />
        <el-table-column prop="accountant_name" label="会计" width="100" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '正常' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.per_page"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="loadData"
        @size-change="loadData"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import { getCustomerList, deleteCustomer } from '@/api/customer'

const loading = ref(false)
const tableData = ref([])

const searchForm = reactive({
  keyword: '',
  taxpayer_type: '',
  status: ''
})

const pagination = reactive({
  page: 1,
  per_page: 20,
  total: 0
})

const loadData = async () => {
  loading.value = true
  try {
    const res = await getCustomerList({
      page: pagination.page,
      per_page: pagination.per_page,
      ...searchForm
    })

    tableData.value = res.data.items
    pagination.total = res.data.total
  } catch (error) {
    console.error('加载客户列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadData()
}

const handleAdd = () => {
  ElMessage.info('新增客户功能开发中')
}

const handleEdit = (row) => {
  ElMessage.info(`编辑客户：${row.company_name}`)
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除客户"${row.company_name}"吗？`, '提示', {
      type: 'warning'
    })

    await deleteCustomer(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    // 用户取消操作
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.customer-list {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-bar {
  display: flex;
  align-items: center;
}
</style>
