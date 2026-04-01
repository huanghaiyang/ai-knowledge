import os
import subprocess
import time
import webbrowser
from dotenv import load_dotenv

def start_frontend(frontend_url):
    """启动前端服务"""
    # 检查前端依赖是否安装
    print('检查前端依赖是否安装...')
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print('警告：未找到npm环境，请安装Node.js以启动前端服务')
            print('前端服务将无法启动，但后端服务仍可正常运行')
            return
        print(f'npm版本: {result.stdout.strip()}')
    except Exception as e:
        print(f'警告：{e}')
        print('前端服务将无法启动，但后端服务仍可正常运行')
        return
    
    # 检查vite是否安装
    print('检查前端依赖是否安装...')
    try:
        result = subprocess.run(['npm', 'list', 'vite'], cwd='frontend', capture_output=True, text=True)
        if result.returncode != 0:
            print('前端依赖未安装，正在安装...')
            # 安装前端依赖
            subprocess.run(['npm', 'install'], cwd='frontend', shell=True)
            print('前端依赖安装成功')
        else:
            print('前端依赖已安装')
    except Exception as e:
        print(f'警告：{e}')
        print('前端服务将无法启动，但后端服务仍可正常运行')
        return
    
    # 启动前端服务
    print('启动前端服务...')
    frontend_process = subprocess.Popen(['npm', 'run', 'dev'], cwd='frontend', shell=True)
    
    # 等待前端服务启动
    time.sleep(10)
    print('前端服务已启动')
    
    # 打开浏览器访问前端页面
    print('打开浏览器访问前端页面...')
    webbrowser.open(frontend_url)
    
    print('前端服务启动完成！')
    print(f'前端服务地址: {frontend_url}')
    print('注意：后端服务未启动，部分功能可能无法使用')
    
    # 等待用户输入以退出
    input('按Enter键停止服务...')
    # 停止前端进程
    subprocess.run(['taskkill', '/F', '/IM', 'node.exe'], shell=True)
    print('前端服务已停止')

def start_backend():
    """启动后端服务"""
    # 检查配置文件是否存在
    print('检查配置文件是否存在...')
    env_file_path = os.path.join('backend', '.env')
    if not os.path.exists(env_file_path):
        print('创建后端环境配置文件...')
        env_content = '''# 数据库配置
DB_USER=postgres
DB_PASSWORD=psql24678
DB_HOST=localhost
DB_PORT=5455
DB_NAME=ai_learning_system

# 后端配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True

# JWT Secret - generate a secure secret key for production
JWT_SECRET_KEY=your-jwt-secret-key-here

# OpenAI API Key - optional, for AI features
OPENAI_API_KEY=your-openai-api-key-here'''
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print('后端环境配置文件创建成功')
    
    # 检查前端配置文件
    frontend_env_path = os.path.join('frontend', '.env')
    if not os.path.exists(frontend_env_path):
        print('创建前端环境配置文件...')
        env_content = '''# 前端环境配置
VITE_FRONTEND_PORT=3000
VITE_BACKEND_URL=http://localhost:8000'''
        with open(frontend_env_path, 'w') as f:
            f.write(env_content)
        print('前端环境配置文件创建成功')
    
    # 加载环境变量
    load_dotenv(dotenv_path=env_file_path)
    load_dotenv(dotenv_path=frontend_env_path)
    
    # 获取配置
    frontend_port = os.getenv('VITE_FRONTEND_PORT', '3000')
    backend_port = os.getenv('BACKEND_PORT', '8000')
    frontend_url = f'http://localhost:{frontend_port}'
    backend_url = f'http://localhost:{backend_port}'
    
    print('配置文件检查通过')
    print(f'前端端口: {frontend_port}')
    print(f'后端端口: {backend_port}')
    
    # 启动后端服务
    print('启动后端服务...')
    backend_process = subprocess.Popen(['python', 'main.py'], cwd='backend', shell=True)
    
    # 等待后端服务启动
    time.sleep(5)
    print('后端服务已启动')
    print(f'后端服务地址: {backend_url}')
    print(f'后端API文档: {backend_url}/docs')
    
    # 启动前端服务
    start_frontend(frontend_url)
    
    # 停止后端进程
    backend_process.terminate()
    print('后端服务已停止')

if __name__ == '__main__':
    print('正在启动AI知识学习与智能测评系统...')

    # 检查Python环境
    print('检查Python环境...')
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print('错误：未找到Python环境，请安装Python 3.7+')
            exit(1)
        print(f'Python版本: {result.stdout.strip()}')
    except Exception as e:
        print(f'错误：{e}')
        exit(1)

    # 检查uvicorn是否安装
    print('检查uvicorn是否安装...')
    try:
        result = subprocess.run(['python', '-m', 'uvicorn', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print('错误：未安装uvicorn，请先安装后端依赖')
            print('请执行：python -m pip install -r backend/requirements.txt')
            print('正在启动前端服务...')
            # 只启动前端服务
            # 检查前端配置文件
            frontend_env_path = os.path.join('frontend', '.env')
            if not os.path.exists(frontend_env_path):
                print('创建前端环境配置文件...')
                env_content = '''# 前端环境配置
VITE_FRONTEND_PORT=3000
VITE_BACKEND_URL=http://localhost:8000'''
                with open(frontend_env_path, 'w') as f:
                    f.write(env_content)
                print('前端环境配置文件创建成功')
            # 加载环境变量
            load_dotenv(dotenv_path=frontend_env_path)
            frontend_port = os.getenv('VITE_FRONTEND_PORT', '3000')
            frontend_url = f'http://localhost:{frontend_port}'
            start_frontend(frontend_url)
        else:
            print(f'uvicorn版本: {result.stdout.strip()}')
            start_backend()
    except Exception as e:
        print(f'错误：{e}')
        print('正在启动前端服务...')
        # 检查前端配置文件
        frontend_env_path = os.path.join('frontend', '.env')
        if not os.path.exists(frontend_env_path):
            print('创建前端环境配置文件...')
            env_content = '''# 前端环境配置
VITE_FRONTEND_PORT=3000
VITE_BACKEND_URL=http://localhost:8000'''
            with open(frontend_env_path, 'w') as f:
                f.write(env_content)
            print('前端环境配置文件创建成功')
        # 加载环境变量
        load_dotenv(dotenv_path=frontend_env_path)
        frontend_port = os.getenv('VITE_FRONTEND_PORT', '3000')
        frontend_url = f'http://localhost:{frontend_port}'
        start_frontend(frontend_url)
