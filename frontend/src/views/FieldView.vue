<template>
  <div class="field-view">
    <el-card class="page-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="title-section">
            <el-icon :size="24" class="title-icon"><Operation /></el-icon>
            <h2 class="page-title">字段管理</h2>
          </div>
          <el-button type="primary" @click="handleAddField" class="add-btn" size="large">
            <el-icon><Plus /></el-icon>
            <span>添加字段</span>
          </el-button>
        </div>
      </template>
      
      <div class="search-section">
        <el-form :model="searchForm" class="search-form" inline>
          <el-form-item label="字段名" class="search-item">
            <el-input v-model="searchForm.field_name" placeholder="请输入字段名" clearable size="large" />
          </el-form-item>
          <el-form-item label="模板类型" class="search-item">
            <el-select v-model="searchForm.promo_reason" placeholder="请选择模板类型" clearable size="large">
              <el-option label="拉丝" value="21" />
              <el-option label="成型" value="11" />
              <el-option label="小循环" value="2" />
              <el-option label="站台" value="1" />
              <el-option label="化工" value="3" />
            </el-select>
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
          :data="fields" 
          style="width: 100%"
          :header-cell-style="headerCellStyle"
          :cell-style="cellStyle"
          stripe
          highlight-current-row
        >
          <el-table-column prop="field_name" label="字段名" min-width="180" />
          <el-table-column prop="label" label="标签" min-width="180" />
          <el-table-column prop="promo_reason" label="模板类型" min-width="120" />
          <el-table-column prop="promo_reason_label" label="模板类型标签" min-width="150" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEditField(scope.row)" plain>
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button type="danger" size="small" @click="handleDeleteField(scope.row)" plain>
                <el-icon><Delete /></el-icon>
                <span>删除</span>
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
    
    <!-- 添加/编辑字段对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form :model="fieldForm" :rules="fieldRules" ref="fieldFormRef" label-width="120px">
        <el-form-item label="字段名" prop="field_name">
          <el-input v-model="fieldForm.field_name" placeholder="请输入字段名" />
        </el-form-item>
        <el-form-item label="标签" prop="label">
          <el-input v-model="fieldForm.label" placeholder="请输入标签" />
        </el-form-item>
        <el-form-item label="模板类型" prop="promo_reason">
          <el-select v-model="fieldForm.promo_reason" placeholder="请选择模板类型">
            <el-option label="拉丝" value="21" />
            <el-option label="成型" value="11" />
            <el-option label="小循环" value="2" />
            <el-option label="站台" value="1" />
            <el-option label="化工" value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="模板类型标签" prop="promo_reason_label">
          <el-input v-model="fieldForm.promo_reason_label" placeholder="请输入模板类型标签" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveField">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Operation, Plus, Search, Refresh, Edit, Delete } from '@element-plus/icons-vue'
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
  field_name: '',
  promo_reason: ''
})

const fields = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('添加字段')
const fieldForm = ref({})
const fieldFormRef = ref(null)

const fieldRules = {
  field_name: [{ required: true, message: '请输入字段名', trigger: 'blur' }],
  label: [{ required: true, message: '请输入标签', trigger: 'blur' }],
  promo_reason: [{ required: true, message: '请选择模板类型', trigger: 'blur' }],
  promo_reason_label: [{ required: true, message: '请输入模板类型标签', trigger: 'blur' }]
}

const getFields = async () => {
  try {
    const response = await axios.get('/api/fields', {
      params: {
        field_name: searchForm.value.field_name,
        promo_reason: searchForm.value.promo_reason,
        page: currentPage.value,
        page_size: pageSize.value
      }
    })
    // 后端返回格式: { success: true, data: [...], message: "..." }
    // axios 拦截器已提取 response.data
    const fieldsData = response.data || []
    fields.value = fieldsData
    total.value = fieldsData.length
  } catch (error) {
    console.error('获取字段列表失败:', error)
    ElMessage.error('获取字段列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  getFields()
}

const resetForm = () => {
  searchForm.value = {
    field_name: '',
    promo_reason: ''
  }
  currentPage.value = 1
  getFields()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  getFields()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getFields()
}

const handleAddField = () => {
  dialogTitle.value = '添加字段'
  fieldForm.value = {
    field_name: '',
    label: '',
    promo_reason: '',
    promo_reason_label: ''
  }
  dialogVisible.value = true
}

const handleEditField = (row) => {
  dialogTitle.value = '编辑字段'
  fieldForm.value = { ...row }
  dialogVisible.value = true
}

const handleSaveField = async () => {
  if (!fieldFormRef.value) return

  try {
    await fieldFormRef.value.validate()

    let response
    if (fieldForm.value.id) {
      // 编辑字段
      response = await axios.put(`/api/fields/${fieldForm.value.id}`, fieldForm.value)
    } else {
      // 添加字段
      response = await axios.post('/api/fields', fieldForm.value)
    }

    // 后端返回: { success: true, data: {...}, message: "..." }
    if (response.code === 200) {
      ElMessage.success(response.message || '操作成功')
      dialogVisible.value = false
      getFields()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('保存字段失败:', error)
    ElMessage.error('保存失败，请检查输入信息')
  }
}

const handleDeleteField = (row) => {
  ElMessageBox.confirm(
    '确定要删除这个字段吗？',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await axios.delete(`/api/fields/${row.id}`)
      // 后端返回: { success: true, data: {...}, message: "..." }
      if (response.code === 200) {
        ElMessage.success(response.message || '删除成功')
        getFields()
      } else {
        ElMessage.error(response.message || '删除失败')
      }
    } catch (error) {
      console.error('删除字段失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

onMounted(() => {
  getFields()
})
</script>

<style scoped>
.field-view {
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
