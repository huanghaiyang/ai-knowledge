import os
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 读取配置文件
config = {}

# 尝试读取config.json文件
# 使用当前文件的绝对路径来定位config.json文件，确保无论从哪个目录运行都能正确找到
current_dir = os.path.dirname(os.path.abspath(__file__))
# 向上导航到项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
config_path = os.path.join(project_root, 'config.json')
if os.path.exists(config_path):
  try:
    with open(config_path, 'r', encoding='utf-8') as f:
      config = json.load(f)
  except Exception as e:
    print(f'配置文件解析失败，请检查config.json文件格式: {e}')
    # 退出程序，因为配置文件是必须的
    exit(1)
else:
  print('配置文件不存在，请先创建config.json文件')
  # 退出程序，因为配置文件是必须的
  exit(1)

# 数据库配置
DB_USER = os.getenv('DB_USER', config['database']['user'])
DB_PASSWORD = os.getenv('DB_PASSWORD', config['database']['password'])
DB_HOST = os.getenv('DB_HOST', config['database']['host'])
DB_PORT = os.getenv('DB_PORT', config['database']['port'])
DB_NAME = os.getenv('DB_NAME', config['database']['name'])

# 前端配置
FRONTEND_HOST = os.getenv('FRONTEND_HOST', config['frontend']['host'])
FRONTEND_PORT = os.getenv('FRONTEND_PORT', config['frontend']['port'])
FRONTEND_PROTOCOL = os.getenv('FRONTEND_PROTOCOL', config['frontend'].get('protocol', 'http'))

# 后端配置
BACKEND_HOST = os.getenv('BACKEND_HOST', config['backend']['host'])
BACKEND_PORT = os.getenv('BACKEND_PORT', config['backend']['port'])
BACKEND_PROTOCOL = os.getenv('BACKEND_PROTOCOL', config['backend'].get('protocol', 'http'))
SECRET_KEY = os.getenv('SECRET_KEY', config['backend']['secret_key'])
# 处理DEBUG配置，环境变量优先，支持字符串和布尔值
DEBUG_ENV = os.getenv('DEBUG')
if DEBUG_ENV is not None:
    # 处理环境变量中的字符串值
    DEBUG = DEBUG_ENV.lower() == 'true'
else:
    # 直接使用配置文件中的布尔值
    DEBUG = config['backend']['debug']

# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', config['jwt']['secret_key'])

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', config['openai']['api_key'])

# 前端配置
FRONTEND_URL = f'{FRONTEND_PROTOCOL}://{FRONTEND_HOST}:{FRONTEND_PORT}'

# 后端URL
BACKEND_URL = f'{BACKEND_PROTOCOL}://{BACKEND_HOST}:{BACKEND_PORT}'
