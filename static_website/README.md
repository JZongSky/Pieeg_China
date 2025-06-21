# PIEEG 静态网站

这是PIEEG官方网站的静态版本，不需要Python后端服务器，可以直接在任何Web服务器上运行。

## 📁 文件结构

```
static_website/
├── index.html          # 首页
├── forum.html          # 论坛页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── charts.js       # 图表JavaScript
├── images/             # 图片资源
│   ├── pieeg-hero.png
│   ├── pieeg-8.png
│   ├── pieeg-16.png
│   ├── ardeeg.png
│   ├── jneeg.png
│   └── brain-waves-pattern.png
├── data/
│   └── sample_eeg_data.json  # 示例EEG数据
└── README.md           # 说明文档
```

## 🚀 快速开始

### 方法1: 使用Python内置服务器
```bash
cd static_website
python3 -m http.server 8000
```
然后访问 http://localhost:8000

### 方法2: 使用Node.js http-server
```bash
# 安装http-server
npm install -g http-server

# 启动服务器
cd static_website
http-server -p 8000
```

### 方法3: 使用Nginx
将`static_website`目录复制到Nginx的web根目录，例如：
```bash
sudo cp -r static_website/* /var/www/html/
sudo systemctl restart nginx
```

### 方法4: 部署到GitHub Pages
1. 将`static_website`内容推送到GitHub仓库
2. 在仓库设置中启用GitHub Pages
3. 选择分支和根目录
4. 获得免费的https://username.github.io/repository-name 网址

## ✨ 功能特性

### 📱 响应式设计
- 支持桌面、平板和手机设备
- 自适应导航栏和布局
- 优化的移动端体验

### 📊 数据可视化
- 使用Plotly.js实现交互式图表
- EEG波形图、频谱分析图等
- 多通道脑电波数据展示
- 产品对比图表

### 🎨 现代化UI
- 基于CSS Grid和Flexbox布局
- 自定义CSS变量系统
- Font Awesome图标
- Google Fonts字体

### 🔧 技术栈
- **HTML5**: 语义化标记
- **CSS3**: 现代样式和动画
- **JavaScript**: 原生ES6+代码
- **Plotly.js**: 数据可视化
- **Font Awesome**: 图标库

## 🌐 部署选项

### 静态网站托管服务
- **GitHub Pages**: 免费，支持自定义域名
- **Netlify**: 免费层，自动部署，表单处理
- **Vercel**: 免费，快速全球CDN
- **Firebase Hosting**: Google云平台
- **AWS S3**: 亚马逊云存储
- **阿里云OSS**: 国内访问速度快

### 传统Web服务器
- **Apache HTTP Server**
- **Nginx** 
- **IIS** (Windows)
- **Caddy**

## 📈 性能优化

### 已实现的优化
- 使用CDN加载第三方库
- 压缩的图片资源
- 最小化的CSS和JavaScript
- 语义化HTML结构

### 可选优化
- 启用Gzip压缩
- 设置缓存头
- 使用WebP图片格式
- 实现Service Worker缓存

## 🔄 与Python版本的区别

### 保留的功能
- ✅ 完整的页面布局和样式
- ✅ 响应式设计
- ✅ 交互式图表
- ✅ 导航和用户界面
- ✅ 产品展示
- ✅ 论坛界面（静态）

### 移除的功能
- ❌ 用户注册和登录
- ❌ 数据库交互
- ❌ 表单提交处理
- ❌ 动态内容生成
- ❌ 后端API接口
- ❌ 文件上传功能

### 静态替代方案
- **论坛功能**: 使用Disqus、Gitalk等第三方评论系统
- **表单处理**: 使用Netlify Forms、Formspree等服务
- **用户认证**: 使用Auth0、Firebase Auth等服务
- **数据存储**: 使用Airtable、Google Sheets API等

## 🛠 自定义修改

### 修改内容
直接编辑HTML文件中的文本内容，图片路径等。

### 修改样式
编辑`css/style.css`文件，使用CSS变量系统：
```css
:root {
  --color-primary: #1A365D;
  --color-secondary: #00B4D8;
  --color-accent: #FF7D00;
}
```

### 添加页面
1. 创建新的HTML文件
2. 复制现有页面的头部和导航结构
3. 添加自定义内容
4. 更新导航链接

### 修改图表
编辑`js/charts.js`文件，使用Plotly.js API创建自定义图表。

## 📞 技术支持

如果您在使用静态网站时遇到问题，可以：
1. 检查浏览器控制台错误信息
2. 确认所有资源文件路径正确
3. 验证Web服务器配置
4. 查看网络请求状态

## 📄 许可证

与原PIEEG项目保持相同的开源许可证。

---

**注意**: 这是一个静态网站版本，适合展示和宣传用途。如需完整的交互功能，请使用Python Flask版本。 