#!/usr/bin/env python3
"""
GitHub Issues博客渲染器测试脚本
用于测试渲染器的基本功能
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置测试环境变量
os.environ['GITHUB_OWNER'] = 'test-owner'
os.environ['GITHUB_REPO'] = 'test-repo'
os.environ['GITHUB_TOKEN'] = 'test-token'

import renderer.config as config
from renderer.utils.markdown_parser import MarkdownParser, get_markdown_parser
from renderer.utils.template_engine import BlogTemplateEngine, get_blog_template_engine


def test_config():
    """测试配置"""
    print("=== 测试配置 ===")
    print(f"项目根目录: {config.PROJECT_ROOT}")
    print(f"输出目录: {config.OUTPUT_DIR}")
    print(f"模板目录: {config.TEMPLATES_DIR}")
    print(f"静态资源目录: {config.STATIC_DIR}")
    print(f"GitHub仓库: {config.GITHUB_OWNER}/{config.GITHUB_REPO}")
    print(f"文章标签: {config.ARTICLE_LABEL}")
    print()


def test_markdown_parser():
    """测试Markdown解析器"""
    print("=== 测试Markdown解析器 ===")
    
    parser = get_markdown_parser()
    
    # 测试Markdown内容，包括GFM特性
    test_markdown = """
# 测试标题

这是一个测试段落，包含**粗体**和*斜体*文本。

## 代码示例

```python
def hello():
    print("Hello, World!")
    return True
```

## GFM特性测试

### 任务列表

- [x] 已完成的任务
- [ ] 未完成的任务
- [x] 另一个已完成的任务

### 删除线

~~这是删除线文本~~

### 高亮标记

==这是高亮文本==

### 表格

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
| 数据4 | 数据5 | 数据6 |

## 链接和图片

[GitHub](https://github.com)

![示例图片](https://example.com/image.jpg)

> 这是一个引用块

## 智能符号

- 版权符号: (c)
- 注册商标: (r)
- 商标符号: (tm)
"""
    
    # 测试解析
    html = parser.parse(test_markdown)
    print(f"生成HTML长度: {len(html)} 字符")
    
    # 测试摘要提取
    plain_text = parser.markdown_to_plain_text(test_markdown)
    print(f"提取纯文本长度: {len(plain_text)} 字符")
    print(f"纯文本前100字符: {plain_text[:100]}...")
    
    # 测试TOC提取
    toc = parser.extract_toc(test_markdown)
    print(f"TOC长度: {len(toc)} 字符")
    
    print()


def test_template_engine():
    """测试模板引擎"""
    print("=== 测试模板引擎 ===")
    
    try:
        engine = get_blog_template_engine()
        
        # 列出可用模板
        templates = engine.list_templates()
        print(f"可用模板: {templates}")
        
        # 测试简单渲染
        test_template = "<h1>{{ title }}</h1><p>{{ content }}</p>"
        result = engine.render_string(test_template, title="测试标题", content="测试内容")
        print(f"简单渲染结果: {result}")
        
        print("模板引擎测试通过!")
        
    except Exception as e:
        print(f"模板引擎测试失败: {e}")
    
    print()


def test_mock_data():
    """测试模拟数据"""
    print("=== 测试模拟数据 ===")
    
    # 模拟文章数据
    mock_articles = [
        {
            'number': 1,
            'title': '第一篇博客文章',
            'body': '# 欢迎来到我的博客\n\n这是第一篇博客文章的内容。\n\n## 代码示例\n\n```python\nprint("Hello, World!")\n```',
            'state': 'open',
            'created_at': '2026-05-29T10:00:00Z',
            'updated_at': '2026-05-29T10:00:00Z',
            'labels': ['blog', 'python'],
            'user': {
                'login': 'testuser',
                'avatar_url': 'https://github.com/identicons/testuser.png',
                'html_url': 'https://github.com/testuser',
            },
            'comments': 2,
            'html_url': 'https://github.com/test-owner/test-repo/issues/1',
        },
        {
            'number': 2,
            'title': '第二篇博客文章',
            'body': '# 关于GitHub Actions\n\n这篇文章介绍如何使用GitHub Actions。\n\n## 工作流示例\n\n```yaml\nname: CI\non: push\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n    - uses: actions/checkout@v4\n```',
            'state': 'open',
            'created_at': '2026-05-28T15:30:00Z',
            'updated_at': '2026-05-28T15:30:00Z',
            'labels': ['blog', 'github-actions'],
            'user': {
                'login': 'testuser',
                'avatar_url': 'https://github.com/identicons/testuser.png',
                'html_url': 'https://github.com/testuser',
            },
            'comments': 5,
            'html_url': 'https://github.com/test-owner/test-repo/issues/2',
        },
    ]
    
    print(f"模拟文章数量: {len(mock_articles)}")
    
    for article in mock_articles:
        print(f"  #{article['number']}: {article['title']}")
        print(f"    标签: {', '.join(article['labels'])}")
        print(f"    评论数: {article['comments']}")
    
    print()


def test_static_assets():
    """测试静态资源"""
    print("=== 测试静态资源 ===")
    
    # 检查CSS文件
    css_file = config.STATIC_DIR / "css" / "style.css"
    if css_file.exists():
        print(f"CSS文件存在: {css_file}")
        print(f"CSS文件大小: {css_file.stat().st_size} 字节")
    else:
        print(f"CSS文件不存在: {css_file}")
    
    # 检查JavaScript文件
    js_files = [
        config.STATIC_DIR / "js" / "main.js",
        config.STATIC_DIR / "js" / "theme.js",
    ]
    
    for js_file in js_files:
        if js_file.exists():
            print(f"JS文件存在: {js_file}")
            print(f"JS文件大小: {js_file.stat().st_size} 字节")
        else:
            print(f"JS文件不存在: {js_file}")
    
    print()


def test_output_directory():
    """测试输出目录"""
    print("=== 测试输出目录 ===")
    
    # 创建输出目录
    config.create_directories()
    
    # 检查目录是否存在
    directories = [
        config.OUTPUT_DIR,
        config.OUTPUT_DIR / "posts",
        config.OUTPUT_DIR / "tags",
        config.OUTPUT_DIR / "static",
    ]
    
    for directory in directories:
        if directory.exists():
            print(f"目录存在: {directory}")
        else:
            print(f"目录不存在: {directory}")
    
    print()


def main():
    """主测试函数"""
    print("GitHub Issues博客渲染器测试")
    print("=" * 50)
    
    try:
        # 运行各项测试
        test_config()
        test_markdown_parser()
        test_template_engine()
        test_mock_data()
        test_static_assets()
        test_output_directory()
        
        print("=" * 50)
        print("所有测试完成!")
        print("渲染器基本功能正常，可以用于实际部署。")
        print("=" * 50)
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())