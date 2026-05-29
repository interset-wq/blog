#!/usr/bin/env python3
"""
测试文档渲染脚本
使用完整的博客模板系统渲染测试文档
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 设置测试环境变量
os.environ['GITHUB_OWNER'] = 'test-owner'
os.environ['GITHUB_REPO'] = 'test-repo'
os.environ['GITHUB_TOKEN'] = 'test-token'

# 导入模块
from renderer.utils.markdown_parser import get_markdown_parser
from renderer.utils.template_engine import get_blog_template_engine
import renderer.config as config

def copy_static_assets():
    """复制静态资源到输出目录"""
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

def test_document(file_path: str, template_engine, markdown_parser) -> bool:
    """测试单个文档"""
    print(f"测试文档: {file_path}")
    
    try:
        # 读取文档内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析Markdown
        content_html = markdown_parser.parse(content)
        
        # 检查渲染结果
        if not content_html:
            print(f"  ❌ 渲染结果为空")
            return False
        
        # 创建文章数据
        article = {
            'number': 1,
            'title': Path(file_path).stem.replace('_', ' ').title(),
            'body': content,
            'state': 'open',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'labels': ['test', 'documentation'],
            'user': {
                'login': 'test-user',
                'avatar_url': 'https://github.com/identicons/test-user.png',
                'html_url': 'https://github.com/test-user',
            },
            'comments': 0,
            'html_url': f'https://github.com/test-owner/test-repo/issues/1',
            'formatted_date': datetime.now().strftime('%Y年%m月%d日'),
            'reading_time': '5分钟',
            'excerpt': content[:200] + '...' if len(content) > 200 else content,
        }
        
        # 使用模板引擎渲染完整页面
        full_html = template_engine.render_article(
            article=article,
            content_html=content_html,
        )
        
        # 检查关键元素
        checks = {
            '完整HTML结构': '<!DOCTYPE html>' in full_html,
            '头部导航': '<header' in full_html,
            '文章内容': '<article' in full_html,
            '底部信息': '<footer' in full_html,
            'CSS样式': 'style.css' in full_html,
            'JavaScript': 'main.js' in full_html,
            '标题': '<h1' in full_html or '<h2' in full_html,
            '段落': '<p>' in full_html,
            '代码块': '<code>' in full_html or '<pre>' in full_html,
            '列表': '<ul>' in full_html or '<ol>' in full_html,
            '链接': '<a ' in full_html,
            '表格': '<table>' in full_html,
            '引用': '<blockquote>' in full_html,
        }
        
        # 检查GFM特性
        gfm_checks = {
            '任务列表': 'task-list' in full_html,
            '删除线': '<del>' in full_html,
            '高亮标记': '<mark>' in full_html,
            '键盘按键': '<kbd>' in full_html,
        }
        
        # 输出检查结果
        print(f"  HTML长度: {len(full_html)} 字符")
        print(f"  结构检查:")
        
        all_passed = True
        for name, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"    {status} {name}")
            if not passed and name in ['完整HTML结构', '头部导航', '文章内容', '底部信息']:
                all_passed = False
        
        # 检查GFM特性
        print(f"  GFM特性检查:")
        for name, passed in gfm_checks.items():
            status = "✅" if passed else "⬜"
            print(f"    {status} {name}")
        
        # 保存渲染结果
        output_dir = project_root / "build" / "test_docs"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{Path(file_path).stem}.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"  输出文件: {output_file}")
        
        return all_passed
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("Markdown文档渲染测试（使用完整模板系统）")
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
    
    # 获取测试文档目录
    test_docs_dir = Path(__file__).parent
    
    # 获取所有测试文档
    test_files = list(test_docs_dir.glob("*.md"))
    
    if not test_files:
        print("❌ 未找到测试文档")
        return 1
    
    print(f"找到 {len(test_files)} 个测试文档:")
    for file in test_files:
        print(f"  - {file.name}")
    
    print("\n" + "=" * 60)
    
    # 测试每个文档
    results = []
    for file_path in test_files:
        if file_path.name == "test_docs.py":  # 跳过测试脚本本身
            continue
        print(f"\n{'='*60}")
        result = test_document(file_path, template_engine, markdown_parser)
        results.append((file_path.name, result))
        print(f"{'='*60}")
    
    # 总结结果
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for filename, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {filename}")
    
    print(f"\n总计: {passed}/{total} 个文档测试通过")
    
    if passed == total:
        print("\n🎉 所有测试文档渲染成功！")
        print("\n渲染结果已保存到: output/test_docs/")
        print("可以在浏览器中打开查看效果。")
        print("\n启动本地服务器预览:")
        print("  make serve")
        print("  或")
        print("  cd output && python3 -m http.server 8000")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个文档测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())