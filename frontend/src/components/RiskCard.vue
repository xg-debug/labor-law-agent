<template>
  <el-card class="risk-card" shadow="never">
    <div class="header">
      <div class="title">{{ risk.title }}</div>
      <el-tag :type="levelType">{{ risk.level || '中' }}风险</el-tag>
    </div>
    <div class="line"><b>说明：</b>{{ risk.description }}</div>
    <div class="line"><b>建议：</b>{{ risk.suggestion }}</div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  risk: {
    type: Object,
    required: true
  }
})

const levelType = computed(() => {
  const level = props.risk.level || ''
  if (level.includes('高')) return 'danger'
  if (level.includes('低')) return 'success'
  return 'warning'
})
</script>

<style scoped>
.risk-card {
  margin-bottom: 10px;
  border: 1px solid #f3f4f6;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  gap: 8px;
}

.title {
  font-weight: 600;
}

.line {
  margin-bottom: 6px;
  line-height: 1.6;
}
</style>
