<template>
  <el-container class="app-layout">
    <el-header class="header">
      <div class="brand" @click="go('/')">劳动法法律 AI Agent</div>
      <el-menu mode="horizontal" :ellipsis="false" :default-active="route.path" @select="go">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/consult">智能咨询</el-menu-item>
        <el-menu-item index="/contract-review">合同审查</el-menu-item>
        <el-menu-item index="/document-generate">文书生成</el-menu-item>
      </el-menu>
    </el-header>

    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const go = (path) => {
  if (route.path !== path) {
    router.push(path)
  }
}
</script>
