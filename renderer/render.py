#!/usr/bin/env python3
"""
GitHub Issues博客渲染器
将当前仓库的Issues渲染为静态HTML网站
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from utils.github_api import GitHubAPI, get_github_client
from utils.markdown_parser import MarkdownParser, get_markdown_parser
from utils.template_engine import BlogTemplateEngine, get_blog_template_engine


class BlogRenderer:
    """博客渲染器主类"""
    
    def __init__(self):
        """初始化渲染器"""
        print("初始化博客渲染器...")
        
        # 验证配置
        errors = config.validate_config()
        if errors:
            print("配置错误:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        
        # 创建必要目录
        config.create_directories()
        
        # 初始化组件
        self.github_api = get_github_client()
        self.markdown_parser = get_markdown_parser()
        self.template_engine = get_blog_template_engine()
        
        # 存储数据
        self.articles = []
        self.tags = {}
        self.all_labels = []
        
        print("渲染器初始化完成")
    
    def fetch_articles(self) -> List[Dict[str, Any]]:
        """
        从GitHub获取博客文章
        
        Returns:
            文章列表
        """
        print(f"正在获取带 '{config.ARTICLE_LABEL}' 标签的Issues...")
        
        articles = self.github_api.get_blog_articles()
        print(f"获取到 {len(articles)} 篇文章")
        
        # 按创建时间倒序排序
        articles.sort(key=lambda x: x['created_at'], reverse=True)
        
        # 处理每篇文章
        processed_articles = []
        for article in articles:
            processed_article = self._process_article(article)
            processed_articles.append(processed_article)
            
            # 收集标签
            for tag in article['labels']:
                if tag not in self.tags:
                    self.tags[tag] = []
                self.tags[tag].append(article['number'])
        
        self.articles = processed_articles
        return processed_articles
    
    def _process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理单篇文章数据
        
        Args:
            article: 原始文章数据
            
        Returns:
            处理后的文章数据
        """
        # 生成摘要
        body = article.get('body', '')
        excerpt = self.markdown_parser.markdown_to_plain_text(body)[:200] + '...'
        
        # 计算阅读时间
        reading_time = self._calculate_reading_time(body)
        
        # 生成URL
        article_url = f"/posts/{article['number']}.html"
        
        return {
            **article,
            'excerpt': excerpt,
            'reading_time': reading_time,
            'url': article_url,
            'formatted_date': self._format_date(article['created_at']),
        }
    
    def _calculate_reading_time(self, text: str) -> str:
        """计算阅读时间"""
        if not text:
            return '1分钟'
        
        # 简单估算：中文每分钟300字，英文每分钟200词
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        
        total_words = chinese_chars + english_words
        minutes = max(1, total_words // 300)
        
        return f'{minutes}分钟'
    
    def _format_date(self, date_string: str) -> str:
        """格式化日期"""
        try:
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return date_obj.strftime('%Y年%m月%d日')
        except:
            return date_string
    
    def generate_pages(self):
        """生成所有页面"""
        print("开始生成页面...")
        
        # 生成首页
        self._generate_index_pages()
        
        # 生成文章详情页
        self._generate_article_pages()
        
        # 生成标签页
        self._generate_tag_pages()
        
        # 生成RSS
        if config.RSS_ENABLED:
            self._generate_rss()
        
        # 生成搜索索引
        if config.SEARCH_ENABLED:
            self._generate_search_index()
        
        # 复制静态资源
        self._copy_static_assets()
        
        print("页面生成完成")
    
    def _generate_index_pages(self):
        """生成首页和分页"""
        print("生成首页...")
        
        articles = self.articles
        per_page = config.ARTICLES_PER_PAGE
        total_count = len(articles)
        total_pages = (total_count + per_page - 1) // per_page
        
        # 生成每一页
        for page in range(1, total_pages + 1):
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            page_articles = articles[start_idx:end_idx]
            
            # 渲染HTML
            html = self.template_engine.render_index(
                articles=page_articles,
                page=page,
                total_pages=total_pages,
                total_count=total_count,
            )
            
            # 保存文件
            if page == 1:
                output_path = config.OUTPUT_DIR / "index.html"
            else:
                output_path = config.OUTPUT_DIR / f"page/{page}.html"
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self._save_html(html, output_path)
            print(f"  生成首页第 {page} 页: {output_path}")
    
    def _generate_article_pages(self):
        """生成文章详情页"""
        print("生成文章详情页...")
        
        # 创建posts目录
        posts_dir = config.OUTPUT_DIR / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        
        for article in self.articles:
            # 渲染Markdown内容为HTML
            content_html = self.markdown_parser.parse(article['body'])
            
            # 渲染完整页面
            html = self.template_engine.render_article(
                article=article,
                content_html=content_html,
            )
            
            # 保存文件
            output_path = posts_dir / f"{article['number']}.html"
            self._save_html(html, output_path)
            print(f"  生成文章: #{article['number']} - {article['title']}")
    
    def _generate_tag_pages(self):
        """生成标签页"""
        print("生成标签页...")
        
        # 创建tags目录
        tags_dir = config.OUTPUT_DIR / "tags"
        tags_dir.mkdir(parents=True, exist_ok=True)
        
        for tag_name, article_numbers in self.tags.items():
            # 获取该标签下的文章
            tag_articles = [
                article for article in self.articles 
                if article['number'] in article_numbers
            ]
            
            # 按时间排序
            tag_articles.sort(key=lambda x: x['created_at'], reverse=True)
            
            # 计算分页
            per_page = config.ARTICLES_PER_PAGE
            total_count = len(tag_articles)
            total_pages = (total_count + per_page - 1) // per_page
            
            # 生成第一页
            page_articles = tag_articles[:per_page]
            html = self.template_engine.render_tag_page(
                tag_name=tag_name,
                articles=page_articles,
                page=1,
                total_pages=total_pages,
            )
            
            # 保存文件
            tag_filename = tag_name.replace(' ', '-').lower()
            output_path = tags_dir / f"{tag_filename}.html"
            self._save_html(html, output_path)
            print(f"  生成标签页: {tag_name}")
    
    def _generate_rss(self):
        """生成RSS feed"""
        print("生成RSS feed...")
        
        html = self.template_engine.render_rss(articles=self.articles)
        output_path = config.OUTPUT_DIR / config.RSS_FILE
        self._save_html(html, output_path)
        print(f"  生成RSS: {output_path}")
    
    def _generate_search_index(self):
        """生成搜索索引"""
        print("生成搜索索引...")
        
        # 创建搜索索引数据
        search_index = []
        for article in self.articles:
            search_index.append({
                'id': article['number'],
                'title': article['title'],
                'excerpt': article['excerpt'],
                'url': article['url'],
                'tags': article['labels'],
                'date': article['created_at'],
            })
        
        # 保存为JSON文件
        output_path = config.OUTPUT_DIR / config.SEARCH_INDEX_FILE
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(search_index, f, ensure_ascii=False, indent=2)
        
        print(f"  生成搜索索引: {output_path}")
    
    def _copy_static_assets(self):
        """复制静态资源"""
        print("复制静态资源...")
        
        static_src = config.STATIC_DIR
        static_dest = config.OUTPUT_DIR / "static"
        
        if static_src.exists():
            if static_dest.exists():
                shutil.rmtree(static_dest)
            
            shutil.copytree(static_src, static_dest)
            print(f"  复制静态资源: {static_src} -> {static_dest}")
        else:
            print(f"  警告: 静态资源目录不存在: {static_src}")
    
    def _save_html(self, html: str, output_path: Path):
        """保存HTML文件"""
        # 确保目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_sitemap(self):
        """生成站点地图"""
        print("生成站点地图...")
        
        base_url = config.BLOG_URL.rstrip('/')
        urls = []
        
        # 首页
        urls.append(f"{base_url}/")
        
        # 文章页
        for article in self.articles:
            urls.append(f"{base_url}/posts/{article['number']}.html")
        
        # 标签页
        for tag_name in self.tags.keys():
            tag_filename = tag_name.replace(' ', '-').lower()
            urls.append(f"{base_url}/tags/{tag_filename}.html")
        
        # 生成XML站点地图
        sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            sitemap_xml += f'  <url>\n'
            sitemap_xml += f'    <loc>{url}</loc>\n'
            sitemap_xml += f'    <lastmod>{datetime.now().isoformat()}</lastmod>\n'
            sitemap_xml += f'    <changefreq>daily</changefreq>\n'
            sitemap_xml += f'  </url>\n'
        
        sitemap_xml += '</urlset>'
        
        output_path = config.OUTPUT_DIR / "sitemap.xml"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_xml)
        
        print(f"  生成站点地图: {output_path}")
    
    def generate_robots_txt(self):
        """生成robots.txt"""
        print("生成robots.txt...")
        
        content = f"""User-agent: *
Allow: /

Sitemap: {config.BLOG_URL.rstrip('/')}/sitemap.xml
"""
        
        output_path = config.OUTPUT_DIR / "robots.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  生成robots.txt: {output_path}")
    
    def run(self):
        """运行渲染器"""
        print("=" * 50)
        print("开始渲染GitHub Issues博客")
        print("=" * 50)
        
        start_time = datetime.now()
        
        try:
            # 1. 获取文章
            self.fetch_articles()
            
            if not self.articles:
                print("没有找到博客文章，请确保Issue带有 '{}' 标签".format(config.ARTICLE_LABEL))
                return
            
            # 2. 生成页面
            self.generate_pages()
            
            # 3. 生成辅助文件
            self.generate_sitemap()
            self.generate_robots_txt()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("=" * 50)
            print(f"渲染完成!")
            print(f"生成了 {len(self.articles)} 篇文章")
            print(f"耗时: {duration:.2f}秒")
            print(f"输出目录: {config.OUTPUT_DIR}")
            print("=" * 50)
            
        except Exception as e:
            print(f"渲染失败: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """主函数"""
    renderer = BlogRenderer()
    renderer.run()


if __name__ == "__main__":
    main()