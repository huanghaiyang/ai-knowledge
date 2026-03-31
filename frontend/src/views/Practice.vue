<template>
  <div class="practice-container">
    <h2>章节刷题</h2>
    <el-card class="practice-card">
      <div class="question-header">
        <span>题目 {{ currentQuestionIndex + 1 }} / {{ questions.length }}</span>
        <span class="difficulty" :class="questions[currentQuestionIndex]?.difficulty">{{ getDifficultyText(questions[currentQuestionIndex]?.difficulty) }}</span>
      </div>
      <div class="question-content" v-if="currentQuestion">
        <h3>{{ currentQuestion.content }}</h3>
        <div class="options" v-if="currentQuestion.options">
          <el-radio-group v-model="userAnswer" v-if="currentQuestion.question_type === 'single_choice'">
            <el-radio v-for="(option, index) in JSON.parse(currentQuestion.options)" :key="index" :label="option">
              {{ option }}
            </el-radio>
          </el-radio-group>
          <el-checkbox-group v-model="userAnswer" v-else-if="currentQuestion.question_type === 'multiple_choice'">
            <el-checkbox v-for="(option, index) in JSON.parse(currentQuestion.options)" :key="index" :label="option">
              {{ option }}
            </el-checkbox>
          </el-checkbox-group>
          <el-radio-group v-model="userAnswer" v-else-if="currentQuestion.question_type === 'true_false'">
            <el-radio label="正确">正确</el-radio>
            <el-radio label="错误">错误</el-radio>
          </el-radio-group>
          <el-input v-model="userAnswer" type="textarea" rows="4" placeholder="请输入答案" v-else-if="currentQuestion.question_type === 'short_answer' || currentQuestion.question_type === 'fill_blank'">
          </el-input>
          <el-input v-model="userAnswer" type="textarea" rows="6" placeholder="请输入代码" v-else-if="currentQuestion.question_type === 'code'">
          </el-input>
        </div>
        <div class="question-actions">
          <el-button @click="prevQuestion" :disabled="currentQuestionIndex === 0">上一题</el-button>
          <el-button type="primary" @click="submitAnswer" :loading="loading">提交答案</el-button>
          <el-button @click="nextQuestion" :disabled="currentQuestionIndex === questions.length - 1">下一题</el-button>
        </div>
        <div class="explanation" v-if="showExplanation">
          <h4>解析</h4>
          <p>{{ currentQuestion.explanation }}</p>
          <p class="correct-answer">正确答案：{{ currentQuestion.correct_answer }}</p>
          <p class="feedback" :class="isCorrect ? 'correct' : 'incorrect'">{{ feedback }}</p>
        </div>
      </div>
      <div class="no-questions" v-else>
        <p>暂无题目，请选择其他章节</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const userStore = useUserStore()

const questions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const loading = ref(false)
const showExplanation = ref(false)
const isCorrect = ref(false)
const feedback = ref('')

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value]
})

const getDifficultyText = (difficulty) => {
  const difficultyMap = {
    'easy': '入门',
    'medium': '进阶',
    'hard': '硬核'
  }
  return difficultyMap[difficulty] || difficulty
}

const fetchQuestions = async () => {
  const knowledgeId = route.query.knowledge_id
  if (!knowledgeId) return
  
  try {
    const response = await axios.get('/api/question/', {
      params: { knowledge_id: knowledgeId }
    })
    questions.value = response.data
  } catch (error) {
    console.error('获取题目失败:', error)
  }
}

const submitAnswer = async () => {
  if (!currentQuestion.value) return
  
  loading.value = true
  try {
    const response = await axios.post('/api/answer/user-answer', {
      question_id: currentQuestion.value.id,
      user_answer: userAnswer.value
    }, {
      headers: {
        Authorization: `Bearer ${userStore.token}`
      }
    })
    
    isCorrect.value = response.data.is_correct
    feedback.value = response.data.feedback
    showExplanation.value = true
    ElMessage.success('答案提交成功')
  } catch (error) {
    console.error('提交答案失败:', error)
    ElMessage.error('提交答案失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    userAnswer.value = ''
    showExplanation.value = false
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.length - 1) {
    currentQuestionIndex.value++
    userAnswer.value = ''
    showExplanation.value = false
  }
}

onMounted(() => {
  fetchQuestions()
})
</script>

<style scoped>
.practice-container {
  padding: 20px 0;
}

.practice-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.difficulty {
  padding: 2px 10px;
  border-radius: 10px;
  font-size: 12px;
}

.difficulty.easy {
  background-color: #f0f9eb;
  color: #67c23a;
}

.difficulty.medium {
  background-color: #ecf5ff;
  color: #409eff;
}

.difficulty.hard {
  background-color: #fef0f0;
  color: #f56c6c;
}

.question-content {
  padding: 20px 0;
}

.question-content h3 {
  font-size: 18px;
  margin-bottom: 20px;
  color: #303133;
}

.options {
  margin-bottom: 30px;
}

.options el-radio,
.options el-checkbox {
  display: block;
  margin-bottom: 10px;
}

.question-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.explanation {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-top: 20px;
}

.explanation h4 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #303133;
}

.explanation p {
  margin-bottom: 10px;
  line-height: 1.5;
}

.correct-answer {
  font-weight: bold;
  color: #67c23a;
}

.feedback {
  font-weight: bold;
}

.feedback.correct {
  color: #67c23a;
}

.feedback.incorrect {
  color: #f56c6c;
}

.no-questions {
  text-align: center;
  padding: 50px 0;
  color: #909399;
}
</style>
