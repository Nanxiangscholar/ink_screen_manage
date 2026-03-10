<template>
  <div class="esl-view">
    <el-card class="page-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="title-section">
            <el-icon :size="24" class="title-icon"><Monitor /></el-icon>
            <h2 class="page-title">电子标签管理</h2>
          </div>
          <el-button type="primary" @click="handleBindESL" class="add-btn" size="large">
            <el-icon><Link /></el-icon>
            <span>绑定标签</span>
          </el-button>
        </div>
      </template>
      
      <div class="search-section">
        <el-form :model="searchForm" class="search-form" inline>
          <el-form-item label="标签ID" class="search-item">
            <el-input v-model="searchForm.esl_id" placeholder="请输入标签ID" clearable size="large" />
          </el-form-item>
          <el-form-item label="SKU" class="search-item">
            <el-input v-model="searchForm.sku" placeholder="请输入SKU" clearable size="large" />
          </el-form-item>
          <el-form-item class="search-item">
            <el-button type="primary" @click="handleSearch" size="large">
              <el-icon><Search /></el-icon>
              <span>查询</span>
            </el-button>
            <el-button @click="resetForm" size="large">
              <el-icon><Refresh /></el-icon>
              <span>重置</span>
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="table-section">
        <el-table 
          :data="eslList" 
          style="width: 100%"
          :header-cell-style="headerCellStyle"
          :cell-style="cellStyle"
          stripe
          highlight-current-row
        >
          <el-table-column prop="esl_id" label="标签ID" min-width="200" />
          <el-table-column prop="sku" label="SKU" min-width="180" />
          <el-table-column prop="store_code" label="产线" min-width="120" />
          <el-table-column prop="position" label="位置" min-width="80" />
          <el-table-column prop="create_time" label="绑定时间" min-width="180" />
          <el-table-column label="操作" width="260" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleUnbindESL(scope.row)" plain>
                <el-icon><Link /></el-icon>
                <span>解绑</span>
              </el-button>
              <el-button type="info" size="small" @click="handleRefreshESL(scope.row)" plain>
                <el-icon><Refresh /></el-icon>
                <span>刷新</span>
              </el-button>
              <el-button type="success" size="small" @click="handleCheckStatus(scope.row)" plain>
                <el-icon><Check /></el-icon>
                <span>状态</span>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
        />
      </div>
    </el-card>
    
    <!-- 绑定标签对话框 -->
    <el-dialog
      v-model="bindDialogVisible"
      title="绑定标签"
      width="600px"
    >
      <el-form :model="bindForm" :rules="bindRules" ref="bindFormRef" label-width="100px">
        <el-form-item label="标签ID" prop="esl_id">
          <el-input v-model="bindForm.esl_id" placeholder="请输入标签ID" />
        </el-form-item>
        <el-form-item label="SKU" prop="sku">
          <el-input v-model="bindForm.sku" placeholder="请输入SKU" />
        </el-form-item>
        <el-form-item label="产线" prop="store_code">
          <el-select v-model="bindForm.store_code" placeholder="请选择产线">
            <el-option label="拉丝" value="lasiqu" />
            <el-option label="成型" value="chengxing" />
            <el-option label="站台" value="zhantai" />
            <el-option label="化工" value="huagong" />
          </el-select>
        </el-form-item>
        <el-form-item label="位置" prop="position">
          <el-input-number v-model="bindForm.position" :min="1" :max="10" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="bindDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveBind">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Monitor, Link, Search, Refresh, Check } from '@element-plus/icons-vue'
import axios from '../utils/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

// 表格样式
const headerCellStyle = () => {
  return {
    backgroundColor: '#f5f7fa',
    color: '#303133',
    fontWeight: '600',
    fontSize: '14px'
  }
}

const cellStyle = () => {
  return {
    fontSize: '14px',
    padding: '12px 0'
  }
}

const searchForm = ref({
  esl_id: '',
  sku: ''
})

const eslList = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const bindDialogVisible = ref(false)
const bindForm = ref({
  esl_id: '',
  sku: '',
  store_code: '',
  position: 5
})
const bindFormRef = ref(null)

const bindRules = {
  esl_id: [{ required: true, message: '请输入标签ID', trigger: 'blur' }],
  sku: [{ required: true, message: '请输入SKU', trigger: 'blur' }],
  store_code: [{ required: true, message: '请选择产线', trigger: 'blur' }],
  position: [{ required: true, message: '请输入位置', trigger: 'blur' }]
}

const getESLList = async () => {
  try {
    const response = await axios.get('/api/esl/goods', {
      params: {
        esl_id: searchForm.value.esl_id,
        sku: searchForm.value.sku
      }
    })
    // 后端返回格式: { success: true, data: [...], message: "..." }
    // axios 拦截器已提取 response.data，所以直接用 response.data
    const eslData = response.data || []
    eslList.value = eslData.map(item => ({
      esl_id: item.esl_id,
      sku: item.sku,
      store_code: item.store_code,
      position: item.position,
      create_time: item.create_time
    }))
    total.value = eslList.value.length
  } catch (error) {
    console.error('获取电子标签列表失败:', error)
    ElMessage.error('获取电子标签列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  getESLList()
}

const resetForm = () => {
  searchForm.value = {
    esl_id: '',
    sku: ''
  }
  currentPage.value = 1
  getESLList()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  getESLList()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getESLList()
}

const handleBindESL = () => {
  bindForm.value = {
    esl_id: '',
    sku: '',
    store_code: '',
    position: 5
  }
  bindDialogVisible.value = true
}

const handleSaveBind = async () => {
  if (!bindFormRef.value) return

  try {
    await bindFormRef.value.validate()

    const response = await axios.post('/api/esl/bind', {
      esl_id: bindForm.value.esl_id,
      sku: bindForm.value.sku
    })

    // 后端返回: { success: true, data: {...}, message: "..." }
    if (response.success === true) {
      ElMessage.success(response.message || '绑定成功')
      bindDialogVisible.value = false
      getESLList()
    } else {
      ElMessage.error(response.message || '绑定失败')
    }
  } catch (error) {
    console.error('绑定标签失败:', error)
    ElMessage.error('绑定失败，请检查输入信息')
  }
}

const handleUnbindESL = (row) => {
  ElMessageBox.confirm(
    '确定要解绑这个标签吗？',
    '解绑确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await axios.post('/api/esl/unbind', {
        esl_id: row.esl_id,
        sku: row.sku
      })
      // 后端返回: { success: true, data: {...}, message: "..." }
      if (response.success === true) {
        ElMessage.success(response.message || '解绑成功')
        getESLList()
      } else {
        ElMessage.error(response.message || '解绑失败')
      }
    } catch (error) {
      console.error('解绑标签失败:', error)
      ElMessage.error('解绑失败')
    }
  }).catch(() => {
    // 取消解绑
  })
}

const handleRefreshESL = async (row) => {
  try {
    const response = await axios.post('/api/esl/refresh', {
      esl_id: row.esl_id
    })
    // 后端返回: { success: true, data: {...}, message: "..." }
    if (response.success === true) {
      ElMessage.success(response.message || '刷新成功')
    } else {
      ElMessage.error(response.message || '刷新失败')
    }
  } catch (error) {
    console.error('刷新标签失败:', error)
    ElMessage.error('刷新失败')
  }
}

const handleCheckStatus = async (row) => {
  try {
    const response = await axios.get(`/api/esl/status/${row.esl_id}`)
    // 后端返回: { success: true, data: { status: '...' }, message: "..." }
    if (response.success === true) {
      const status = response.data?.status
      ElMessage.success(`标签状态: ${status === 'online' ? '在线' : '离线'}`)
    } else {
      ElMessage.error(response.message || '获取状态失败')
    }
  } catch (error) {
    console.error('检查标签状态失败:', error)
    ElMessage.error('检查状态失败')
  }
}

onMounted(() => {
  getESLList()
})
</script>

<style scoped>
.esl-view {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-card {
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  color: #409eff;
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.search-section {
  background-color: #fafafa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: flex-end;
}

.search-item {
  margin-bottom: 0;
}

.search-item :deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

.table-section {
  margin-bottom: 24px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}

/* 对话框样式 */
:deep(.el-dialog__header) {
  border-bottom: 1px solid #ebeef5;
  padding: 20px 24px;
  margin-right: 0;
}

:deep(.el-dialog__title) {
  font-weight: 600;
  font-size: 18px;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  border-top: 1px solid #ebeef5;
  padding: 16px 24px;
}
</style>
