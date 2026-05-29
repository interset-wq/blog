const puppeteer = require('puppeteer');
const path = require('path');

async function debugFooter() {
    console.log('🚀 启动浏览器...');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 设置视口大小
    await page.setViewport({ width: 1440, height: 900 });
    
    // 访问首页
    console.log('📷 访问首页...');
    await page.goto('http://localhost:8000', { waitUntil: 'networkidle2' });
    
    // 等待页面加载
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 检查footer元素
    console.log('🔍 检查footer元素...');
    
    const footerInfo = await page.evaluate(() => {
        const footer = document.querySelector('.site-footer');
        if (!footer) {
            return { found: false };
        }
        
        const rect = footer.getBoundingClientRect();
        const style = window.getComputedStyle(footer);
        
        return {
            found: true,
            rect: {
                x: rect.x,
                y: rect.y,
                width: rect.width,
                height: rect.height
            },
            style: {
                padding: style.padding,
                margin: style.margin,
                backgroundColor: style.backgroundColor
            },
            innerHTML: footer.innerHTML.substring(0, 500) + '...',
            childElementCount: footer.childElementCount,
            children: Array.from(footer.children).map(child => ({
                tagName: child.tagName,
                className: child.className,
                height: child.getBoundingClientRect().height
            }))
        };
    });
    
    console.log('Footer信息:', JSON.stringify(footerInfo, null, 2));
    
    // 截取footer区域
    if (footerInfo.found) {
        const screenshotPath = path.join(__dirname, 'screenshots', 'footer-debug.png');
        await page.screenshot({
            path: screenshotPath,
            clip: {
                x: Math.max(0, footerInfo.rect.x - 10),
                y: Math.max(0, footerInfo.rect.y - 10),
                width: footerInfo.rect.width + 20,
                height: footerInfo.rect.height + 20
            }
        });
        
        console.log(`✅ 已保存: ${screenshotPath}`);
    }
    
    await browser.close();
    console.log('🎉 完成！');
}

debugFooter().catch(console.error);