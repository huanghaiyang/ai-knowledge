<template>
  <div class="home-container">
    <el-carousel :interval="5000" type="card" height="400px" class="carousel">
      <el-carousel-item v-for="item in carouselItems" :key="item.id">
        <div class="carousel-item">
          <h3>{{ item.title }}</h3>
          <p>{{ item.description }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>
    
    <div class="features">
      <el-row :gutter="20">
        <el-col :span="6" v-for="feature in features" :key="feature.id" class="feature-card">
          <el-card shadow="hover">
            <div class="feature-icon">
              <el-icon v-if="feature.icon === 'Reading'">Reading</el-icon>
              <el-icon v-else-if="feature.icon === 'Edit'">Edit</el-icon>
              <el-icon v-else-if="feature.icon === 'CollectionTag'">CollectionTag</el-icon>
              <el-icon v-else-if="feature.icon === 'Timer'">Timer</el-icon>
              <el-icon v-else-if="feature.icon === 'WarningFilled'">WarningFilled</el-icon>
              <el-icon v-else-if="feature.icon === 'Document'">Document</el-icon>
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
            <el-button type="primary" @click="navigateTo(feature.path)">{{ feature.buttonText }}</el-button>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="learning-path">
      <h2>AI学习路径</h2>
      <el-timeline>
        <el-timeline-item
          v-for="(item, index) in learningPath"
          :key="index"
          :timestamp="item.stage"
          placement="top"
        >
          <el-card>
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
            <el-button type="primary" @click="navigateTo(item.path)">开始学习</el-button>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Reading, Edit, Timer, WarningFilled, Document, CollectionTag } from '@element-plus/icons-vue'

const router = useRouter()

const carouselItems = [
  {
    id: 1,
    title: 'AI知识学习与智能测评系统',
    description: '专为AI初学者打造的在线学习平台，提供智能出题、在线答题、自动批改和学习报告等功能。'
  },
  {
    id: 2,
    title: 'AI学习路径',
    description: '从AI基础概念到深度学习、大模型应用，为您提供完整的AI学习路径。'
  },
  {
    id: 3,
    title: '智能测评',
    description: 'AI自动出题，在线答题，即时批改，帮助您快速掌握AI知识。'
  }
]

const features = [
  {
    id: 1,
    icon: 'Reading',
    title: '学习中心',
    description: 'AI知识体系，按学习路径分层，方便您系统学习。',
    path: '/study',
    buttonText: '进入学习'
  },
  {
    id: 2,
    icon: 'Edit',
    title: '章节刷题',
    description: '按章节练习，即时显示解析，巩固知识点。',
    path: '/practice',
    buttonText: '开始练习'
  },
  {
    id: 3,
    icon: 'CollectionTag',
    title: '专项训练',
    description: '针对特定知识点进行强化训练，提高学习效率。',
    path: '/special',
    buttonText: '开始训练'
  },
  {
    id: 4,
    icon: 'Timer',
    title: '模拟考试',
    description: '模拟真实考试环境，检验学习成果。',
    path: '/exam',
    buttonText: '开始考试'
  },
  {
    id: 5,
    icon: 'WarningFilled',
    title: '错题本',
    description: '自动收录错题，提供同类题强化训练。',
    path: '/wrong',
    buttonText: '查看错题'
  },
  {
    id: 6,
    icon: 'Document',
    title: '学习报告',
    description: '生成学习报告，分析薄弱知识点，推荐学习内容。',
    path: '/report',
    buttonText: '查看报告'
  }
]

const learningPath = [
  {
    stage: '第一阶段',
    title: 'AI基础概念',
    description: '了解人工智能的基本概念、发展历史和应用领域。',
    path: '/study'
  },
  {
    stage: '第二阶段',
    title: '数学基础',
    description: '学习线性代数、概率统计、微积分等AI所需的数学知识。',
    path: '/study'
  },
  {
    stage: '第三阶段',
    title: 'Python与数据处理',
    description: '掌握Python编程基础和数据处理库的使用。',
    path: '/study'
  },
  {
    stage: '第四阶段',
    title: '机器学习算法',
    description: '学习各种机器学习算法的原理和应用。',
    path: '/study'
  },
  {
    stage: '第五阶段',
    title: '深度学习基础',
    description: '了解深度学习的基本概念和神经网络基础。',
    path: '/study'
  },
  {
    stage: '第六阶段',
    title: '大模型（LLM）原理与应用',
    description: '学习大型语言模型的原理和应用。',
    path: '/study'
  }
]

const navigateTo = (path) => {
  router.push(path)
}
</script>

<style scoped>
.home-container {
  padding: 20px 0;
}

.carousel {
  margin-bottom: 40px;
}

.carousel-item {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 0 40px;
  text-align: center;
}

.carousel-item h3 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.carousel-item p {
  font-size: 16px;
  color: #606266;
  line-height: 1.5;
}

.features {
  margin-bottom: 40px;
}

.feature-card {
  margin-bottom: 20px;
}

.feature-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #303133;
}

.feature-card p {
  font-size: 14px;
  color: #606266;
  margin-bottom: 20px;
  line-height: 1.5;
}

.learning-path {
  margin-top: 40px;
}

.learning-path h2 {
  font-size: 24px;
  margin-bottom: 30px;
  color: #303133;
  text-align: center;
}

.el-timeline-item {
  margin-bottom: 30px;
}

.el-timeline-item__timestamp {
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
}

.el-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-card h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #303133;
}

.el-card p {
  font-size: 14px;
  color: #606266;
  margin-bottom: 20px;
  line-height: 1.5;
}
</style>
