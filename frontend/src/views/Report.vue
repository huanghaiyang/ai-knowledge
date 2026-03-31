<template>
  <div class="report-container">
    <h2>学习报告</h2>
    <el-card class="report-card">
      <template #header>
        <div class="card-header">
          <span>学习统计</span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ reportData.total_questions || 0 }}</div>
              <div class="stat-label">总答题数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ reportData.correct_questions || 0 }}</div>
              <div class="stat-label">正确题数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ Math.round((reportData.accuracy || 0) * 100) }}%</div>
              <div class="stat-label">正确率</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-item">
              <div class="stat-value">{{ reportData.learning_hours || 0 }}</div>
              <div class="stat-label">学习时长(小时)</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    
    <el-card class="mastery-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>知识点掌握度</span>
        </div>
      </template>
      <div class="mastery-chart" v-if="Object.keys(reportData.knowledge_mastery || {}).length > 0">
        <!-- 这里可以使用ECharts等图表库绘制雷达图 -->
        <div class="placeholder-chart">
          <p>知识点掌握度雷达图</p>
          <ul>
            <li v-for="(mastery, knowledge) in reportData.knowledge_mastery" :key="knowledge">
              {{ knowledge }}: {{ Math.round(mastery * 100) }}%
            </li>
          </ul>
        </div>
      </div>
      <div class="no-data" v-else>
        <p>暂无学习数据</p>
      </div>
    </el-card>
    
    <el-card class="weak-points-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>薄弱知识点</span>
        </div>
      </template>
      <el-table :data="weakPoints" style="width: 100%" v-if="weakPoints.length > 0">
        <el-table-column prop="knowledge_title" label="知识点" width="200"></el-table-column>
        <el-table-column prop="error_rate" label="错误率">
          <template #default="scope">
            <el-progress :percentage="Math.round(scope.row.error_rate * 100)" :color="getProgressColor(scope.row.error_rate)"></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="total_questions" label="总题数" width="100"></el-table-column>
        <el-table-column prop="incorrect_questions" label="错误题数" width="100"></el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="primary" size="small" @click="startSpecialTraining(scope.row.knowledge_id)">专项训练</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="no-data" v-else>
        <p>暂无薄弱知识点</p>
      </div>
    </el-card>
    
    <el-card class="recommendations-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>学习推荐</span>
        </div>
      </template>
      <el-list v-if="reportData.recommended_learning && reportData.recommended_learning.length > 0">
        <el-list-item v-for="(item, index) in reportData.recommended_learning" :key="index">
          <div class="recommendation-item">
            <span class="recommendation-title">{{ item.knowledge_title }}</span>
            <span class="recommendation-mastery">掌握度：{{ Math.round(item.mastery * 100) }}%</span>
            <p class="recommendation-desc">{{ item.recommendation }}</p>
          </div>
        </el-list-item>
      </el-list>
      <div class="no-data" v-else>
        <p>暂无学习推荐</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const reportData = ref({})
const weakPoints = ref([])

const fetchLearningReport = async () => {
  try {
    const response = await axios.get('/api/report/learning-report', {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    reportData.value = response.data
  } catch (error) {
    console.error('获取学习报告失败:', error)
    ElMessage.error('获取学习报告失败，请稍后重试')
  }
}

const fetchWeakPoints = async () => {
  try {
    const response = await axios.get('/api/report/weak-points', {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    weakPoints.value = response.data
  } catch (error) {
    console.error('获取薄弱知识点失败:', error)
    ElMessage.error('获取薄弱知识点失败，请稍后重试')
  }
}

const getProgressColor = (errorRate) => {
  if (errorRate > 0.8) return '#f56c6c'
  if (errorRate > 0.5) return '#e6a23c'
  return '#67c23a'
}

const startSpecialTraining = (knowledgeId) => {
  router.push(`/special?knowledge_id=${knowledgeId}`)
}

onMounted(() => {
  fetchLearningReport()
  fetchWeakPoints()
})
</script>

<style scoped>
.report-container {
  padding: 20px 0;
}

.report-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-card {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.mastery-chart {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-chart {
  text-align: center;
  width: 100%;
}

.placeholder-chart p {
  font-size: 16px;
  margin-bottom: 20px;
  color: #303133;
}

.placeholder-chart ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.placeholder-chart li {
  padding: 10px 20px;
  background-color: #f5f7fa;
  border-radius: 20px;
  font-size: 14px;
}

.no-data {
  text-align: center;
  padding: 50px 0;
  color: #909399;
}

.recommendation-item {
  padding: 10px 0;
  border-bottom: 1px solid #e4e7ed;
}

.recommendation-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-right: 20px;
}

.recommendation-mastery {
  font-size: 14px;
  color: #606266;
  margin-right: 20px;
}

.recommendation-desc {
  font-size: 14px;
  color: #606266;
  margin-top: 5px;
  line-height: 1.5;
}
</style>
