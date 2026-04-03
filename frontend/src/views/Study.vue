<template>
  <div class="study-container">
    <!-- 页面标题和面包屑 -->
    <div class="page-header">
      <h2 class="page-title">AI知识体系</h2>
      <el-breadcrumb v-if="breadcrumb" separator="/" class="breadcrumb">
        <el-breadcrumb-item :to="'/study'">知识中心</el-breadcrumb-item>
        <el-breadcrumb-item v-for="(item, index) in breadcrumb" :key="index" :to="`/study?id=${item.id}`">
          {{ item.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 搜索框 -->
    <div class="search-box mb-4">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索知识点"
        clearable
        prefix-icon="el-icon-search"
        @keyup.enter="handleSearch"
        class="search-input"
      >
        <template #append>
          <el-button @click="handleSearch" type="primary" class="search-button">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </template>
      </el-input>
    </div>

    <div class="content-container flex-grow">
      <el-row :gutter="24" style="height: 100%;">
        <!-- 左侧知识树 -->
        <el-col :span="8" style="height: 100%;">
          <el-card class="knowledge-tree" style="height: 100%;">
            <template #header>
              <div class="card-header">
                <span class="tree-title">知识树</span>
                <span class="tree-count">{{ totalKnowledgeCount }} 个知识点</span>
              </div>
            </template>
            <el-tree
              :data="filteredKnowledgeTree"
              :props="defaultProps"
              @node-click="handleNodeClick"
              node-key="id"
              default-expand-all
              :expand-on-click-node="false"
              :highlight-current="true"
              :current-node-key="selectedKnowledge?.id"
              class="knowledge-tree-content"
              style="height: calc(100% - 60px);"
            >
              <template #default="{ node, data }">
              <span class="tree-node">
                <span class="node-label">{{ node.label }}</span>
              </span>
            </template>
            </el-tree>
          </el-card>
        </el-col>

        <!-- 右侧知识详情 -->
        <el-col :span="16" style="height: 100%;">
          <el-card class="knowledge-detail" v-if="selectedKnowledge" style="height: 100%;">
            <template #header>
              <div class="card-header">
                <span class="detail-title">{{ selectedKnowledge.title }}</span>
                <el-button type="primary" @click="startPractice(selectedKnowledge.id)">
                  <el-icon><Check /></el-icon>
                  开始练习
                </el-button>
              </div>
            </template>
            <div class="knowledge-content" style="height: calc(100% - 60px); overflow-y: auto;">
              <!-- 章节内容展示 -->
              <div v-if="loadingContent" class="content-loading">
                <el-skeleton :rows="10" animated />
              </div>
              <div v-else-if="knowledgeContent && knowledgeContent.content_sections && knowledgeContent.content_sections.length > 0" class="content-sections">
                <div v-for="(section, index) in knowledgeContent.content_sections" :key="section.id" class="content-section">
                  <h4 class="section-title">{{ section.section_title }}</h4>
                  <div class="section-content" v-html="formatContent(section.content)"></div>
                </div>
              </div>
              <div v-else class="content-sections">
                <div class="content-section">
                  <h4 class="section-title">暂无内容</h4>
                  <div class="section-content">该知识点暂无详细内容</div>
                </div>
              </div>
              
              <div class="knowledge-actions mt-6">
                <el-button type="primary" @click="startPractice(selectedKnowledge.id)">
                  <el-icon><Check /></el-icon>
                  开始练习
                </el-button>
                <el-button type="info" @click="viewRelatedKnowledge">
                  <el-icon><Link /></el-icon>
                  相关知识
                </el-button>
                <el-button type="warning" @click="addToFavorites">
                  <el-icon><Star /></el-icon>
                  收藏
                </el-button>
              </div>
            </div>
          </el-card>
          <el-card class="knowledge-detail empty-state" v-else style="height: 100%;">
            <template #header>
              <div class="card-header">
                <span>知识详情</span>
              </div>
            </template>
            <div class="empty-content" style="height: calc(100% - 60px);">
              <el-empty
                description="请从左侧知识树中选择一个知识点查看详情"
              >
                <el-button type="primary" @click="expandAll">展开知识树</el-button>
              </el-empty>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { Check, Link, Star, Search, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const knowledgeTree = ref([])
const selectedKnowledge = ref(null)
const searchKeyword = ref('')
const breadcrumb = ref([])
const knowledgeContent = ref(null)
const loadingContent = ref(false)

const defaultProps = {
  children: 'children',
  label: 'title'
}

// 计算知识点总数
const totalKnowledgeCount = computed(() => {
  const countNodes = (nodes) => {
    return nodes.reduce((count, node) => {
      return count + 1 + (node.children ? countNodes(node.children) : 0)
    }, 0)
  }
  return countNodes(knowledgeTree.value)
})

// 过滤后的知识树
const filteredKnowledgeTree = computed(() => {
  if (!searchKeyword.value) {
    return knowledgeTree.value
  }
  
  const keyword = searchKeyword.value.toLowerCase()
  
  const filterTree = (items) => {
    return items
      .map(item => {
        const filteredChildren = filterTree(item.children || [])
        if (item.title.toLowerCase().includes(keyword) || filteredChildren.length > 0) {
          return {
            ...item,
            children: filteredChildren
          }
        }
        return null
      })
      .filter(Boolean)
  }
  
  return filterTree(knowledgeTree.value)
})

// 获取知识树数据
const fetchKnowledgeTree = async () => {
  try {
    const response = await axios.get('/api/knowledge')
    // 按照order字段排序
    const sortedItems = response.data.sort((a, b) => {
      // 如果没有order字段，使用id排序
      const orderA = a.order !== undefined ? a.id : a.order
      const orderB = b.order !== undefined ? b.id : b.order
      return orderA - orderB
    })
    // 构建知识树结构
    const buildTree = (items, parentId = null) => {
      return items
        .filter(item => item.parent_id === parentId)
        .map(item => ({
          id: item.id,
          title: item.title,
          description: item.description,
          level: item.level,
          order: item.order,
          children: buildTree(items, item.id)
        }))
    }
    knowledgeTree.value = buildTree(sortedItems)
    
    // 检查URL参数
    const id = route.query.id
    let targetId = null
    
    if (id) {
      targetId = parseInt(id)
    } else {
      // 检查localStorage中存储的上一次学习的知识点
      const lastKnowledgeId = localStorage.getItem('lastKnowledgeId')
      if (lastKnowledgeId) {
        targetId = parseInt(lastKnowledgeId)
      }
    }
    
    if (targetId) {
      await selectKnowledgeById(targetId)
    } else if (knowledgeTree.value.length > 0) {
      // 默认选择第一个知识点
      let firstKnowledge = knowledgeTree.value[0]
      // 如果有子节点，使用第一个子节点
      if (firstKnowledge.children && firstKnowledge.children.length > 0) {
        firstKnowledge = firstKnowledge.children[0]
      }
      await selectKnowledgeById(firstKnowledge.id)
      // 更新URL参数
      router.push({ path: '/study', query: { id: firstKnowledge.id } })
    }
  } catch (error) {
    console.error('获取知识树失败:', error)
  }
}

// 根据ID选择知识点
const selectKnowledgeById = async (id) => {
  const findKnowledge = (items) => {
    for (const item of items) {
      if (item.id === id) {
        return item
      }
      if (item.children && item.children.length > 0) {
        const found = findKnowledge(item.children)
        if (found) {
          return found
        }
      }
    }
    return null
  }
  
  const knowledge = findKnowledge(knowledgeTree.value)
  if (knowledge) {
    selectedKnowledge.value = knowledge
    updateBreadcrumb(knowledge)
    // 获取章节内容
    await fetchKnowledgeContent(knowledge.id)
    // 存储到localStorage
    localStorage.setItem('lastKnowledgeId', knowledge.id)
  }
}

// 更新面包屑
const updateBreadcrumb = (knowledge) => {
  const breadcrumbItems = []
  let current = knowledge
  
  // 构建面包屑路径
  while (current) {
    breadcrumbItems.unshift({
      id: current.id,
      title: current.title
    })
    // 这里简化处理，实际应该从父节点关系中获取
    current = null
  }
  
  breadcrumb.value = breadcrumbItems
}

// 处理节点点击
const handleNodeClick = async (data) => {
  selectedKnowledge.value = data
  updateBreadcrumb(data)
  // 更新URL参数
  router.push({ path: '/study', query: { id: data.id } })
  
  // 获取章节内容
  await fetchKnowledgeContent(data.id)
}

// 获取知识点章节内容
const fetchKnowledgeContent = async (knowledgeId) => {
  loadingContent.value = true
  try {
    const response = await axios.get(`/api/knowledge/${knowledgeId}/content`)
    knowledgeContent.value = response.data
  } catch (error) {
    console.error('获取章节内容失败:', error)
    knowledgeContent.value = null
  } finally {
    loadingContent.value = false
  }
}

// 初始化 markdown-it 实例
const md = new MarkdownIt({
  html: true,        // 允许HTML标签
  linkify: true,     // 自动识别链接
  typographer: true, // 自动替换一些排版符号
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return '' // 使用默认处理
  }
})

// 格式化内容，使用 markdown-it 解析 Markdown
const formatContent = (content) => {
  if (!content) return ''
  // 使用 markdown-it 解析 Markdown 内容
  return md.render(content)
}

// 开始练习
const startPractice = (knowledgeId) => {
  router.push(`/practice?knowledge_id=${knowledgeId}`)
}

// 查看相关知识
const viewRelatedKnowledge = () => {
  // 这里可以实现相关知识的逻辑
  ElMessage.info('相关知识功能开发中')
}

// 添加到收藏
const addToFavorites = () => {
  // 这里可以实现收藏功能的逻辑
  ElMessage.success('已添加到收藏')
}

// 处理搜索
const handleSearch = () => {
  // 搜索逻辑已经在computed属性中处理
}

// 展开知识树
const expandAll = () => {
  // 由于我们使用的是 default-expand-all 属性，知识树默认已经全部展开
  // 这里可以添加一些额外的逻辑，比如滚动到顶部
  const treeElement = document.querySelector('.knowledge-tree-content')
  if (treeElement) {
    treeElement.scrollTop = 0
  }
}

// 监听路由变化
watch(() => route.query.id, (newId) => {
  if (newId) {
    selectKnowledgeById(parseInt(newId))
  }
})

onMounted(() => {
  fetchKnowledgeTree()
})
</script>

<style scoped>
.study-container {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.page-header {
  margin-bottom: 30px;
  padding: 20px 0;
  border-bottom: 1px solid #eaeaea;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 32px;
  margin-bottom: 15px;
  color: #2c3e50;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
}

.breadcrumb {
  font-size: 14px;
}

.search-box {
  margin-bottom: 24px;
}

.content-container {
  flex-grow: 1;
  min-height: 0;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

.flex-grow {
  flex-grow: 1;
  min-height: 0;
}

.search-input {
  border-radius: 25px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.search-input:focus {
  box-shadow: 0 4px 12px rgba(46, 162, 255, 0.3);
  border-color: #409EFF;
}

.search-button {
  border-radius: 25px;
  font-weight: bold;
}

.knowledge-tree {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  background: white;
  transition: all 0.3s ease;
}

.knowledge-tree:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
  border-radius: 12px 12px 0 0;
  height: 60px;
  box-sizing: border-box;
}

.tree-title {
  font-size: 18px;
  color: #2c3e50;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tree-count {
  font-size: 14px;
  color: #909399;
  background: #f0f9ff;
  padding: 4px 12px;
  border-radius: 12px;
}

.knowledge-tree-content {
  padding: 10px;
  overflow-y: auto;
}

.knowledge-detail {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  background: white;
  transition: all 0.3s ease;
  overflow: hidden;
}

.knowledge-detail:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
}

.empty-content {
  width: 100%;
  text-align: center;
  padding: 80px 20px;
}

.knowledge-content {
  padding: 24px;
}

.knowledge-meta {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.knowledge-id {
  font-size: 14px;
  color: #909399;
  margin-left: auto;
  background: #f9f9f9;
  padding: 4px 12px;
  border-radius: 12px;
}

.knowledge-description {
  margin-bottom: 32px;
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
  transition: all 0.3s ease;
}

.knowledge-description:hover {
  background: #f0f9ff;
  box-shadow: 0 2px 8px rgba(46, 162, 255, 0.15);
}

.description-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 12px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
}

.knowledge-description p {
  font-size: 16px;
  line-height: 1.7;
  color: #606266;
  margin-bottom: 0;
}

.content-loading {
  padding: 20px;
}

.content-sections {
  margin-bottom: 32px;
}

.content-section {
  margin-bottom: 32px;
  padding: 24px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
  transition: all 0.3s ease;
}

.content-section:hover {
  background: #f0f9ff;
  box-shadow: 0 2px 8px rgba(46, 162, 255, 0.15);
  transform: translateX(4px);
}

.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e4e7ed;
}

.section-content {
  font-size: 16px;
  line-height: 1.8;
  color: #606266;
}

.section-content >>> br {
  margin-bottom: 12px;
  display: block;
  content: "";
}

.knowledge-actions {
  margin-top: 32px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.knowledge-actions .el-button {
  border-radius: 8px;
  padding: 10px 20px;
  font-weight: bold;
  transition: all 0.3s ease;
}

.knowledge-actions .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.detail-title {
  font-size: 22px;
  font-weight: bold;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.tree-node {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
  cursor: pointer;
  margin: 2px 0;
}

.tree-node:hover {
  transform: translateX(4px);
}

.node-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 15px;
  line-height: 28px;
  color: #303133;
}

.knowledge-tree-content {
  padding: 15px;
  overflow-y: auto;
  overflow-x: hidden;
}

/* 滚动条样式 */
.knowledge-tree ::-webkit-scrollbar {
  width: 8px;
}

.knowledge-tree ::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.knowledge-tree ::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.knowledge-tree ::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 动画效果 */
.el-tree-node {
  transition: all 0.3s ease;
}

.el-tree-node.is-current > .el-tree-node__content {
  background: #ecf5ff !important;
  color: #409EFF;
  font-weight: bold;
  border-radius: 6px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .el-col {
    width: 100% !important;
    margin-bottom: 24px;
  }
  
  .knowledge-tree {
    height: 400px;
  }
  
  .knowledge-detail {
    min-height: 500px;
  }
  
  .page-title {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .study-container {
    padding: 10px 0;
  }
  
  .page-header {
    padding: 15px;
    margin-bottom: 20px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  .knowledge-content {
    padding: 16px;
  }
  
  .knowledge-actions {
    flex-direction: column;
  }
  
  .knowledge-actions .el-button {
    width: 100%;
  }
}

/* 代码块样式 */
.section-content pre {
  background: #f5f5f5;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 16px 0;
  font-family: 'Courier New', Courier, monospace;
}

.section-content code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
}

.section-content pre code {
  background: none;
  padding: 0;
}

/* 加载动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.study-container {
  animation: fadeIn 0.5s ease-out;
}

.knowledge-tree, .knowledge-detail {
  animation: fadeIn 0.6s ease-out 0.1s both;
}

.search-box {
  animation: fadeIn 0.6s ease-out 0.2s both;
}
</style>
