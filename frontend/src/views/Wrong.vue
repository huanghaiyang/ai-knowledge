<template>
  <div class="wrong-container">
    <h2>错题本</h2>
    <el-card class="wrong-card">
      <template #header>
        <div class="card-header">
          <span>我的错题</span>
          <el-button type="primary" @click="startWrongPractice">开始错题重练</el-button>
        </div>
      </template>
      <el-table :data="wrongAnswers" style="width: 100%">
        <el-table-column prop="questionId" label="题目ID" width="80"></el-table-column>
        <el-table-column prop="questionContent" label="题目内容"></el-table-column>
        <el-table-column prop="userAnswer" label="我的答案" width="180"></el-table-column>
        <el-table-column prop="correctAnswer" label="正确答案" width="180"></el-table-column>
        <el-table-column prop="feedback" label="反馈" width="200"></el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="text" @click="reviewQuestion(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <el-dialog v-model="dialogVisible" title="错题详情">
      <div class="question-detail" v-if="selectedQuestion">
        <h3>{{ selectedQuestion.questionContent }}</h3>
        <div class="options" v-if="selectedQuestion.options">
          <el-radio-group v-model="reviewAnswer" v-if="selectedQuestion.questionType === 'single_choice'" disabled>
            <el-radio v-for="(option, index) in JSON.parse(selectedQuestion.options)" :key="index" :label="option">
              {{ option }}
            </el-radio>
          </el-radio-group>
          <el-checkbox-group v-model="reviewAnswer" v-else-if="selectedQuestion.questionType === 'multiple_choice'" disabled>
            <el-checkbox v-for="(option, index) in JSON.parse(selectedQuestion.options)" :key="index" :label="option">
              {{ option }}
            </el-checkbox>
          </el-checkbox-group>
          <el-radio-group v-model="reviewAnswer" v-else-if="selectedQuestion.questionType === 'true_false'" disabled>
            <el-radio label="正确">正确</el-radio>
            <el-radio label="错误">错误</el-radio>
          </el-radio-group>
          <el-input v-model="reviewAnswer" type="textarea" rows="4" placeholder="请输入答案" v-else-if="selectedQuestion.questionType === 'short_answer' || selectedQuestion.questionType === 'fill_blank'" disabled>
          </el-input>
          <el-input v-model="reviewAnswer" type="textarea" rows="6" placeholder="请输入代码" v-else-if="selectedQuestion.questionType === 'code'" disabled>
          </el-input>
        </div>
        <div class="answer-info">
          <p><strong>我的答案：</strong>{{ selectedQuestion.userAnswer }}</p>
          <p><strong>正确答案：</strong>{{ selectedQuestion.correctAnswer }}</p>
          <p><strong>反馈：</strong>{{ selectedQuestion.feedback }}</p>
        </div>
        <div class="explanation" v-if="selectedQuestion.explanation">
          <h4>解析</h4>
          <p>{{ selectedQuestion.explanation }}</p>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '../utils/request'
import { ElMessage } from 'element-plus'

const wrongAnswers = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const selectedQuestion = ref(null)
const reviewAnswer = ref('')

const fetchWrongAnswers = async () => {
  try {
    const response = await request.get('/answer/user-answers/incorrect')
    wrongAnswers.value = response.data.map(item => ({
      id: item.id,
      questionId: item.question_id,
      questionContent: item.question?.content || '题目已删除',
      questionType: item.question?.question_type || '',
      options: item.question?.options || '',
      explanation: item.question?.explanation || '',
      userAnswer: item.user_answer,
      correctAnswer: item.question?.correct_answer || '',
      feedback: item.feedback
    }))
    total.value = wrongAnswers.value.length
  } catch (error) {
    console.error('获取错题失败:', error)
    ElMessage.error('获取错题失败，请稍后重试')
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  // 这里可以添加分页逻辑
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  // 这里可以添加分页逻辑
}

const reviewQuestion = (row) => {
  selectedQuestion.value = row
  reviewAnswer.value = row.userAnswer
  dialogVisible.value = true
}

const startWrongPractice = () => {
  if (wrongAnswers.value.length === 0) {
    ElMessage.info('暂无错题')
    return
  }
  // 这里可以跳转到错题重练页面
  ElMessage.success('开始错题重练')
}

onMounted(() => {
  fetchWrongAnswers()
})
</script>

<style scoped>
.wrong-container {
  padding: 20px 0;
}

.wrong-container h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.question-detail {
  padding: 20px 0;
}

.question-detail h3 {
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

.answer-info {
  margin-bottom: 20px;
}

.answer-info p {
  margin-bottom: 10px;
  line-height: 1.5;
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
</style>
