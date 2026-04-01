from flask import Flask, jsonify, g
from flask_cors import CORS
import asyncio
import os
from dotenv import load_dotenv
from app.utils.database import engine, Base
from app.models import user, knowledge, question, answer

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
CORS(app)

# 创建数据库表
Base.metadata.create_all(bind=engine)

@app.route('/')
async def root():
    return jsonify({"message": "AI知识学习与智能测评系统API"})

# 请求钩子，在请求结束时关闭数据库会话
@app.teardown_appcontext
def teardown_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# 导入路由
from app.api import user, knowledge, question, answer, report

# 注册路由
user.register_routes(app)
knowledge.register_routes(app)
question.register_routes(app)
answer.register_routes(app)
report.register_routes(app)

if __name__ == "__main__":
    host = os.getenv('BACKEND_HOST', '0.0.0.0')
    port = int(os.getenv('BACKEND_PORT', '8000'))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(host=host, port=port, debug=debug)
