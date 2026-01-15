# 🚀 新闻早报助手 - 部署指南

本文档提供新闻早报助手的完整部署指南，支持多种部署方式。

## 📋 目录

- [本地部署](#本地部署)
- [Docker部署](#docker部署)
- [云平台部署](#云平台部署)
- [API使用说明](#api使用说明)

---

## 🖥️ 本地部署

### 前置要求

- Python 3.11+
- pip

### 部署步骤

1. **克隆项目**
```bash
git clone https://github.com/cheesuanchen1203/news-morning-brief.git
cd news-morning-brief
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：
```env
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here
COZE_INTEGRATION_MODEL_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

4. **启动服务**
```bash
# 使用启动脚本
./scripts/http_run.sh -p 8000

# 或直接使用Python
python src/main.py -m http -p 8000
```

5. **访问应用**

打开浏览器访问：http://localhost:8000

---

## 🐳 Docker部署

### 方式一：使用Docker命令

1. **构建镜像**
```bash
docker build -t news-bot:latest .
```

2. **运行容器**
```bash
docker run -d \
  -p 8000:8000 \
  -e COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here \
  -e COZE_INTEGRATION_MODEL_BASE_URL=https://ark.cn-beijing.volces.com/api/v3 \
  --name news-bot \
  news-bot:latest
```

3. **查看日志**
```bash
docker logs -f news-bot
```

### 方式二：使用Docker Compose（推荐）

1. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，填入你的API密钥
```

2. **启动服务**
```bash
docker-compose up -d
```

3. **访问应用**

打开浏览器访问：http://localhost:8000

4. **停止服务**
```bash
docker-compose down
```

5. **查看日志**
```bash
docker-compose logs -f
```

---

## ☁️ 云平台部署

### 方式一：Railway（推荐）

1. **准备代码**
```bash
git clone https://github.com/cheesuanchen1203/news-morning-brief.git
cd news-morning-brief
```

2. **连接Railway**
```bash
# 安装Railway CLI
npm install -g @railway/cli

# 登录Railway
railway login

# 初始化项目
railway init

# 添加环境变量
railway variables set COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here
railway variables set COZE_INTEGRATION_MODEL_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 部署
railway up
```

3. **获取访问地址**

部署完成后，Railway会提供一个公开的URL。

### 方式二：Render

1. **连接GitHub**

在Render控制面板连接你的GitHub仓库。

2. **创建Web Service**

- 选择：Web Service
- 仓库：news-morning-brief
- 构建命令：`pip install -r requirements.txt`
- 启动命令：`python src/main.py -m http -p 8000`

3. **设置环境变量**

在Render的Environment Variables中添加：
- `COZE_WORKLOAD_IDENTITY_API_KEY`
- `COZE_INTEGRATION_MODEL_BASE_URL`

4. **部署**

点击Deploy，等待部署完成。

### 方式三：Vercel（Serverless）

1. **安装Vercel CLI**
```bash
npm install -g vercel
```

2. **部署**
```bash
vercel
```

3. **配置环境变量**

在Vercel Dashboard中添加环境变量。

### 方式四：腾讯云/阿里云服务器

1. **购买服务器**

购买云服务器（推荐配置：2核4G）

2. **安装Docker**
```bash
curl -fsSL https://get.docker.com | sh
systemctl start docker
systemctl enable docker
```

3. **部署应用**
```bash
git clone https://github.com/cheesuanchen1203/news-morning-brief.git
cd news-morning-brief

cp .env.example .env
# 编辑.env文件

docker-compose up -d
```

4. **配置域名和SSL**

使用Nginx配置反向代理和SSL证书。

---

## 📡 API使用说明

### 健康检查

```bash
GET /health
```

响应：
```json
{
  "status": "ok",
  "message": "Service is running"
}
```

### 运行对话（同步）

```bash
POST /run
Content-Type: application/json

{
  "query": "今天新闻早报",
  "session_id": "12345"
}
```

响应：
```json
{
  "content": "新闻早报内容...",
  "run_id": "abc123"
}
```

### 运行对话（流式）

```bash
POST /stream_run
Content-Type: application/json

{
  "query": "今天新闻早报",
  "session_id": "12345"
}
```

响应：Server-Sent Events (SSE) 流

### OpenAI兼容接口

```bash
POST /v1/chat/completions
Content-Type: application/json

{
  "model": "doubao-seed-1-6-251015",
  "messages": [
    {"role": "user", "content": "今天新闻早报"}
  ]
}
```

### 取消执行

```bash
POST /cancel/{run_id}
```

---

## 🔧 故障排查

### 问题1：无法连接到后端服务

**解决方案**：
- 检查服务是否正在运行：`ps aux | grep python`
- 检查端口是否被占用：`lsof -i :8000`
- 查看日志：`tail -f logs/app.log`

### 问题2：环境变量未设置

**解决方案**：
```bash
# 检查环境变量
echo $COZE_WORKLOAD_IDENTITY_API_KEY

# 重新加载.env文件
source .env
```

### 问题3：Docker容器启动失败

**解决方案**：
```bash
# 查看容器日志
docker logs news-bot

# 重新构建镜像
docker build -t news-bot:latest .

# 清理并重启
docker-compose down
docker-compose up -d --build
```

### 问题4：网络请求失败

**解决方案**：
- 检查防火墙设置
- 确保可以访问外部API
- 检查代理配置

---

## 📊 监控和日志

### 查看实时日志

```bash
# Docker环境
docker logs -f news-bot

# 本地环境
tail -f logs/app.log
```

### 日志文件位置

- 应用日志：`logs/app.log`
- 错误日志：`logs/error.log`

---

## 🔒 安全建议

1. **不要将.env文件提交到Git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **使用强密码保护API密钥**

3. **配置HTTPS**
   - 使用Nginx反向代理
   - 配置SSL证书（Let's Encrypt）

4. **限制访问频率**
   - 使用API网关
   - 实现速率限制

5. **定期更新依赖**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

---

## 📈 性能优化

1. **增加缓存**

2. **使用CDN加速静态资源**

3. **配置负载均衡**

4. **优化数据库查询**

---

## 🆘 获取帮助

- GitHub Issues: https://github.com/cheesuanchen1203/news-morning-brief/issues
- 查看API文档: http://localhost:8000/docs

---

## 📝 更新日志

- v1.0.0 (2026-01-15): 初始版本发布
- 支持Docker部署
- 添加Web界面
- 支持多种云平台部署
