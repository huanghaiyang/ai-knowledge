from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI知识学习与智能测评系统",
    description="一个面向AI初学者的在线学习与测评平台",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI知识学习与智能测评系统API"}

# 导入路由
from app.api import user, knowledge, question, answer, report

app.include_router(user.router, prefix="/api/user", tags=["用户"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["知识体系"])
app.include_router(question.router, prefix="/api/question", tags=["题目"])
app.include_router(answer.router, prefix="/api/answer", tags=["答题"])
app.include_router(report.router, prefix="/api/report", tags=["学习报告"])
