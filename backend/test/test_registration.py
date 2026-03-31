"""
用户注册安全校验测试脚本
"""
import sys
sys.path.append('.')

from app.schemas.user import UserCreate
from app.utils.validators import UserValidator, validate_user_registration
from pydantic import ValidationError

def test_username_validation():
    """测试用户名验证"""
    print("=" * 50)
    print("测试用户名验证")
    print("=" * 50)
    
    test_cases = [
        ("testuser", True, "正常用户名"),
        ("ab", False, "太短（少于3字符）"),
        ("a" * 21, False, "太长（超过20字符）"),
        ("1user", False, "以数字开头"),
        ("test-user", False, "包含连字符"),
        ("test@user", False, "包含特殊字符@"),
        ("admin", False, "保留关键字"),
        ("ADMIN", False, "保留关键字（大写）"),
        ("test_user", True, "带下划线的用户名"),
        ("测试用户", True, "中文用户名"),
        ("", False, "空用户名"),
    ]
    
    for username, expected, description in test_cases:
        is_valid, message = UserValidator.validate_username(username)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {description}: '{username}' -> {message}")
    
    print()

def test_password_validation():
    """测试密码验证"""
    print("=" * 50)
    print("测试密码验证")
    print("=" * 50)
    
    test_cases = [
        ("Test@1234", True, "强密码"),
        ("12345678", False, "纯数字"),
        ("password", False, "纯小写字母"),
        ("PASSWORD", False, "纯大写字母"),
        ("Test1234", False, "缺少特殊字符"),
        ("test@1234", False, "缺少大写字母"),
        ("TEST@1234", False, "缺少小写字母"),
        ("Test@abcd", False, "缺少数字"),
        ("Test 1234", False, "包含空格"),
        ("Test@1", False, "太短（少于8字符）"),
        ("Test@12345678901234567890123456789012345678901234567890" 
         "12345678901234567890123456789012345678901234567890", False, "太长（超过128字符）"),
        ("password", False, "常见弱密码"),
    ]
    
    for password, expected, description in test_cases:
        is_valid, message = UserValidator.validate_password(password)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {description}: '{password[:20]}...' -> {message}")
    
    print()

def test_email_validation():
    """测试邮箱验证"""
    print("=" * 50)
    print("测试邮箱验证")
    print("=" * 50)
    
    test_cases = [
        ("user@example.com", True, "正常邮箱"),
        ("user@tempmail.com", False, "临时邮箱"),
        ("user@yopmail.com", False, "临时邮箱"),
        ("user@gmail.com", True, "Gmail邮箱"),
        ("user@qq.com", True, "QQ邮箱"),
    ]
    
    for email, expected, description in test_cases:
        is_valid, message = UserValidator.validate_email_domain(email)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {description}: '{email}' -> {message}")
    
    print()

def test_xss_sanitization():
    """测试XSS清理"""
    print("=" * 50)
    print("测试XSS清理")
    print("=" * 50)
    
    test_cases = [
        ("<script>alert(1)</script>", "", "Script标签"),
        ("javascript:alert(1)", "alert(1)", "JavaScript协议"),
        ("<img src=x onerror=alert(1)>", "<img src=x alert(1)>", "事件处理器"),
        ("正常用户名", "正常用户名", "正常文本"),
        ("admin", "admin", "保留字"),
    ]
    
    for input_str, expected, description in test_cases:
        cleaned = UserValidator.sanitize_input(input_str)
        status = "✓" if cleaned == expected else "✗"
        print(f"{status} {description}:")
        print(f"  原始: {input_str}")
        print(f"  清理: {cleaned}")
    
    print()

def test_pydantic_validation():
    """测试Pydantic模型验证"""
    print("=" * 50)
    print("测试Pydantic模型验证")
    print("=" * 50)
    
    # 测试有效数据
    try:
        user = UserCreate(
            username="testuser",
            email="test@example.com",
            password="Test@1234"
        )
        print("✓ 有效数据通过验证")
        print(f"  用户名: {user.username}")
        print(f"  邮箱: {user.email}")
    except ValidationError as e:
        print(f"✗ 有效数据验证失败: {e}")
    
    # 测试无效数据
    invalid_cases = [
        {
            "username": "ad",
            "email": "test@example.com",
            "password": "Test@1234"
        },
        {
            "username": "admin",
            "email": "test@example.com",
            "password": "Test@1234"
        },
        {
            "username": "testuser",
            "email": "test@tempmail.com",
            "password": "Test@1234"
        },
        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345678"
        },
    ]
    
    for i, data in enumerate(invalid_cases, 1):
        try:
            user = UserCreate(**data)
            print(f"✗ 无效数据{i}应该被拒绝，但通过了验证")
        except ValidationError as e:
            print(f"✓ 无效数据{i}被正确拒绝")
            print(f"  错误: {e.errors()[0]['msg']}")
    
    print()

def test_registration_limiter():
    """测试注册频率限制"""
    print("=" * 50)
    print("测试注册频率限制")
    print("=" * 50)
    
    from app.utils.validators import RegistrationLimiter
    
    limiter = RegistrationLimiter()
    
    # 测试IP限制
    ip = "192.168.1.1"
    is_allowed, message = limiter.check_ip_limit(ip)
    print(f"✓ IP首次注册: {message}")
    
    # 记录多次注册
    for i in range(5):
        limiter.record_ip_registration(ip)
    
    is_allowed, message = limiter.check_ip_limit(ip)
    print(f"✓ IP多次注册后: {message}")
    
    # 测试邮箱限制
    email = "test@example.com"
    is_allowed, message = limiter.check_email_limit(email)
    print(f"✓ 邮箱首次注册: {message}")
    
    limiter.record_email_registration(email)
    is_allowed, message = limiter.check_email_limit(email)
    print(f"✓ 邮箱重复注册: {message}")
    
    print()

def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("用户注册安全校验测试")
    print("=" * 50 + "\n")
    
    test_username_validation()
    test_password_validation()
    test_email_validation()
    test_xss_sanitization()
    test_pydantic_validation()
    test_registration_limiter()
    
    print("=" * 50)
    print("测试完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()