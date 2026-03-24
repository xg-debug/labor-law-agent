<template>
  <div class="auth-page">
    <el-card class="auth-card" shadow="never">
      <h2>登录</h2>
      <p>登录后可使用咨询、合同审查和文书生成功能。</p>

      <el-form label-position="top">
        <el-form-item label="账号">
          <el-input v-model="form.account" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" />
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
        登录
      </el-button>

      <div class="auth-footer">
        没有账号？
        <el-button text @click="router.push('/register')">去注册</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = reactive({
  account: '',
  password: ''
})

const submit = async () => {
  if (!form.account.trim() || !form.password.trim()) return
  await authStore.login({
    account: form.account.trim(),
    password: form.password.trim()
  })
  const redirect = route.query.redirect || '/'
  router.push(String(redirect))
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
