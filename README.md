# GitHub Issues 博客系统

一个基于GitHub Issues的静态博客系统，通过GitHub Actions自动将Issues渲染为静态网站，部署到GitHub Pages。

## ✨ 特性

- **🚀 完全自动化**：Issue创建/编辑时自动触发构建和部署
- **📦 静态网站**：无需后端服务器，纯HTML/CSS/JS
- **🎨 原生前端**：不使用任何CDN资源，完全自定义
- **📱 响应式设计**：支持移动端访问
- **🌙 主题切换**：支持深色/浅色主题
- **🔍 代码高亮**：支持多种编程语言
- **📡 RSS订阅**：自动生成RSS feed
- **🔍 搜索功能**：客户端搜索（可选）
- **📝 GFM支持**：完整的GitHub Flavored Markdown支持
  - 任务列表：`- [x]` 和 `- [ ]`
  - 删除线：`~~删除线文本~~`
  - 高亮标记：`==高亮文本==`
  - 表格：标准Markdown表格
  - 围栏代码块：```语言名称
  - 自动链接：自动转换URL为链接
  - 表情符号：`:emoji_name:`（可选）
  - 键盘按键：`<kbd>Ctrl</kbd> + <kbd>C</kbd>`

## 🚀 快速开始

### 1. 克隆或下载项目

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. 启用GitHub Pages

1. 进入仓库的 **Settings** > **Pages**
2. 在 **Source** 部分选择 **Deploy from a branch**
3. 选择 **gh-pages** 分支和 **/ (root)** 目录
4. 点击 **Save**

### 3. 配置仓库权限

1. 进入仓库的 **Settings** > **Actions** > **General**
2. 在 **Workflow permissions** 部分选择 **Read and write permissions**
3. 勾选 **Allow GitHub Actions to create and approve pull requests**
4. 点击 **Save**

### 4. 发布第一篇文章

1. 在仓库中创建新Issue
2. 添加 `blog` 标签
3. 编写文章内容（支持Markdown格式）
4. 提交Issue

GitHub Actions会自动：
- 获取所有带`blog`标签的Issues
- 渲染为静态HTML页面
- 推送到`gh-pages`分支
- 部署到GitHub Pages

## 📝 文章格式

### 标题
使用Markdown标题格式：
```markdown
# 一级标题
## 二级标题
### 三级标题
```

### 代码块
使用三个反引号包裹代码，并指定语言：
````markdown
```python
def hello():
    print("Hello, World!")
```
````

### 列表
```markdown
- 无序列表项1
- 无序列表项2

1. 有序列表项1
2. 有序列表项2
```

### 链接和图片
```markdown
[链接文字](https://example.com)
![图片描述](https://example.com/image.jpg)
```

### 表格
```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
```

### GFM特性

#### 任务列表
```markdown
- [x] 已完成的任务
- [ ] 未完成的任务
- [x] 另一个已完成的任务
```

#### 删除线
```markdown
~~这是删除线文本~~
```

#### 高亮标记
```markdown
==这是高亮文本==
```

#### 键盘按键
```markdown
按 <kbd>Ctrl</kbd> + <kbd>C</kbd> 复制
```

#### 自动链接
```markdown
https://github.com 会自动转换为可点击链接
```

#### 表情符号（可选）
```markdown
:smile: :heart: :thumbsup:
```

## 🎨 自定义配置

### 环境变量

在仓库的 **Settings** > **Secrets and variables** > **Actions** 中添加以下变量：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `GITHUB_OWNER` | 仓库所有者 | 自动获取 |
| `GITHUB_REPO` | 仓库名称 | 自动获取 |
| `GITHUB_TOKEN` | GitHub令牌 | 自动提供 |
| `ARTICLE_LABEL` | 文章标签 | `blog` |
| `BLOG_TITLE` | 博客标题 | `{repo} Blog` |
| `BLOG_DESCRIPTION` | 博客描述 | 自动生成 |
| `BLOG_URL` | 博客URL | 自动生成 |

### 配置文件

编辑 `renderer/config.py` 文件可以自定义更多设置：

```python
# 文章配置
ARTICLES_PER_PAGE = 10  # 每页文章数
MAX_ARTICLES = 100      # 最大文章数

# Markdown配置
CODE_HILITE_STYLE = "monokai"  # 代码高亮主题

# RSS配置
RSS_ENABLED = True  # 是否启用RSS
```

## 📁 项目结构

```
github-issues-blog/
├── .github/
│   └── workflows/
│       └── blog.yml          # GitHub Actions工作流
├── renderer/
│   ├── render.py            # 主渲染脚本
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python依赖
│   └── utils/
│       ├── github_api.py   # GitHub API封装
│       ├── markdown_parser.py # Markdown解析
│       └── template_engine.py # 模板引擎
├── templates/
│   ├── base.html           # 基础模板
│   ├── index.html          # 首页模板
│   ├── post.html           # 文章详情模板
│   ├── tag.html            # 标签页模板
│   └── rss.xml             # RSS模板
├── static/
│   ├── css/
│   │   └── style.css       # 主样式文件
│   └── js/
│       ├── main.js         # 主JavaScript
│       └── theme.js        # 主题切换
└── output/                 # 生成的静态文件（git忽略）
```

## 🔧 本地开发

### 1. 安装依赖

```bash
cd renderer
pip install -r requirements.txt
```

### 2. 设置环境变量

```bash
export GITHUB_OWNER="your-username"
export GITHUB_REPO="your-repo"
export GITHUB_TOKEN="your-github-token"
```

### 3. 运行渲染器

```bash
python render.py
```

### 4. 本地预览

```bash
cd output
python -m http.server 8000
```

访问 http://localhost:8000 查看生成的网站。

## 🎯 高级功能

### 1. 自定义域名

1. 在仓库根目录创建 `CNAME` 文件，内容为你的域名
2. 在域名DNS设置中添加CNAME记录指向 `your-username.github.io`
3. 在GitHub仓库的 **Settings** > **Pages** 中设置自定义域名

### 2. 评论系统（Giscus）

本项目使用 [Giscus](https://giscus.app/) 作为评论系统，基于GitHub Discussions。

#### 配置步骤：

1. **启用GitHub Discussions**
   - 进入仓库 **Settings** > **General**
   - 向下滚动到 **Features** 部分
   - 勾选 **Discussions**

2. **获取Giscus配置**
   - 访问 https://giscus.app/
   - 输入你的仓库名称
   - 选择讨论分类（建议使用 "Announcements"）
   - 复制生成的配置

3. **设置环境变量**
   ```bash
   # 在 .env 文件中添加
   GISCUS_REPO_ID=R_xxxxx  # 仓库ID
   GISCUS_CATEGORY=Announcements  # 讨论分类
   GISCUS_CATEGORY_ID=DIC_xxxxx  # 分类ID
   ```

4. **本地测试**
   ```bash
   # 修改 local_render.py 中的配置
   os.environ['GISCUS_REPO_ID'] = 'R_...'
   os.environ['GISCUS_CATEGORY'] = 'Announcements'
   os.environ['GISCUS_CATEGORY_ID'] = 'DIC_...'
   ```

#### Giscus特性：
- ✅ 基于GitHub Discussions
- ✅ 支持Markdown格式
- ✅ 支持表情反应
- ✅ 支持主题切换
- ✅ 支持多语言
- ✅ 无需额外注册

### 3. 搜索功能

搜索功能在客户端实现，需要先生成搜索索引。渲染器会自动生成 `search-index.json` 文件。

### 4. 多语言支持

修改 `renderer/config.py` 中的 `BLOG_LANGUAGE` 设置：

```python
BLOG_LANGUAGE = "en"  # 英语
BLOG_LANGUAGE = "zh-CN"  # 中文
```

## 🐛 故障排除

### 1. GitHub Actions失败

检查仓库的 **Actions** 标签页，查看工作流运行日志。常见问题：
- GitHub Token权限不足
- 仓库未启用GitHub Pages
- 配置错误

### 2. 文章未显示

确保：
- Issue已添加`blog`标签
- Issue状态为开放（open）
- 等待GitHub Actions完成构建

### 3. 样式问题

检查浏览器控制台是否有CSS加载错误。确保静态资源路径正确。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请创建Issue或联系维护者。

---

**享受你的GitHub Issues博客！** 🎉