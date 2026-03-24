<template>
  <div class="home-page">
    <el-card class="home-hero" shadow="never">
      <div class="hero-title">今天想咨询什么劳动法问题？</div>
      <div class="hero-subtitle">输入问题即可开始分析，也可切换到合同审查或文书生成。</div>

      <el-segmented v-model="scene" :options="sceneOptions" class="scene-switch" />

      <el-input
        v-model="question"
        type="textarea"
        :rows="5"
        resize="none"
        placeholder="例如：公司以不能胜任工作为由辞退我是否合法？我需要准备哪些证据？"
        @keydown.enter.exact.prevent="submit"
        @keydown.shift.enter.exact.stop
      />

      <div class="hero-actions">
        <div class="hero-left">
          <el-button @click="fillDemo">示例问题</el-button>
          <el-tooltip content="图片上传入口（预留）">
            <el-button circle>
              <el-icon><Picture /></el-icon>
            </el-button>
          </el-tooltip>
          <el-tooltip content="文件上传入口（预留）">
            <el-button circle>
              <el-icon><Paperclip /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
        <el-button type="primary" :disabled="!question.trim()" @click="submit">
          <el-icon><Promotion /></el-icon>
          开始处理
        </el-button>
      </div>
    </el-card>

    <el-row :gutter="12" class="home-grid">
      <el-col :xl="8" :md="8" :sm="24">
        <el-card class="feature-card" shadow="never">
          <template #header>法律咨询</template>
          <p>多轮对话分析劳动争议问题，给出争议焦点、风险提示和证据建议。</p>
        </el-card>
      </el-col>
      <el-col :xl="8" :md="8" :sm="24">
        <el-card class="feature-card" shadow="never">
          <template #header>合同审查</template>
          <p>识别劳动合同中的高风险条款，并给出修改建议和法律依据。</p>
        </el-card>
      </el-col>
      <el-col :xl="8" :md="8" :sm="24">
        <el-card class="feature-card" shadow="never">
          <template #header>文书生成</template>
          <p>根据事实与诉求生成劳动仲裁申请书等文书初稿，便于后续完善。</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { Paperclip, Picture, Promotion } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLawAssistantStore } from '../stores/lawAssistant'

const router = useRouter()
const store = useLawAssistantStore()

const scene = ref('consult')
const question = ref('')

const sceneOptions = [
  { label: '法律咨询', value: 'consult' },
  { label: '合同审查', value: 'contract' },
  { label: '文书生成', value: 'document' }
]

const fillDemo = () => {
  question.value = '公司长期安排加班但不支付加班费，我应该如何准备仲裁材料？'
}

const submit = () => {
  const text = question.value.trim()
  if (!text) return

  if (scene.value === 'contract') {
    store.contractText = text
    router.push('/contract-review')
    return
  }

  if (scene.value === 'document') {
    store.documentForm.facts = text
    router.push('/document-generate')
    return
  }

  store.setUserInput(text)
  router.push('/consult')
}
</script>

<style scoped>
.home-page {
  max-width: 1040px;
  margin: 0 auto;
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 14px;
}

.home-hero {
  border-radius: 14px;
  border: 1px solid #e2e8f0;
  padding: 6px;
}

.hero-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.hero-subtitle {
  margin-top: 8px;
  color: #64748b;
  font-size: 14px;
}

.scene-switch {
  margin: 16px 0 14px;
  width: 340px;
  max-width: 100%;
}

.hero-actions {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.hero-left {
  display: flex;
  gap: 8px;
}

.feature-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.feature-card p {
  margin: 0;
  color: #475569;
  line-height: 1.8;
  font-size: 13px;
}

@media (max-width: 768px) {
  .home-page {
    min-height: auto;
    gap: 10px;
  }

  .hero-title {
    font-size: 22px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
