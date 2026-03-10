<template>
  <div class="home">
    <el-container>
      <el-header height="64px" class="header">
        <div class="logo">
          <el-icon :size="28" class="logo-icon"><Monitor /></el-icon>
          <span class="logo-text">水墨屏数据管理系统</span>
        </div>
        <div class="user-info">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-dropdown">
              <el-avatar :size="36" class="user-avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="username">{{ userInfo.username }}</span>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  <span>退出登录</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-container>
        <el-aside width="220px" class="aside">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            @select="handleMenuSelect"
            :router="true"
          >
            <el-menu-item index="/product">
              <el-icon><Goods /></el-icon>
              <span>产品管理</span>
            </el-menu-item>
            <el-menu-item index="/esl">
              <el-icon><Monitor /></el-icon>
              <span>电子标签</span>
            </el-menu-item>
            <el-menu-item index="/field">
              <el-icon><Operation /></el-icon>
              <span>字段管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" :key="$route.path" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Goods, Monitor, Operation, User, ArrowDown, SwitchButton } from '@element-plus/icons-vue'
import axios from '../utils/axios'

const router = useRouter()
const route = useRoute()
const userInfo = ref({ username: '管理员' })
const activeMenu = ref('/product')

// 监听路由变化
const updateActiveMenu = () => {
  activeMenu.value = route.path
}

const handleCommand = (command) => {
  if (command === 'logout') {
    logout()
  }
}

const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  updateActiveMenu()

  // 检查是否登录
  const user = localStorage.getItem('user')
  if (!user) {
    router.push('/login')
  } else {
    try {
      userInfo.value = JSON.parse(user)
    } catch (e) {
      console.error('解析用户信息失败:', e)
      router.push('/login')
    }
  }
})

// 监听路由变化
import { watch } from 'vue'
watch(() => route.path, updateActiveMenu)
</script>

<style scoped>
.home {
  height: 100vh;
  overflow: hidden;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  color: white;
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 1px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.user-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.username {
  font-size: 14px;
  font-weight: 500;
}

.dropdown-icon {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.aside {
  background-color: #1a1a2e;
  color: white;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 220px;
  min-height: 400px;
}

.el-menu {
  background-color: #1a1a2e;
  border-right: none;
}

.el-menu-item {
  color: #a0a0b0;
  margin: 4px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.el-menu-item:hover {
  background-color: rgba(64, 158, 255, 0.1);
  color: #409eff;
}

.el-menu-item.is-active {
  color: #409eff;
  background-color: rgba(64, 158, 255, 0.15);
}

.main {
  padding: 24px;
  background-color: #f0f2f5;
  overflow-y: auto;
  width: 100%;
}

/* 路由切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
