import time
from locust import HttpUser, task, between, LoadTestShape

class KnowledgeAPIUser(HttpUser):
    """测试知识API的用户"""
    wait_time = between(1, 3)  # 每个用户在请求之间的等待时间
    host = "http://127.0.0.1:8000"  # 使用127.0.0.1而不是localhost，避免DNS解析问题
    
    @task(3)
    def get_knowledge_points(self):
        """测试获取所有知识点接口"""
        self.client.get("/api/knowledge")
    
    @task(2)
    def get_knowledge_content(self):
        """测试获取知识点内容接口"""
        # 使用实际存在的知识点ID（假设1-6是一级知识点）
        knowledge_ids = [1, 2, 3, 4, 5, 6]
        for knowledge_id in knowledge_ids:
            try:
                self.client.get(f"/api/knowledge/{knowledge_id}/content")
            except Exception as e:
                # 忽略错误，继续测试
                pass
    
    @task(1)
    def search_knowledge(self):
        """测试搜索知识点接口"""
        search_terms = ["人工智能", "机器学习", "深度学习", "自然语言处理", "计算机视觉"]
        for term in search_terms:
            try:
                self.client.get(f"/api/knowledge/search?q={term}")
            except Exception as e:
                # 忽略错误，继续测试
                pass

class CustomLoadShape(LoadTestShape):
    """自定义负载测试形状"""
    stages = [
        # 持续时间(秒), 用户数量, 用户生成速率
        (30, 50, 5),  # 30秒内增加到50用户
        (60, 100, 10),  # 接下来30秒增加到100用户
        (90, 150, 15),  # 接下来30秒增加到150用户
        (120, 200, 20),  # 接下来30秒增加到200用户
        (180, 200, 0),  # 保持200用户60秒
        (210, 100, -10),  # 30秒内减少到100用户
        (240, 0, -10),  # 30秒内减少到0用户
    ]
    
    def tick(self):
        """返回当前阶段的用户数和生成速率"""
        run_time = self.get_run_time()
        
        for stage in self.stages:
            if run_time < stage[0]:
                duration = stage[0] - run_time
                return (stage[1], stage[2])
        
        return None

if __name__ == "__main__":
    print("高并发测试脚本")
    print("使用方法:")
    print("1. 确保后端服务正在运行 (http://127.0.0.1:8000)")
    print("2. 运行命令: locust -f test_load.py")
    print("3. 在浏览器中打开 http://localhost:8089 开始测试")
    print("\n或者使用命令行模式:")
    print("locust -f test_load.py --headless -u 200 -r 20 -t 4m")
    print("-u: 用户数")
    print("-r: 每秒生成的用户数")
    print("-t: 测试持续时间")
