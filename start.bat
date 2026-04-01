@echo off

echo 正在启动AI知识学习与智能测评系统...

REM 使用PowerShell读取配置文件
for /f "delims=" %%i in ('powershell -Command "$config = Get-Content -Path 'config.json' -Raw | ConvertFrom-Json; Write-Output $config.backend.port"') do set BACKEND_PORT=%%i

for /f "delims=" %%i in ('powershell -Command "$config = Get-Content -Path 'config.json' -Raw | ConvertFrom-Json; Write-Output $config.frontend.port"') do set FRONTEND_PORT=%%i

for /f "delims=" %%i in ('powershell -Command "$config = Get-Content -Path 'config.json' -Raw | ConvertFrom-Json; $protocol = $config.frontend.protocol; if (!$protocol) { $protocol = 'http' }; $host = $config.frontend.host; $port = $config.frontend.port; Write-Output ($protocol + '://' + $host + ':' + $port)"') do set FRONTEND_URL=%%i

for /f "delims=" %%i in ('powershell -Command "$config = Get-Content -Path 'config.json' -Raw | ConvertFrom-Json; $protocol = $config.backend.protocol; if (!$protocol) { $protocol = 'http' }; $host = $config.backend.host; $port = $config.backend.port; Write-Output ($protocol + '://' + $host + ':' + $port)"') do set BACKEND_URL=%%i

REM 启动后端服务
start "Backend Server" powershell -Command "cd backend; python -m uvicorn main:app --reload --port %BACKEND_PORT%"

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
start %FRONTEND_URL%

echo 系统启动完成！
echo 后端服务地址: %BACKEND_URL%
echo 前端服务地址: %FRONTEND_URL%
echo 按任意键退出...
pause >nul
