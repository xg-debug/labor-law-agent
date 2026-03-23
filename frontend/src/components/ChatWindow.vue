<template>
  <div class="chat-window">
    <div v-for="message in messages" :key="message.id" class="message-row" :class="message.role">
      <div class="bubble">
        <div class="meta">{{ message.role === 'user' ? '我' : '法律助手' }}</div>
        <div class="content">{{ message.content }}</div>
      </div>
    </div>

    <div v-if="loading" class="message-row assistant">
      <div class="bubble">
        <div class="meta">法律助手</div>
        <div class="content">分析中，请稍候...</div>
      </div>
    </div>

    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" class="error" />
  </div>
</template>

<script setup>
defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.chat-window {
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
  min-height: 280px;
  max-height: 520px;
  overflow-y: auto;
  background: #fafafa;
}

.message-row {
  display: flex;
  margin-bottom: 10px;
}

.message-row.user {
  justify-content: flex-end;
}

.bubble {
  max-width: 78%;
  border-radius: 10px;
  padding: 10px 12px;
  background: #fff;
}

.message-row.user .bubble {
  background: #e8f3ff;
}

.meta {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.content {
  white-space: pre-wrap;
  line-height: 1.6;
}

.error {
  margin-top: 8px;
}
</style>
