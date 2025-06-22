# PIEEG Hugo 网站

这是使用Hugo静态网站生成器构建的PIEEG官方网站，提供了更好的内容管理和模板复用能力。

## 🏗️ 项目结构

```
pieeg-hugo/
├── hugo.toml              # Hugo配置文件
├── content/               # 内容文件（Markdown）
│   ├── _index.md         # 首页内容

├── layouts/               # 模板文件
│   ├── _default/
│   │   └── baseof.html   # 基础模板
│   └── index.html        # 首页模板
├── static/                # 静态资源
│   ├── css/
│   ├── js/
│   ├── images/
│   └── data/
├── data/                  # 数据文件
│   ├── products.yaml     # 产品数据
│   └── applications.yaml # 应用场景数据
└── public/                # 生成的静态网站（hugo构建后）
```

## 🚀 快速开始

### 前提条件
确保已安装Hugo Extended版本：
```bash
# macOS
brew install hugo

# Windows
winget install Hugo.Hugo.Extended

# Linux
snap install hugo --channel=extended
```

### 开发模式
```bash
cd pieeg-hugo

# 启动开发服务器
hugo server --buildDrafts

# 或指定端口
hugo server --buildDrafts --port 1313
```
访问 http://localhost:1313

### 构建生产版本
```bash
# 构建静态网站到public目录
hugo

# 构建到指定目录
hugo --destination ../dist
```

## ✨ Hugo 版本的优势

### 🎯 内容管理
- **分离关注点**: 内容与表现分离
- **Markdown支持**: 使用Markdown编写内容
- **数据驱动**: 使用YAML数据文件管理结构化内容
- **多语言支持**: 内置国际化功能

### 🔧 开发体验
- **热重载**: 开发时自动刷新
- **模板继承**: 减少重复代码
- **部分模板**: 可重用的组件
- **快速构建**: 毫秒级构建速度

### 🌐 部署优势
- **纯静态**: 生成的是纯HTML/CSS/JS
- **SEO友好**: 预渲染的内容
- **CDN优化**: 可缓存的静态资源
- **安全性**: 无服务器端安全漏洞

## 📝 内容编辑

### 修改首页内容
编辑 `content/_index.md` 文件的 front matter：
```yaml
---
title: "页面标题"
description: "页面描述"
---
```

### 修改产品信息
编辑 `data/products.yaml`：
```yaml
- name: "产品名称"
  image: "images/product.png"
  description: "产品描述"
  features:
    - "特性1"
    - "特性2"
  link: "products/product-slug/"
```

### 修改应用场景
编辑 `data/applications.yaml`：
```yaml
- title: "应用标题"
  icon: "fas fa-icon"
  description: "应用描述"
```



## 🎨 样式定制

### CSS修改
编辑 `static/css/style.css` 文件：
- 使用CSS变量系统进行主题定制
- 修改颜色、字体、间距等

### 模板修改
- 基础模板: `layouts/_default/baseof.html`
- 首页模板: `layouts/index.html`


## 📊 数据可视化

图表功能通过以下文件提供：
- JavaScript: `static/js/charts.js`
- 数据: `static/data/sample_eeg_data.json`
- 依赖: Plotly.js (通过CDN加载)

## 🔧 配置选项

### 基本配置 (hugo.toml)
```toml
baseURL = 'https://pieeg.cn'
languageCode = 'zh-CN'
title = 'PIEEG - 低成本脑机接口设备'

[params]
  description = "网站描述"
  keywords = "关键词"
  author = "作者"
```

### 菜单配置
```toml
[menu]
  [[menu.main]]
    name = "菜单项"
    url = "/path/"
    weight = 10
```

## 🚀 部署选项

### 1. GitHub Pages + GitHub Actions
创建 `.github/workflows/hugo.yml`：
```yaml
name: Deploy Hugo to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          extended: true
      - name: Build
        run: hugo --minify
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

### 2. Netlify
1. 连接GitHub仓库
2. 构建命令: `hugo --minify`
3. 发布目录: `public`
4. 环境变量: `HUGO_VERSION` = `0.147.8`

### 3. Vercel
创建 `vercel.json`：
```json
{
  "build": {
    "env": {
      "HUGO_VERSION": "0.147.8"
    }
  },
  "functions": {
    "app/api/**/*.go": {
      "runtime": "vercel-go"
    }
  }
}
```

### 4. 传统服务器
```bash
# 构建
hugo --minify

# 上传public目录到服务器
rsync -avz public/ user@server:/var/www/html/
```

## 🛠️ 开发工具

### VS Code扩展推荐
- Hugo Language and Syntax Support
- Front Matter CMS
- YAML
- Markdown All in One

### 有用的Hugo命令
```bash
# 创建新内容
hugo new content posts/my-post.md

# 检查配置
hugo config

# 清理缓存
hugo --cleanDestinationDir

# 分析构建
hugo --templateMetrics
```

## 📈 性能优化

### 已实现优化
- 资源压缩和合并
- 图片优化
- CSS/JS最小化
- 语义化HTML

### 可选优化
```toml
# hugo.toml中添加
[minify]
  disableCSS = false
  disableHTML = false
  disableJS = false
  disableJSON = false
  disableSVG = false
  disableXML = false

[imaging]
  quality = 85
  resampleFilter = "lanczos"
```

## 🔄 与其他版本对比

| 特性 | 纯HTML版本 | Hugo版本 | Flask版本 |
|------|------------|----------|-----------|
| 部署复杂度 | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 内容管理 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 开发效率 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 可扩展性 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| SEO优化 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 📞 技术支持

遇到问题时：
1. 检查Hugo版本是否为Extended版
2. 验证配置文件语法
3. 查看终端错误信息
4. 检查模板语法

## 📚 学习资源

- [Hugo官方文档](https://gohugo.io/documentation/)
- [Hugo模板语法](https://gohugo.io/templates/)
- [Hugo主题开发](https://gohugo.io/themes/)

---

**Hugo版本的优势**: 更好的内容管理、模板复用、开发体验和SEO优化，适合需要频繁更新内容的网站。 