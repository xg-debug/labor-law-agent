<template>
  <el-card class="section-card" v-if="result">
    <template #header>
      <div class="panel-head">
        <span>分析结果</span>
        <el-button text size="small" @click="expanded = !expanded">{{ expanded ? '收起' : '展开' }}</el-button>
      </div>
    </template>

    <div class="result-list" v-show="expanded">
      <p><b>问题摘要：</b>{{ result.question_summary || '-' }}</p>
      <p><b>关键事实：</b>{{ toText(result.facts) }}</p>
      <p><b>争议焦点：</b>{{ toText(result.issues) }}</p>
      <p><b>初步分析：</b>{{ result.analysis || '-' }}</p>
      <p><b>结论：</b>{{ result.conclusion || '-' }}</p>
      <p><b>风险提示：</b>{{ toText(result.risk_tips) }}</p>
      <p><b>后续建议：</b>{{ toText(result.suggestions) }}</p>
      <p><b>证据建议：</b>{{ toText(result.evidence_list) }}</p>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  result: {
    type: Object,
    default: null
  }
})

const expanded = ref(true)

const toText = (value) => {
  if (!value) return '-'
  if (Array.isArray(value)) return value.join('；')
  return value
}
</script>

<style scoped>
.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-list p {
  line-height: 1.7;
  margin: 6px 0;
  white-space: pre-wrap;
}
</style>
