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

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# 设置测试环境变量
os.environ['GITHUB_OWNER'] = 'test-owner'
os.environ['GITHUB_REPO'] = 'test-repo'
os.environ['GITHUB_TOKEN'] = 'test-token'

# Giscus配置（需要在 https://giscus.app/ 获取）
os.environ['GISCUS_REPO_ID'] = 'R_...'  # 替换为实际的仓库ID
os.environ['GISCUS_CATEGORY'] = 'Announcements'
os.environ['GISCUS_CATEGORY_ID'] = 'DIC_...'  # 替换为实际的分类ID

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
            'html_url': f'https://github.com/test-owner/test-repo/issues/{i}',
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
    
    print(f"\n{'='*60}")
    print("渲染完成！")
    print(f"{'='*60}")
    
    print(f"\n生成的文件:")
    print(f"  - 首页: build/index.html")
    print(f"  - 文章: build/posts/ ({len(rendered_articles)} 篇)")
    print(f"  - 标签: build/tags/ ({len(all_tags)} 个)")
    print(f"  - 静态资源: build/static/")
    
    print(f"\n启动本地服务器预览:")
    print(f"  make serve")
    print(f"  或")
    print(f"  cd build && python3 -m http.server 8000")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())