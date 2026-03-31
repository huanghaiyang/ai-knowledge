<template>
  <div class="exam-container">
    <h2>模拟考试</h2>
    <el-card class="exam-card">
      <template #header>
        <div class="card-header">
          <span>考试设置</span>
        </div>
      </template>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="考试时间" prop="examTime">
          <el-input-number v-model="form.examTime" :min="30" :max="120" :step="15"></el-input-number>
          <span style="margin-left: 10px;">分钟</span>
        </el-form-item>
        <el-form-item label="题量" prop="questionCount">
          <el-input-number v-model="form.questionCount" :min="10" :max="50" :step="5"></el-input-number>
          <span style="margin-left: 10px;">题</span>
        </el-form-item>
        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="form.difficulty" placeholder="请选择难度">
            <el-option label="入门" value="easy"></el-option>
            <el-option label="进阶" value="medium"></el-option>
            <el-option label="硬核" value="hard"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="startExam" :loading="loading">开始考试</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="exam-interface" v-if="showExam">
      <template #header>
        <div class="exam-header">
          <span>模拟考试</span>
          <span class="countdown" :class="{ 'warning': remainingTime < 600, 'danger': remainingTime < 300 }">
            剩余时间：{{ formatTime(remainingTime) }}
          </span>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="16">
          <div class="question-content" v-if="currentQuestion">
            <h3>{{ currentQuestion.content }}</h3>
            <div class="options" v-if="currentQuestion.options">
              <el-radio-group v-model="userAnswers[currentQuestionIndex]" v-if="currentQuestion.question_type === 'single_choice'">
                <el-radio v-for="(option, index) in JSON.parse(currentQuestion.options)" :key="index" :label="option">
                  {{ option }}
                </el-radio>
              </el-radio-group>
              <el-checkbox-group v-model="userAnswers[currentQuestionIndex]" v-else-if="currentQuestion.question_type === 'multiple_choice'">
                <el-checkbox v-for="(option, index) in JSON.parse(currentQuestion.options)" :key="index" :label="option">
                  {{ option }}
                </el-checkbox>
              </el-checkbox-group>
              <el-radio-group v-model="userAnswers[currentQuestionIndex]" v-else-if="currentQuestion.question_type === 'true_false'">
                <el-radio label="正确">正确</el-radio>
                <el-radio label="错误">错误</el-radio>
              </el-radio-group>
              <el-input v-model="userAnswers[currentQuestionIndex]" type="textarea" rows="4" placeholder="请输入答案" v-else-if="currentQuestion.question_type === 'short_answer' || currentQuestion.question_type === 'fill_blank'">
              </el-input>
              <el-input v-model="userAnswers[currentQuestionIndex]" type="textarea" rows="6" placeholder="请输入代码" v-else-if="currentQuestion.question_type === 'code'">
              </el-input>
            </div>
            <div class="question-actions">
              <el-button @click="prevQuestion" :disabled="currentQuestionIndex === 0">上一题</el-button>
              <el-button type="primary" @click="nextQuestion">下一题</el-button>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="answer-card">
            <h4>答题卡</h4>
            <div class="answer-buttons">
              <el-button 
                v-for="(question, index) in questions" 
                :key="index"
                :class="{
                  'answered': userAnswers[index] !== '',
                  'current': index === currentQuestionIndex
                }"
                @click="goToQuestion(index)"
              >
                {{ index + 1 }}
              </el-button>
            </div>
            <el-button type="danger" @click="submitExam" :loading="submitting" style="width: 100%; margin-top: 20px;">提交考试</el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <el-card class="exam-result" v-if="showResult">
      <template #header>
        <div class="card-header">
          <span>考试结果</span>
        </div>
      </template>
      <div class="result-content">
        <h3>考试完成</h3>
        <el-descriptions :column="2">
          <el-descriptions-item label="总题数">{{ questions.length }}</el-descriptions-item>
          <el-descriptions-item label="正确题数">{{ correctCount }}</el-descriptions-item>
          <el-descriptions-item label="错误题数">{{ incorrectCount }}</el-descriptions-item>
          <el-descriptions-item label="正确率">{{ accuracy }}%</el-descriptions-item>
          <el-descriptions-item label="得分">{{ score }}</el-descriptions-item>
          <el-descriptions-item label="考试时间">{{ formatTime(form.examTime * 60) }}</el-descriptions-item>
        </el-descriptions>
        <h4>错题分析</h4>
        <el-table :data="wrongQuestions" style="width: 100%; margin-top: 20px;">
          <el-table-column prop="questionNumber" label="题号" width="80"></el-table-column>
          <el-table-column prop="content" label="题目"></el-table-column>
          <el-table-column prop="userAnswer" label="你的答案"></el-table-column>
          <el-table-column prop="correctAnswer" label="正确答案"></el-table-column>
        </el-table>
        <el-button type="primary" @click="resetExam" style="margin-top: 20px;">重新考试</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '../store/user'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()

const form = ref({
  examTime: 60,
  questionCount: 20,
  difficulty: 'medium'
})
const rules = {
  examTime: [
    { required: true, message: '请设置考试时间', trigger: 'blur' }
  ],
  questionCount: [
    { required: true, message: '请设置题量', trigger: 'blur' }
  ],
  difficulty: [
    { required: true, message: '请选择难度', trigger: 'blur' }
  ]
}

const formRef = ref(null)
const loading = ref(false)
const showExam = ref(false)
const questions = ref([])
const currentQuestionIndex = ref(0)
const userAnswers = ref([])
const remainingTime = ref(0)
const timer = ref(null)
const submitting = ref(false)
const showResult = ref(false)
const correctCount = ref(0)
const incorrectCount = ref(0)
const wrongQuestions = ref([])

const currentQuestion = computed(() => {
  return questions.value[currentQuestionIndex.value]
})

const accuracy = computed(() => {
  if (questions.length === 0) return 0
  return Math.round((correctCount.value / questions.length) * 100)
})

const score = computed(() => {
  if (questions.length === 0) return 0
  return Math.round((correctCount.value / questions.length) * 100)
})

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const startExam = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 获取题目（这里简化处理，实际应根据难度和题量获取）
        const response = await axios.get('/api/question/', {
          params: {
            difficulty: form.value.difficulty
          }
        })
        // 随机选择指定数量的题目
        const shuffled = response.data.sort(() => 0.5 - Math.random())
        questions.value = shuffled.slice(0, form.value.questionCount)
        userAnswers.value = new Array(questions.value.length).fill('')
        showExam.value = true
        showResult.value = false
        currentQuestionIndex.value = 0
        remainingTime.value = form.value.examTime * 60
        
        // 启动倒计时
        startTimer()
      } catch (error) {
        console.error('获取题目失败:', error)
        ElMessage.error('获取题目失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }
  })
}

const startTimer = () => {
  if (timer.value) clearInterval(timer.value)
  timer.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
    } else {
      // 时间到，自动提交
      submitExam()
    }
  }, 1000)
}

const stopTimer = () => {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.length - 1) {
    currentQuestionIndex.value++
  }
}

const goToQuestion = (index) => {
  currentQuestionIndex.value = index
}

const submitExam = async () => {
  submitting.value = true
  stopTimer()
  
  try {
    // 提交所有答案
    const promises = questions.value.map((question, index) => {
      if (userAnswers.value[index] !== '') {
        return axios.post('/api/answer/user-answer', {
          question_id: question.id,
          user_answer: userAnswers.value[index]
        }, {
          headers: {
            Authorization: `Bearer ${userStore.token}`
          }
        })
      }
      return Promise.resolve(null)
    })
    
    const responses = await Promise.all(promises)
    
    // 统计结果
    correctCount.value = 0
    incorrectCount.value = 0
    wrongQuestions.value = []
    
    responses.forEach((response, index) => {
      if (response) {
        if (response.data.is_correct) {
          correctCount.value++
        } else {
          incorrectCount.value++
          wrongQuestions.value.push({
            questionNumber: index + 1,
            content: questions.value[index].content,
            userAnswer: userAnswers.value[index],
            correctAnswer: questions.value[index].correct_answer
          })
        }
      } else {
        incorrectCount.value++
        wrongQuestions.value.push({
          questionNumber: index + 1,
          content: questions.value[index].content,
          userAnswer: '未作答',
          correctAnswer: questions.value[index].correct_answer
        })
      }
    })
    
    showResult.value = true
    showExam.value = false
    ElMessage.success('考试提交成功')
  } catch (error) {
    console.error('提交考试失败:', error)
    ElMessage.error('提交考试失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

const resetExam = () => {
  showResult.value = false
  showExam.value = false
  questions.value = []
  userAnswers.value = []
  currentQuestionIndex.value = 0
  remainingTime.value = 0
  stopTimer()
  correctCount.value = 0
  incorrectCount.value = 0
  wrongQuestions.value = []
}

onMounted(() => {
  // 组件挂载时的初始化
})

onUnmounted(() => {
  // 组件卸载时清除定时器
  stopTimer()
})
</script>

<style scoped>
.exam-container {
  padding: 20px 0;
}

.exam-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.exam-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.countdown {
  font-size: 16px;
  font-weight: bold;
}

.countdown.warning {
  color: #e6a23c;
}

.countdown.danger {
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

.answer-card {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.answer-card h4 {
  font-size: 16px;
  margin-bottom: 20px;
  color: #303133;
}

.answer-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.answer-buttons el-button {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.answer-buttons el-button.answered {
  background-color: #67c23a;
  border-color: #67c23a;
  color: white;
}

.answer-buttons el-button.current {
  background-color: #409eff;
  border-color: #409eff;
  color: white;
}

.result-content {
  padding: 20px 0;
}

.result-content h3 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #303133;
  text-align: center;
}

.result-content h4 {
  font-size: 16px;
  margin-top: 30px;
  margin-bottom: 15px;
  color: #303133;
}
</style>
