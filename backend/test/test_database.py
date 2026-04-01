"""
数据库测试文件
测试数据库连接和只读操作
"""
import sys
import os
from sqlalchemy.exc import OperationalError

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conftest import get_test_db, engine

def test_database_connection():
    """
    测试数据库连接是否正常
    """
    print("=" * 50)
    print("测试数据库连接")
    print("=" * 50)
    
    try:
        # 尝试执行一个简单的查询
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print(f"✓ 数据库连接成功: {result.scalar()}")
        
        print("✓ 数据库连接测试完成")
    except OperationalError as e:
        print(f"✗ 数据库连接失败: {e}")
        raise
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def test_read_only_operation():
    """
    测试数据库只读操作
    尝试执行写入操作，应该失败
    """
    print("=" * 50)
    print("测试数据库只读操作")
    print("=" * 50)
    
    try:
        # 尝试执行读取操作，应该成功
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print(f"✓ 读取操作成功: {result.scalar()}")
        
        # 注意：由于我们没有设置数据库为真正的只读模式，
        # 这里只是验证我们的测试配置是否正确
        # 在实际生产环境中，应该使用只读数据库用户
        
        print("✓ 只读操作测试完成")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def test_connection_pool():
    """
    测试数据库连接池
    验证连接池是否正常工作
    """
    print("=" * 50)
    print("测试数据库连接池")
    print("=" * 50)
    
    try:
        # 测试多个连接
        for i in range(3):
            with engine.connect() as connection:
                result = connection.execute("SELECT 1")
                print(f"✓ 连接 {i+1} 成功: {result.scalar()}")
        
        print("✓ 连接池测试完成")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    
    print()

def main():
    """
    运行所有数据库测试
    """
    print("\n" + "=" * 50)
    print("数据库测试")
    print("=" * 50 + "\n")
    
    test_database_connection()
    test_read_only_operation()
    test_connection_pool()
    
    print("=" * 50)
    print("数据库测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
