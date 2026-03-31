@echo off

echo 正在停止AI知识学习与智能测评系统...

REM 停止后端服务（uvicorn）
echo 停止后端服务...
taskkill /F /IM uvicorn.exe >nul 2>&1

REM 停止前端服务（npm）
echo 停止前端服务...
taskkill /F /IM node.exe >nul 2>&1

echo 系统停止完成！
echo 按任意键退出...
pause >nul
