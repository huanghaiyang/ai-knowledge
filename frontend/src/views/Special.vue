<template>
  <div class="special-container">
    <h2>专项训练</h2>
    <el-card class="special-card">
      <template #header>
        <div class="card-header">
          <span>选择训练类型</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="知识点" prop="knowledgeId">
          <el-select v-model="form.knowledgeId" placeholder="请选择知识点">
            <el-option
              v-for="knowledge in knowledgePoints"
              :key="knowledge.id"
              :label="knowledge.title"
              :value="knowledge.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="form.difficulty" placeholder="请选择难度">
            <el-option label="入门" value="easy"></el-option>
            <el-option label="进阶" value="medium"></el-option>
            <el-option label="硬核" value="hard"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="题量" prop="questionCount">
          <el-input-number v-model="form.questionCount" :min="5" :max="50" :step="5"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="startTraining" :loading="loading">开始训练</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="training-card" v-if="showTraining">
      <template #header>
        <div class="card-header">
          <span>专项训练</span>
          <span class="progress">{{ currentQuestionIndex + 1 }} / {{ questions.length }}</span>
        </div>
      </template>
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
          <el-button type="primary" @click="submitAnswer" :loading="submitting">提交答案</el-button>
          <el-button @click="nextQuestion" :disabled="currentQuestionIndex === questions.length - 1">下一题</el-button>
        </div>
        <div class="explanation" v-if="showExplanation">
          <h4>解析</h4>
          <p>{{ currentQuestion.explanation }}</p>
          <p class="correct-answer">正确答案：{{ currentQuestion.correct_answer }}</p>
          <p class="feedback" :class="isCorrect ? 'correct' : 'incorrect'">{{ feedback }}</p>
        </div>
      </div>
      <div class="training-result" v-if="showResult">
        <h3>训练完成</h3>
        <el-descriptions :column="2">
          <el-descriptions-item label="总题数">{{ questions.length }}</el-descriptions-item>
          <el-descriptions-item label="正确题数">{{ correctCount }}</el-descriptions-item>
          <el-descriptions-item label="错误题数">{{ incorrectCount }}</el-descriptions-item>
          <el-descriptions-item label="正确率">{{ accuracy }}%</el-descriptions-item>
        </el-descriptions>
        <el-button type="primary" @click="resetTraining">重新训练</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

const knowledgePoints = ref([])
const form = ref({
  knowledgeId: '',
  difficulty: 'medium',
  questionCount: 10
})
const rules = {
  knowledgeId: [
    { required: true, message: '请选择知识点', trigger: 'blur' }
  ],
  difficulty: [
    { required: true, message: '请选择难度', trigger: 'blur' }
  ],
  questionCount: [
    { required: true, message: '请输入题量', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const loading = ref(false)
const showTraining = ref(false)
const questions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const submitting = ref(false)
const showExplanation = ref(false)
const isCorrect = ref(false)
const feedback = ref('')
const showResult = ref(false)
const correctCount = ref(0)
const incorrectCount = ref(0)

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value]
})

const accuracy = computed(() => {
  if (questions.length === 0) return 0
  return Math.round((correctCount.value / questions.length) * 100)
})

const fetchKnowledgePoints = async () => {
  try {
    const response = await axios.get('/api/knowledge/')
    knowledgePoints.value = response.data
  } catch (error) {
    console.error('获取知识点失败:', error)
  }
}

const startTraining = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const response = await axios.get('/api/question/', {
          params: {
            knowledge_id: form.value.knowledgeId,
            difficulty: form.value.difficulty
          }
        })
        // 随机选择指定数量的题目
        const shuffled = response.data.sort(() => 0.5 - Math.random())
        questions.value = shuffled.slice(0, form.value.questionCount)
        showTraining.value = true
        showResult.value = false
        currentQuestionIndex.value = 0
        userAnswer.value = ''
        showExplanation.value = false
        correctCount.value = 0
        incorrectCount.value = 0
      } catch (error) {
        console.error('获取题目失败:', error)
        ElMessage.error('获取题目失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}

const submitAnswer = async () => {
  if (!currentQuestion.value) return
  
  submitting.value = true
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
    
    if (isCorrect.value) {
      correctCount.value++
    } else {
      incorrectCount.value++
    }
    
    ElMessage.success('答案提交成功')
  } catch (error) {
    console.error('提交答案失败:', error)
    ElMessage.error('提交答案失败，请稍后重试')
  } finally {
    submitting.value = false
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
  } else {
    // 训练完成
    showResult.value = true
  }
}

const resetTraining = () => {
  showTraining.value = false
  showResult.value = false
  questions.value = []
  currentQuestionIndex.value = 0
  userAnswer.value = ''
  showExplanation.value = false
  correctCount.value = 0
  incorrectCount.value = 0
}

onMounted(() => {
  fetchKnowledgePoints()
})
</script>

<style scoped>
.special-container {
  padding: 20px 0;
}

.special-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress {
  font-size: 14px;
  color: #409eff;
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

.training-result {
  padding: 30px 0;
  text-align: center;
}

.training-result h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #303133;
}

.training-result .el-descriptions {
  margin-bottom: 30px;
}
</style>
