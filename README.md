# PIEEG 官方网站

基于 Hugo 静态网站生成器构建的 PIEEG 低成本脑机接口设备官方网站，提供产品展示、数据可视化和技术文档功能。

## 🏗️ 项目结构

```
pieeg/
├── hugo.toml               # Hugo主配置文件
├── content/                # 页面内容（Markdown）
│   ├── _index.md          # 首页内容
│   ├── disclaimer.md      # 免责声明
│   └── products/          # 产品页面
│       ├── _index.md      # 产品索引
│       ├── pieeg-8.md     # PiEEG-8产品页
│       ├── pieeg-16.md    # PiEEG-16产品页
│       ├── ardeeg.md      # ardEEG产品页
│       ├── jneeg.md       # JNEEG产品页
│       └── education-kit.md # 教育套件页
├── layouts/                # 模板文件
│   ├── _default/
│   │   ├── baseof.html    # 基础模板
│   │   └── single.html    # 单页模板
│   ├── index.html         # 首页模板
│   └── products/          # 产品页面模板
│       ├── list.html      # 产品列表模板
│       └── single.html    # 产品详情模板
├── static/                 # 静态资源
│   ├── css/
│   │   └── style.css      # 主要样式文件
│   ├── js/
│   │   └── charts.js      # 数据可视化脚本
│   ├── images/            # 产品图片和资源
│   └── data/
│       └── sample_eeg_data.json # 示例EEG数据
├── data/                   # 数据配置文件
│   ├── products.yaml      # 产品数据
│   └── applications.yaml  # 应用场景数据
├── public/                 # 构建输出目录（自动生成）
├── docs/                   # 项目文档
└── archetypes/             # 内容模板
    └── default.md
```

## 🚀 快速开始

### 环境要求

- **Hugo Extended** 版本 0.100.0 或更高
- **Git** 用于版本控制
- **现代浏览器** 用于预览和测试

### 安装 Hugo

```bash
# macOS
brew install hugo

# Windows (Chocolatey)
choco install hugo-extended

# Windows (Scoop)
scoop install hugo-extended

# Linux (Snap)
snap install hugo --channel=extended

# Linux (APT)
sudo apt install hugo

# 验证安装
hugo version
```

### 本地开发

```bash
# 克隆项目
git clone <repository-url>
cd pieeg

# 启动开发服务器
hugo server --buildDrafts --bind 0.0.0.0 --port 1313

# 或者使用构建脚本
./build.sh dev
```

访问 http://localhost:1313 查看网站

### 构建生产版本

```bash
# 构建静态网站
hugo --minify

# 或使用构建脚本
./build.sh prod

# 输出目录: public/
```

## ⚙️ 配置选项

### 主配置文件 (hugo.toml)

```toml
# 基本配置
baseURL = 'https://pieeg.cn'
languageCode = 'zh-CN'
title = 'PIEEG - 低成本脑机接口设备'
defaultContentLanguage = 'zh-cn'
hasCJKLanguage = true

# 构建配置
buildDrafts = false
buildFuture = false
buildExpired = false

# 输出配置
disableKinds = ['taxonomy', 'term']
enableEmoji = true
enableGitInfo = true
enableRobotsTXT = true

# 网站参数
[params]
  description = "PIEEG提供低成本脑机接口设备，包括EEG、EMG、ECG采集方案，支持教育和研究应用"
  keywords = "脑机接口,EEG,EMG,ECG,Arduino,开源硬件,神经科学,生物信号"
  author = "PIEEG Team"
  version = "2.0.0"
  
  # 社交媒体
  [params.social]
    github = "https://github.com/pieeg"
    email = "info@pieeg.cn"

# 菜单配置
[menu]
  [[menu.main]]
    name = "首页"
    url = "/"
    weight = 10
  [[menu.main]]
    name = "产品中心"
    url = "/products/"
    weight = 20
  [[menu.main]]
    name = "数据可视化"
    url = "/#visualization"
    weight = 30

# 标记配置
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
  [markup.highlight]
    style = 'github'
    lineNos = true

# 分析配置
[params.analytics]
  [params.analytics.baidu]
    enabled = true
    site_id = "your_baidu_site_id_here"
  [params.analytics.google]
    enabled = false
    tracking_id = ""

# 压缩配置
[minify]
  disableCSS = false
  disableHTML = false
  disableJS = false
  disableJSON = false
  disableSVG = false
  disableXML = false

# 图像处理配置
[imaging]
  quality = 85
  resampleFilter = "lanczos"
  [imaging.exif]
    includeFields = ""
    excludeFields = ".*"
    disableDate = false
    disableLatLong = true
```

### 产品数据配置 (data/products.yaml)

```yaml
- name: "PiEEG-8"
  subtitle: "8通道EEG采集板"
  image: "images/pieeg8/pieeg8-1.png"
  price: "¥899"
  description: "基于树莓派的8通道EEG信号采集板，适合教学和基础研究"
  features:
    - "8通道同步采集"
    - "24位ADC精度"
    - "250Hz采样率"
    - "树莓派兼容"
    - "Python SDK"
  specifications:
    - "输入阻抗: >100MΩ"
    - "CMRR: >110dB"
    - "噪声: <1μVrms"
    - "带宽: 0.1-100Hz"
  link: "products/pieeg-8/"
  order: 1

- name: "PiEEG-16"
  subtitle: "16通道EEG采集板"
  image: "images/pieeg16/pieeg16-1.png"
  price: "¥1599"
  description: "专业级16通道EEG信号采集系统，支持高精度脑电信号研究"
  features:
    - "16通道同步采集"
    - "24位ADC精度"
    - "500Hz采样率"
    - "低噪声设计"
    - "实时处理"
  specifications:
    - "输入阻抗: >100MΩ"
    - "CMRR: >120dB"
    - "噪声: <0.8μVrms"
    - "带宽: 0.1-200Hz"
  link: "products/pieeg-16/"
  order: 2
```

### 应用场景配置 (data/applications.yaml)

```yaml
- title: "脑机接口研究"
  icon: "fas fa-brain"
  description: "支持P300、SSVEP、运动想象等经典BCI范式研究，提供完整的信号处理工具链"

- title: "神经反馈训练"
  icon: "fas fa-wave-square"
  description: "实时脑电反馈系统，支持注意力训练、冥想状态监测等应用"

- title: "教育教学"
  icon: "fas fa-graduation-cap"
  description: "配套教学课程和实验指导，适用于生物医学工程、神经科学等专业教学"

- title: "睡眠监测"
  icon: "fas fa-bed"
  description: "长时间睡眠EEG监测，支持睡眠分期分析和睡眠质量评估"
```

## 📝 内容管理

### 修改首页内容

编辑 `content/_index.md`：

```yaml
---
title: "PIEEG - 低成本脑机接口设备"
description: "专业的脑机接口硬件解决方案"
draft: false
---

# 首页内容使用模板和数据文件动态生成
# 修改产品信息请编辑 data/products.yaml
# 修改应用场景请编辑 data/applications.yaml
```

### 添加新产品页面

```bash
# 创建新产品页面
hugo new content/products/new-product.md

# 编辑产品信息
```

产品页面示例：

```yaml
---
title: "新产品名称"
description: "产品描述"
image: "images/new-product.png"
price: "¥999"
features:
  - "特性1"
  - "特性2"
specifications:
  - "规格1"
  - "规格2"
draft: false
---

产品的详细描述内容...
```

## 🎨 样式定制

### 主样式文件 (static/css/style.css)

```css
/* CSS变量系统 */
:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --accent-color: #e74c3c;
  --background-color: #ffffff;
  --text-color: #2c3e50;
  --border-color: #ecf0f1;
  --header-height: 80px;
}

/* 自定义主题色 */
.theme-blue {
  --primary-color: #3498db;
  --secondary-color: #2980b9;
}

.theme-green {
  --primary-color: #27ae60;
  --secondary-color: #229954;
}
```

### 修改颜色主题

1. 编辑 `static/css/style.css` 中的 CSS 变量
2. 或在 `hugo.toml` 中添加自定义参数：

```toml
[params.theme]
  primary_color = "#3498db"
  secondary_color = "#2980b9"
  accent_color = "#e74c3c"
```

## 📊 数据可视化配置

### 图表配置 (static/js/charts.js)

```javascript
// 全局图表配置
const CHART_CONFIG = {
  displayModeBar: false,
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
};

// 默认布局配置
const DEFAULT_LAYOUT = {
  showlegend: false,
  margin: { l: 40, r: 40, t: 40, b: 40 },
  font: { family: 'Arial, sans-serif', size: 12 },
  plot_bgcolor: 'rgba(0,0,0,0)',
  paper_bgcolor: 'rgba(0,0,0,0)'
};
```

### EEG数据格式 (static/data/sample_eeg_data.json)

```json
{
  "eeg": {
    "channels": ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4"],
    "sampling_rate": 250,
    "data": [[...], [...], ...],
    "timestamps": [0, 0.004, 0.008, ...]
  },
  "emg": {
    "channels": ["EMG1", "EMG2"],
    "sampling_rate": 1000,
    "data": [[...], [...]],
    "timestamps": [0, 0.001, 0.002, ...]
  }
}
```

## 🚀 部署选项

### 1. GitHub Pages 自动部署

创建 `.github/workflows/hugo.yml`：

```yaml
name: Deploy Hugo to GitHub Pages

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive
          
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.147.8'
          extended: true
          
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v4
        
      - name: Build with Hugo
        env:
          HUGO_ENVIRONMENT: production
          HUGO_ENV: production
        run: |
          hugo \
            --minify \
            --baseURL "${{ steps.pages.outputs.base_url }}/"
            
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v3
```

### 2. Netlify 部署

1. **通过Git连接**：
   - 登录 Netlify
   - 选择 "New site from Git"
   - 连接 GitHub 仓库

2. **构建设置**：
   ```
   Build command: hugo --minify
   Publish directory: public
   Environment variables:
     HUGO_VERSION: 0.147.8
     HUGO_ENV: production
   ```

3. **自定义域名**（可选）：
   ```
   Domain management → Add custom domain
   ```

### 3. Vercel 部署

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

### 4. 云服务器部署

#### 4.1 服务器环境准备

```bash
# 安装 Hugo
wget https://github.com/gohugoio/hugo/releases/download/v0.147.8/hugo_extended_0.147.8_Linux-64bit.tar.gz
tar -xzf hugo_extended_0.147.8_Linux-64bit.tar.gz
sudo mv hugo /usr/local/bin/

# 安装 Nginx
sudo apt update
sudo apt install nginx

# 配置防火墙
sudo ufw allow 'Nginx Full'
```

#### 4.2 自动部署脚本

创建 `deploy.sh`：

```bash
#!/bin/bash

# 部署脚本
SITE_DIR="/var/www/pieeg"
BACKUP_DIR="/var/backups/pieeg"
LOG_FILE="/var/log/pieeg-deploy.log"

echo "$(date): Starting deployment" >> $LOG_FILE

# 备份当前版本
if [ -d "$SITE_DIR" ]; then
    sudo cp -r $SITE_DIR $BACKUP_DIR/$(date +%Y%m%d-%H%M%S)
fi

# 构建网站
hugo --minify --destination $SITE_DIR

# 设置权限
sudo chown -R www-data:www-data $SITE_DIR
sudo chmod -R 755 $SITE_DIR

# 重启 Nginx
sudo systemctl reload nginx

echo "$(date): Deployment completed" >> $LOG_FILE
```

#### 4.3 Nginx 配置

创建 `/etc/nginx/sites-available/pieeg`：

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name pieeg.cn www.pieeg.cn;

    root /var/www/pieeg;
    index index.html;

    # 启用压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 主要位置块
    location / {
        try_files $uri $uri/ =404;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/pieeg /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🛠️ 开发工具和命令

### 常用 Hugo 命令

```bash
# 开发服务器
hugo server --buildDrafts --bind 0.0.0.0 --port 1313

# 构建网站
hugo --minify

# 检查配置
hugo config

# 清理缓存和构建目录
hugo --cleanDestinationDir

# 分析模板性能
hugo --templateMetrics

# 创建新内容
hugo new content/posts/my-post.md

# 列出所有内容
hugo list all

# 检查链接
hugo --printPathWarnings
```

### 推荐的 VS Code 扩展

```json
{
  "recommendations": [
    "budparr.language-hugo-vscode",
    "eliostruyf.vscode-front-matter",
    "redhat.vscode-yaml",
    "yzhang.markdown-all-in-one",
    "ms-vscode.vscode-json"
  ]
}
```

### 开发工作流

```bash
# 1. 创建新分支
git checkout -b feature/new-feature

# 2. 启动开发服务器
hugo server --buildDrafts

# 3. 进行开发和测试

# 4. 构建并测试
hugo --minify

# 5. 提交更改
git add .
git commit -m "Add new feature"

# 6. 推送和创建PR
git push origin feature/new-feature
```

## 📈 性能优化

### 已实现的优化

- **资源压缩**：HTML、CSS、JS 自动压缩
- **图片优化**：WebP 格式支持，懒加载
- **缓存策略**：静态资源长期缓存
- **CDN 加速**：Plotly.js 通过 CDN 加载
- **语义化 HTML**：更好的 SEO 和可访问性

### 高级优化配置

```toml
# hugo.toml 中添加
[caches]
  [caches.getjson]
    dir = ":cacheDir/:project"
    maxAge = "1h"
  [caches.getcsv]
    dir = ":cacheDir/:project"
    maxAge = "1h"
  [caches.images]
    dir = ":cacheDir/:project"
    maxAge = "24h"

[outputs]
  home = ["HTML", "RSS", "JSON"]
  page = ["HTML"]
  section = ["HTML", "RSS"]

[mediaTypes]
  [mediaTypes."application/manifest+json"]
    suffixes = ["webmanifest"]
  [mediaTypes."text/netlify"]
    delimiter = ""
    suffixes = [""]

[outputFormats]
  [outputFormats.WebAppManifest]
    mediaType = "application/manifest+json"
    rel = "manifest"
```

## 🔧 故障排除

### 常见问题和解决方案

#### 1. Hugo 服务器启动失败

```bash
# 检查端口占用
lsof -i :1313

# 使用不同端口
hugo server --port 1314

# 检查配置文件语法
hugo config
```

#### 2. 构建错误

```bash
# 启用详细错误信息
hugo --verbose --debug

# 检查模板语法
hugo server --templateMetrics
```

#### 3. 图片不显示

```bash
# 检查图片路径
ls static/images/

# 重新构建
hugo --cleanDestinationDir
```

#### 4. CSS/JS 更改不生效

```bash
# 清理浏览器缓存
# 或强制刷新 Ctrl+F5

# 清理 Hugo 缓存
hugo --cleanDestinationDir
```

### 调试技巧

```bash
# 查看站点变量
{{ printf "%#v" .Site }}

# 查看页面变量
{{ printf "%#v" .Page }}

# 调试数据文件
{{ printf "%#v" .Site.Data }}
```

## 📚 文档和资源

### 官方文档

- [Hugo 官方文档](https://gohugo.io/documentation/)
- [Hugo 模板语法](https://gohugo.io/templates/)
- [Hugo 主题开发](https://gohugo.io/themes/)

### 相关资源

- [Plotly.js 文档](https://plotly.com/javascript/)
- [YAML 语法参考](https://yaml.org/spec/）
- [Markdown 语法指南](https://www.markdownguide.org/)

### 项目文档

项目相关的历史文档和开发记录保存在 `docs/` 目录：

- `PYTHON_PROJECT_HISTORY.md` - Python 项目历史
- `DEPLOYMENT_SUMMARY.md` - 部署总结
- `PROJECT_CLEANUP_SUMMARY.md` - 项目整理记录
- `ANALYTICS_SETUP.md` - 分析工具配置

## 🤝 贡献指南

### 开发规范

1. **分支命名**：`feature/功能名` 或 `fix/问题描述`
2. **提交信息**：使用清晰的中文描述
3. **代码风格**：遵循项目既有风格
4. **测试要求**：确保构建成功和功能正常

### 提交流程

```bash
# 1. Fork 项目
# 2. 创建功能分支
git checkout -b feature/new-feature

# 3. 进行开发
# 4. 测试功能
hugo server

# 5. 提交更改
git add .
git commit -m "添加新功能：描述"

# 6. 推送到 Fork
git push origin feature/new-feature

# 7. 创建 Pull Request
```

## 📄 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 📞 技术支持

如有问题或建议，请通过以下方式联系：

- 📧 邮箱：info@pieeg.cn
- 🐛 问题反馈：GitHub Issues
- 💬 技术讨论：GitHub Discussions

---

**最后更新**：2024年6月22日  
**Hugo 版本**：0.147.8  
**项目版本**：2.0.0 