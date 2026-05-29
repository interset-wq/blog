# 代码高亮测试文档

本文档测试各种编程语言的代码高亮功能。

## Python

### 基础语法

```python
# 这是一个Python注释
def hello_world():
    """打印Hello World"""
    print("Hello, World!")

# 调用函数
hello_world()
```

### 类和对象

```python
class Person:
    """人类"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"我叫{self.name}，今年{self.age}岁"
    
    @staticmethod
    def species():
        return "人类"

# 创建实例
person = Person("张三", 25)
print(person.introduce())
print(Person.species())
```

### 列表推导式

```python
# 列表推导式
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# 字典推导式
square_dict = {x: x**2 for x in range(5)}

# 集合推导式
unique_squares = {x**2 for x in range(-5, 5)}

print(squares)
print(even_squares)
print(square_dict)
print(unique_squares)
```

## JavaScript

### ES6+ 语法

```javascript
// 箭头函数
const greet = (name) => `Hello, ${name}!`;

// 解构赋值
const user = { name: 'John', age: 30 };
const { name, age } = user;

// 模板字符串
const message = `My name is ${name} and I'm ${age} years old.`;

// Promise
const fetchData = () => {
    return new Promise((resolve, reject) => {
        setTimeout(() => resolve('Data loaded'), 1000);
    });
};

// async/await
async function loadData() {
    try {
        const data = await fetchData();
        console.log(data);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

### React组件

```jsx
import React, { useState, useEffect } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    useEffect(() => {
        document.title = `Count: ${count}`;
    }, [count]);
    
    return (
        <div>
            <p>You clicked {count} times</p>
            <button onClick={() => setCount(count + 1)}>
                Click me
            </button>
        </div>
    );
}

export default Counter;
```

## HTML

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>示例页面</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>欢迎来到我的网站</h1>
        <nav>
            <ul>
                <li><a href="#home">首页</a></li>
                <li><a href="#about">关于</a></li>
                <li><a href="#contact">联系</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="home">
            <h2>首页内容</h2>
            <p>这是一个示例页面。</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2026 版权所有</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>
```

## CSS

```css
/* 全局样式 */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .sidebar {
        display: none;
    }
}

/* Flexbox布局 */
.flex-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

/* Grid布局 */
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-gap: 20px;
}

/* 动画 */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.fade-in {
    animation: fadeIn 0.5s ease-in-out;
}
```

## SQL

```sql
-- 创建表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入数据
INSERT INTO users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com'),
('bob_wilson', 'bob@example.com');

-- 查询数据
SELECT 
    u.username,
    u.email,
    COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2026-01-01'
GROUP BY u.id, u.username, u.email
HAVING COUNT(o.id) > 0
ORDER BY order_count DESC
LIMIT 10;
```

## JSON

```json
{
  "name": "GitHub Issues Blog",
  "version": "1.0.0",
  "description": "基于GitHub Issues的博客系统",
  "main": "index.js",
  "scripts": {
    "start": "node server.js",
    "build": "webpack --mode production",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "react": "^18.2.0",
    "vue": "^3.3.4"
  },
  "devDependencies": {
    "webpack": "^5.88.0",
    "jest": "^29.5.0"
  },
  "keywords": ["blog", "github", "issues"],
  "author": "Developer",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  }
}
```

## YAML

```yaml
# GitHub Actions工作流
name: Build and Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Build project
      run: |
        python build.py
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./output
```

## Markdown

````markdown
# Markdown文档示例

这是一个Markdown文档的示例。

## 代码块

```python
def hello():
    print("Hello, World!")
```

## 列表

- 项目1
- 项目2
- 项目3

## 表格

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 数据1 | 数据2 | 数据3 |
````

## Shell/Bash

```bash
#!/bin/bash

# 变量定义
NAME="World"
GREETING="Hello"

# 函数定义
greet() {
    echo "$GREETING, $1!"
}

# 条件判断
if [ "$NAME" = "World" ]; then
    greet "$NAME"
else
    echo "Name is not World"
fi

# 循环
for i in {1..5}; do
    echo "Number: $i"
done

# 文件操作
if [ -f "file.txt" ]; then
    echo "File exists"
    cat file.txt
else
    echo "File does not exist"
fi

# 命令替换
CURRENT_DATE=$(date +%Y-%m-%d)
echo "Current date: $CURRENT_DATE"
```

## Docker

```dockerfile
# 基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["npm", "start"]
```

## 总结

这个文档测试了多种编程语言的代码高亮：
- Python（包括类、装饰器、推导式）
- JavaScript（ES6+、React JSX）
- HTML（完整的页面结构）
- CSS（Flexbox、Grid、动画）
- SQL（复杂查询）
- JSON（配置文件）
- YAML（CI/CD配置）
- Markdown（嵌套代码块）
- Shell/Bash（脚本）
- Docker（Dockerfile）

所有这些语言都应该有正确的语法高亮，使代码更易读。