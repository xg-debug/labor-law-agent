<template>
  <div>
    <h2 class="page-title">智能法律咨询</h2>
    <p class="page-subtitle">多轮问答 + 结构化分析 + 法律依据</p>
    <el-alert
      v-if="store.healthStatus"
      :title="`后端状态：${store.healthStatus.status} / ${store.healthStatus.service}`"
      type="success"
      :closable="false"
      class="section-card"
    />
    <el-alert
      v-else-if="store.errors.health"
      :title="`后端不可用：${store.errors.health}`"
      type="warning"
      :closable="false"
      class="section-card"
    />

    <el-row :gutter="16">
      <el-col :md="11" :sm="24">
        <el-card class="section-card">
          <template #header>对话窗口</template>
          <ChatWindow :messages="store.messages" :loading="store.loading.consult" :error="store.errors.consult" />

          <el-space wrap style="margin-top: 12px">
            <el-button v-for="question in demoQuestions" :key="question" size="small" @click="fillDemo(question)">
              {{ question }}
            </el-button>
          </el-space>

          <el-input
            v-model="store.userInput"
            type="textarea"
            :rows="4"
            placeholder="请输入劳动法问题，例如：公司辞退我是否合法？"
            style="margin-top: 12px"
          />

          <el-space style="margin-top: 12px" wrap>
            <el-button type="primary" :loading="store.loading.consult" @click="submit">提交问题</el-button>
            <el-button :loading="store.loading.consult" @click="submitDemo">使用示例结果</el-button>
            <el-button @click="store.clearConsult()">重新提问</el-button>
          </el-space>
        </el-card>
      </el-col>

      <el-col :md="13" :sm="24">
        <ResultPanel :result="store.consultResult" />

        <el-card class="section-card" v-if="lawReferences.length">
          <template #header>法律依据</template>
          <LawReferenceCard v-for="item in lawReferences" :key="item.name + item.summary" :item="item" />
        </el-card>

        <el-card class="section-card" v-if="store.consultResult">
          <el-space>
            <el-button type="success" @click="goDocument">一键进入文书生成</el-button>
            <el-button @click="continueAsk">继续追问</el-button>
          </el-space>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ChatWindow from '../components/ChatWindow.vue'
import LawReferenceCard from '../components/LawReferenceCard.vue'
import ResultPanel from '../components/ResultPanel.vue'
import { useLawAssistantStore } from '../stores/lawAssistant'
import { demoQuestions } from '../utils/mockData'

const store = useLawAssistantStore()
const router = useRouter()

const lawReferences = computed(() => store.consultResult?.law_references || [])

onMounted(() => {
  store.setScene('consult')
  if (!store.healthStatus && !store.loading.health) {
    store.checkHealth()
  }
})

const fillDemo = (question) => {
  store.setUserInput(question)
}

const submit = async () => {
  await store.submitConsult(store.userInput)
}

const submitDemo = async () => {
  if (!store.userInput) fillDemo(demoQuestions[0])
  await store.submitConsult(store.userInput, true)
}

const continueAsk = () => {
  store.setUserInput('请结合以上分析，告诉我仲裁前最需要准备的材料。')
}

const goDocument = () => {
  store.hydrateDocumentContext()
  router.push('/document-generate')
}
</script>
