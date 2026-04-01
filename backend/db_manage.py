import os
import sys
import json
from dotenv import load_dotenv

try:
    import pg8000
except ImportError:
    print("错误: 缺少pg8000库")
    print("请执行: pip install pg8000")
    sys.exit(1)

# 读取配置文件
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
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

# 获取数据库连接信息
DB_USER = os.getenv("DB_USER", config['database']['user'])
DB_PASSWORD = os.getenv("DB_PASSWORD", config['database']['password'])
DB_HOST = os.getenv("DB_HOST", config['database']['host'])
DB_PORT = os.getenv("DB_PORT", config['database']['port'])
DB_NAME = os.getenv("DB_NAME", config['database']['name'])

# 检查配置是否完整
if not DB_USER:
    print("错误: 数据库用户名未设置")
    sys.exit(1)

if not DB_PASSWORD:
    print("错误: 数据库密码未设置")
    sys.exit(1)

if not DB_HOST:
    print("错误: 数据库主机未设置")
    sys.exit(1)

if not DB_PORT:
    print("错误: 数据库端口未设置")
    sys.exit(1)

if not DB_NAME:
    print("错误: 数据库名称未设置")
    sys.exit(1)

def create_database():
    """创建数据库"""
    print("正在创建数据库...")
    
    # 检查环境变量是否设置
    if not DB_USER or not DB_PASSWORD:
        print("错误: 数据库用户名或密码未设置")
        print("请在backend/.env文件中配置DB_USER和DB_PASSWORD")
        return
    
    try:
        # 连接到postgres默认数据库
        conn = pg8000.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"
        )
        conn.autocommit = True
        
        # 创建游标
        cursor = conn.cursor()
        
        # 检查数据库是否存在
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")
        exists = cursor.fetchone()
        
        if exists:
            print(f"数据库 {DB_NAME} 已存在")
        else:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"数据库 {DB_NAME} 创建成功")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        # 初始化表结构
        initialize_tables()
        
    except pg8000.InterfaceError as e:
        try:
            print(f"连接数据库失败: {e}")
        except UnicodeEncodeError:
            print("连接数据库失败: 无法显示错误信息（编码问题）")
        print("请确保PostgreSQL服务已启动，并且连接信息正确")
        print("提示: 检查PostgreSQL服务是否正在运行，端口是否正确")
    except pg8000.DatabaseError as e:
        try:
            print(f"数据库错误: {e}")
        except UnicodeEncodeError:
            print("数据库错误: 密码验证失败")
        print("提示: 检查用户名和密码是否正确，以及用户是否有创建数据库的权限")
    except Exception as e:
        try:
            print(f"错误: {e}")
        except UnicodeEncodeError:
            print("错误: 无法显示错误信息（编码问题）")
        print("请检查PostgreSQL配置和.env文件中的连接信息")

def initialize_tables():
    """初始化数据库表结构"""
    print("正在初始化表结构...")
    try:
        # 导入模型以确保表被创建
        from app.models import user, knowledge, question, answer
        from app.utils.database import Base, engine
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("表结构初始化成功")
    except Exception as e:
        print(f"表结构初始化失败: {e}")

def dump_database():
    """导出数据库"""
    print("正在导出数据库...")
    
    # 生成导出文件名
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_file = f"db_dump_{timestamp}.sql"
    dump_path = os.path.join(os.path.dirname(__file__), "backups", dump_file)
    
    # 创建备份目录
    os.makedirs(os.path.join(os.path.dirname(__file__), "backups"), exist_ok=True)
    
    try:
        # 连接到数据库
        conn = pg8000.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        conn.autocommit = True
        
        # 创建游标
        cursor = conn.cursor()
        
        # 导出表结构和数据
        with open(dump_path, 'w', encoding='utf-8') as f:
            # 获取所有表
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
            """)
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                # 导出表结构（使用标准SQL）
                cursor.execute(f"""
                    SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = '{table_name}'
                    ORDER BY ordinal_position
                """)
                columns = cursor.fetchall()
                if columns:
                    f.write(f"-- Table: {table_name}\n")
                    f.write(f"CREATE TABLE {table_name} (\n")
                    column_defs = []
                    for col in columns:
                        col_name = col[0]
                        col_type = col[1]
                        col_length = col[2]
                        col_default = col[3]
                        col_nullable = col[4]
                        
                        # 构建列定义
                        col_def = f"    {col_name} {col_type}"
                        if col_length:
                            col_def += f"({col_length})"
                        if col_nullable == 'NO':
                            col_def += " NOT NULL"
                        if col_default:
                            col_def += f" DEFAULT {col_default}"
                        column_defs.append(col_def)
                    
                    # 添加主键约束（简化处理）
                    cursor.execute(f"""
                        SELECT column_name
                        FROM information_schema.key_column_usage
                        WHERE table_schema = 'public' AND table_name = '{table_name}' AND constraint_name LIKE '%_pkey'
                    """)
                    primary_keys = cursor.fetchall()
                    if primary_keys:
                        pk_columns = [pk[0] for pk in primary_keys]
                        column_defs.append(f"    PRIMARY KEY ({', '.join(pk_columns)})")
                    
                    f.write(',\n'.join(column_defs))
                    f.write('\n);\n\n')
                
                # 导出数据
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()
                if rows:
                    # 获取列名
                    columns = [desc[0] for desc in cursor.description]
                    columns_str = ', '.join(columns)
                    
                    f.write(f"-- Data for table: {table_name}\n")
                    for row in rows:
                        # 处理值
                        values = []
                        for value in row:
                            if value is None:
                                values.append('NULL')
                            elif isinstance(value, str):
                                # 转义单引号
                                escaped = value.replace("'", "''")
                                values.append(f"'{escaped}'")
                            else:
                                values.append(str(value))
                        values_str = ', '.join(values)
                        f.write(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
                    f.write('\n')
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print(f"数据库导出成功，文件: {dump_path}")
        
    except pg8000.InterfaceError as e:
        print(f"连接数据库失败: {e}")
        print("请确保PostgreSQL服务已启动，并且连接信息正确")
    except Exception as e:
        print(f"错误: {e}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python db_manage.py [create|dump]")
        print("  create: 创建数据库并初始化表结构")
        print("  dump: 导出数据库")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "create":
        create_database()
    elif command == "dump":
        dump_database()
    else:
        print(f"未知命令: {command}")
        print("用法: python db_manage.py [create|dump]")
        sys.exit(1)

if __name__ == "__main__":
    main()
