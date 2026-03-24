<template>
  <div class="contract-page">
    <h2 class="page-title">合同审查</h2>
    <p class="page-subtitle">粘贴劳动合同文本，识别风险条款并给出修改建议。</p>

    <el-row :gutter="16">
      <el-col :md="11" :sm="24">
        <el-card class="section-card page-card" shadow="never">
          <template #header>合同输入</template>

          <el-input
            v-model="store.contractText"
            type="textarea"
            :rows="16"
            placeholder="请粘贴劳动合同全文或关键条款"
          />

          <el-space style="margin-top: 12px" wrap>
            <el-button type="primary" :loading="store.loading.contract" @click="submit">开始审查</el-button>
            <el-button :loading="store.loading.contract" @click="submitDemo">使用示例数据</el-button>
            <el-tag type="info">文件上传入口（预留）</el-tag>
          </el-space>

          <el-alert
            v-if="store.errors.contract"
            :title="store.errors.contract"
            type="error"
            :closable="false"
            style="margin-top: 12px"
          />
        </el-card>
      </el-col>

      <el-col :md="13" :sm="24">
        <el-card class="section-card page-card" v-if="store.contractResult" shadow="never">
          <template #header>审查结果</template>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="风险摘要" name="summary">
              <p><b>合同类型：</b>{{ store.contractResult.contract_type }}</p>
              <p><b>审查条款：</b>{{ toText(store.contractResult.review_items) }}</p>
              <p><b>总体建议：</b>{{ toText(store.contractResult.suggestions) }}</p>
            </el-tab-pane>
            <el-tab-pane label="详细说明" name="detail">
              <RiskCard v-for="risk in store.contractResult.risks || []" :key="risk.title" :risk="risk" />
            </el-tab-pane>
          </el-tabs>
        </el-card>

        <el-card class="section-card page-card" v-if="store.contractResult?.law_references?.length" shadow="never">
          <template #header>相关法律依据</template>
          <LawReferenceCard
            v-for="item in store.contractResult.law_references"
            :key="item.name + item.summary"
            :item="item"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import LawReferenceCard from '../components/LawReferenceCard.vue'
import RiskCard from '../components/RiskCard.vue'
import { useLawAssistantStore } from '../stores/lawAssistant'

const store = useLawAssistantStore()
const activeTab = ref('summary')

onMounted(() => {
  store.setScene('contract-review')
})

const toText = (value) => {
  if (!value) return '-'
  if (Array.isArray(value)) return value.join('；')
  return value
}

const submit = async () => {
  await store.submitContractReview()
}

const submitDemo = async () => {
  await store.submitContractReview(true)
}
</script>

<style scoped>
.contract-page {
  max-width: 1240px;
  margin: 0 auto;
}

.page-card {
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}

@media (min-width: 992px) {
  .contract-page :deep(.el-row > .el-col:last-child) {
    max-height: calc(100vh - 150px);
    overflow-y: auto;
    padding-right: 4px;
  }
}
</style>
