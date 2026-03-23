<template>
  <el-card v-if="document">
    <template #header>
      <div class="preview-head">
        <span>{{ document.title || '文书预览' }}</span>
        <el-button size="small" @click="copyContent">复制全文</el-button>
      </div>
    </template>

    <div class="doc-content">{{ document.content || '暂无内容' }}</div>

    <el-divider />
    <p><b>使用说明：</b>{{ document.usage_notes || '-' }}</p>
    <p><b>风险提示：</b>{{ toText(document.risk_tips) }}</p>
  </el-card>
</template>

<script setup>
import { ElMessage } from 'element-plus'

const props = defineProps({
  document: {
    type: Object,
    default: null
  }
})

const toText = (value) => {
  if (!value) return '-'
  if (Array.isArray(value)) return value.join('；')
  return value
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(props.document?.content || '')
    ElMessage.success('已复制文书内容')
  } catch {
    ElMessage.error('复制失败，请手动复制')
  }
}
</script>

<style scoped>
.preview-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.doc-content {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  line-height: 1.8;
  white-space: pre-wrap;
  background: #fafafa;
}

p {
  line-height: 1.7;
  white-space: pre-wrap;
}
</style>
