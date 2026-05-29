import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.extensions.nl2br import Nl2BrExtension
from pygments.formatters import HtmlFormatter
import re
import os
import sys

# 检查pymdownx是否可用
try:
    import pymdownx
    PYMDOWNX_AVAILABLE = True
except ImportError:
    PYMDOWNX_AVAILABLE = False
    print("警告: pymdown-extensions未安装，GFM功能可能受限")

# 添加父目录到路径，以便导入config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class MarkdownParser:
    """Markdown解析器，将Markdown转换为HTML"""
    
    def __init__(self):
        """初始化Markdown解析器"""
        self._setup_extensions()
    
    def _setup_extensions(self):
        """设置Markdown扩展，包括GFM支持"""
        # 使用字符串形式的扩展名称
        self.extensions = [
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
            'markdown.extensions.nl2br',
            'markdown.extensions.smarty',
            'markdown.extensions.wikilinks',
            'markdown.extensions.meta',
            'markdown.extensions.abbr',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.md_in_html',
        ]
        
        # 添加GFM扩展（如果可用）
        if PYMDOWNX_AVAILABLE:
            self.extensions.extend([
                'pymdownx.tasklist',  # 任务列表
                'pymdownx.tilde',     # 删除线和下标
                'pymdownx.smartsymbols',  # 智能符号
                'pymdownx.mark',      # 高亮标记
                'pymdownx.keys',      # 键盘按键
                'pymdownx.caret',     # 上标
                'pymdownx.details',   # 折叠块
            ])
        
        self.extension_configs = {
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'linenums': config.CODE_HILITE_LINENOS,
                'guess_lang': True,
            },
            'markdown.extensions.toc': {
                'title': '目录',
                'toc_class': 'toc',
                'anchorlink': True,
                'permalink': True,
                'permalink_class': 'headerlink',
                'permalink_title': '永久链接',
            },
        }
        
        # GFM扩展配置 - 使用默认配置
        # 注意：pymdownx扩展有默认配置，这里只配置需要自定义的部分
        if PYMDOWNX_AVAILABLE:
            self.extension_configs.update({
                'pymdownx.tasklist': {
                    'custom_checkbox': True,
                },
                'pymdownx.tilde': {
                    'subscript': True,
                },
                'pymdownx.smartsymbols': {
                    'trademark': True,
                    'copyright': True,
                    'registered': True,
                },
            })
    
    def parse(self, markdown_text: str) -> str:
        """
        将Markdown文本转换为HTML
        
        Args:
            markdown_text: Markdown文本
            
        Returns:
            HTML字符串
        """
        if not markdown_text:
            return ''
        
        # 创建Markdown实例
        md = markdown.Markdown(
            extensions=self.extensions,
            extension_configs=self.extension_configs,
            output_format='html5',
        )
        
        # 转换Markdown为HTML
        html = md.convert(markdown_text)
        
        # 后处理
        html = self._post_process(html)
        
        return html
    
    def _post_process(self, html: str) -> str:
        """
        后处理HTML，添加额外的样式和功能
        
        Args:
            html: 原始HTML
            
        Returns:
            处理后的HTML
        """
        # 为表格添加响应式包装器
        html = re.sub(
            r'<table>',
            '<div class="table-responsive"><table class="table">',
            html
        )
        html = re.sub(
            r'</table>',
            '</table></div>',
            html
        )
        
        # 为图片添加懒加载和响应式类
        html = re.sub(
            r'<img([^>]*?)>',
            r'<img\1 class="img-fluid" loading="lazy">',
            html
        )
        
        # 为外部链接添加target="_blank"
        html = re.sub(
            r'<a href="(https?://[^"]*?)"',
            r'<a href="\1" target="_blank" rel="noopener noreferrer"',
            html
        )
        
        return html
    
    def get_pygments_css(self) -> str:
        """
        获取Pygments代码高亮的CSS样式
        
        Returns:
            CSS字符串
        """
        formatter = HtmlFormatter(style=config.CODE_HILITE_STYLE)
        return formatter.get_style_defs('.highlight')
    
    def extract_toc(self, markdown_text: str) -> str:
        """
        从Markdown文本中提取目录
        
        Args:
            markdown_text: Markdown文本
            
        Returns:
            目录HTML
        """
        if not markdown_text:
            return ''
        
        # 创建临时Markdown实例来提取TOC
        md = markdown.Markdown(
            extensions=['toc'],
            extension_configs={
                'toc': {
                    'title': '目录',
                    'toc_class': 'toc',
                    'anchorlink': True,
                }
            }
        )
        
        # 转换以生成TOC
        md.convert(markdown_text)
        
        return md.toc
    
    def sanitize_html(self, html: str) -> str:
        """
        清理HTML，移除潜在的危险标签和属性
        
        Args:
            html: 原始HTML
            
        Returns:
            清理后的HTML
        """
        # 移除script标签
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        
        # 移除on*事件属性
        html = re.sub(r'\s*on\w+="[^"]*"', '', html)
        html = re.sub(r"\s*on\w+='[^']*'", '', html)
        
        # 移除javascript:协议
        html = re.sub(r'javascript:', '', html, flags=re.IGNORECASE)
        
        return html
    
    def markdown_to_plain_text(self, markdown_text: str) -> str:
        """
        将Markdown转换为纯文本（移除格式）
        
        Args:
            markdown_text: Markdown文本
            
        Returns:
            纯文本
        """
        if not markdown_text:
            return ''
        
        # 移除标题标记
        text = re.sub(r'^#+\s*', '', markdown_text, flags=re.MULTILINE)
        
        # 移除粗体和斜体标记
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)
        
        # 移除链接，保留文本
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # 移除图片标记
        text = re.sub(r'!\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
        # 移除代码块
        text = re.sub(r'```[^\`]*```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # 移除水平线
        text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        
        # 移除块引用标记
        text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
        
        # 移除列表标记
        text = re.sub(r'^\s*[-*+]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
        
        # 清理多余空白
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text


def get_markdown_parser() -> MarkdownParser:
    """获取Markdown解析器实例"""
    return MarkdownParser()


if __name__ == "__main__":
    # 测试Markdown解析器
    test_markdown = """
# 测试标题

这是一个测试段落。

## 代码示例

```python
def hello():
    print("Hello, World!")
```

**粗体文本**和*斜体文本*

- 列表项1
- 列表项2

| 列1 | 列2 |
|-----|-----|
| 数据1 | 数据2 |
"""
    
    parser = get_markdown_parser()
    html = parser.parse(test_markdown)
    
    print("生成的HTML:")
    print(html[:500] + "..." if len(html) > 500 else html)
    
    print("\nPygments CSS:")
    css = parser.get_pygments_css()
    print(css[:200] + "..." if len(css) > 200 else css)