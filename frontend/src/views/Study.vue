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
        <el-col :span="7" style="height: 100%;">
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
        <el-col :span="17" style="height: 100%;">
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
                <div v-for="(section, index) in knowledgeContent.content_sections" :key="section.id" class="content-section" :data-section-id="section.id">
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
    
    <!-- 笔记输入框 -->
    <div 
      v-if="isNoteInputVisible" 
      class="note-input"
      :style="{ left: noteInputPosition.x + 'px', top: noteInputPosition.y + 'px' }"
    >
      <textarea 
        v-model="noteInputContent" 
        placeholder="添加笔记..."
        class="note-textarea"
      ></textarea>
      <div class="note-actions">
        <el-button type="primary" @click="saveHighlight">保存</el-button>
        <el-button @click="cancelHighlight">取消</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { Check, Link, Star, Search } from '@element-plus/icons-vue'
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
const contentRef = ref(null)

// 高亮相关状态
const highlights = ref([])
const isNoteInputVisible = ref(false)
const noteInputContent = ref('')
const selectedText = ref('')
const currentHighlightId = ref('')
const noteInputPosition = ref({ x: 0, y: 0 })

const defaultProps = {
  children: 'children',
  label: 'title'
}

// 处理文本选择
const handleTextSelection = () => {
  const selection = window.getSelection()
  if (selection && selection.toString().trim()) {
    selectedText.value = selection.toString().trim()
    const range = selection.getRangeAt(0)
    
    // 检查是否选择了公式
    const commonAncestor = range.commonAncestorContainer
    const mathElement = commonAncestor.closest ? commonAncestor.closest('.mjx-chtml, .mjx-svg, .MathJax') : null
    
    // 计算输入框位置
    const rect = range.getBoundingClientRect()
    noteInputPosition.value = {
      x: rect.left + window.scrollX,
      y: rect.bottom + window.scrollY + 10
    }
    
    // 显示笔记输入框
    isNoteInputVisible.value = true
  }
}

// 生成唯一ID
const generateId = () => {
  return 'hl_' + Date.now() + '_' + Math.floor(Math.random() * 1000)
}

// 计算高亮位置
const getHighlightPosition = (range, sectionElement) => {
  // 创建一个从section开始到高亮开始的范围
  const startRange = document.createRange()
  startRange.setStart(sectionElement, 0)
  startRange.setEnd(range.startContainer, range.startOffset)
  
  // 计算起始位置
  const startPos = startRange.toString().length
  
  // 计算结束位置
  const endPos = startPos + range.toString().length
  
  return { startPos, endPos }
}

// 获取高亮上下文
const getHighlightContext = (range, contextLength = 50) => {
  // 获取高亮前的上下文
  const startContextRange = document.createRange()
  const startContainer = range.startContainer
  const startOffset = Math.max(0, range.startOffset - contextLength)
  startContextRange.setStart(startContainer, startOffset)
  startContextRange.setEnd(startContainer, range.startOffset)
  const startContext = startContextRange.toString()
  
  // 获取高亮后的上下文
  const endContextRange = document.createRange()
  const endContainer = range.endContainer
  const endOffset = Math.min(endContainer.textContent.length, range.endOffset + contextLength)
  endContextRange.setStart(endContainer, range.endOffset)
  endContextRange.setEnd(endContainer, endOffset)
  const endContext = endContextRange.toString()
  
  return { startContext, endContext }
}

// 保存高亮和笔记
const saveHighlight = async () => {
  if (!selectedText.value) return
  
  const highlightId = generateId()
  currentHighlightId.value = highlightId
  
  // 创建高亮元素
  const sel = window.getSelection()
  if (sel) {
    const range = sel.getRangeAt(0)
    const commonAncestor = range.commonAncestorContainer
    const mathElement = commonAncestor.closest ? commonAncestor.closest('.mjx-chtml, .mjx-svg, .MathJax') : null
    
    // 获取section元素
    const sectionElement = document.querySelector('.content-section')
    let sectionId = null
    let startPos = 0
    let endPos = 0
    let startContext = ''
    let endContext = ''
    
    if (sectionElement) {
      // 计算位置
      const position = getHighlightPosition(range, sectionElement)
      startPos = position.startPos
      endPos = position.endPos
      
      // 获取上下文
      const context = getHighlightContext(range)
      startContext = context.startContext
      endContext = context.endContext
      
      // 获取章节ID
      sectionId = sectionElement.dataset.sectionId
    }
    
    if (mathElement) {
      // 处理公式高亮
      const mathHighlight = document.createElement('div')
      mathHighlight.className = 'formula-highlight'
      mathHighlight.dataset.id = highlightId
      mathHighlight.style.position = 'relative'
      mathHighlight.style.display = 'inline-block'
      mathHighlight.style.margin = '4px 0'
      
      // 创建背景节点
      const bgNode = document.createElement('div')
      bgNode.className = 'highlight-bg'
      bgNode.style.position = 'absolute'
      bgNode.style.top = '0'
      bgNode.style.left = '0'
      bgNode.style.right = '0'
      bgNode.style.bottom = '0'
      bgNode.style.backgroundColor = 'rgba(255, 255, 204, 0.7)'
      bgNode.style.borderRadius = '6px'
      bgNode.style.border = '2px solid #ffeb3b'
      bgNode.style.zIndex = '-1'
      
      // 复制公式内容
      mathHighlight.innerHTML = mathElement.outerHTML
      mathHighlight.appendChild(bgNode)
      
      // 替换原公式
      mathElement.parentNode.replaceChild(mathHighlight, mathElement)
    } else {
      // 处理普通文本高亮
      try {
        // 创建高亮容器
        const highlightContainer = document.createElement('span')
        highlightContainer.className = 'text-highlight-container'
        highlightContainer.dataset.id = highlightId
        highlightContainer.style.position = 'relative'
        highlightContainer.style.display = 'inline'
        
        // 创建背景节点
        const bgNode = document.createElement('span')
        bgNode.className = 'highlight-bg'
        bgNode.style.position = 'absolute'
        bgNode.style.top = '0'
        bgNode.style.left = '0'
        bgNode.style.right = '0'
        bgNode.style.bottom = '0'
        bgNode.style.backgroundColor = 'rgba(255, 255, 204, 0.7)'
        bgNode.style.borderRadius = '3px'
        bgNode.style.borderBottom = '2px solid #ffeb3b'
        bgNode.style.zIndex = '-1'
        
        // 复制选中内容
        const selectedContent = range.extractContents()
        highlightContainer.appendChild(selectedContent)
        highlightContainer.appendChild(bgNode)
        
        // 插入高亮容器
        range.insertNode(highlightContainer)
        
        // 重新选择文本以保持用户体验
        const newRange = document.createRange()
        newRange.selectNodeContents(highlightContainer)
        sel.removeAllRanges()
        sel.addRange(newRange)
      } catch (e) {
        console.error('无法创建高亮:', e)
        ElMessage.error('无法创建高亮，请选择连续的文本')
        return
      }
    }
    
    // 保存到数据库
    try {
      await axios.post('/api/knowledge/highlight', {
        knowledge_id: selectedKnowledge.value.id,
        section_id: sectionId,
        highlight_id: highlightId,
        text: selectedText.value,
        note: noteInputContent.value,
        start_pos: startPos,
        end_pos: endPos,
        start_context: startContext,
        end_context: endContext
      })
      
      // 添加到本地高亮列表
      highlights.value.push({
        id: highlightId,
        text: selectedText.value,
        note: noteInputContent.value,
        start_pos: startPos,
        end_pos: endPos,
        start_context: startContext,
        end_context: endContext
      })
      
      ElMessage.success('高亮保存成功')
    } catch (error) {
      console.error('保存高亮失败:', error)
      ElMessage.error('保存高亮失败，请重试')
    }
  }
  
  // 重置状态
  isNoteInputVisible.value = false
  noteInputContent.value = ''
  selectedText.value = ''
}

// 取消高亮
const cancelHighlight = () => {
  isNoteInputVisible.value = false
  noteInputContent.value = ''
  selectedText.value = ''
}

// 应用高亮
const applyHighlight = (highlight) => {
  const sectionElement = document.querySelector('.content-section')
  if (!sectionElement) return
  
  try {
    // 创建范围
    const range = document.createRange()
    
    // 定位到起始位置
    let currentPos = 0
    let startContainer = sectionElement
    let startOffset = 0
    
    // 遍历DOM树找到正确的位置
    const findPosition = (node, targetPos, currentPos) => {
      if (node.nodeType === Node.TEXT_NODE) {
        const nodeLength = node.textContent.length
        if (currentPos + nodeLength > targetPos) {
          startContainer = node
          startOffset = targetPos - currentPos
          return true
        }
        return currentPos + nodeLength
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        for (let i = 0; i < node.childNodes.length; i++) {
          const result = findPosition(node.childNodes[i], targetPos, currentPos)
          if (result === true) {
            return true
          } else if (typeof result === 'number') {
            currentPos = result
          }
        }
      }
      return currentPos
    }
    
    findPosition(sectionElement, highlight.start_pos, 0)
    
    // 定位到结束位置
    let endContainer = sectionElement
    let endOffset = 0
    
    findPosition(sectionElement, highlight.end_pos, 0)
    
    // 设置范围
    range.setStart(startContainer, startOffset)
    range.setEnd(endContainer, endOffset)
    
    // 创建高亮容器
    const highlightContainer = document.createElement('span')
    highlightContainer.className = 'text-highlight-container'
    highlightContainer.dataset.id = highlight.highlight_id
    highlightContainer.style.position = 'relative'
    highlightContainer.style.display = 'inline'
    
    // 创建背景节点
    const bgNode = document.createElement('span')
    bgNode.className = 'highlight-bg'
    bgNode.style.position = 'absolute'
    bgNode.style.top = '0'
    bgNode.style.left = '0'
    bgNode.style.right = '0'
    bgNode.style.bottom = '0'
    bgNode.style.backgroundColor = 'rgba(255, 255, 204, 0.7)'
    bgNode.style.borderRadius = '3px'
    bgNode.style.borderBottom = '2px solid #ffeb3b'
    bgNode.style.zIndex = '-1'
    bgNode.style.transition = 'all 0.2s ease'
    
    // 复制选中内容
    const selectedContent = range.extractContents()
    highlightContainer.appendChild(selectedContent)
    highlightContainer.appendChild(bgNode)
    
    // 插入高亮容器
    range.insertNode(highlightContainer)
  } catch (error) {
    console.error('应用高亮失败:', error)
  }
}

// 加载高亮
const loadHighlights = async (knowledgeId) => {
  try {
    // 获取sectionId
    const sectionElement = document.querySelector('.content-section')
    let sectionId = null
    if (sectionElement) {
      sectionId = sectionElement.dataset.sectionId
    }
    
    // 构建请求URL
    let url = `/api/knowledge/${knowledgeId}/highlights`
    if (sectionId) {
      url += `?section_id=${sectionId}`
    }
    
    const response = await axios.get(url)
    highlights.value = response.data
    
    // 应用高亮
    nextTick(() => {
      highlights.value.forEach(highlight => {
        applyHighlight(highlight)
      })
    })
  } catch (error) {
    console.error('加载高亮失败:', error)
  }
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
  typographer: false, // 禁用自动排版，避免影响MathJax
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return '' // 使用默认处理
  }
})

// 初始化 MathJax
let mathJaxLoaded = false

const initMathJax = async () => {
  if (mathJaxLoaded) return
  
  // 等待MathJax加载完成
  const checkMathJax = () => {
    return new Promise((resolve) => {
      if (window.MathJax && window.MathJax.typesetPromise) {
        resolve()
      } else {
        setTimeout(() => checkMathJax().then(resolve), 100)
      }
    })
  }
  
  await checkMathJax()
  mathJaxLoaded = true
}

const renderMathJax = async (element) => {
  if (!mathJaxLoaded) {
    await initMathJax()
  }
  if (window.MathJax && window.MathJax.typesetPromise && element) {
    try {
      await window.MathJax.typesetPromise([element])
    } catch (error) {
      console.error('MathJax rendering error:', error)
    }
  }
}

// 格式化内容，使用 markdown-it 解析 Markdown
const formatContent = (content) => {
  if (!content) return ''
  // 使用 markdown-it 解析 Markdown 内容
  return md.render(content)
}

// 监听内容变化，渲染MathJax并加载高亮
watch(knowledgeContent, async (newContent) => {
  if (newContent && newContent.content_sections && newContent.content_sections.length > 0) {
    // 等待DOM完全更新
    await nextTick()
    // 等待一小段时间确保所有内容都已渲染
    await new Promise(resolve => setTimeout(resolve, 100))
    // 选择所有section-content元素
    const contentElements = document.querySelectorAll('.section-content')
    for (const element of contentElements) {
      if (element) {
        await renderMathJax(element)
      }
    }
    // 加载高亮
    if (selectedKnowledge.value) {
      await loadHighlights(selectedKnowledge.value.id)
    }
  }
}, { deep: true })

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
  // 添加文本选择监听
  document.addEventListener('mouseup', handleTextSelection)
})

onUnmounted(() => {
  // 移除文本选择监听
  document.removeEventListener('mouseup', handleTextSelection)
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

/* Markdown 样式隔离 */
.section-content :deep(h1),
.section-content :deep(h2),
.section-content :deep(h3),
.section-content :deep(h4),
.section-content :deep(h5),
.section-content :deep(h6) {
  font-weight: bold;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  color: #2c3e50;
  line-height: 1.4;
}

.section-content :deep(h1) {
  font-size: 2em;
  border-bottom: 2px solid #e4e7ed;
  padding-bottom: 0.3em;
}

.section-content :deep(h2) {
  font-size: 1.5em;
  border-bottom: 1px solid #e4e7ed;
  padding-bottom: 0.3em;
}

.section-content :deep(h3) {
  font-size: 1.25em;
}

.section-content :deep(h4) {
  font-size: 1.1em;
}

.section-content :deep(h5) {
  font-size: 1em;
}

.section-content :deep(h6) {
  font-size: 0.9em;
  color: #909399;
}

/* 段落样式 */
.section-content :deep(p) {
  margin: 1em 0;
  text-align: justify;
}

.section-content :deep(p:first-child) {
  margin-top: 0;
}

.section-content :deep(p:last-child) {
  margin-bottom: 0;
}

/* 列表样式 */
.section-content :deep(ul),
.section-content :deep(ol) {
  margin: 1em 0;
  padding-left: 2em;
}

.section-content :deep(ul) {
  list-style-type: disc;
}

.section-content :deep(ol) {
  list-style-type: decimal;
}

.section-content :deep(li) {
  margin: 0.5em 0;
  line-height: 1.6;
}

.section-content :deep(ul ul),
.section-content :deep(ol ol),
.section-content :deep(ul ol),
.section-content :deep(ol ul) {
  margin: 0.5em 0;
}

/* 引用样式 */
.section-content :deep(blockquote) {
  margin: 1.5em 0;
  padding: 0.5em 1em;
  border-left: 4px solid #409EFF;
  background: #f0f9ff;
  color: #606266;
  font-style: italic;
}

.section-content :deep(blockquote p) {
  margin: 0;
}

/* 代码样式 */
.section-content :deep(code) {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
  background: rgba(64, 158, 255, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  color: #2c3e50;
}

.section-content :deep(pre) {
  background: #f5f5f5;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 1.5em 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.6;
}

.section-content :deep(pre code) {
  background: none;
  padding: 0;
  border-radius: 0;
  color: inherit;
}

/* 表格样式 */
.section-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5em 0;
  font-size: 0.95em;
}

.section-content :deep(table th),
.section-content :deep(table td) {
  border: 1px solid #e4e7ed;
  padding: 12px;
  text-align: left;
}

.section-content :deep(table th) {
  background: #f5f7fa;
  font-weight: bold;
  color: #2c3e50;
}

.section-content :deep(table tr:nth-child(even)) {
  background: #fafafa;
}

.section-content :deep(table tr:hover) {
  background: #f0f9ff;
}

/* 链接样式 */
.section-content :deep(a) {
  color: #409EFF;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.section-content :deep(a:hover) {
  color: #66b1ff;
  border-bottom-color: #66b1ff;
}

.section-content :deep(a:visited) {
  color: #409EFF;
}

/* 图片样式 */
.section-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 1em 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 分隔线样式 */
.section-content :deep(hr) {
  border: none;
  border-top: 2px solid #e4e7ed;
  margin: 2em 0;
}

/* 强调样式 */
.section-content :deep(strong) {
  font-weight: bold;
  color: #2c3e50;
}

.section-content :deep(em) {
  font-style: italic;
  color: #606266;
}

/* 删除线样式 */
.section-content :deep(del) {
  text-decoration: line-through;
  color: #909399;
}

/* 行内代码样式 */
.section-content :deep(kbd) {
  background: #f5f5f5;
  border: 1px solid #dcdcdc;
  border-radius: 4px;
  padding: 2px 6px;
  font-size: 0.9em;
  font-family: 'Courier New', Courier, monospace;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 任务列表样式 */
.section-content :deep(input[type="checkbox"]) {
  margin-right: 8px;
  cursor: pointer;
}

.section-content :deep(li input[type="checkbox"]) {
  margin-left: -20px;
}

/* 定义列表样式 */
.section-content :deep(dl) {
  margin: 1em 0;
}

.section-content :deep(dt) {
  font-weight: bold;
  color: #2c3e50;
  margin-top: 0.8em;
}

.section-content :deep(dd) {
  margin-left: 2em;
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

/* 文本高亮容器 */
:deep(.text-highlight-container) {
  position: relative;
  display: inline;
  cursor: pointer;
  transition: all 0.2s ease;
}

:deep(.text-highlight-container:hover) {
  z-index: 1;
}

:deep(.text-highlight-container:hover .highlight-bg) {
  background-color: rgba(255, 235, 59, 0.8);
  box-shadow: 0 0 0 2px rgba(255, 235, 59, 0.5);
}

/* 公式高亮容器 */
:deep(.formula-highlight) {
  position: relative;
  display: inline-block;
  margin: 4px 0;
  cursor: pointer;
  transition: all 0.2s ease;
}

:deep(.formula-highlight:hover) {
  z-index: 1;
}

:deep(.formula-highlight:hover .highlight-bg) {
  background-color: rgba(255, 235, 59, 0.8);
  box-shadow: 0 0 8px rgba(255, 235, 59, 0.6);
}

/* 高亮背景 */
:deep(.highlight-bg) {
  transition: all 0.2s ease;
}

/* 笔记输入框 */
.note-input {
  position: absolute;
  width: 320px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  font-family: inherit;
  animation: noteInputFadeIn 0.3s ease-out;
}

@keyframes noteInputFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.note-textarea {
  width: 100%;
  min-height: 100px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 12px;
  font-size: 14px;
  font-family: inherit;
  transition: border-color 0.2s ease;
}

.note-textarea:focus {
  outline: none;
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.note-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
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

/* MathJax 数学公式样式隔离 */
.section-content :deep(.mjx-chtml) {
  font-size: 1.1em;
  color: #2c3e50;
  font-family: 'MathJax_Main', 'Times New Roman', Times, serif;
  line-height: 1.2;
}

.section-content :deep(.mjx-chtml .mjx-math) {
  margin: 0;
}

.section-content :deep(.mjx-chtml .mjx-math > mjx-container) {
  overflow-x: auto;
}

/* 块级公式样式 */
.section-content :deep(.mjx-chtml .mjx-display) {
  margin: 1.5em 0;
  overflow-x: auto;
  padding: 1.2em;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 8px;
  border-left: 4px solid #409EFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.section-content :deep(.mjx-chtml .mjx-display > mjx-container) {
  margin: 0;
}

/* 行内公式样式 */
.section-content :deep(.mjx-chtml .mjx-math) {
  padding: 2px 4px;
  background: rgba(64, 158, 255, 0.08);
  border-radius: 4px;
  display: inline-block;
  vertical-align: middle;
}

/* MathJax 公式元素样式 */
.section-content :deep(.mjx-chtml .mjx-mrow) {
  position: relative;
  white-space: nowrap;
  width: min-content;
}

.section-content :deep(.mjx-chtml .mjx-mi) {
  font-style: italic;
}

.section-content :deep(.mjx-chtml .mjx-mo) {
  font-family: 'MathJax_Main', 'Times New Roman', Times, serif;
}

.section-content :deep(.mjx-chtml .mjx-mn) {
  font-family: 'MathJax_Main', 'Times New Roman', Times, serif;
}

.section-content :deep(.mjx-chtml .mjx-mtext) {
  font-family: 'MathJax_Main', 'Times New Roman', Times, serif;
}

/* 分数样式 */
.section-content :deep(.mjx-chtml .mjx-frac) {
  padding: 0 0.1em;
}

.section-content :deep(.mjx-chtml .mjx-frac .mjx-num) {
  display: block;
  text-align: center;
}

.section-content :deep(.mjx-chtml .mjx-frac .mjx-den) {
  display: block;
  text-align: center;
  border-top: 1px solid #2c3e50;
}

.section-content :deep(.mjx-chtml .mjx-frac .mjx-dbox) {
  border-top: 1px solid #2c3e50;
}

/* 上下标样式 */
.section-content :deep(.mjx-chtml .mjx-sup) {
  font-size: 0.7em;
  vertical-align: super;
}

.section-content :deep(.mjx-chtml .mjx-sub) {
  font-size: 0.7em;
  vertical-align: sub;
}

/* 求和、积分等符号 */
.section-content :deep(.mjx-chtml .mjx-op) {
  font-family: 'MathJax_Size1', 'MathJax_Main', 'Times New Roman', Times, serif;
}

.section-content :deep(.mjx-chtml .mjx-op .mjx-large-op) {
  font-size: 1.2em;
}

/* 矩阵样式 */
.section-content :deep(.mjx-chtml .mjx-mtable) {
  border-spacing: 0;
  margin: 0.5em 0;
}

.section-content :deep(.mjx-chtml .mjx-mtable .mjx-mtr) {
  display: flex;
}

.section-content :deep(.mjx-chtml .mjx-mtable .mjx-mtd) {
  padding: 0 0.2em;
}

/* 括号样式 */
.section-content :deep(.mjx-chtml .mjx-mo) {
  font-family: 'MathJax_Size1', 'MathJax_Main', 'Times New Roman', Times, serif;
}

/* 空格样式 */
.section-content :deep(.mjx-chtml .mjx-mspace) {
  display: inline-block;
}

/* 错误提示样式 */
.section-content :deep(.mjx-chtml .mjx-merror) {
  color: #cc0000;
  background: #ffeeee;
  padding: 2px 4px;
  border-radius: 3px;
  border: 1px solid #ffcccc;
}

/* SVG渲染样式 */
.section-content :deep(.mjx-svg) {
  font-size: 1.1em;
  color: #2c3e50;
  font-family: 'MathJax_Main', 'Times New Roman', Times, serif;
  line-height: 1.2;
}

.section-content :deep(.mjx-svg .mjx-math) {
  margin: 0;
}

.section-content :deep(.mjx-svg .mjx-display) {
  margin: 1.5em 0;
  overflow-x: auto;
  padding: 1.2em;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 8px;
  border-left: 4px solid #409EFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.section-content :deep(.mjx-svg .mjx-math) {
  padding: 2px 4px;
  background: rgba(64, 158, 255, 0.08);
  border-radius: 4px;
  display: inline-block;
  vertical-align: middle;
}

.section-content :deep(.mjx-svg svg) {
  display: inline-block;
  vertical-align: middle;
  max-width: 100%;
  height: auto;
}

/* 代码块样式 */
.section-content :deep(pre) {
  background: #f5f5f5;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  margin: 1.5em 0;
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.6;
}

.section-content :deep(code) {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
  background: rgba(64, 158, 255, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  color: #2c3e50;
}

.section-content :deep(pre code) {
  background: none;
  padding: 0;
  border-radius: 0;
  color: inherit;
}

/* 代码高亮样式 */
.section-content :deep(.hljs) {
  background: transparent;
  padding: 0;
}

.section-content :deep(.hljs-comment),
.section-content :deep(.hljs-quote) {
  color: #998;
  font-style: italic;
}

.section-content :deep(.hljs-keyword),
.section-content :deep(.hljs-selector-tag),
.section-content :deep(.hljs-subst) {
  color: #333;
  font-weight: bold;
}

.section-content :deep(.hljs-number),
.section-content :deep(.hljs-literal),
.section-content :deep(.hljs-variable),
.section-content :deep(.hljs-template-variable),
.section-content :deep(.hljs-tag .hljs-attr) {
  color: #008080;
}

.section-content :deep(.hljs-string),
.section-content :deep(.hljs-doctag) {
  color: #d14;
}

.section-content :deep(.hljs-title),
.section-content :deep(.hljs-section),
.section-content :deep(.hljs-selector-id) {
  color: #900;
  font-weight: bold;
}

.section-content :deep(.hljs-subst) {
  font-weight: normal;
}

.section-content :deep(.hljs-type),
.section-content :deep(.hljs-class .hljs-title) {
  color: #458;
  font-weight: bold;
}

.section-content :deep(.hljs-tag),
.section-content :deep(.hljs-name),
.section-content :deep(.hljs-attribute) {
  color: #000080;
  font-weight: normal;
}

.section-content :deep(.hljs-regexp),
.section-content :deep(.hljs-link) {
  color: #009926;
}

.section-content :deep(.hljs-symbol),
.section-content :deep(.hljs-bullet) {
  color: #990073;
}

.section-content :deep(.hljs-built_in),
.section-content :deep(.hljs-builtin-name) {
  color: #0086b3;
}

.section-content :deep(.hljs-meta) {
  color: #999;
  font-weight: bold;
}

.section-content :deep(.hljs-deletion) {
  background: #fdd;
}

.section-content :deep(.hljs-addition) {
  background: #dfd;
}

.section-content :deep(.hljs-emphasis) {
  font-style: italic;
}

.section-content :deep(.hljs-strong) {
  font-weight: bold;
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
