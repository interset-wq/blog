import os
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys

# 添加父目录到路径，以便导入config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class TemplateEngine:
    """Jinja2模板引擎封装"""
    
    def __init__(self, templates_dir: Path = None):
        """
        初始化模板引擎
        
        Args:
            templates_dir: 模板目录路径（默认使用config中的配置）
        """
        self.templates_dir = templates_dir or config.TEMPLATES_DIR
        
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"模板目录不存在: {self.templates_dir}")
        
        # 初始化Jinja2环境
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # 添加自定义过滤器和函数
        self._add_custom_filters()
        self._add_custom_functions()
    
    def _add_custom_filters(self):
        """添加自定义Jinja2过滤器"""
        self.env.filters['datetimeformat'] = self._datetimeformat
        self.env.filters['truncate_text'] = self._truncate_text
        self.env.filters['markdown_preview'] = self._markdown_preview
    
    def _add_custom_functions(self):
        """添加自定义Jinja2全局函数"""
        self.env.globals['now'] = self._get_current_time
        self.env.globals['config'] = config
        self.env.globals['theme_class'] = self._get_theme_class
        self.env.globals['url_for'] = self._url_for
    
    def _datetimeformat(self, value, format='%Y-%m-%d %H:%M'):
        """日期时间格式化过滤器"""
        if isinstance(value, str):
            from datetime import datetime
            try:
                value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                return value
        return value.strftime(format)
    
    def _truncate_text(self, text, length=100, suffix='...'):
        """文本截断过滤器"""
        if not text:
            return ''
        if len(text) <= length:
            return text
        return text[:length].rsplit(' ', 1)[0] + suffix
    
    def _markdown_preview(self, markdown_text, length=200):
        """Markdown文本预览过滤器"""
        from .markdown_parser import get_markdown_parser
        parser = get_markdown_parser()
        plain_text = parser.markdown_to_plain_text(markdown_text)
        return self._truncate_text(plain_text, length)
    
    def _get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        return datetime.now()
    
    def _get_theme_class(self, theme=None):
        """获取主题CSS类"""
        theme = theme or config.DEFAULT_THEME
        return config.AVAILABLE_THEMES.get(theme, {}).get('css_class', 'theme-light')
    
    def _url_for(self, endpoint, **kwargs):
        """模拟Flask的url_for函数"""
        if endpoint == 'static':
            # 返回静态文件路径
            filename = kwargs.get('filename', '')
            return f'/static/{filename}'
        elif endpoint == 'index':
            return '/'
        elif endpoint == 'post':
            post_id = kwargs.get('post_id', '')
            return f'/posts/{post_id}.html'
        elif endpoint == 'tag':
            tag_name = kwargs.get('tag_name', '')
            return f'/tags/{tag_name}.html'
        else:
            # 默认返回根路径
            return '/'
    
    def render_template(self, template_name: str, **kwargs) -> str:
        """
        渲染模板
        
        Args:
            template_name: 模板文件名
            **kwargs: 模板变量
            
        Returns:
            渲染后的HTML字符串
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except Exception as e:
            print(f"渲染模板 {template_name} 失败: {e}")
            raise
    
    def render_string(self, template_string: str, **kwargs) -> str:
        """
        渲染模板字符串
        
        Args:
            template_string: 模板字符串
            **kwargs: 模板变量
            
        Returns:
            渲染后的HTML字符串
        """
        try:
            template = self.env.from_string(template_string)
            return template.render(**kwargs)
        except Exception as e:
            print(f"渲染模板字符串失败: {e}")
            raise
    
    def get_template(self, template_name: str):
        """
        获取模板对象
        
        Args:
            template_name: 模板文件名
            
        Returns:
            Jinja2模板对象
        """
        return self.env.get_template(template_name)
    
    def list_templates(self):
        """
        列出所有可用模板
        
        Returns:
            模板文件名列表
        """
        return self.env.list_templates()


class BlogTemplateEngine(TemplateEngine):
    """博客专用模板引擎"""
    
    def __init__(self):
        """初始化博客模板引擎"""
        super().__init__()
        self._setup_blog_specific_filters()
    
    def _setup_blog_specific_filters(self):
        """设置博客专用过滤器"""
        self.env.filters['format_date'] = self._format_date
        self.env.filters['reading_time'] = self._reading_time
        self.env.filters['excerpt'] = self._excerpt
    
    def _format_date(self, date_string, format='%Y年%m月%d日'):
        """中文日期格式化"""
        if isinstance(date_string, str):
            from datetime import datetime
            try:
                date_string = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            except ValueError:
                return date_string
        return date_string.strftime(format)
    
    def _reading_time(self, text, words_per_minute=200):
        """估算阅读时间"""
        if not text:
            return '1分钟'
        
        from .markdown_parser import get_markdown_parser
        parser = get_markdown_parser()
        plain_text = parser.markdown_to_plain_text(text)
        
        # 中文按字符数计算，英文按单词数计算
        import re
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', plain_text))
        english_words = len(re.findall(r'[a-zA-Z]+', plain_text))
        
        # 中文字符数 + 英文单词数（英文单词平均5个字符）
        total_words = chinese_chars + english_words
        minutes = max(1, total_words // words_per_minute)
        
        return f'{minutes}分钟'
    
    def _excerpt(self, markdown_text, length=200):
        """生成文章摘要"""
        return self._markdown_preview(markdown_text, length)
    
    def render_index(self, articles, page=1, total_pages=1, total_count=0):
        """
        渲染首页
        
        Args:
            articles: 文章列表
            page: 当前页码
            total_pages: 总页数
            total_count: 文章总数
            
        Returns:
            渲染后的HTML
        """
        return self.render_template(
            'index.html',
            articles=articles,
            page=page,
            total_pages=total_pages,
            total_count=total_count,
        )
    
    def render_article(self, article, content_html, comments=None):
        """
        渲染文章详情页
        
        Args:
            article: 文章数据
            content_html: 文章内容HTML
            comments: 评论列表
            
        Returns:
            渲染后的HTML
        """
        return self.render_template(
            'post.html',
            article=article,
            content_html=content_html,
            comments=comments or [],
        )
    
    def render_tag_page(self, tag_name, articles, page=1, total_pages=1):
        """
        渲染标签页
        
        Args:
            tag_name: 标签名称
            articles: 文章列表
            page: 当前页码
            total_pages: 总页数
            
        Returns:
            渲染后的HTML
        """
        return self.render_template(
            'tag.html',
            tag_name=tag_name,
            articles=articles,
            page=page,
            total_pages=total_pages,
        )
    
    def render_rss(self, articles):
        """
        渲染RSS feed
        
        Args:
            articles: 文章列表
            
        Returns:
            RSS XML字符串
        """
        return self.render_template('rss.xml', articles=articles)


def get_template_engine() -> TemplateEngine:
    """获取模板引擎实例"""
    return TemplateEngine()


def get_blog_template_engine() -> BlogTemplateEngine:
    """获取博客模板引擎实例"""
    return BlogTemplateEngine()


if __name__ == "__main__":
    # 测试模板引擎
    print("测试模板引擎...")
    
    try:
        engine = get_template_engine()
        
        # 列出可用模板
        templates = engine.list_templates()
        print(f"可用模板: {templates}")
        
        # 测试渲染简单模板
        test_template = "<h1>{{ title }}</h1><p>{{ content }}</p>"
        result = engine.render_string(test_template, title="测试标题", content="测试内容")
        print(f"渲染结果: {result}")
        
    except Exception as e:
        print(f"测试失败: {e}")