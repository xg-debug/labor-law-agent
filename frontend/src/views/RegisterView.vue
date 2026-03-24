<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="never">
      <h2>注册</h2>
      <p>创建账号后即可使用系统全部功能。</p>

      <el-form label-position="top">
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="form.account" placeholder="请输入账号（3-32位）" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码（至少6位）" />
        </el-form-item>
      </el-form>

      <el-alert
        v-if="authStore.error"
        :title="authStore.error"
        type="error"
        :closable="false"
        show-icon
        style="margin-bottom: 12px"
      />

      <el-button type="primary" :loading="authStore.loading" style="width: 100%" @click="submit">
        注册并登录
      </el-button>

      <div class="auth-footer">
        已有账号？
        <el-button text @click="router.push('/login')">去登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  nickname: '',
  account: '',
  password: ''
})

const submit = async () => {
  if (!form.nickname.trim() || !form.account.trim() || !form.password.trim()) return
  await authStore.register({
    nickname: form.nickname.trim(),
    account: form.account.trim(),
    password: form.password.trim()
  })
  router.push('/')
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 120px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.auth-card {
  width: 420px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}

h2 {
  margin: 0;
  font-size: 24px;
}

p {
  margin: 8px 0 16px;
  color: #64748b;
  font-size: 13px;
}

.auth-footer {
  margin-top: 12px;
  text-align: center;
  font-size: 13px;
  color: #64748b;
}
</style>
