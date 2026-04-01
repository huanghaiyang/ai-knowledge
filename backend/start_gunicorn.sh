#!/bin/bash

# 加载环境变量
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | xargs)
fi

# 从环境变量中获取端口，默认8000
PORT=${BACKEND_PORT:-8000}

# 使用Gunicorn启动应用，使用默认的sync worker
gunicorn -w 4 --bind $BACKEND_HOST:$PORT main:app
