<template>
  <div class="document-page">
    <h2 class="page-title">法律文书生成</h2>
    <p class="page-subtitle">根据事实与诉求生成文书初稿，可从咨询结果自动带入上下文。</p>

    <el-row :gutter="16">
      <el-col :md="11" :sm="24">
        <el-card class="section-card page-card" shadow="never">
          <template #header>生成参数</template>

          <el-form label-position="top">
            <el-form-item label="文书类型">
              <el-select v-model="store.documentForm.doc_type" style="width: 100%">
                <el-option label="劳动仲裁申请书初稿" value="劳动仲裁申请书初稿" />
                <el-option label="情况说明函" value="情况说明函" />
                <el-option label="解除劳动合同通知书" value="解除劳动合同通知书" />
                <el-option label="沟通函/告知函" value="沟通函/告知函" />
              </el-select>
            </el-form-item>

            <el-form-item label="基础事实">
              <el-input v-model="store.documentForm.facts" type="textarea" :rows="5" />
            </el-form-item>

            <el-form-item label="用户诉求/用途">
              <el-input v-model="store.documentForm.claim" type="textarea" :rows="4" />
            </el-form-item>

            <el-form-item label="上下文（可选）">
              <el-input v-model="store.documentForm.context" type="textarea" :rows="6" />
            </el-form-item>
          </el-form>

          <el-space wrap>
            <el-button type="primary" :loading="store.loading.document" @click="submit">生成文书</el-button>
            <el-button :loading="store.loading.document" @click="submitDemo">使用示例结果</el-button>
            <el-button @click="backConsult">回到咨询页补充信息</el-button>
          </el-space>

          <el-alert
            v-if="store.errors.document"
            :title="store.errors.document"
            type="error"
            :closable="false"
            style="margin-top: 12px"
          />
        </el-card>
      </el-col>

      <el-col :md="13" :sm="24">
        <div class="preview-wrap">
          <DocumentPreview :document="store.documentResult" />
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DocumentPreview from '../components/DocumentPreview.vue'
import { useLawAssistantStore } from '../stores/lawAssistant'

const router = useRouter()
const store = useLawAssistantStore()

onMounted(() => {
  store.setScene('document-generate')
})

const submit = async () => {
  await store.submitDocumentGenerate()
}

const submitDemo = async () => {
  await store.submitDocumentGenerate(true)
}

const backConsult = () => {
  router.push('/consult')
}
</script>

<style scoped>
.document-page {
  max-width: 1240px;
  margin: 0 auto;
}

.page-card {
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}

.preview-wrap {
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 2px;
  background: #fff;
}

@media (min-width: 992px) {
  .preview-wrap {
    max-height: calc(100vh - 150px);
    overflow-y: auto;
  }
}
</style>
