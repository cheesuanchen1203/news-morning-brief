# 📰 新闻早报助手

智能新闻早报自动化助手，每天自动抓取全球14家权威媒体新闻，智能分类并生成摘要。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-brightgreen.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)

## ✨ 功能特性

- 🌍 **全球新闻源**：覆盖14家国内外权威媒体
- 🤖 **智能分类**：自动分类为科技、经济、政治/社会
- 📝 **智能摘要**：每条新闻自动生成30-50字摘要
- 💬 **对话交互**：自然语言交互，使用便捷
- 🎨 **Web界面**：美观的Web界面，支持浏览器访问
- 🚀 **多种部署**：支持本地、Docker、云平台部署
- 📡 **API接口**：提供RESTful API，方便集成

## 📂 新闻源覆盖

### 科技类
- 36氪
- IT之家
- TechCrunch
- The Verge

### 经济类
- 华尔街见闻
- 财联社
- 彭博社（Bloomberg）
- 路透社（Reuters）
- 华尔街日报（WSJ）
- 金融时报（FT）

### 政治/社会类
- 澎湃新闻
- BBC新闻
- CNN
- 纽约时报（NYT）

## 🚀 快速开始

### 方式一：Docker部署（推荐）

```bash
# 克隆项目
git clone https://github.com/cheesuanchen1203/news-morning-brief.git
cd news-morning-brief

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入API密钥

# 启动服务
docker-compose up -d

# 访问应用
# 打开浏览器访问 http://localhost:8000
```

### 方式二：本地部署

```bash
# 克隆项目
git clone https://github.com/cheesuanchen1203/news-morning-brief.git
cd news-morning-brief

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件

# 启动服务
./scripts/http_run.sh -p 8000

# 访问应用
# 打开浏览器访问 http://localhost:8000
```

## 💬 使用示例

### Web界面使用

1. 访问 http://localhost:8000
2. 输入 "今天新闻早报" 或点击快捷按钮
3. 查看生成的新闻早报

### API调用示例

```bash
# 健康检查
curl http://localhost:8000/health

# 获取新闻早报
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "query": "今天新闻早报",
    "session_id": "12345"
  }'
```

### Python调用示例

```python
import requests

# 发送请求
response = requests.post(
    "http://localhost:8000/run",
    json={
        "query": "今天新闻早报",
        "session_id": "12345"
    }
)

# 获取结果
result = response.json()
print(result['content'])
```

## 📦 项目结构

```
.
├── config/                   # 配置文件
│   └── agent_llm_config.json # 模型配置和系统提示词
├── src/                      # 源代码
│   ├── agents/               # Agent代码
│   │   └── agent.py         # Agent核心逻辑
│   ├── tools/               # 工具定义
│   │   └── news_scraper.py # 新闻抓取工具
│   ├── storage/             # 记忆存储
│   ├── main.py             # HTTP服务入口
│   └── utils/              # 工具函数
├── web/                     # Web界面
│   └── index.html          # 前端页面
├── scripts/                 # 部署脚本
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── requirements.txt        # Python依赖
├── .env.example           # 环境变量模板
├── DEPLOYMENT.md          # 部署指南
└── README.md              # 项目说明
```

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置以下变量：

```env
# Coze Workload Identity API Key
COZE_WORKLOAD_IDENTITY_API_KEY=your_api_key_here

# Coze Integration Model Base URL
COZE_INTEGRATION_MODEL_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

### 模型配置

在 `config/agent_llm_config.json` 中配置模型参数：

```json
{
  "config": {
    "model": "doubao-seed-1-6-251015",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_completion_tokens": 10000,
    "timeout": 600,
    "thinking": "disabled"
  }
}
```

## 🌐 部署到云平台

### Railway

```bash
railway login
railway init
railway up
```

### Render

连接GitHub仓库到Render，配置构建命令和启动命令。

### Vercel

```bash
vercel
```

更多部署方式请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 📡 API文档

启动服务后，访问以下地址查看完整API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要API端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | Web界面 |
| `/health` | GET | 健康检查 |
| `/run` | POST | 同步对话 |
| `/stream_run` | POST | 流式对话 |
| `/v1/chat/completions` | POST | OpenAI兼容接口 |

## 🔍 故障排查

### 服务无法启动

```bash
# 检查端口占用
lsof -i :8000

# 查看日志
tail -f logs/app.log
```

### 环境变量未生效

```bash
# 重新加载.env
source .env

# 检查环境变量
echo $COZE_WORKLOAD_IDENTITY_API_KEY
```

### Docker容器问题

```bash
# 查看容器日志
docker logs -f news-bot

# 重建容器
docker-compose up -d --build
```

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📝 更新日志

### v1.0.0 (2026-01-15)

- ✅ 初始版本发布
- 🌍 支持14家国内外新闻源
- 🤖 智能分类和摘要功能
- 💬 Web界面和API接口
- 🚀 Docker和云平台部署支持

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢以下开源项目：

- [LangChain](https://github.com/langchain-ai/langchain)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## 📮 联系方式

- GitHub: https://github.com/cheesuanchen1203/news-morning-brief
- Issues: https://github.com/cheesuanchen1203/news-morning-brief/issues

---

**⭐ 如果这个项目对你有帮助，请给个Star！**
