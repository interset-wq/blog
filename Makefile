# GitHub Issues 博客系统 Makefile
# 提供通用命令行管理功能

.PHONY: help serve test build clean install deploy

# 默认目标
help: ## 显示帮助信息
	@echo "GitHub Issues 博客系统"
	@echo "====================="
	@echo ""
	@echo "可用命令:"
	@echo "  make help      - 显示此帮助信息"
	@echo "  make install   - 安装依赖"
	@echo "  make serve     - 启动本地服务器预览"
	@echo "  make test      - 运行测试"
	@echo "  make build     - 构建项目"
	@echo "  make clean     - 清理生成的文件"
	@echo "  make deploy    - 部署到GitHub Pages"
	@echo "  make docs      - 生成测试文档"
	@echo "  make lint      - 代码检查"
	@echo "  make format    - 代码格式化"
	@echo ""
	@echo "示例:"
	@echo "  make install   # 安装依赖"
	@echo "  make serve     # 启动本地服务器"
	@echo "  make test      # 运行测试"

# 安装依赖
install: ## 安装Python依赖
	@echo "安装依赖..."
	cd renderer && pip install -r requirements.txt
	@echo "依赖安装完成！"

# 启动本地服务器
serve: ## 启动本地服务器预览
	@echo "启动本地服务器..."
	@echo "访问 http://localhost:8000 查看网站"
	@echo "按 Ctrl+C 停止服务器"
	@echo ""
	cd build && python3 -m http.server 8000

# 启动开发服务器（带热重载）
serve-dev: ## 启动开发服务器（带热重载）
	@echo "启动开发服务器..."
	@echo "访问 http://localhost:8000 查看网站"
	@echo "文件更改时自动刷新"
	@echo ""
	@echo "注意：需要安装 livereload: pip install livereload"
	@python -c "
	import livereload
	server = livereload.Server()
	server.watch('output/', livereload.ReloadServer)
	server.serve(port=8000, root='output')
	"

# 运行测试
test: ## 运行测试
	@echo "运行测试..."
	@echo "1. 运行渲染器测试..."
	python test_renderer.py
	@echo ""
	@echo "2. 运行文档测试..."
	python test_docs/test_docs.py
	@echo ""
	@echo "测试完成！"

# 构建项目
build: ## 构建项目（生成静态文件）
	@echo "构建项目..."
	@echo "设置环境变量..."
	@if [ -f .env ]; then \
		echo "使用 .env 文件中的环境变量"; \
		export $(cat .env | xargs); \
	else \
		echo "警告：未找到 .env 文件，使用默认值"; \
		export GITHUB_OWNER=test-owner; \
		export GITHUB_REPO=test-repo; \
		export GITHUB_TOKEN=test-token; \
	fi
	@echo "运行渲染器..."
	cd renderer && python3 render.py
	@echo ""
	@echo "构建完成！静态文件已生成到 build/ 目录"

# 清理生成的文件
clean: ## 清理生成的文件
	@echo "清理生成的文件..."
	@echo "删除 build/ 目录..."
	rm -rf build/
	@echo "删除 __pycache__ 目录..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "删除 .pyc 文件..."
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "删除 .pyo 文件..."
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "清理完成！"

# 部署到GitHub Pages
deploy: build ## 构建并部署到GitHub Pages
	@echo "部署到GitHub Pages..."
	@if [ -d ".git" ]; then \
		echo "检测到Git仓库"; \
		cd build && \
		git init && \
		git add -A && \
		git commit -m "Deploy to GitHub Pages" && \
		git push -f git@github.com:$(GITHUB_OWNER)/$(GITHUB_REPO).git master:gh-pages; \
		echo "部署完成！"; \
		echo "访问 https://$(GITHUB_OWNER).github.io/$(GITHUB_REPO)/"; \
	else \
		echo "错误：未检测到Git仓库"; \
		echo "请先初始化Git仓库：git init"; \
		exit 1; \
	fi

# 生成测试文档
docs: ## 生成测试文档
	@echo "生成测试文档..."
	@echo "运行文档测试..."
	python test_docs/test_docs.py
	@echo ""
	@echo "测试文档已生成到 build/test_docs/ 目录"
	@echo "可以在浏览器中打开查看效果"

# 代码检查
lint: ## 代码检查
	@echo "运行代码检查..."
	@echo "检查Python代码..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 renderer/ --max-line-length=120 --ignore=E501,W503; \
	else \
		echo "警告：flake8未安装，跳过代码检查"; \
		echo "安装：pip install flake8"; \
	fi
	@echo ""
	@echo "检查JavaScript代码..."
	@if [ -f "static/js/main.js" ]; then \
		echo "JavaScript文件存在"; \
	else \
		echo "警告：未找到JavaScript文件"; \
	fi
	@echo ""
	@echo "代码检查完成！"

# 代码格式化
format: ## 代码格式化
	@echo "运行代码格式化..."
	@echo "格式化Python代码..."
	@if command -v black >/dev/null 2>&1; then \
		black renderer/ --line-length=120; \
	else \
		echo "警告：black未安装，跳过代码格式化"; \
		echo "安装：pip install black"; \
	fi
	@echo ""
	@echo "格式化JavaScript代码..."
	@if [ -f "static/js/main.js" ]; then \
		echo "JavaScript文件存在"; \
	else \
		echo "警告：未找到JavaScript文件"; \
	fi
	@echo ""
	@echo "代码格式化完成！"

# 安装开发依赖
install-dev: ## 安装开发依赖
	@echo "安装开发依赖..."
	pip install pytest black flake8 livereload
	@echo "开发依赖安装完成！"

# 运行单元测试
test-unit: ## 运行单元测试
	@echo "运行单元测试..."
	@if [ -d "tests" ]; then \
		python -m pytest tests/ -v; \
	else \
		echo "警告：未找到 tests/ 目录"; \
		echo "跳过单元测试"; \
	fi

# 生成覆盖率报告
coverage: ## 生成测试覆盖率报告
	@echo "生成测试覆盖率报告..."
	@if command -v coverage >/dev/null 2>&1; then \
		coverage run -m pytest tests/; \
		coverage report; \
		coverage html; \
		echo "覆盖率报告已生成到 htmlcov/ 目录"; \
	else \
		echo "警告：coverage未安装"; \
		echo "安装：pip install coverage"; \
	fi

# 检查依赖安全
security: ## 检查依赖安全
	@echo "检查依赖安全..."
	@if command -v safety >/dev/null 2>&1; then \
		safety check -r renderer/requirements.txt; \
	else \
		echo "警告：safety未安装"; \
		echo "安装：pip install safety"; \
	fi

# 生成依赖树
deps: ## 显示依赖树
	@echo "显示依赖树..."
	@if command -v pipdeptree >/dev/null 2>&1; then \
		pipdeptree; \
	else \
		echo "警告：pipdeptree未安装"; \
		echo "安装：pip install pipdeptree"; \
		echo ""; \
		echo "当前已安装的包："; \
		pip list; \
	fi

# 备份项目
backup: ## 备份项目
	@echo "备份项目..."
	@BACKUP_NAME="backup_$(shell date +%Y%m%d_%H%M%S).tar.gz"; \
	echo "创建备份: $$BACKUP_NAME"; \
	tar -czvf "$$BACKUP_NAME" \
		--exclude=".venv" \
		--exclude=".git" \
		--exclude="__pycache__" \
		--exclude="*.pyc" \
		--exclude="output" \
		.; \
	echo "备份完成: $$BACKUP_NAME"

# 恢复项目
restore: ## 恢复项目（从备份）
	@echo "恢复项目..."
	@echo "可用的备份文件："
	@ls -la backup_*.tar.gz 2>/dev/null || echo "未找到备份文件"
	@echo ""
	@echo "请使用以下命令恢复："
	@echo "  tar -xzvf backup_FILE.tar.gz"

# 显示项目信息
info: ## 显示项目信息
	@echo "项目信息"
	@echo "========"
	@echo "项目名称: GitHub Issues 博客系统"
	@echo "项目位置: $(shell pwd)"
	@echo "Python版本: $(shell python --version)"
	@echo ""
	@echo "目录结构:"
	@echo "  renderer/     - 渲染器代码"
	@echo "  templates/    - HTML模板"
	@echo "  static/       - 静态资源"
	@echo "  test_docs/    - 测试文档"
	@echo "  output/       - 生成的静态文件"
	@echo ""
	@echo "文件统计:"
	@echo "  Python文件: $(shell find . -name "*.py" -not -path "./.venv/*" | wc -l)"
	@echo "  HTML文件: $(shell find . -name "*.html" -not -path "./.venv/*" | wc -l)"
	@echo "  CSS文件: $(shell find . -name "*.css" -not -path "./.venv/*" | wc -l)"
	@echo "  JavaScript文件: $(shell find . -name "*.js" -not -path "./.venv/*" | wc -l)"
	@echo "  Markdown文件: $(shell find . -name "*.md" -not -path "./.venv/*" | wc -l)"

# 监控文件变化并自动构建
watch: ## 监控文件变化并自动构建
	@echo "监控文件变化..."
	@echo "按 Ctrl+C 停止监控"
	@echo ""
	@if command -v inotifywait >/dev/null 2>&1; then \
		while true; do \
			inotifywait -r -e modify,create,delete \
				renderer/ templates/ static/; \
			echo "文件变化检测到，重新构建..."; \
			make build; \
		done; \
	else \
		echo "警告：inotifywait未安装"; \
		echo "安装：sudo apt-get install inotify-tools"; \
		echo ""; \
		echo "使用简单监控..."; \
		while true; do \
			sleep 5; \
			make build; \
		done; \
	fi