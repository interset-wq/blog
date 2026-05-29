# 基础Markdown测试文档

这是一个用于测试基础Markdown语法的文档。

## 段落和换行

这是第一个段落。Markdown段落之间需要空行分隔。

这是第二个段落。在Markdown中，行尾添加两个空格可以实现换行。  
这是同一段落中的新行。

## 强调文本

**粗体文本** 使用双星号包裹。

*斜体文本* 使用单星号包裹。

***粗斜体文本*** 使用三个星号包裹。

~~删除线文本~~ 使用双波浪号包裹（GFM扩展）。

## 引用

> 这是一个引用块。
> 
> 引用可以包含多个段落。
> 
> > 这是嵌套引用。

## 列表

### 无序列表

- 第一项
- 第二项
  - 嵌套项 2.1
  - 嵌套项 2.2
    - 深层嵌套项 2.2.1
- 第三项

### 有序列表

1. 第一步
2. 第二步
   1. 子步骤 2.1
   2. 子步骤 2.2
3. 第三步

### 混合列表

1. 有序列表项
   - 无序子项
   - 另一个无序子项
2. 另一个有序列表项

## 链接和图片

### 链接

[GitHub](https://github.com "GitHub首页")

[相对链接](./02_gfm_features.md)

[带标题的链接](https://github.com "鼠标悬停显示的标题")

### 图片

![GitHub Logo](https://github.githubassets.com/favicons/favicon.png "GitHub Logo")

![相对路径图片](./images/test.png "测试图片")

## 代码

### 行内代码

使用 `console.log()` 输出日志。

### 代码块

```
这是一个没有语法高亮的代码块。
```

```javascript
// JavaScript代码块
function greet(name) {
    return `Hello, ${name}!`;
}

console.log(greet('World'));
```

```python
# Python代码块
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
```

## 分隔线

---

***

___

## 特殊字符

版权符号: &copy;

注册商标: &reg;

商标: &trade;

和号: &amp;

引号: &quot;

## 转义字符

\*这不是斜体\*

\[这不是链接\]

\`这不是代码\`

## 段落中的换行

这是第一行。  
这是第二行（行尾有两个空格）。

这是另一个段落。

## 长段落测试

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## 总结

这个文档测试了基础的Markdown语法，包括：
- 段落和换行
- 强调文本（粗体、斜体、删除线）
- 引用块
- 列表（有序、无序、嵌套）
- 链接和图片
- 代码（行内和块）
- 分隔线
- 特殊字符和转义字符

所有这些语法都应该被正确渲染为HTML。