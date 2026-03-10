<template>
  <div class="product-view">
    <el-card class="page-card" shadow="never">
      <template #header>
        <div class="card-header">
          <div class="title-section">
            <el-icon :size="24" class="title-icon"><Goods /></el-icon>
            <h2 class="page-title">产品管理</h2>
          </div>
          <el-button type="primary" @click="handleAddProduct" class="add-btn" size="large">
            <el-icon><Plus /></el-icon>
            <span>添加产品</span>
          </el-button>
        </div>
      </template>
      
      <div class="search-section">
        <el-form :model="searchForm" class="search-form" inline>
          <el-form-item label="产线" class="search-item">
            <el-select v-model="searchForm.store_code" placeholder="请选择产线" clearable size="large">
              <el-option label="拉丝" value="lasiqu" />
              <el-option label="成型" value="chengxing" />
              <el-option label="站台" value="zhantai" />
              <el-option label="化工" value="huagong" />
            </el-select>
          </el-form-item>
          <el-form-item label="模板类型" class="search-item">
            <el-select v-model="searchForm.template_type" placeholder="请选择模板类型" clearable size="large">
              <el-option label="拉丝" value="拉丝" />
              <el-option label="成型" value="成型" />
              <el-option label="小循环" value="小循环" />
              <el-option label="站台" value="站台" />
              <el-option label="化工" value="化工" />
            </el-select>
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
          :data="products" 
          style="width: 100%"
          :header-cell-style="headerCellStyle"
          :cell-style="cellStyle"
          stripe
          highlight-current-row
        >
          <el-table-column prop="sku" label="SKU" min-width="180" />
          <el-table-column prop="store_code" label="产线" min-width="120" />
          <el-table-column prop="item_name" label="产品名称" min-width="200" />
          <el-table-column prop="brand" label="品牌" min-width="120" />
          <el-table-column prop="promo_reason" label="模板类型" min-width="120" />
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="scope">
              <el-button type="primary" size="small" @click="handleEditProduct(scope.row)" plain>
                <el-icon><Edit /></el-icon>
                <span>编辑</span>
              </el-button>
              <el-button type="danger" size="small" @click="handleDeleteProduct(scope.row)" plain>
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
    
    <!-- 添加/编辑产品对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
    >
      <el-form :model="productForm" :rules="productRules" ref="productFormRef" label-width="120px">
        <el-form-item label="SKU" prop="sku">
          <el-input v-model="productForm.sku" placeholder="请输入SKU" />
        </el-form-item>
        <el-form-item label="产线" prop="store_code">
          <el-select v-model="productForm.store_code" placeholder="请选择产线">
            <el-option label="拉丝" value="lasiqu" />
            <el-option label="成型" value="chengxing" />
            <el-option label="站台" value="zhantai" />
            <el-option label="化工" value="huagong" />
          </el-select>
        </el-form-item>
        <el-form-item label="产品名称" prop="item_name">
          <el-input v-model="productForm.item_name" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="品牌" prop="brand">
          <el-input v-model="productForm.brand" placeholder="请输入品牌" />
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="productForm.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="模板类型" prop="promo_reason">
          <el-select v-model="productForm.promo_reason" placeholder="请选择模板类型">
            <el-option label="拉丝" value="21" />
            <el-option label="成型" value="11" />
            <el-option label="小循环" value="2" />
            <el-option label="站台" value="1" />
            <el-option label="化工" value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveProduct">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Goods, Plus, Search, Refresh, Edit, Delete } from '@element-plus/icons-vue'
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
  store_code: '',
  template_type: '',
  sku: ''
})

const products = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const dialogVisible = ref(false)
const dialogTitle = ref('添加产品')
const productForm = ref({})
const productFormRef = ref(null)

const productRules = {
  sku: [{ required: true, message: '请输入SKU', trigger: 'blur' }],
  store_code: [{ required: true, message: '请选择产线', trigger: 'blur' }],
  item_name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }],
  brand: [{ required: true, message: '请输入品牌', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  promo_reason: [{ required: true, message: '请选择模板类型', trigger: 'blur' }]
}

const getProducts = async () => {
  if (!searchForm.value.store_code) {
    // 清空产品列表
    products.value = []
    total.value = 0
    return
  }

  try {
    const response = await axios.get('/api/product/products', {
      params: {
        store_code: searchForm.value.store_code,
        template_type: searchForm.value.template_type
      }
    })
    // 后端返回格式: { success: true, data: [...], message: "..." }
    // axios 拦截器已提取 response.data，所以直接用 response.data
    const productList = response.data || []
    products.value = productList.map(item => ({
      sku: item.sku,
      store_code: item.store_code,
      item_name: item.item_name || '',
      brand: item.brand || '',
      promo_reason: item.promo_reason || '',
      unit: item.unit || ''
    }))
    total.value = products.value.length
  } catch (error) {
    console.error('获取产品列表失败:', error)
    ElMessage.error('获取产品列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  getProducts()
}

const resetForm = () => {
  searchForm.value = {
    store_code: '',
    template_type: '',
    sku: ''
  }
  currentPage.value = 1
  getProducts()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  getProducts()
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  getProducts()
}

const handleAddProduct = () => {
  dialogTitle.value = '添加产品'
  productForm.value = {
    sku: '',
    store_code: '',
    item_name: '',
    brand: '',
    unit: '',
    promo_reason: ''
  }
  dialogVisible.value = true
}

const handleEditProduct = (row) => {
  dialogTitle.value = '编辑产品'
  productForm.value = { ...row }
  dialogVisible.value = true
}

const handleSaveProduct = async () => {
  if (!productFormRef.value) return
  
  try {
    await productFormRef.value.validate()
    
    const response = await axios.post('/api/product/save', productForm.value)

    if (response.code === 200) {
      ElMessage.success(response.message || '操作成功')
      dialogVisible.value = false
      getProducts()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error) {
    console.error('保存产品失败:', error)
    ElMessage.error('保存失败，请检查输入信息')
  }
}

const handleDeleteProduct = (row) => {
  ElMessageBox.confirm(
    '确定要删除这个产品吗？',
    '删除确认',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      const response = await axios.post('/api/product/delete', {
        sku: row.sku,
        store_code: row.store_code
      })
      if (response.code === 200) {
        ElMessage.success(response.message || '删除成功')
        getProducts()
      } else {
        ElMessage.error(response.message || '删除失败')
      }
    } catch (error) {
      console.error('删除产品失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {
    // 取消删除
  })
}

onMounted(() => {
  getProducts()
})
</script>

<style scoped>
.product-view {
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
