import re
from typing import Tuple, List, Optional
from flask import abort

class UserValidator:
    """用户数据验证器"""
    
    # 密码策略配置
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    
    # 禁止的用户名（保留关键字）
    RESERVED_USERNAMES = {
        'admin', 'administrator', 'root', 'system', 'test', 'guest',
        'user', 'manager', 'support', 'service', 'api', 'web',
        'www', 'mail', 'ftp', 'localhost', '127.0.0.1'
    }
    
    # 禁止的邮箱域名
    BLOCKED_EMAIL_DOMAINS = {
        'tempmail.com', '10minutemail.com', 'guerrillamail.com',
        'mailinator.com', 'yopmail.com', 'throwawaymail.com'
    }
    
    @classmethod
    def validate_username(cls, username: str) -> Tuple[bool, str]:
        """
        验证用户名
        规则：
        1. 长度3-20个字符
        2. 只能包含字母、数字、下划线、中文
        3. 不能以数字开头
        4. 不能是保留关键字
        """
        if not username:
            return False, "用户名不能为空"
        
        if len(username) < cls.MIN_USERNAME_LENGTH:
            return False, f"用户名长度不能少于{cls.MIN_USERNAME_LENGTH}个字符"
        
        if len(username) > cls.MAX_USERNAME_LENGTH:
            return False, f"用户名长度不能超过{cls.MAX_USERNAME_LENGTH}个字符"
        
        # 检查是否以数字开头
        if username[0].isdigit():
            return False, "用户名不能以数字开头"
        
        # 检查是否包含非法字符（只允许字母、数字、下划线、中文）
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
            return False, "用户名只能包含字母、数字、下划线和中文"
        
        # 检查是否为保留关键字（不区分大小写）
        if username.lower() in cls.RESERVED_USERNAMES:
            return False, "该用户名已被保留，不能使用"
        
        return True, "用户名验证通过"
    
    @classmethod
    def validate_password(cls, password: str) -> Tuple[bool, str]:
        """
        验证密码强度
        规则：
        1. 长度8-128个字符
        2. 必须包含至少一个大写字母
        3. 必须包含至少一个小写字母
        4. 必须包含至少一个数字
        5. 必须包含至少一个特殊字符
        6. 不能包含空格
        """
        if not password:
            return False, "密码不能为空"
        
        if len(password) < cls.MIN_PASSWORD_LENGTH:
            return False, f"密码长度不能少于{cls.MIN_PASSWORD_LENGTH}个字符"
        
        if len(password) > cls.MAX_PASSWORD_LENGTH:
            return False, f"密码长度不能超过{cls.MAX_PASSWORD_LENGTH}个字符"
        
        # 检查是否包含空格
        if ' ' in password:
            return False, "密码不能包含空格"
        
        # 检查是否包含大写字母
        if not re.search(r'[A-Z]', password):
            return False, "密码必须包含至少一个大写字母"
        
        # 检查是否包含小写字母
        if not re.search(r'[a-z]', password):
            return False, "密码必须包含至少一个小写字母"
        
        # 检查是否包含数字
        if not re.search(r'\d', password):
            return False, "密码必须包含至少一个数字"
        
        # 检查是否包含特殊字符
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            return False, "密码必须包含至少一个特殊字符(!@#$%^&*等)"
        
        # 检查常见弱密码
        common_passwords = ['12345678', 'password', 'qwerty', 'abc123', 'letmein']
        if password.lower() in common_passwords:
            return False, "密码过于简单，请使用更复杂的密码"
        
        return True, "密码强度符合要求"
    
    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, str]:
        """
        验证邮箱格式
        规则：
        1. 必须包含@符号
        2. @前后必须有内容
        3. 域名部分必须包含点
        4. 不能是临时邮箱或禁止的域名
        """
        if not email:
            return False, "邮箱不能为空"
        
        # 检查邮箱格式
        if '@' not in email:
            return False, "邮箱格式不正确，缺少@符号"
        
        try:
            local_part, domain = email.split('@')
            if not local_part or not domain:
                return False, "邮箱格式不正确，@前后必须有内容"
            
            if '.' not in domain:
                return False, "邮箱格式不正确，域名部分必须包含点"
            
            # 检查是否为临时邮箱或禁止的域名
            if domain.lower() in cls.BLOCKED_EMAIL_DOMAINS:
                return False, "该邮箱域名不允许注册"
            
            return True, "邮箱验证通过"
        except Exception:
            return False, "邮箱格式不正确"
    
    @classmethod
    def validate_email_domain(cls, email: str) -> Tuple[bool, str]:
        """
        验证邮箱域名
        检查是否为临时邮箱或禁止的域名
        """
        try:
            domain = email.split('@')[1].lower()
            if domain in cls.BLOCKED_EMAIL_DOMAINS:
                return False, "该邮箱域名不允许注册"
            return True, "邮箱域名验证通过"
        except IndexError:
            return False, "邮箱格式不正确"
    
    @classmethod
    def sanitize_input(cls, input_str: str) -> str:
        """
        清理用户输入，防止XSS攻击
        """
        if not input_str:
            return input_str
        
        # 移除潜在的XSS攻击向量
        dangerous_patterns = [
            (r'<script[^>]*>.*?</script>', ''),  # 移除script标签
            (r'javascript:', ''),  # 移除javascript协议
            (r'on\w+\s*=', ''),  # 移除事件处理器
            (r'<iframe[^>]*>.*?</iframe>', ''),  # 移除iframe
            (r'<object[^>]*>.*?</object>', ''),  # 移除object标签
            (r'<embed[^>]*>.*?</embed>', ''),  # 移除embed标签
        ]
        
        cleaned = input_str
        for pattern, replacement in dangerous_patterns:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        return cleaned.strip()


class RegistrationLimiter:
    """注册频率限制器"""
    
    def __init__(self):
        # 存储IP注册记录: {ip: [timestamp1, timestamp2, ...]}
        self._ip_records = {}
        # 存储邮箱注册记录: {email: timestamp}
        self._email_records = {}
        # 同一IP每小时最多注册次数
        self.MAX_REGISTRATION_PER_HOUR = 5
        # 同一邮箱注册间隔（秒）
        self.EMAIL_COOLDOWN = 300  # 5分钟
    
    def check_ip_limit(self, ip_address: str) -> Tuple[bool, str]:
        """
        检查IP注册频率限制
        """
        import time
        current_time = time.time()
        one_hour_ago = current_time - 3600
        
        # 清理过期记录
        if ip_address in self._ip_records:
            self._ip_records[ip_address] = [
                ts for ts in self._ip_records[ip_address] 
                if ts > one_hour_ago
            ]
        else:
            self._ip_records[ip_address] = []
        
        # 检查注册次数
        if len(self._ip_records[ip_address]) >= self.MAX_REGISTRATION_PER_HOUR:
            return False, f"该IP注册次数过多，请稍后再试"
        
        return True, "IP验证通过"
    
    def record_ip_registration(self, ip_address: str):
        """记录IP注册"""
        import time
        if ip_address not in self._ip_records:
            self._ip_records[ip_address] = []
        self._ip_records[ip_address].append(time.time())
    
    def check_email_limit(self, email: str) -> Tuple[bool, str]:
        """
        检查邮箱注册频率限制
        """
        import time
        current_time = time.time()
        
        if email in self._email_records:
            last_registration = self._email_records[email]
            if current_time - last_registration < self.EMAIL_COOLDOWN:
                remaining = int(self.EMAIL_COOLDOWN - (current_time - last_registration))
                return False, f"该邮箱注册过于频繁，请{remaining}秒后再试"
        
        return True, "邮箱频率验证通过"
    
    def record_email_registration(self, email: str):
        """记录邮箱注册"""
        import time
        self._email_records[email] = time.time()


# 创建全局注册限制器实例
registration_limiter = RegistrationLimiter()


def validate_user_registration(username: str, email: str, password: str, ip_address: str = None) -> None:
    """
    完整的用户注册验证
    如果验证失败，抛出abort异常
    """
    # 验证用户名
    is_valid, message = UserValidator.validate_username(username)
    if not is_valid:
        abort(400, description=message)
    
    # 验证密码
    is_valid, message = UserValidator.validate_password(password)
    if not is_valid:
        abort(400, description=message)
    
    # 验证邮箱域名
    is_valid, message = UserValidator.validate_email_domain(email)
    if not is_valid:
        abort(400, description=message)
    
    # 检查注册频率限制
    if ip_address:
        is_allowed, message = registration_limiter.check_ip_limit(ip_address)
        if not is_allowed:
            abort(429, description=message)
    
    is_allowed, message = registration_limiter.check_email_limit(email)
    if not is_allowed:
        abort(429, description=message)


def record_registration(ip_address: str, email: str) -> None:
    """记录注册信息用于频率限制"""
    if ip_address:
        registration_limiter.record_ip_registration(ip_address)
    registration_limiter.record_email_registration(email)


class KnowledgeValidator:
    """知识点验证器"""
    
    # 知识点标题长度限制
    MIN_TITLE_LENGTH = 2
    MAX_TITLE_LENGTH = 100
    
    # 知识点描述长度限制
    MAX_DESCRIPTION_LENGTH = 1000
    
    @classmethod
    def validate_title(cls, title: str) -> Tuple[bool, str]:
        """
        验证知识点标题
        """
        if not title:
            return False, "知识点标题不能为空"
        
        if len(title) < cls.MIN_TITLE_LENGTH:
            return False, f"知识点标题长度不能少于{cls.MIN_TITLE_LENGTH}个字符"
        
        if len(title) > cls.MAX_TITLE_LENGTH:
            return False, f"知识点标题长度不能超过{cls.MAX_TITLE_LENGTH}个字符"
        
        return True, "知识点标题验证通过"
    
    @classmethod
    def validate_description(cls, description: str) -> Tuple[bool, str]:
        """
        验证知识点描述
        """
        if description and len(description) > cls.MAX_DESCRIPTION_LENGTH:
            return False, f"知识点描述长度不能超过{cls.MAX_DESCRIPTION_LENGTH}个字符"
        
        return True, "知识点描述验证通过"


class QuestionValidator:
    """题目验证器"""
    
    # 题目内容长度限制
    MIN_CONTENT_LENGTH = 5
    MAX_CONTENT_LENGTH = 2000
    
    # 选项长度限制
    MAX_OPTIONS_LENGTH = 1000
    
    # 答案长度限制
    MAX_ANSWER_LENGTH = 500
    
    # 支持的题目类型
    SUPPORTED_QUESTION_TYPES = {
        'single_choice', 'multiple_choice', 'true_false',
        'fill_blank', 'short_answer', 'code'
    }
    
    # 支持的难度级别
    SUPPORTED_DIFFICULTY_LEVELS = {'easy', 'medium', 'hard'}
    
    @classmethod
    def validate_content(cls, content: str) -> Tuple[bool, str]:
        """
        验证题目内容
        """
        if not content:
            return False, "题目内容不能为空"
        
        if len(content) < cls.MIN_CONTENT_LENGTH:
            return False, f"题目内容长度不能少于{cls.MIN_CONTENT_LENGTH}个字符"
        
        if len(content) > cls.MAX_CONTENT_LENGTH:
            return False, f"题目内容长度不能超过{cls.MAX_CONTENT_LENGTH}个字符"
        
        return True, "题目内容验证通过"
    
    @classmethod
    def validate_options(cls, options: str) -> Tuple[bool, str]:
        """
        验证题目选项
        """
        if options and len(options) > cls.MAX_OPTIONS_LENGTH:
            return False, f"题目选项长度不能超过{cls.MAX_OPTIONS_LENGTH}个字符"
        
        return True, "题目选项验证通过"
    
    @classmethod
    def validate_answer(cls, answer: str) -> Tuple[bool, str]:
        """
        验证正确答案
        """
        if not answer:
            return False, "正确答案不能为空"
        
        if len(answer) > cls.MAX_ANSWER_LENGTH:
            return False, f"正确答案长度不能超过{cls.MAX_ANSWER_LENGTH}个字符"
        
        return True, "正确答案验证通过"
    
    @classmethod
    def validate_question_type(cls, question_type: str) -> Tuple[bool, str]:
        """
        验证题目类型
        """
        if not question_type:
            return False, "题目类型不能为空"
        
        if question_type not in cls.SUPPORTED_QUESTION_TYPES:
            return False, f"不支持的题目类型，支持的类型有：{', '.join(cls.SUPPORTED_QUESTION_TYPES)}"
        
        return True, "题目类型验证通过"
    
    @classmethod
    def validate_difficulty(cls, difficulty: str) -> Tuple[bool, str]:
        """
        验证难度级别
        """
        if not difficulty:
            return False, "难度级别不能为空"
        
        if difficulty not in cls.SUPPORTED_DIFFICULTY_LEVELS:
            return False, f"不支持的难度级别，支持的级别有：{', '.join(cls.SUPPORTED_DIFFICULTY_LEVELS)}"
        
        return True, "难度级别验证通过"