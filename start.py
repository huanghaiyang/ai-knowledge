import os
import subprocess
import time
import webbrowser
import json
from dotenv import load_dotenv

# 读取配置文件
def load_config():
    """加载配置文件"""
    # 尝试读取config.json文件
    config_path = os.path.join(os.getcwd(), 'config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print('配置文件读取成功')
            return config
        except Exception as e:
            print(f'配置文件解析失败，请检查config.json文件格式: {e}')
            exit(1)
    else:
        print('配置文件不存在，请先创建config.json文件')
        exit(1)

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
    # 加载配置
    config = load_config()
    
    # 检查配置文件是否存在
    print('检查配置文件是否存在...')
    env_file_path = os.path.join('backend', '.env')
    if not os.path.exists(env_file_path):
        print('创建后端环境配置文件...')
        env_content = f'''
# 数据库配置
DB_USER={config['database']['user']}
DB_PASSWORD={config['database']['password']}
DB_HOST={config['database']['host']}
DB_PORT={config['database']['port']}
DB_NAME={config['database']['name']}

# 后端配置
BACKEND_HOST={config['backend']['host']}
BACKEND_PORT={config['backend']['port']}
SECRET_KEY={config['backend']['secret_key']}
DEBUG={config['backend']['debug']}

# JWT Secret - generate a secure secret key for production
JWT_SECRET_KEY={config['jwt']['secret_key']}

# OpenAI API Key - optional, for AI features
OPENAI_API_KEY={config['openai']['api_key']}
'''
        with open(env_file_path, 'w') as f:
            f.write(env_content)
        print('后端环境配置文件创建成功')
    
    # 检查前端配置文件
    frontend_env_path = os.path.join('frontend', '.env')
    if not os.path.exists(frontend_env_path):
        print('创建前端环境配置文件...')
        backend_protocol = config['backend'].get('protocol', 'http')
        backend_url = f'{backend_protocol}://{config['backend']['host']}:{config['backend']['port']}'
        env_content = f'''
# 前端环境配置
VITE_FRONTEND_PORT={config['frontend']['port']}
VITE_BACKEND_URL={backend_url}
'''
        with open(frontend_env_path, 'w') as f:
            f.write(env_content)
        print('前端环境配置文件创建成功')
    
    # 加载环境变量
    load_dotenv(dotenv_path=env_file_path)
    load_dotenv(dotenv_path=frontend_env_path)
    
    # 导入配置管理模块
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    from app.utils.config import FRONTEND_URL, BACKEND_URL
    
    print('配置文件检查通过')
    print(f'前端端口: {FRONTEND_URL}')
    print(f'后端端口: {BACKEND_URL}')
    
    # 启动后端服务
    print('启动后端服务...')
    backend_process = subprocess.Popen(['python', 'main.py'], cwd='backend', shell=True)
    
    # 等待后端服务启动
    time.sleep(5)
    print('后端服务已启动')
    print(f'后端服务地址: {BACKEND_URL}')
    print(f'后端API文档: {BACKEND_URL}/docs')
    
    # 启动前端服务
    start_frontend(FRONTEND_URL)
    
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
                # 加载配置
                config = load_config()
                backend_protocol = config['backend'].get('protocol', 'http')
                backend_url = f'{backend_protocol}://{config['backend']['host']}:{config['backend']['port']}'
                env_content = f'''
# 前端环境配置
VITE_FRONTEND_PORT={config['frontend']['port']}
VITE_BACKEND_URL={backend_url}
'''
                with open(frontend_env_path, 'w') as f:
                    f.write(env_content)
                print('前端环境配置文件创建成功')
            # 加载环境变量
            load_dotenv(dotenv_path=frontend_env_path)
            # 导入配置管理模块
            import sys
            sys.path.append(os.path.join(os.getcwd(), 'backend'))
            from app.utils.config import FRONTEND_URL
            start_frontend(FRONTEND_URL)
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
            # 加载配置
            config = load_config()
            backend_protocol = config['backend'].get('protocol', 'http')
            backend_url = f'{backend_protocol}://{config['backend']['host']}:{config['backend']['port']}'
            env_content = f'''
# 前端环境配置
VITE_FRONTEND_PORT={config['frontend']['port']}
VITE_BACKEND_URL={backend_url}
'''
            with open(frontend_env_path, 'w') as f:
                f.write(env_content)
            print('前端环境配置文件创建成功')
        # 加载环境变量
        load_dotenv(dotenv_path=frontend_env_path)
        # 导入配置管理模块
        import sys
        sys.path.append(os.path.join(os.getcwd(), 'backend'))
        from app.utils.config import FRONTEND_URL
        start_frontend(FRONTEND_URL)
