const { exec } = require('child_process');

console.log('正在停止AI知识学习与智能测评系统...');

// 停止后端服务（uvicorn）
console.log('停止后端服务...');
exec('taskkill /F /IM uvicorn.exe', (error, stdout, stderr) => {
  if (error) {
    console.log('后端服务可能已停止或不存在');
  } else {
    console.log('后端服务已停止');
  }
  
  // 停止前端服务（node）
  console.log('停止前端服务...');
  exec('taskkill /F /IM node.exe', (error, stdout, stderr) => {
    if (error) {
      console.log('前端服务可能已停止或不存在');
    } else {
      console.log('前端服务已停止');
    }
    
    console.log('系统停止完成！');
    process.exit();
  });
});
