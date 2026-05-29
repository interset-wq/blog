#!/usr/bin/env python3
"""
本地渲染脚本
用于本地测试，读取.md文件并渲染成博客文章
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# 设置测试环境变量
os.environ['GITHUB_OWNER'] = 'interset-wq'
os.environ['GITHUB_REPO'] = 'blog'
os.environ['GITHUB_TOKEN'] = 'test-token'

# Giscus配置（已配置）
os.environ['GISCUS_REPO_ID'] = 'R_kgDOSrMqxg'
os.environ['GISCUS_CATEGORY'] = 'Announcements'
os.environ['GISCUS_CATEGORY_ID'] = 'DIC_kwDOSrMqxs4C-E96'

# 导入模块
from renderer.utils.markdown_parser import get_markdown_parser
from renderer.utils.template_engine import get_blog_template_engine
import renderer.config as config

def copy_static_assets():
    """复制静态资源到build目录"""
    print("复制静态资源...")
    
    static_src = project_root / "static"
    static_dest = project_root / "build" / "static"
    
    if static_src.exists():
        # 如果目标目录存在，先删除
        if static_dest.exists():
            shutil.rmtree(static_dest)
        
        # 复制静态资源
        shutil.copytree(static_src, static_dest)
        print(f"  ✅ 静态资源已复制到: {static_dest}")
        return True
    else:
        print(f"  ❌ 静态资源目录不存在: {static_src}")
        return False

def read_markdown_files():
    """读取所有Markdown文件"""
    print("读取Markdown文件...")
    
    test_docs_dir = project_root / "test_docs"
    if not test_docs_dir.exists():
        print(f"  ❌ 测试文档目录不存在: {test_docs_dir}")
        return []
    
    md_files = list(test_docs_dir.glob("*.md"))
    print(f"  找到 {len(md_files)} 个Markdown文件")
    
    articles = []
    for i, md_file in enumerate(md_files, 1):
        print(f"  读取: {md_file.name}")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 从文件名生成标题
        title = md_file.stem.replace('_', ' ').title()
        
        # 创建文章数据
        article = {
            'number': i,
            'title': title,
            'body': content,
            'state': 'open',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'labels': ['test', 'documentation', 'markdown'],
            'user': {
                'login': 'test-user',
                'avatar_url': 'https://github.com/identicons/test-user.png',
                'html_url': 'https://github.com/test-user',
            },
            'comments': 0,
            'html_url': f'https://github.com/interset-wq/blog/issues/{i}',
            'formatted_date': datetime.now().strftime('%Y年%m月%d日'),
            'reading_time': '5分钟',
            'excerpt': content[:200] + '...' if len(content) > 200 else content,
            'file_path': md_file,
        }
        
        articles.append(article)
    
    return articles

def render_article(article, template_engine, markdown_parser):
    """渲染单个文章"""
    print(f"渲染文章: {article['title']}")
    
    try:
        # 解析Markdown
        content_html = markdown_parser.parse(article['body'])
        
        # 渲染完整页面
        full_html = template_engine.render_article(
            article=article,
            content_html=content_html,
        )
        
        return full_html
        
    except Exception as e:
        print(f"  ❌ 渲染失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def render_index(articles, template_engine):
    """渲染首页"""
    print("渲染首页...")
    
    try:
        # 渲染首页
        full_html = template_engine.render_index(
            articles=articles,
            page=1,
            total_pages=1,
            total_count=len(articles),
        )
        
        return full_html
        
    except Exception as e:
        print(f"  ❌ 渲染首页失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_html(html_content, output_path):
    """保存HTML文件"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  保存到: {output_path}")

def main():
    """主函数"""
    print("=" * 60)
    print("本地博客渲染器")
    print("=" * 60)
    
    # 复制静态资源
    if not copy_static_assets():
        print("❌ 静态资源复制失败")
        return 1
    
    # 初始化模板引擎和Markdown解析器
    try:
        template_engine = get_blog_template_engine()
        markdown_parser = get_markdown_parser()
        print("✅ 模板引擎和Markdown解析器初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return 1
    
    # 读取Markdown文件
    articles = read_markdown_files()
    if not articles:
        print("❌ 未找到Markdown文件")
        return 1
    
    print(f"\n开始渲染 {len(articles)} 篇文章...")
    print("=" * 60)
    
    # 渲染每篇文章
    rendered_articles = []
    for article in articles:
        print(f"\n{'='*60}")
        
        # 渲染文章
        html_content = render_article(article, template_engine, markdown_parser)
        if html_content:
            # 保存文章页面
            output_path = project_root / "build" / "posts" / f"{article['number']}.html"
            save_html(html_content, output_path)
            
            # 更新文章数据
            article['url'] = f"/posts/{article['number']}.html"
            rendered_articles.append(article)
        
        print(f"{'='*60}")
    
    # 渲染首页
    print(f"\n{'='*60}")
    index_html = render_index(rendered_articles, template_engine)
    if index_html:
        index_path = project_root / "build" / "index.html"
        save_html(index_html, index_path)
    
    # 生成标签页面
    print(f"\n{'='*60}")
    print("生成标签页面...")
    
    # 收集所有标签
    all_tags = set()
    for article in rendered_articles:
        all_tags.update(article['labels'])
    
    for tag in all_tags:
        # 获取该标签下的文章
        tag_articles = [a for a in rendered_articles if tag in a['labels']]
        
        # 渲染标签页面
        tag_html = template_engine.render_tag_page(
            tag_name=tag,
            articles=tag_articles,
            page=1,
            total_pages=1,
        )
        
        if tag_html:
            tag_path = project_root / "build" / "tags" / f"{tag}.html"
            save_html(tag_html, tag_path)
    
    # 生成归档页面
    print(f"\n{'='*60}")
    print("生成归档页面...")
    
    # 按年份分组文章
    archives = defaultdict(list)
    for article in rendered_articles:
        try:
            date = datetime.fromisoformat(article['created_at'].replace('Z', '+00:00'))
            year = date.year
            archives[year].append(article)
        except:
            archives[2026].append(article)
    
    # 渲染归档页面
    archives_html = template_engine.render_template(
        'archives.html',
        archives=archives,
        total_count=len(rendered_articles),
        page=1,
        total_pages=1,
    )
    
    if archives_html:
        archives_path = project_root / "build" / "archives.html"
        save_html(archives_html, archives_path)
    
    # 生成分类页面
    print(f"\n{'='*60}")
    print("生成分类页面...")
    
    # 按分类分组文章
    categories = defaultdict(list)
    for article in rendered_articles:
        for label in article['labels']:
            categories[label].append(article)
    
    # 渲染分类页面
    categories_html = template_engine.render_template(
        'categories.html',
        categories=categories,
    )
    
    if categories_html:
        categories_path = project_root / "build" / "categories.html"
        save_html(categories_html, categories_path)
    
    # 生成关于页面
    print(f"\n{'='*60}")
    print("生成关于页面...")
    
    about_html = template_engine.render_template('about.html')
    if about_html:
        about_path = project_root / "build" / "about.html"
        save_html(about_html, about_path)
    
    # 生成友链页面
    print(f"\n{'='*60}")
    print("生成友链页面...")
    
    # 示例友链数据
    blog_links = [
        {
            'name': 'GitHub',
            'url': 'https://github.com',
            'avatar': 'https://github.githubassets.com/favicons/favicon.png',
            'description': '全球最大的代码托管平台'
        },
        {
            'name': 'GitHub Pages',
            'url': 'https://pages.github.com',
            'avatar': 'https://github.githubassets.com/favicons/favicon.png',
            'description': '免费的静态网站托管服务'
        },
    ]
    
    tech_links = [
        {
            'name': 'GitHub Actions',
            'url': 'https://github.com/features/actions',
            'icon': '⚡',
            'description': '自动化工作流'
        },
        {
            'name': 'Giscus',
            'url': 'https://giscus.app',
            'icon': '💬',
            'description': '基于GitHub Discussions的评论系统'
        },
        {
            'name': 'Jinja2',
            'url': 'https://jinja.palletsprojects.com',
            'icon': '🎨',
            'description': 'Python模板引擎'
        },
        {
            'name': 'PyGitHub',
            'url': 'https://pygithub.readthedocs.io',
            'icon': '📦',
            'description': 'GitHub官方Python库'
        },
    ]
    
    links_html = template_engine.render_template(
        'links.html',
        blog_links=blog_links,
        tech_links=tech_links,
    )
    
    if links_html:
        links_path = project_root / "build" / "links.html"
        save_html(links_html, links_path)
    
    print(f"\n{'='*60}")
    print("渲染完成！")
    print(f"{'='*60}")
    
    print(f"\n生成的文件:")
    print(f"  - 首页: build/index.html")
    print(f"  - 文章: build/posts/ ({len(rendered_articles)} 篇)")
    print(f"  - 标签: build/tags/ ({len(all_tags)} 个)")
    print(f"  - 归档: build/archives.html")
    print(f"  - 分类: build/categories.html")
    print(f"  - 关于: build/about.html")
    print(f"  - 友链: build/links.html")
    print(f"  - 静态资源: build/static/")
    
    print(f"\n启动本地服务器预览:")
    print(f"  make serve")
    print(f"  或")
    print(f"  cd build && python3 -m http.server 8000")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())