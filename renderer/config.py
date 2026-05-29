import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "build"

# 静态资源目录
STATIC_DIR = PROJECT_ROOT / "static"

# 模板目录
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# GitHub配置
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

# 博客配置
BLOG_TITLE = os.getenv("BLOG_TITLE", f"{GITHUB_REPO} Blog")
BLOG_DESCRIPTION = os.getenv("BLOG_DESCRIPTION", f"基于GitHub Issues的博客 - {GITHUB_OWNER}/{GITHUB_REPO}")
BLOG_URL = os.getenv("BLOG_URL", f"https://{GITHUB_OWNER}.github.io/{GITHUB_REPO}/")
BLOG_LANGUAGE = "zh-CN"

# 文章配置
ARTICLE_LABEL = os.getenv("ARTICLE_LABEL", "blog")  # 用于标识文章的标签
ARTICLES_PER_PAGE = 10
MAX_ARTICLES = 100  # 最大获取文章数

# 缓存配置
CACHE_ENABLED = True
CACHE_TTL = 300  # 5分钟缓存

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

CODE_HILITE_STYLE = "monokai"
CODE_HILITE_LINENOS = False

# RSS配置
RSS_ENABLED = True
RSS_FILE = "feed.xml"
RSS_TITLE = BLOG_TITLE
RSS_DESCRIPTION = BLOG_DESCRIPTION
RSS_LANGUAGE = BLOG_LANGUAGE

# 主题配置
DEFAULT_THEME = "light"
AVAILABLE_THEMES = ["light", "dark"]

# 搜索配置
SEARCH_ENABLED = True
SEARCH_INDEX_FILE = "search-index.json"

# Giscus评论系统配置
# 已在 https://giscus.app/ 获取配置
GISCUS_REPO_ID = os.getenv("GISCUS_REPO_ID", "R_kgDOSrMqxg")  # 仓库ID
GISCUS_CATEGORY = os.getenv("GISCUS_CATEGORY", "Announcements")  # 讨论分类
GISCUS_CATEGORY_ID = os.getenv("GISCUS_CATEGORY_ID", "DIC_kwDOSrMqxs4C-E96")  # 分类ID

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 验证配置
def validate_config():
    """验证配置是否完整"""
    errors = []
    
    if not GITHUB_OWNER:
        errors.append("GITHUB_OWNER 环境变量未设置")
    
    if not GITHUB_REPO:
        errors.append("GITHUB_REPO 环境变量未设置")
    
    if not GITHUB_TOKEN:
        errors.append("GITHUB_TOKEN 环境变量未设置")
    
    return errors

# 创建必要目录
def create_directories():
    """创建必要的目录结构"""
    directories = [
        OUTPUT_DIR,
        OUTPUT_DIR / "posts",
        OUTPUT_DIR / "tags",
        OUTPUT_DIR / "static",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # 测试配置
    errors = validate_config()
    if errors:
        print("配置错误:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("配置验证通过")
        print(f"项目根目录: {PROJECT_ROOT}")
        print(f"输出目录: {OUTPUT_DIR}")
        print(f"GitHub仓库: {GITHUB_OWNER}/{GITHUB_REPO}")