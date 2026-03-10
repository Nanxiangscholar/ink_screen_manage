<template>
  <div class="register-container">
    <div class="register-background"></div>
    <el-card class="register-card">
      <template #header>
        <div class="register-header">
          <div class="logo-icon">
            <el-icon :size="40"><Monitor /></el-icon>
          </div>
          <h2>用户注册</h2>
          <p>请填写以下信息完成注册</p>
        </div>
      </template>
      <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="80px" class="register-form">
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名（3-20个字符）"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码（至少6个字符，包含字母和数字）"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        <el-form-item label="用户ID" prop="userId">
          <el-input
            v-model="registerForm.userId"
            placeholder="请输入用户ID"
            prefix-icon="UserFilled"
            size="large"
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="registerForm.role" placeholder="请选择角色" size="large" style="width: 100%">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item label="邀请码" prop="invitationCode">
          <el-input
            v-model="registerForm.invitationCode"
            placeholder="请输入邀请码"
            prefix-icon="Key"
            size="large"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            @click="handleRegister"
            class="register-button"
            size="large"
            :loading="loading"
          >
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
        <el-form-item>
          <el-button text @click="goToLogin" class="login-link">
            已有账号？立即登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Monitor, User, Lock, UserFilled, Key } from '@element-plus/icons-vue'
import axios from '../utils/axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)
const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
  userId: '',
  role: 'user',
  invitationCode: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.value.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少需要 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  userId: [
    { required: true, message: '请输入用户ID', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  invitationCode: [
    { required: true, message: '请输入邀请码', trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    await registerFormRef.value.validate()

    loading.value = true

    // 调用注册 API
    const response = await axios.post('/api/auth/register', {
      username: registerForm.value.username,
      password: registerForm.value.password,
      role: registerForm.value.role,
      user_id: registerForm.value.userId,
      invitation_code: registerForm.value.invitationCode
    })

    if (response.success === true) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } else {
      ElMessage.error(response.message)
    }
  } catch (error) {
    console.error('注册失败:', error)
    ElMessage.error(error.response?.data?.message || '注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

.register-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 0;
}

.register-card {
  width: 450px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  z-index: 1;
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-header {
  text-align: center;
  margin-bottom: 20px;
}

.logo-icon {
  margin-bottom: 15px;
  color: #409eff;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-header h2 {
  color: #303133;
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: 600;
}

.register-header p {
  color: #909399;
  font-size: 14px;
  margin: 0;
}

.register-form {
  padding: 20px 0;
}

.register-button {
  width: 100%;
  height: 42px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.register-button:active {
  transform: translateY(0);
}

.login-link {
  width: 100%;
  text-align: center;
  color: #409eff;
}

.login-link:hover {
  color: #66b1ff;
}
</style>