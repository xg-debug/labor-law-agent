<template>
  <el-container v-if="!isAuthPage" class="app-layout shell">
    <el-aside width="248px" class="shell-aside">
      <div class="brand-block" @click="go('/')">
        <div class="brand-title">劳动法法律 AI Agent</div>
        <div class="brand-subtitle">Labor Law Workspace</div>
      </div>

      <el-menu :default-active="route.path" class="side-menu" @select="go">
        <el-menu-item index="/">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/consult">
          <el-icon><ChatDotRound /></el-icon>
          <span>智能咨询</span>
        </el-menu-item>
        <el-menu-item index="/contract-review">
          <el-icon><DocumentChecked /></el-icon>
          <span>合同审查</span>
        </el-menu-item>
        <el-menu-item index="/document-generate">
          <el-icon><EditPen /></el-icon>
          <span>文书生成</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="shell-header">
        <div class="header-title">{{ currentTitle }}</div>
        <el-button
          v-if="!authStore.isAuthenticated"
          size="small"
          class="user-login-btn"
          @click="router.push('/login')"
        >
          登录 / 注册
        </el-button>
        <el-dropdown v-else trigger="click" class="user-dropdown">
          <span class="el-dropdown-link">
            {{ authStore.user?.nickname || '未登录用户' }}
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-menu
          class="mobile-menu"
          mode="horizontal"
          :default-active="route.path"
          @select="go"
        >
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/consult">咨询</el-menu-item>
          <el-menu-item index="/contract-review">合同</el-menu-item>
          <el-menu-item index="/document-generate">文书</el-menu-item>
        </el-menu>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
  <el-container v-else class="app-layout auth-layout">
    <el-main class="main auth-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ArrowDown, ChatDotRound, DocumentChecked, EditPen, House } from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const titleMap = {
  '/': '首页',
  '/consult': '智能法律咨询',
  '/contract-review': '劳动合同审查',
  '/document-generate': '法律文书生成'
}

const currentTitle = computed(() => titleMap[route.path] || '劳动法法律 AI Agent')
const isAuthPage = computed(() => Boolean(route.meta?.authPage))

const go = (path) => {
  if (route.path !== path) {
    router.push(path)
  }
}

const logout = () => {
  authStore.clearAuth()
  router.push('/login')
}
</script>
