const { exec, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// 检查环境文件
if (!fs.existsSync('./backend/.env')) {
    console.log('创建后端环境配置文件...');
    const envContent = `# 数据库配置
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
OPENAI_API_KEY=your-openai-api-key-here`;
    fs.writeFileSync('./backend/.env', envContent);
    console.log('后端环境配置文件创建成功');
}

if (!fs.existsSync('./frontend/.env')) {
    console.log('创建前端环境配置文件...');
    const envContent = `# 前端环境配置
VITE_FRONTEND_PORT=3000
VITE_BACKEND_URL=http://localhost:8000`;
    fs.writeFileSync('./frontend/.env', envContent);
    console.log('前端环境配置文件创建成功');
}

// 读取环境变量
const dotenv = require('dotenv');
dotenv.config({ path: './backend/.env' });
dotenv.config({ path: './frontend/.env' });

const frontendPort = process.env.VITE_FRONTEND_PORT || 3000;
const backendPort = process.env.BACKEND_PORT || 8000;
const frontendUrl = `http://localhost:${frontendPort}`;
const backendUrl = `http://localhost:${backendPort}`;

console.log('正在启动AI知识学习与智能测评系统...');

// 检查Python环境
console.log('检查Python环境...');
exec('python --version', (error, stdout, stderr) => {
  if (error) {
    console.error('错误：未找到Python环境，请安装Python 3.7+');
    process.exit(1);
  }
  console.log(`Python版本: ${stdout.trim()}`);
  
  // 检查uvicorn是否安装
  console.log('检查uvicorn是否安装...');
  exec('python -m uvicorn --version', (error, stdout, stderr) => {
    if (error) {
      console.error('错误：未安装uvicorn，请先安装后端依赖');
      console.error('请执行：python -m pip install -r backend/requirements.txt');
      console.error('正在启动前端服务...');
      // 默认只启动前端服务，不需要用户输入
      startFrontend();
    } else {
      console.log(`uvicorn版本: ${stdout.trim()}`);
      startBackend();
    }
  });

  // 启动前端服务的函数
  function startFrontend() {
    // 检查前端依赖是否安装
    console.log('检查前端依赖是否安装...');
    exec('npm --version', (error, stdout, stderr) => {
      if (error) {
        console.error('警告：未找到npm环境，请安装Node.js以启动前端服务');
        console.error('前端服务将无法启动，但后端服务仍可正常运行');
        return;
      }
      console.log(`npm版本: ${stdout.trim()}`);
      
      // 检查vite是否安装（作为前端依赖是否安装的标志）
      console.log('检查前端依赖是否安装...');
      exec('npm list vite', { cwd: path.join(__dirname, 'frontend') }, (error, stdout, stderr) => {
        if (error) {
          console.log('前端依赖未安装，正在安装...');
          // 安装前端依赖
          const installProcess = spawn('npm', ['install'], {
            cwd: path.join(__dirname, 'frontend'),
            stdio: 'inherit',
            shell: true
          });
          
          installProcess.on('exit', (code) => {
            if (code === 0) {
              console.log('前端依赖安装成功');
              // 启动前端服务
              startFrontendService();
            } else {
              console.error('警告：前端依赖安装失败');
              console.error('前端服务将无法启动，但后端服务仍可正常运行');
              return;
            }
          });
        } else {
          console.log('前端依赖已安装');
          // 启动前端服务
          startFrontendService();
        }
      });
    });
  }

  // 启动前端服务的函数
  function startFrontendService() {
    console.log('启动前端服务...');
    const frontendProcess = spawn('npm', ['run', 'dev'], {
      cwd: path.join(__dirname, 'frontend'),
      stdio: 'inherit',
      shell: true
    });
    
    // 等待前端服务启动
    setTimeout(() => {
      console.log('前端服务已启动');
      
      // 打开浏览器访问前端页面
      console.log('打开浏览器访问前端页面...');
      // 使用child_process模块打开浏览器
      if (process.platform === 'win32') {
        exec(`start ${frontendUrl}`);
      } else if (process.platform === 'darwin') {
        exec(`open ${frontendUrl}`);
      } else {
        exec(`xdg-open ${frontendUrl}`);
      }
      
      console.log('前端服务启动完成！');
      console.log(`前端服务地址: ${frontendUrl}`);
      console.log('注意：后端服务未启动，部分功能可能无法使用');
    }, 10000); // 等待10秒
    
    // 处理进程退出
    process.on('SIGINT', () => {
      console.log('正在停止服务...');
      // 停止前端进程
      exec('taskkill /F /IM node.exe', (error, stdout, stderr) => {
        if (error) {
          console.log('前端服务可能已停止或不存在');
        } else {
          console.log('前端服务已停止');
        }
        process.exit();
      });
    });
  }

  // 启动后端服务的函数
  function startBackend() {
    
    // 启动后端服务
    console.log('启动后端服务...');
    const backendProcess = spawn('python', ['main.py'], {
      cwd: path.join(__dirname, 'backend'),
      stdio: 'inherit',
      shell: true
    });
    
    // 等待后端服务启动
    setTimeout(() => {
      console.log('后端服务已启动');
      console.log(`后端服务地址: ${backendUrl}`);
      console.log(`后端API文档: ${backendUrl}/docs`);
      
      // 检查前端依赖是否安装
      console.log('检查前端依赖是否安装...');
      exec('npm --version', (error, stdout, stderr) => {
        if (error) {
          console.error('警告：未找到npm环境，请安装Node.js以启动前端服务');
          console.error('前端服务将无法启动，但后端服务仍可正常运行');
          console.log('系统启动完成！');
          console.log(`后端服务地址: ${backendUrl}`);
          return;
        }
        console.log(`npm版本: ${stdout.trim()}`);
        
        // 启动前端服务
        console.log('启动前端服务...');
        const frontendProcess = spawn('npm', ['run', 'dev'], {
          cwd: path.join(__dirname, 'frontend'),
          stdio: 'inherit',
          shell: true
        });
        
        // 等待前端服务启动
        setTimeout(() => {
          console.log('前端服务已启动');
          
          // 打开浏览器访问前端页面
          console.log('打开浏览器访问前端页面...');
          // 使用child_process模块打开浏览器
          if (process.platform === 'win32') {
            exec(`start ${frontendUrl}`);
          } else if (process.platform === 'darwin') {
            exec(`open ${frontendUrl}`);
          } else {
            exec(`xdg-open ${frontendUrl}`);
          }
          
          console.log('系统启动完成！');
          console.log(`后端服务地址: ${backendUrl}`);
          console.log(`前端服务地址: ${frontendUrl}`);
        }, 10000); // 等待10秒
      });
    }, 5000); // 等待5秒
    
    // 处理进程退出
    process.on('SIGINT', () => {
      console.log('正在停止服务...');
      backendProcess.kill();
      // 停止前端进程
      exec('taskkill /F /IM node.exe', (error, stdout, stderr) => {
        if (error) {
          console.log('前端服务可能已停止或不存在');
        } else {
          console.log('前端服务已停止');
        }
        process.exit();
      });
    });
  }
});
