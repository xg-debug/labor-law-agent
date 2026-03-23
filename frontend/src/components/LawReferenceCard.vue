<template>
  <el-card class="law-card" shadow="hover">
    <template #header>
      <div class="title-wrap">
        <span class="title">{{ item.name || '法律依据' }}</span>
        <el-tag size="small">{{ item.source || '法规' }}</el-tag>
      </div>
    </template>
    <div class="content">{{ item.summary || item.content }}</div>
  </el-card>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.law-card {
  margin-bottom: 10px;
}

.title-wrap {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  align-items: center;
}

.title {
  font-weight: 600;
}

.content {
  white-space: pre-wrap;
  line-height: 1.7;
}
</style>
