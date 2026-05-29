const puppeteer = require('puppeteer');
const path = require('path');

async function takeFooterScreenshot() {
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
    
    // 获取footer元素的位置和大小
    console.log('🔍 查找footer元素...');
    const footer = await page.$('.site-footer');
    
    if (footer) {
        const footerRect = await footer.boundingBox();
        console.log(`Footer位置: x=${footerRect.x}, y=${footerRect.y}, width=${footerRect.width}, height=${footerRect.height}`);
        
        // 截取footer区域，添加一些边距
        const screenshotPath = path.join(__dirname, 'screenshots', 'footer-only.png');
        await page.screenshot({
            path: screenshotPath,
            clip: {
                x: Math.max(0, footerRect.x - 10),
                y: Math.max(0, footerRect.y - 10),
                width: footerRect.width + 20,
                height: footerRect.height + 20
            }
        });
        
        console.log(`✅ 已保存: ${screenshotPath}`);
    } else {
        console.log('❌ 未找到footer元素');
    }
    
    await browser.close();
    console.log('🎉 完成！');
}

takeFooterScreenshot().catch(console.error);