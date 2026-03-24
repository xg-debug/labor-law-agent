<template>
  <div class="consult-page">
    <div class="consult-header">
      <div>
        <h2>智能法律咨询</h2>
        <p>多轮对话 · 争议焦点 · 法律依据 · 证据建议</p>
      </div>
      <div class="header-actions">
        <el-tag :type="store.healthStatus ? 'success' : 'warning'" effect="light">
          {{ store.healthStatus ? '服务正常' : '服务异常' }}
        </el-tag>
        <el-button size="small" :disabled="!store.consultResult" @click="goDocument">
          <el-icon><Document /></el-icon>
          一键生成文书
        </el-button>
      </div>
    </div>

    <el-row :gutter="12">
      <el-col :xl="6" :lg="7" :md="24" :sm="24" :xs="24">
        <el-card class="left-panel" shadow="never">
          <template #header>
            <div class="panel-title">示例问题</div>
          </template>

          <el-input v-model="keyword" placeholder="搜索示例问题" clearable>
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <div class="example-list">
            <el-button
              v-for="item in filteredExamples"
              :key="item"
              class="example-item"
              text
              @click="fillDemo(item)"
            >
              {{ item }}
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :xl="12" :lg="10" :md="24" :sm="24" :xs="24">
        <el-card class="chat-panel" shadow="never">
          <template #header>
            <div class="panel-title">咨询会话</div>
          </template>

          <div ref="messageContainer" class="message-list">
            <TransitionGroup name="msg" tag="div">
              <div
                v-for="msg in store.messages"
                :key="msg.id"
                class="msg-row"
                :class="msg.role === 'user' ? 'row-user' : 'row-ai'"
              >
                <div class="msg-bubble" :class="msg.role === 'user' ? 'bubble-user' : 'bubble-ai'">
                  {{ msg.content }}
                </div>
              </div>
            </TransitionGroup>

            <el-empty
              v-if="!store.messages.length && !store.loading.consult"
              :image-size="72"
              description="输入劳动法问题，开始第一轮咨询"
            />

            <div v-if="store.loading.consult" class="loading-row">
              <el-icon class="is-loading"><Loading /></el-icon>
              <span>正在分析中...</span>
            </div>
          </div>

          <div class="input-area">
            <div class="quick-actions">
              <el-button
                v-for="question in demoQuestions"
                :key="question"
                size="small"
                round
                @click="fillDemo(question)"
              >
                {{ shortText(question) }}
              </el-button>
            </div>

            <el-input
              v-model="store.userInput"
              type="textarea"
              :rows="4"
              resize="none"
              placeholder="请输入问题，Enter 发送，Shift + Enter 换行"
              @keydown.enter.exact.prevent="submit"
              @keydown.shift.enter.exact.stop
            />

            <div class="input-actions">
              <div class="left-icons">
                <el-tooltip content="示例回答">
                  <el-button circle @click="mockAsk" :disabled="store.loading.consult">
                    <el-icon><MagicStick /></el-icon>
                  </el-button>
                </el-tooltip>
                <el-tooltip content="清空会话">
                  <el-button circle @click="store.clearConsult()" :disabled="store.loading.consult">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </el-tooltip>
              </div>

              <el-button type="primary" :loading="store.loading.consult" @click="submit">
                <el-icon><Promotion /></el-icon>
                发送
              </el-button>
            </div>

            <el-alert
              v-if="store.errors.consult"
              :title="store.errors.consult"
              type="error"
              :closable="false"
              show-icon
            />
          </div>
        </el-card>
      </el-col>

      <el-col :xl="6" :lg="7" :md="24" :sm="24" :xs="24">
        <el-card class="right-panel" shadow="never">
          <template #header>
            <div class="panel-title panel-title-row">
              <span>结构化结果</span>
              <el-tag size="small" effect="light">{{ resultStatus }}</el-tag>
            </div>
          </template>

          <el-segmented v-model="activeTab" :options="resultTabs" class="result-tabs" />

          <el-empty v-if="!store.consultResult" :image-size="72" description="暂无分析结果" />

          <div v-else class="result-content">
            <template v-if="activeTab === 'analysis'">
              <el-collapse>
                <el-collapse-item title="问题摘要" name="summary">
                  <p>{{ store.consultResult.question_summary || '-' }}</p>
                </el-collapse-item>
                <el-collapse-item title="争议焦点" name="issues">
                  <p>{{ toText(store.consultResult.issues) }}</p>
                </el-collapse-item>
                <el-collapse-item title="风险提示" name="risks">
                  <p>{{ toText(store.consultResult.risk_tips) }}</p>
                </el-collapse-item>
              </el-collapse>
            </template>

            <template v-if="activeTab === 'law'">
              <el-card
                v-for="law in store.consultResult.law_references || []"
                :key="law.name + law.summary"
                class="result-item"
                shadow="never"
              >
                <h4>{{ law.name }}</h4>
                <p>{{ law.summary }}</p>
              </el-card>
            </template>

            <template v-if="activeTab === 'evidence'">
              <el-card
                v-for="item in store.consultResult.evidence_list || []"
                :key="item"
                class="result-item"
                shadow="never"
              >
                {{ item }}
              </el-card>
            </template>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  Document,
  Loading,
  MagicStick,
  Promotion,
  Refresh,
  Search
} from '@element-plus/icons-vue'
import { useLawAssistantStore } from '../stores/lawAssistant'
import { demoQuestions } from '../utils/mockData'

const router = useRouter()
const store = useLawAssistantStore()
const messageContainer = ref(null)
const keyword = ref('')
const activeTab = ref('analysis')
const resultStatus = ref('待分析')

const resultTabs = [
  { label: '分析', value: 'analysis' },
  { label: '法条', value: 'law' },
  { label: '证据', value: 'evidence' }
]

const filteredExamples = computed(() => {
  const key = keyword.value.trim().toLowerCase()
  if (!key) return demoQuestions
  return demoQuestions.filter((item) => item.toLowerCase().includes(key))
})

const shortText = (text) => (text.length > 16 ? `${text.slice(0, 16)}...` : text)

const fillDemo = (question) => {
  store.setUserInput(question)
}

const toText = (value) => (Array.isArray(value) ? value.join('；') : value || '-')

const submit = async () => {
  if (store.loading.consult) return
  await store.submitConsult(store.userInput)
  activeTab.value = 'analysis'
}

const mockAsk = async () => {
  if (!store.userInput) store.setUserInput(demoQuestions[0])
  await store.submitConsult(store.userInput, true)
  activeTab.value = 'analysis'
}

const goDocument = () => {
  if (!store.consultResult) return
  store.hydrateDocumentContext()
  router.push('/document-generate')
}

watch(
  () => store.loading.consult,
  (loading) => {
    resultStatus.value = loading ? '分析中' : store.consultResult ? '已生成' : '待分析'
  },
  { immediate: true }
)

watch(
  () => store.consultResult,
  (result) => {
    if (result && !store.loading.consult) resultStatus.value = '已生成'
  }
)

watch(
  () => store.messages.length,
  async () => {
    await nextTick()
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  }
)

onMounted(() => {
  store.setScene('consult')
  if (!store.healthStatus && !store.loading.health) {
    store.checkHealth()
  }
})
</script>

<style scoped>
.consult-page {
  max-width: 1240px;
  margin: 0 auto;
  padding: 2px;
}

.consult-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}

.consult-header h2 {
  margin: 0;
  font-size: 22px;
}

.consult-header p {
  margin: 4px 0 0;
  color: #64748b;
  font-size: 13px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title {
  font-weight: 600;
  color: #334155;
}

.panel-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.left-panel,
.chat-panel,
.right-panel {
  border-radius: 14px;
  border: 1px solid #e2e8f0;
}

.example-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 560px;
  overflow: auto;
}

.example-item {
  justify-content: flex-start;
  margin: 0;
  white-space: normal;
  line-height: 1.5;
}

.message-list {
  height: 420px;
  overflow-y: auto;
  padding: 6px;
}

.msg-row {
  display: flex;
  margin-bottom: 10px;
}

.row-user {
  justify-content: flex-end;
}

.row-ai {
  justify-content: flex-start;
}

.msg-bubble {
  max-width: 78%;
  border-radius: 14px;
  padding: 10px 12px;
  line-height: 1.7;
  white-space: pre-wrap;
}

.bubble-user {
  background: #111827;
  color: #fff;
}

.bubble-ai {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #334155;
}

.loading-row {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 10px;
  border-radius: 8px;
  background: #f8fafc;
  color: #64748b;
  font-size: 12px;
}

.input-area {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
  border-top: 1px solid #f1f5f9;
  padding-top: 12px;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left-icons {
  display: flex;
  gap: 8px;
}

.result-tabs {
  margin-bottom: 10px;
  width: 100%;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.result-item h4 {
  margin: 0 0 6px;
  font-size: 13px;
  color: #1f2937;
}

.result-item p {
  margin: 0;
  font-size: 13px;
  line-height: 1.7;
  color: #475569;
}

@media (max-width: 1200px) {
  .message-list {
    height: 380px;
  }
}

@media (max-width: 768px) {
  .consult-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }
}
</style>
