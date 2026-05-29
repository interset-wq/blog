/**
 * GitHub Issues 博客 - 主题切换脚本
 */

// 主题管理器
const ThemeManager = {
    // 可用主题
    themes: {
        light: {
            name: '浅色主题',
            icon: '🌞',
            cssClass: 'theme-light'
        },
        dark: {
            name: '深色主题',
            icon: '🌙',
            cssClass: 'theme-dark'
        }
    },
    
    // 当前主题
    currentTheme: 'light',
    
    /**
     * 初始化主题管理器
     */
    init() {
        // 从本地存储获取保存的主题
        const savedTheme = localStorage.getItem('blog-theme');
        
        if (savedTheme && this.themes[savedTheme]) {
            this.currentTheme = savedTheme;
        } else {
            // 检测系统主题偏好
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                this.currentTheme = 'dark';
            }
        }
        
        // 应用主题
        this.applyTheme(this.currentTheme);
        
        // 监听系统主题变化
        this.watchSystemTheme();
        
        // 绑定主题切换按钮
        this.bindThemeToggle();
        
        console.log(`主题管理器初始化完成，当前主题: ${this.currentTheme}`);
    },
    
    /**
     * 应用主题
     * @param {string} themeName - 主题名称
     */
    applyTheme(themeName) {
        if (!this.themes[themeName]) {
            console.error(`未知主题: ${themeName}`);
            return;
        }
        
        const theme = this.themes[themeName];
        
        // 移除所有主题类
        document.documentElement.classList.remove(...Object.values(this.themes).map(t => t.cssClass));
        
        // 添加新主题类
        document.documentElement.classList.add(theme.cssClass);
        
        // 更新body类名
        document.body.className = document.body.className.replace(/theme-\w+/g, '');
        document.body.classList.add(theme.cssClass);
        
        // 更新当前主题
        this.currentTheme = themeName;
        
        // 保存到本地存储
        localStorage.setItem('blog-theme', themeName);
        
        // 更新主题切换按钮状态
        this.updateToggleButton();
        
        // 触发主题变化事件
        this.dispatchThemeChangeEvent(themeName);
        
        console.log(`已切换到主题: ${theme.name}`);
    },
    
    /**
     * 切换主题
     */
    toggle() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    },
    
    /**
     * 监听系统主题变化
     */
    watchSystemTheme() {
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            
            mediaQuery.addEventListener('change', (e) => {
                // 只有当用户没有手动设置主题时，才跟随系统
                if (!localStorage.getItem('blog-theme')) {
                    const newTheme = e.matches ? 'dark' : 'light';
                    this.applyTheme(newTheme);
                }
            });
        }
    },
    
    /**
     * 绑定主题切换按钮
     */
    bindThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggle();
            });
        }
    },
    
    /**
     * 更新主题切换按钮状态
     */
    updateToggleButton() {
        const themeToggle = document.getElementById('theme-toggle');
        
        if (themeToggle) {
            const theme = this.themes[this.currentTheme];
            
            // 更新按钮提示
            themeToggle.title = `当前: ${theme.name}，点击切换`;
            themeToggle.setAttribute('aria-label', `切换主题，当前: ${theme.name}`);
            
            // 更新按钮图标显示
            const lightIcon = themeToggle.querySelector('.light-icon');
            const darkIcon = themeToggle.querySelector('.dark-icon');
            
            if (lightIcon && darkIcon) {
                lightIcon.style.display = this.currentTheme === 'light' ? 'none' : 'inline';
                darkIcon.style.display = this.currentTheme === 'dark' ? 'none' : 'inline';
            }
        }
    },
    
    /**
     * 触发主题变化事件
     * @param {string} themeName - 新主题名称
     */
    dispatchThemeChangeEvent(themeName) {
        const event = new CustomEvent('themechange', {
            detail: {
                theme: themeName,
                themeConfig: this.themes[themeName]
            }
        });
        
        document.dispatchEvent(event);
        
        // 更新Giscus主题
        this.updateGiscusTheme(themeName);
    },
    
    /**
     * 更新Giscus评论系统主题
     * @param {string} themeName - 主题名称
     */
    updateGiscusTheme(themeName) {
        // Giscus主题映射
        const giscusThemeMap = {
            'light': 'light',
            'dark': 'dark'
        };
        
        const giscusTheme = giscusThemeMap[themeName] || 'light';
        
        // 向Giscus iframe发送主题消息
        const giscusFrame = document.querySelector('iframe.giscus-frame');
        if (giscusFrame) {
            giscusFrame.contentWindow.postMessage(
                { giscus: { setConfig: { theme: giscusTheme } } },
                'https://giscus.app'
            );
        }
    },
    
    /**
     * 获取当前主题
     * @returns {string} 当前主题名称
     */
    getCurrentTheme() {
        return this.currentTheme;
    },
    
    /**
     * 获取主题配置
     * @param {string} themeName - 主题名称
     * @returns {Object} 主题配置
     */
    getThemeConfig(themeName) {
        return this.themes[themeName] || null;
    },
    
    /**
     * 检查是否为深色主题
     * @returns {boolean} 是否为深色主题
     */
    isDarkTheme() {
        return this.currentTheme === 'dark';
    },
    
    /**
     * 重置为系统主题
     */
    resetToSystemTheme() {
        localStorage.removeItem('blog-theme');
        
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            this.applyTheme('dark');
        } else {
            this.applyTheme('light');
        }
    }
};

// 页面加载完成后初始化主题管理器
document.addEventListener('DOMContentLoaded', function() {
    ThemeManager.init();
});

// 导出主题管理器供其他脚本使用
window.ThemeManager = ThemeManager;

// 为其他脚本提供主题变化监听
document.addEventListener('themechange', function(e) {
    console.log('主题已变化:', e.detail);
    
    // 这里可以添加其他需要响应主题变化的代码
    // 例如：更新图表颜色、更新代码高亮主题等
});

/**
 * 主题相关的工具函数
 */
const ThemeUtils = {
    /**
     * 获取CSS变量值
     * @param {string} variableName - CSS变量名
     * @returns {string} CSS变量值
     */
    getCSSVariable(variableName) {
        return getComputedStyle(document.documentElement).getPropertyValue(variableName).trim();
    },
    
    /**
     * 设置CSS变量值
     * @param {string} variableName - CSS变量名
     * @param {string} value - CSS变量值
     */
    setCSSVariable(variableName, value) {
        document.documentElement.style.setProperty(variableName, value);
    },
    
    /**
     * 获取当前主题的主要颜色
     * @returns {Object} 主题颜色对象
     */
    getThemeColors() {
        return {
            background: this.getCSSVariable('--bg-color'),
            text: this.getCSSVariable('--text-color'),
            heading: this.getCSSVariable('--heading-color'),
            link: this.getCSSVariable('--link-color'),
            border: this.getCSSVariable('--border-color')
        };
    },
    
    /**
     * 应用自定义主题
     * @param {Object} customTheme - 自定义主题配置
     */
    applyCustomTheme(customTheme) {
        Object.entries(customTheme).forEach(([variable, value]) => {
            this.setCSSVariable(variable, value);
        });
    }
};

// 导出主题工具函数
window.ThemeUtils = ThemeUtils;