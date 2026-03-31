<template>
  <div class="study-container">
    <h2>AI知识体系</h2>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="knowledge-tree">
          <template #header>
            <div class="card-header">
              <span>知识树</span>
            </div>
          </template>
          <el-tree
            :data="knowledgeTree"
            :props="defaultProps"
            @node-click="handleNodeClick"
            node-key="id"
            default-expand-all
          />
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card class="knowledge-detail" v-if="selectedKnowledge">
          <template #header>
            <div class="card-header">
              <span>{{ selectedKnowledge.title }}</span>
            </div>
          </template>
          <div class="knowledge-content">
            <p>{{ selectedKnowledge.description }}</p>
            <el-button type="primary" @click="startPractice(selectedKnowledge.id)">开始练习</el-button>
          </div>
        </el-card>
        <el-card class="knowledge-detail" v-else>
          <template #header>
            <div class="card-header">
              <span>知识详情</span>
            </div>
          </template>
          <div class="knowledge-content">
            <p>请从左侧知识树中选择一个知识点查看详情</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../store/user'

const router = useRouter()
const userStore = useUserStore()

const knowledgeTree = ref([])
const selectedKnowledge = ref(null)

const defaultProps = {
  children: 'children',
  label: 'title'
}

const fetchKnowledgeTree = async () => {
  try {
    const response = await axios.get('/api/knowledge/')
    // 构建知识树结构
    const buildTree = (items, parentId = null) => {
      return items
        .filter(item => item.parent_id === parentId)
        .map(item => ({
          id: item.id,
          title: item.title,
          description: item.description,
          children: buildTree(items, item.id)
        }))
    }
    knowledgeTree.value = buildTree(response.data)
  } catch (error) {
    console.error('获取知识树失败:', error)
  }
}

const handleNodeClick = (data) => {
  selectedKnowledge.value = data
}

const startPractice = (knowledgeId) => {
  router.push(`/practice?knowledge_id=${knowledgeId}`)
}

onMounted(() => {
  fetchKnowledgeTree()
})
</script>

<style scoped>
.study-container {
  padding: 20px 0;
}

.study-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.knowledge-tree {
  height: 600px;
  overflow-y: auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.knowledge-content {
  padding: 20px 0;
}

.knowledge-content p {
  font-size: 16px;
  line-height: 1.5;
  color: #606266;
  margin-bottom: 30px;
}
</style>
