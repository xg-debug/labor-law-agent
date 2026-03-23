import { defineStore } from 'pinia'
import { healthCheck, askQuestion, reviewContract, generateDocument } from '../api/lawService'
import { mockConsultResult, mockContractReview, mockDocument } from '../utils/mockData'

const toError = (error) => error?.message || '请求失败，请稍后重试'

export const useLawAssistantStore = defineStore('law-assistant', {
  state: () => ({
    currentScene: 'consult',
    userInput: '',
    messages: [],
    consultResult: null,
    contractText: '',
    contractResult: null,
    documentForm: {
      doc_type: '劳动仲裁申请书初稿',
      facts: '',
      claim: '',
      context: ''
    },
    documentResult: null,
    loading: {
      health: false,
      consult: false,
      contract: false,
      document: false
    },
    errors: {
      health: '',
      consult: '',
      contract: '',
      document: ''
    },
    healthStatus: null
  }),
  getters: {
    hasHistory: (state) => state.messages.length > 0
  },
  actions: {
    setScene(scene) {
      this.currentScene = scene
    },
    setUserInput(value) {
      this.userInput = value
    },
    clearConsult() {
      this.messages = []
      this.consultResult = null
      this.errors.consult = ''
      this.userInput = ''
    },
    hydrateDocumentContext() {
      if (!this.consultResult) return
      this.documentForm.context = JSON.stringify(
        {
          question_summary: this.consultResult.question_summary,
          analysis: this.consultResult.analysis,
          suggestions: this.consultResult.suggestions
        },
        null,
        2
      )
      if (!this.documentForm.facts) {
        this.documentForm.facts = Array.isArray(this.consultResult.facts)
          ? this.consultResult.facts.join('；')
          : this.consultResult.facts || ''
      }
    },
    async checkHealth() {
      this.loading.health = true
      this.errors.health = ''
      try {
        this.healthStatus = await healthCheck()
      } catch (error) {
        this.errors.health = toError(error)
        this.healthStatus = null
      } finally {
        this.loading.health = false
      }
    },
    async submitConsult(question, useDemo = false) {
      const text = (question || this.userInput).trim()
      if (!text) return
      this.loading.consult = true
      this.errors.consult = ''
      this.messages.push({ id: Date.now(), role: 'user', content: text })

      try {
        const result = useDemo
          ? mockConsultResult
          : await askQuestion({
              question: text,
              history: this.messages.map((item) => ({ role: item.role, content: item.content }))
            })

        this.consultResult = result
        this.messages.push({
          id: Date.now() + 1,
          role: 'assistant',
          content: result.analysis || result.conclusion || '已完成分析，请查看右侧结构化结果。'
        })
        this.userInput = ''
      } catch (error) {
        this.errors.consult = toError(error)
      } finally {
        this.loading.consult = false
      }
    },
    async submitContractReview(useDemo = false) {
      const contract = this.contractText.trim()
      if (!contract && !useDemo) return
      this.loading.contract = true
      this.errors.contract = ''
      try {
        this.contractResult = useDemo
          ? mockContractReview
          : await reviewContract({ contract_text: contract })
      } catch (error) {
        this.errors.contract = toError(error)
      } finally {
        this.loading.contract = false
      }
    },
    async submitDocumentGenerate(useDemo = false) {
      this.loading.document = true
      this.errors.document = ''
      try {
        this.documentResult = useDemo ? mockDocument : await generateDocument(this.documentForm)
      } catch (error) {
        this.errors.document = toError(error)
      } finally {
        this.loading.document = false
      }
    },
    resetDocument() {
      this.documentResult = null
      this.errors.document = ''
    }
  }
})
