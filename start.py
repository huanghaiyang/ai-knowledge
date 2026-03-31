import os
import subprocess
import time
import webbrowser

def start_frontend():
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
    webbrowser.open('http://localhost:3000')
    
    print('前端服务启动完成！')
    print('前端服务地址: http://localhost:3000')
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
        print('错误：配置文件.env不存在')
        print('请在backend目录下创建.env文件，并配置相关信息')
        return
    print('配置文件检查通过')
    
    # 启动后端服务
    print('启动后端服务...')
    backend_process = subprocess.Popen(['python', '-m', 'uvicorn', 'main:app', '--reload', '--port', '8003'], cwd='backend', shell=True)
    
    # 等待后端服务启动
    time.sleep(5)
    print('后端服务已启动')
    print('后端服务地址: http://127.0.0.1:8003')
    print('后端API文档: http://127.0.0.1:8003/docs')
    
    # 启动前端服务
    start_frontend()
    
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
            start_frontend()
        else:
            print(f'uvicorn版本: {result.stdout.strip()}')
            start_backend()
    except Exception as e:
        print(f'错误：{e}')
        print('正在启动前端服务...')
        start_frontend()
