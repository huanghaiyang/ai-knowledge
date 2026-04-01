<template>
  <div class="home-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section bg-gradient bg-primary text-white rounded-lg p-5 mb-5">
      <h2 class="display-5 fw-bold mb-3">欢迎使用AI知识学习与智能测评系统</h2>
      <p class="lead mb-4">
        基于人工智能技术，为您提供个性化的学习体验和智能测评服务
      </p>
      <div class="d-flex gap-3">
        <router-link to="/study" class="btn btn-light btn-lg text-primary fw-bold">
          开始学习
        </router-link>
        <router-link to="/exam" class="btn btn-outline-light btn-lg">
          模拟考试
        </router-link>
      </div>
    </div>

    <!-- 功能模块 -->
    <div class="features-section mb-5">
      <h3 class="h4 fw-bold mb-4">核心功能</h3>
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col">
          <div class="card h-100">
            <div class="card-body">
              <div class="icon-wrapper bg-primary bg-opacity-10 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                <span class="text-primary text-2xl">📚</span>
              </div>
              <h4 class="card-title fw-bold mb-2">学习中心</h4>
              <p class="card-text text-muted">
                AI知识体系，按学习路径分层，方便您系统学习。
              </p>
              <router-link to="/study" class="btn btn-primary btn-sm mt-3">
                进入学习
              </router-link>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100">
            <div class="card-body">
              <div class="icon-wrapper bg-primary bg-opacity-10 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                <span class="text-primary text-2xl">✏️</span>
              </div>
              <h4 class="card-title fw-bold mb-2">专项练习</h4>
              <p class="card-text text-muted">
                针对不同知识点的专项练习，巩固学习成果。
              </p>
              <router-link to="/practice" class="btn btn-primary btn-sm mt-3">
                开始练习
              </router-link>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100">
            <div class="card-body">
              <div class="icon-wrapper bg-primary bg-opacity-10 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                <span class="text-primary text-2xl">📝</span>
              </div>
              <h4 class="card-title fw-bold mb-2">模拟考试</h4>
              <p class="card-text text-muted">
                真实模拟考试环境，检验学习效果。
              </p>
              <router-link to="/exam" class="btn btn-primary btn-sm mt-3">
                开始考试
              </router-link>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100">
            <div class="card-body">
              <div class="icon-wrapper bg-primary bg-opacity-10 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                <span class="text-primary text-2xl">❌</span>
              </div>
              <h4 class="card-title fw-bold mb-2">错题集</h4>
              <p class="card-text text-muted">
                自动收集错题，针对性复习，避免重复错误。
              </p>
              <router-link to="/wrong" class="btn btn-primary btn-sm mt-3">
                查看错题
              </router-link>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100">
            <div class="card-body">
              <div class="icon-wrapper bg-primary bg-opacity-10 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                <span class="text-primary text-2xl">⭐</span>
              </div>
              <h4 class="card-title fw-bold mb-2">专题训练</h4>
              <p class="card-text text-muted">
                针对特定领域的深度训练，提升专业技能。
              </p>
              <router-link to="/special" class="btn btn-primary btn-sm mt-3">
                进入训练
              </router-link>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card h-100">
            <div class="card-body">
              <div class="icon-wrapper bg-primary bg-opacity-10 rounded-full w-12 h-12 flex items-center justify-center mb-4">
                <span class="text-primary text-2xl">📊</span>
              </div>
              <h4 class="card-title fw-bold mb-2">学习报告</h4>
              <p class="card-text text-muted">
                AI分析学习数据，生成个性化学习报告。
              </p>
              <router-link to="/report" class="btn btn-primary btn-sm mt-3">
                查看报告
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习统计 -->
    <div class="stats-section mb-5">
      <h3 class="h4 fw-bold mb-4">学习统计</h3>
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
        <div class="col">
          <div class="card text-center h-100">
            <div class="card-body">
              <div class="text-primary text-3xl mb-2">📚</div>
              <h5 class="card-title fw-bold mb-1">学习时长</h5>
              <p class="card-text text-muted">12.5 小时</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card text-center h-100">
            <div class="card-body">
              <div class="text-primary text-3xl mb-2">✏️</div>
              <h5 class="card-title fw-bold mb-1">已做题目</h5>
              <p class="card-text text-muted">128 题</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card text-center h-100">
            <div class="card-body">
              <div class="text-primary text-3xl mb-2">✅</div>
              <h5 class="card-title fw-bold mb-1">正确率</h5>
              <p class="card-text text-muted">78%</p>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card text-center h-100">
            <div class="card-body">
              <div class="text-primary text-3xl mb-2">🏆</div>
              <h5 class="card-title fw-bold mb-1">学习等级</h5>
              <p class="card-text text-muted">Lv.3</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 推荐学习 -->
    <div class="recommendation-section">
      <h3 class="h4 fw-bold mb-4">推荐学习</h3>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title fw-bold mb-3">基于您的学习情况，推荐以下内容</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6 class="fw-bold">机器学习基础</h6>
                <p class="text-muted small">掌握机器学习的核心概念和算法</p>
              </div>
              <router-link to="/study" class="btn btn-sm btn-outline-primary">
                开始学习
              </router-link>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6 class="fw-bold">深度学习进阶</h6>
                <p class="text-muted small">深入理解神经网络和深度学习模型</p>
              </div>
              <router-link to="/study" class="btn btn-sm btn-outline-primary">
                开始学习
              </router-link>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <div>
                <h6 class="fw-bold">自然语言处理</h6>
                <p class="text-muted small">学习NLP的关键技术和应用</p>
              </div>
              <router-link to="/study" class="btn btn-sm btn-outline-primary">
                开始学习
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 可以在这里添加组件逻辑
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* 让核心功能部分的card-body里的按钮底部对齐 */
.features-section .card {
  position: relative;
}

.features-section .card-body {
  padding-bottom: 50px; /* 为按钮留出空间 */
}

.features-section .card-body .btn {
  position: absolute;
  bottom: 20px;
  left: 20px;
}

@media (max-width: 768px) {
  .welcome-section {
    text-align: center;
  }
  
  .welcome-section .d-flex {
    justify-content: center;
  }
  
  .features-section .card-body .btn {
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
