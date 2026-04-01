"""
API测试文件
测试API端点的功能，确保它们正常工作，并且只执行只读操作
"""
import sys
import os
import json
import requests
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 读取配置文件
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')
if not os.path.exists(config_path):
    print("错误: 配置文件不存在")
    print("请先创建config.json文件")
    sys.exit(1)

try:
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except Exception as e:
    print(f"错误: 配置文件解析失败: {e}")
    sys.exit(1)

# 加载环境变量
load_dotenv()

# 从环境变量或配置文件中获取后端API地址
backend_host = os.getenv('BACKEND_HOST', config['backend']['host'])
backend_port = os.getenv('BACKEND_PORT', config['backend']['port'])
base_url = os.getenv('BACKEND_URL', f'http://{backend_host}:{backend_port}')

def test_root_endpoint():
    """
    测试根端点
    """
    print("=" * 50)
    print("测试根端点")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200
        data = response.json()
        print(f"✓ 根端点响应成功: {data['message']}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def test_knowledge_endpoint():
    """
    测试知识点端点
    """
    print("=" * 50)
    print("测试知识点端点")
    print("=" * 50)
    
    try:
        # 测试获取知识点列表
        response = requests.get(f"{base_url}/api/knowledge")
        assert response.status_code == 200
        data = response.json()
        print(f"✓ 知识点列表获取成功，数量: {len(data)}")
        
        # 如果有知识点，测试获取单个知识点
        if data:
            knowledge_id = data[0]['id']
            response = requests.get(f"{base_url}/api/knowledge/{knowledge_id}")
            assert response.status_code == 200
            knowledge_data = response.json()
            print(f"✓ 单个知识点获取成功: {knowledge_data['title']}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def test_question_endpoint():
    """
    测试题目端点
    """
    print("=" * 50)
    print("测试题目端点")
    print("=" * 50)
    
    try:
        # 测试获取题目列表
        response = requests.get(f"{base_url}/api/question")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 题目列表获取成功，数量: {len(data)}")
            
            # 如果有题目，测试获取单个题目
            if data:
                question_id = data[0]['id']
                response = requests.get(f"{base_url}/api/question/{question_id}")
                if response.status_code == 200:
                    question_data = response.json()
                    print(f"✓ 单个题目获取成功: {question_data['content'][:50]}...")
                else:
                    print(f"⚠ 单个题目获取失败: {response.status_code}")
                    print(f"  响应: {response.text}")
        else:
            print(f"⚠ 题目列表获取失败: {response.status_code}")
            print(f"  响应: {response.text}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def test_user_endpoint():
    """
    测试用户端点
    """
    print("=" * 50)
    print("测试用户端点")
    print("=" * 50)
    
    try:
        # 测试用户登录（需要先注册）
        # 注意：这里我们不测试注册，因为注册会写入数据库
        # 只测试登录功能
        login_data = {
            "email": "test3@example.com",
            "password": "Test123!"
        }
        response = requests.post(f"{base_url}/api/user/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 用户登录成功")
            print(f"  访问令牌: {data['access_token'][:20]}...")
        else:
            print(f"⚠ 登录失败（可能用户不存在）: {response.status_code}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def main():
    """
    运行所有API测试
    """
    print("\n" + "=" * 50)
    print("API测试")
    print("=" * 50 + "\n")
    
    test_root_endpoint()
    test_knowledge_endpoint()
    test_question_endpoint()
    test_user_endpoint()
    
    print("=" * 50)
    print("API测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
