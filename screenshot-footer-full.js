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
    
    // 滚动到页面底部
    console.log('📜 滚动到页面底部...');
    await page.evaluate(() => {
        window.scrollTo(0, document.body.scrollHeight);
    });
    
    // 等待滚动完成
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 截取整个页面，但只显示底部区域
    console.log('📷 截取页面底部区域...');
    const screenshotPath = path.join(__dirname, 'screenshots', 'page-bottom.png');
    
    // 获取页面高度
    const pageHeight = await page.evaluate(() => document.body.scrollHeight);
    
    // 截取底部500像素区域
    await page.screenshot({
        path: screenshotPath,
        clip: {
            x: 0,
            y: Math.max(0, pageHeight - 500),
            width: 1440,
            height: 500
        }
    });
    
    console.log(`✅ 已保存: ${screenshotPath}`);
    
    await browser.close();
    console.log('🎉 完成！');
}

takeFooterScreenshot().catch(console.error);