<template>
  <div>
    <h1 class="page-title">劳动法法律 AI Agent</h1>
    <p class="page-subtitle">
      面向劳动者、求职者与企业 HR，提供劳动法律咨询、争议风险分析、合同审查和文书生成能力。
    </p>

    <el-row :gutter="16" class="section-card">
      <el-col :md="8" :sm="24" v-for="item in abilities" :key="item.title">
        <el-card shadow="hover" style="margin-bottom: 12px; height: 180px">
          <h3>{{ item.title }}</h3>
          <p class="muted">{{ item.desc }}</p>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="section-card">
      <template #header>功能入口</template>
      <el-space wrap>
        <el-button type="primary" @click="go('/consult')">开始法律咨询</el-button>
        <el-button type="success" @click="go('/contract-review')">合同审查</el-button>
        <el-button type="warning" @click="go('/document-generate')">文书生成</el-button>
      </el-space>
    </el-card>

    <el-alert
      title="注意：本系统用于法律辅助，不构成正式法律意见。重大事项请咨询专业律师。"
      type="warning"
      :closable="false"
      show-icon
    />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const abilities = [
  { title: '劳动法律咨询', desc: '围绕试用期、辞退、加班费、未签合同等高频问题进行结构化分析。' },
  { title: '合同审查', desc: '识别试用期、工资、加班、社保、解除条款的潜在劳动法风险。' },
  { title: '文书生成', desc: '生成劳动仲裁申请书、通知函、说明函等文书初稿，支持二次编辑。' }
]

const go = (path) => router.push(path)
</script>
