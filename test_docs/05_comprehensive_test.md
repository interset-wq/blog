# 综合测试文档

本文档综合测试所有Markdown和GFM特性，模拟真实博客文章。

# GitHub Issues博客系统开发指南

## 项目概述

这是一个基于GitHub Issues的静态博客系统，通过GitHub Actions自动将Issues渲染为静态网站。

### 核心特性

- **完全自动化**：Issue变更自动触发构建
- **静态生成**：纯HTML/CSS/JS，无需后端
- **GFM支持**：完整的GitHub Flavored Markdown
- **响应式设计**：支持移动端访问
- **主题切换**：深色/浅色主题

## 快速开始

### 环境准备

首先确保安装了以下工具：

```bash
# 检查Python版本
python --version  # 需要3.10+

# 检查Git版本
git --version

# 检查Node.js版本（可选）
node --version
```

### 项目克隆

```bash
# 克隆项目
git clone https://github.com/your-username/github-issues-blog.git
cd github-issues-blog

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 配置说明

### 环境变量

创建 `.env` 文件：

```env
# GitHub配置
GITHUB_OWNER=your-username
GITHUB_REPO=your-repo
GITHUB_TOKEN=your-github-token

# 博客配置
BLOG_TITLE=我的博客
BLOG_DESCRIPTION=基于GitHub Issues的博客
BLOG_URL=https://your-username.github.io/your-repo/
BLOG_LANGUAGE=zh-CN

# 文章配置
ARTICLE_LABEL=blog
ARTICLES_PER_PAGE=10
```

### 配置文件

编辑 `renderer/config.py`：

```python
# Markdown配置
MARKDOWN_EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "tables",
    "toc",
    "nl2br",
    "smarty",
    "wikilinks",
    "meta",
    "abbr",
    "attr_list",
    "def_list",
    "footnotes",
    "md_in_html",
]

# 代码高亮配置
CODE_HILITE_STYLE = "monokai"
CODE_HILITE_LINENOS = False

# RSS配置
RSS_ENABLED = True
RSS_FILE = "feed.xml"
```

## 使用指南

### 发布文章

1. **创建Issue**：在GitHub仓库中创建新Issue
2. **添加标签**：添加 `blog` 标签
3. **编写内容**：使用Markdown/GFM语法编写
4. **提交Issue**：保存后自动触发构建

### 文章格式

```markdown
# 文章标题

## 简介

这是文章简介，支持**粗体**和*斜体*。

## 代码示例

```python
def hello():
    print("Hello, World!")
```

## 任务列表

- [x] 完成功能开发
- [ ] 编写测试用例
- [ ] 部署到生产环境

## 表格

| 功能 | 状态 | 说明 |
|------|------|------|
| Markdown解析 | ✅ | 支持标准语法 |
| GFM扩展 | ✅ | 任务列表、表格等 |
| 代码高亮 | ✅ | 支持多种语言 |

## 引用

> 重要的事情说三遍：
> 测试！测试！测试！

## 链接

访问 [GitHub](https://github.com) 获取更多信息。
```

## 技术架构

### 系统架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Issue  │───▶│  GitHub Actions │───▶│   Static Site   │
│   (Markdown)    │    │   (Renderer)    │    │   (HTML/CSS)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML/CSS/JS | 原生技术，无CDN |
| 模板 | Jinja2 | Python模板引擎 |
| 渲染 | Python | Markdown解析 |
| API | PyGitHub | GitHub官方库 |
| 部署 | GitHub Pages | 静态托管 |
| CI/CD | GitHub Actions | 自动化构建 |

### 数据流

1. **输入**：GitHub Issue（Markdown格式）
2. **处理**：
   - PyGitHub获取Issue内容
   - Markdown解析器转换
   - Jinja2模板渲染
3. **输出**：静态HTML文件
4. **部署**：推送到gh-pages分支

## 开发指南

### 本地开发

```bash
# 运行测试
python test_renderer.py

# 本地预览
cd output
python -m http.server 8000

# 访问 http://localhost:8000
```

### 添加新功能

1. **创建分支**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **开发功能**
   - 修改 `renderer/` 目录下的文件
   - 更新 `templates/` 模板
   - 添加 `static/` 静态资源

3. **测试验证**
   ```bash
   python test_renderer.py
   ```

4. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/new-feature
   ```

### 代码规范

#### Python代码规范

```python
# 使用类型提示
def process_article(article: dict) -> dict:
    """处理文章数据"""
    return {
        'title': article['title'],
        'content': article['body'],
        'tags': article['labels'],
    }

# 使用dataclass
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    id: int
    title: str
    content: str
    created_at: datetime
    tags: list[str]
```

#### JavaScript代码规范

```javascript
// 使用ES6+语法
const processArticles = (articles) => {
    return articles.map(article => ({
        ...article,
        excerpt: article.body.substring(0, 200),
        readingTime: calculateReadingTime(article.body),
    }));
};

// 使用async/await
async function fetchArticles() {
    try {
        const response = await fetch('/api/articles');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch articles:', error);
        throw error;
    }
}
```

## 部署指南

### GitHub Pages部署

1. **启用GitHub Pages**
   - 进入仓库 Settings > Pages
   - 选择 gh-pages 分支
   - 选择 / (root) 目录

2. **配置自定义域名**（可选）
   ```bash
   # 创建CNAME文件
   echo "blog.example.com" > CNAME
   ```

3. **配置HTTPS**
   - 在GitHub Pages设置中启用HTTPS
   - 等待证书颁发

### 监控和维护

#### 监控指标

| 指标 | 阈值 | 说明 |
|------|------|------|
| 构建时间 | < 5分钟 | GitHub Actions构建时间 |
| 页面加载 | < 3秒 | 首页加载时间 |
| 错误率 | < 0.1% | 构建失败率 |
| 可用性 | > 99.9% | 网站可用性 |

#### 日志查看

```bash
# 查看GitHub Actions日志
# 进入仓库 Actions 标签页

# 查看本地日志
tail -f logs/renderer.log
```

## 故障排除

### 常见问题

#### 1. 构建失败

**症状**：GitHub Actions构建失败

**可能原因**：
- GitHub Token权限不足
- 仓库未启用GitHub Pages
- 配置错误

**解决方案**：
```bash
# 检查Token权限
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# 检查仓库设置
# 进入 Settings > Actions > General
# 确保启用了 Read and write permissions
```

#### 2. 文章未显示

**症状**：Issue已创建，但网站未显示

**可能原因**：
- Issue未添加`blog`标签
- Issue状态不是open
- 构建未完成

**解决方案**：
1. 检查Issue标签
2. 检查Issue状态
3. 查看GitHub Actions运行状态

#### 3. 样式问题

**症状**：页面样式错乱

**可能原因**：
- CSS文件路径错误
- 浏览器缓存
- 主题切换问题

**解决方案**：
```bash
# 清除浏览器缓存
# Ctrl+Shift+R (Windows/Linux)
# Cmd+Shift+R (Mac)

# 检查CSS文件
ls -la static/css/
```

## 性能优化

### 前端优化

1. **图片优化**
   - 使用WebP格式
   - 压缩图片大小
   - 实现懒加载

2. **CSS优化**
   - 合并CSS文件
   - 移除未使用样式
   - 使用CSS变量

3. **JavaScript优化**
   - 代码分割
   - 懒加载模块
   - 使用Web Workers

### 后端优化

1. **缓存策略**
   - 内存缓存
   - 文件缓存
   - CDN缓存

2. **数据库优化**
   - 索引优化
   - 查询优化
   - 连接池

3. **API优化**
   - 分页查询
   - 字段选择
   - 压缩响应

## 安全指南

### 安全最佳实践

1. **输入验证**
   ```python
   import re
   
   def validate_email(email: str) -> bool:
       pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       return re.match(pattern, email) is not None
   ```

2. **输出编码**
   ```python
   from markupsafe import escape
   
   def safe_html(text: str) -> str:
       return escape(text)
   ```

3. **CSRF防护**
   ```python
   from flask_wtf.csrf import CSRFProtect
   
   csrf = CSRFProtect(app)
   ```

4. **HTTPS配置**
   ```nginx
   server {
       listen 443 ssl;
       server_name blog.example.com;
       
       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;
       
       # 强制HTTPS
       add_header Strict-Transport-Security "max-age=31536000" always;
   }
   ```

## 总结

这个综合测试文档包含了：

1. **项目概述**：特性和快速开始
2. **配置说明**：环境变量和配置文件
3. **使用指南**：发布文章和格式示例
4. **技术架构**：系统架构和技术栈
5. **开发指南**：本地开发和代码规范
6. **部署指南**：GitHub Pages部署
7. **故障排除**：常见问题和解决方案
8. **性能优化**：前端和后端优化
9. **安全指南**：安全最佳实践

这个文档模拟了真实的技术博客文章，包含了代码块、表格、列表、任务列表、引用、链接等各种Markdown和GFM特性，用于全面测试渲染器的功能。