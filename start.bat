@echo off

echo 正在启动AI知识学习与智能测评系统...

REM 启动后端服务
start "Backend Server" powershell -Command "cd backend; python -m uvicorn main:app --reload --port 8000"

REM 等待后端服务启动
echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

REM 启动前端服务
start "Frontend Server" powershell -Command "cd frontend; npm run dev"

REM 等待前端服务启动
echo 等待前端服务启动...
timeout /t 10 /nobreak >nul

REM 打开浏览器访问前端页面
echo 打开浏览器访问前端页面...
start http://localhost:3000

echo 系统启动完成！
echo 后端服务地址: http://localhost:8000
echo 前端服务地址: http://localhost:3000
echo 按任意键退出...
pause >nul
