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
    
    // 截取footer区域
    console.log('📷 截取footer区域...');
    const footer = await page.$('.site-footer');
    
    if (footer) {
        const screenshotPath = path.join(__dirname, 'screenshots', 'footer-detail.png');
        await footer.screenshot({
            path: screenshotPath
        });
        
        console.log(`✅ 已保存: ${screenshotPath}`);
    } else {
        console.log('❌ 未找到footer元素');
    }
    
    await browser.close();
    console.log('🎉 完成！');
}

takeFooterScreenshot().catch(console.error);