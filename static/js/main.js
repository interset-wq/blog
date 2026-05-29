/**
 * GitHub Issues 博客 - 主JavaScript文件
 */

// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    console.log('GitHub Issues 博客已加载');
    
    // 初始化各个模块
    initMobileMenu();
    initBackToTop();
    initSearch();
    initCodeHighlight();
    initImageLazyLoading();
    initExternalLinks();
});

/**
 * 初始化移动端菜单
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            menuToggle.classList.toggle('active');
        });
        
        // 点击菜单项后关闭菜单
        const navLinks = mainNav.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                mainNav.classList.remove('active');
                menuToggle.classList.remove('active');
            });
        });
    }
}

/**
 * 初始化回到顶部按钮
 */
function initBackToTop() {
    const backToTopButton = document.getElementById('back-to-top');
    
    if (backToTopButton) {
        // 监听滚动事件
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });
        
        // 点击回到顶部
        backToTopButton.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

/**
 * 初始化搜索功能
 */
function initSearch() {
    const searchForm = document.querySelector('.search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const queryInput = this.querySelector('.search-input');
            const query = queryInput.value.trim();
            
            if (query) {
                // 如果存在搜索索引，执行客户端搜索
                performSearch(query);
            }
        });
    }
}

/**
 * 执行搜索
 * @param {string} query - 搜索关键词
 */
function performSearch(query) {
    // 尝试加载搜索索引
    fetch('/search-index.json')
        .then(response => response.json())
        .then(searchIndex => {
            const results = searchInIndex(searchIndex, query);
            displaySearchResults(results, query);
        })
        .catch(error => {
            console.error('搜索索引加载失败:', error);
            // 如果没有搜索索引，跳转到GitHub搜索
            const repoUrl = document.querySelector('a[href*="github.com"]').href;
            if (repoUrl) {
                window.open(`${repoUrl}/issues?q=${encodeURIComponent(query)}`, '_blank');
            }
        });
}

/**
 * 在搜索索引中搜索
 * @param {Array} index - 搜索索引
 * @param {string} query - 搜索关键词
 * @returns {Array} 搜索结果
 */
function searchInIndex(index, query) {
    const queryLower = query.toLowerCase();
    
    return index.filter(item => {
        const titleMatch = item.title.toLowerCase().includes(queryLower);
        const excerptMatch = item.excerpt.toLowerCase().includes(queryLower);
        const tagMatch = item.tags.some(tag => tag.toLowerCase().includes(queryLower));
        
        return titleMatch || excerptMatch || tagMatch;
    });
}

/**
 * 显示搜索结果
 * @param {Array} results - 搜索结果
 * @param {string} query - 搜索关键词
 */
function displaySearchResults(results, query) {
    // 创建搜索结果模态框
    const modal = document.createElement('div');
    modal.className = 'search-modal';
    modal.innerHTML = `
        <div class="search-modal-content">
            <div class="search-modal-header">
                <h2>搜索结果: "${query}"</h2>
                <button class="search-modal-close">&times;</button>
            </div>
            <div class="search-modal-body">
                ${results.length > 0 ? 
                    results.map(item => `
                        <div class="search-result-item">
                            <h3><a href="${item.url}">${item.title}</a></h3>
                            <p>${item.excerpt}</p>
                            <div class="search-result-meta">
                                <span class="search-result-date">${new Date(item.date).toLocaleDateString()}</span>
                                <div class="search-result-tags">
                                    ${item.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                                </div>
                            </div>
                        </div>
                    `).join('') 
                    : '<p class="no-results">未找到相关文章</p>'
                }
            </div>
        </div>
    `;
    
    // 添加到页面
    document.body.appendChild(modal);
    
    // 关闭按钮事件
    const closeButton = modal.querySelector('.search-modal-close');
    closeButton.addEventListener('click', function() {
        document.body.removeChild(modal);
    });
    
    // 点击模态框外部关闭
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            document.body.removeChild(modal);
        }
    });
    
    // 按ESC键关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && document.body.contains(modal)) {
            document.body.removeChild(modal);
        }
    });
}

/**
 * 初始化代码高亮
 */
function initCodeHighlight() {
    // 为代码块添加复制按钮
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(block => {
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-button';
        copyButton.textContent = '复制';
        copyButton.title = '复制代码';
        
        copyButton.addEventListener('click', function() {
            const code = block.textContent;
            navigator.clipboard.writeText(code).then(() => {
                copyButton.textContent = '已复制!';
                setTimeout(() => {
                    copyButton.textContent = '复制';
                }, 2000);
            }).catch(err => {
                console.error('复制失败:', err);
            });
        });
        
        // 将按钮添加到代码块容器
        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
    });
}

/**
 * 初始化图片懒加载
 */
function initImageLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // 降级处理：直接加载所有图片
        images.forEach(img => {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
}

/**
 * 初始化外部链接
 */
function initExternalLinks() {
    const externalLinks = document.querySelectorAll('a[href^="http"]');
    
    externalLinks.forEach(link => {
        // 检查是否是外部链接
        if (link.hostname !== window.location.hostname) {
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
            
            // 添加外部链接图标
            const icon = document.createElement('span');
            icon.className = 'external-link-icon';
            icon.innerHTML = ' ↗';
            icon.style.fontSize = '0.75em';
            link.appendChild(icon);
        }
    });
}

/**
 * 工具函数：防抖
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间
 * @returns {Function} 防抖后的函数
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 工具函数：节流
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 限制时间
 * @returns {Function} 节流后的函数
 */
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// 导出函数供其他模块使用
window.BlogJS = {
    initMobileMenu,
    initBackToTop,
    initSearch,
    performSearch,
    initCodeHighlight,
    initImageLazyLoading,
    initExternalLinks,
    debounce,
    throttle
};