Write-Host "开始安装依赖..." -ForegroundColor Green

# 检查是否安装了Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未安装 Node.js" -ForegroundColor Red
    Write-Host "请先安装 Node.js: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# 检查是否安装了npm
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未安装 npm" -ForegroundColor Red
    Write-Host "请检查 Node.js 安装是否完整" -ForegroundColor Yellow
    exit 1
}

try {
    # 使用淘宝镜像安装依赖
    Write-Host "正在使用淘宝镜像安装依赖..." -ForegroundColor Cyan
    npm install --registry=https://registry.npmmirror.com

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n依赖安装成功!" -ForegroundColor Green
        Write-Host "现在可以运行 'npm run dev' 启动开发服务器" -ForegroundColor Cyan
    }
    else {
        Write-Host "`n依赖安装失败!" -ForegroundColor Red
        Write-Host "请检查网络连接或尝试使用管理员权限运行" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "`n安装过程中出现错误:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
finally {
    Write-Host "`n按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 