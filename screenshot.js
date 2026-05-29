const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// 要截图的页面列表
const pages = [
    { name: 'index', url: '/', title: '首页' },
    { name: 'archives', url: '/archives.html', title: '归档页面' },
    { name: 'categories', url: '/categories.html', title: '分类页面' },
    { name: 'about', url: '/about.html', title: '关于页面' },
    { name: 'links', url: '/links.html', title: '友链页面' },
    { name: 'post', url: '/posts/1.html', title: '文章详情' },
    { name: 'tags', url: '/tags/test.html', title: '标签页面' },
];

async function takeScreenshots() {
    console.log('🚀 启动浏览器...');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    // 创建截图目录
    const screenshotDir = path.join(__dirname, 'screenshots');
    if (!fs.existsSync(screenshotDir)) {
        fs.mkdirSync(screenshotDir);
    }
    
    console.log('📸 开始截图...\n');
    
    for (const page of pages) {
        try {
            console.log(`📷 截图: ${page.title} (${page.url})`);
            
            const tab = await browser.newPage();
            
            // 设置视口大小
            await tab.setViewport({ width: 1440, height: 900 });
            
            // 访问页面
            const url = `http://localhost:8000${page.url}`;
            await tab.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
            
            // 等待页面加载
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // 截取完整页面
            const screenshotPath = path.join(screenshotDir, `${page.name}.png`);
            await tab.screenshot({
                path: screenshotPath,
                fullPage: true
            });
            
            console.log(`   ✅ 已保存: ${screenshotPath}`);
            
            await tab.close();
        } catch (error) {
            console.error(`   ❌ 截图失败: ${error.message}`);
        }
    }
    
    // 截取移动端视图
    console.log('\n📱 截取移动端视图...');
    
    const mobilePage = await browser.newPage();
    await mobilePage.setViewport({ width: 375, height: 812 }); // iPhone X 尺寸
    
    try {
        await mobilePage.goto('http://localhost:8000', { waitUntil: 'networkidle2' });
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const mobileScreenshotPath = path.join(screenshotDir, 'index-mobile.png');
        await mobilePage.screenshot({
            path: mobileScreenshotPath,
            fullPage: true
        });
        
        console.log(`   ✅ 已保存: ${mobileScreenshotPath}`);
    } catch (error) {
        console.error(`   ❌ 移动端截图失败: ${error.message}`);
    }
    
    await mobilePage.close();
    await browser.close();
    
    console.log('\n🎉 截图完成！');
    console.log(`📁 截图保存在: ${screenshotDir}`);
}

// 运行截图
takeScreenshots().catch(console.error);