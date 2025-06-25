# Hugo + Nginx 部署指南

本指南将详细说明如何使用 Hugo 生成静态文件并通过 Nginx 提供服务。

## 🚀 快速部署（推荐）

使用我们提供的自动化脚本：

```bash
# 1. 构建 Hugo 静态文件
hugo --minify --cleanDestinationDir

# 2. 运行自动部署脚本
./deploy-nginx.sh

# 或使用自定义域名
./deploy-nginx.sh -d yourdomain.com
```

## 📋 手动部署步骤

### 第1步：生成静态文件

```bash
# 切换到项目目录
cd /path/to/your/hugo/project

# 清理并构建优化的静态文件
hugo --cleanDestinationDir --minify

# 验证生成的文件
ls -la public/
```

**构建选项说明：**
- `--minify`: 压缩 HTML、CSS、JS 文件
- `--cleanDestinationDir`: 清理目标目录
- `--environment production`: 设置生产环境
- `--baseURL https://yourdomain.com`: 设置基础URL

### 第2步：安装 Nginx

#### Ubuntu/Debian
```bash
# 更新包列表
sudo apt update

# 安装 Nginx
sudo apt install nginx

# 启动并启用 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 检查状态
sudo systemctl status nginx
```

#### CentOS/RHEL
```bash
# 安装 Nginx
sudo yum install nginx
# 或使用 dnf (较新版本)
sudo dnf install nginx

# 启动并启用 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 防火墙配置
```bash
# Ubuntu/Debian
sudo ufw allow 'Nginx Full'

# CentOS/RHEL
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 第3步：创建站点目录

```bash
# 创建网站根目录
sudo mkdir -p /var/www/pieeg

# 创建备份目录
sudo mkdir -p /var/backups/pieeg

# 复制 Hugo 生成的文件
sudo cp -r public/* /var/www/pieeg/

# 设置正确的权限
sudo chown -R www-data:www-data /var/www/pieeg
sudo chmod -R 755 /var/www/pieeg
```

### 第4步：创建 Nginx 配置

创建站点配置文件：

```bash
sudo nano /etc/nginx/sites-available/pieeg
```

添加以下配置内容：

```nginx
# PIEEG Hugo 站点配置
server {
    listen 80;
    listen [::]:80;
    server_name pieeg.cn www.pieeg.cn;
    
    root /var/www/pieeg;
    index index.html index.htm;
    
    # 访问和错误日志
    access_log /var/log/nginx/pieeg.access.log;
    error_log /var/log/nginx/pieeg.error.log;
    
    # 启用 Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/xml
        application/xml+rss
        application/json
        image/svg+xml;
    
    # 安全头部
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline' 'unsafe-eval'" always;
    
    # 静态资源缓存 (1年)
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|otf)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary "Accept-Encoding";
        try_files $uri =404;
    }
    
    # HTML 文件缓存 (1小时)
    location ~* \.(html|htm)$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
        try_files $uri $uri/ =404;
    }
    
    # JSON 和 XML 文件处理
    location ~* \.(json|xml)$ {
        expires 1h;
        add_header Content-Type "application/json; charset=utf-8";
        try_files $uri =404;
    }
    
    # 主要位置配置
    location / {
        try_files $uri $uri/ =404;
        
        # 处理尾部斜杠
        if ($request_uri ~ ^/(.*)/$ ) {
            return 301 /$1;
        }
    }
    
    # 特殊文件处理
    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }
    
    location = /favicon.ico {
        log_not_found off;
        access_log off;
        expires 1y;
    }
    
    # 拒绝访问隐藏文件
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # 拒绝访问备份文件
    location ~ ~$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}

# 重定向 www 到非 www（可选）
server {
    listen 80;
    listen [::]:80;
    server_name www.pieeg.cn;
    return 301 http://pieeg.cn$request_uri;
}
```

### 第5步：启用站点

```bash
# 创建符号链接启用站点
sudo ln -s /etc/nginx/sites-available/pieeg /etc/nginx/sites-enabled/

# 测试 Nginx 配置
sudo nginx -t

# 重新加载 Nginx
sudo systemctl reload nginx
```

### 第6步：设置 SSL（可选但推荐）

#### 使用 Let's Encrypt 免费 SSL

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取 SSL 证书
sudo certbot --nginx -d pieeg.cn -d www.pieeg.cn

# 设置自动续期
sudo crontab -e
# 添加以下行：
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔄 更新部署流程

创建更新脚本：

```bash
#!/bin/bash
# update-site.sh

set -e

SITE_ROOT="/var/www/pieeg"
BACKUP_DIR="/var/backups/pieeg"
PROJECT_DIR="/path/to/your/hugo/project"

echo "Starting site update..."

# 进入项目目录
cd "$PROJECT_DIR"

# 拉取最新代码
git pull origin main

# 构建新版本
hugo --cleanDestinationDir --minify

# 备份当前版本
BACKUP_NAME="$(date +%Y%m%d-%H%M%S)"
sudo cp -r "$SITE_ROOT" "$BACKUP_DIR/$BACKUP_NAME"

# 部署新版本
sudo rm -rf "$SITE_ROOT"/*
sudo cp -r public/* "$SITE_ROOT/"

# 设置权限
sudo chown -R www-data:www-data "$SITE_ROOT"
sudo chmod -R 755 "$SITE_ROOT"

# 重新加载 Nginx
sudo systemctl reload nginx

echo "Site updated successfully!"
echo "Backup saved to: $BACKUP_DIR/$BACKUP_NAME"
```

使脚本可执行：

```bash
chmod +x update-site.sh
```

## 📊 性能优化

### Nginx 全局优化

编辑 `/etc/nginx/nginx.conf`：

```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # 基本设置
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;
    
    # MIME 类型
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;
    
    # 包含站点配置
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 缓存优化

添加更详细的缓存规则：

```nginx
# 图片和字体 - 长期缓存
location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary "Accept-Encoding";
}

# 字体文件
location ~* \.(woff|woff2|ttf|eot|otf)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Access-Control-Allow-Origin "*";
}

# CSS 和 JavaScript
location ~* \.(css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    add_header Vary "Accept-Encoding";
}

# HTML 文件 - 短期缓存
location ~* \.(html|htm)$ {
    expires 1h;
    add_header Cache-Control "public, must-revalidate";
}
```

## 🔍 监控和日志

### 日志分析

```bash
# 查看访问日志
sudo tail -f /var/log/nginx/pieeg.access.log

# 查看错误日志
sudo tail -f /var/log/nginx/pieeg.error.log

# 分析最常访问的页面
sudo awk '{print $7}' /var/log/nginx/pieeg.access.log | sort | uniq -c | sort -rn | head -10

# 分析访问者IP
sudo awk '{print $1}' /var/log/nginx/pieeg.access.log | sort | uniq -c | sort -rn | head -10
```

### 性能监控

```bash
# 检查 Nginx 状态
sudo systemctl status nginx

# 检查 Nginx 配置
sudo nginx -t

# 重新加载配置
sudo systemctl reload nginx

# 查看 Nginx 进程
ps aux | grep nginx
```

## 🛠️ 故障排除

### 常见问题

#### 1. 403 Forbidden 错误
```bash
# 检查文件权限
ls -la /var/www/pieeg/

# 修复权限
sudo chown -R www-data:www-data /var/www/pieeg/
sudo chmod -R 755 /var/www/pieeg/
```

#### 2. 504 Gateway Timeout
```bash
# 检查 Nginx 配置
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/error.log
```

#### 3. CSS/JS 文件不加载
```bash
# 检查 MIME 类型
sudo nginx -T | grep mime

# 检查文件路径
ls -la /var/www/pieeg/css/
ls -la /var/www/pieeg/js/
```

### 配置测试

```bash
# 测试 Nginx 配置语法
sudo nginx -t

# 重新加载配置
sudo systemctl reload nginx

# 测试网站响应
curl -I http://yourdomain.com

# 测试 Gzip 压缩
curl -H "Accept-Encoding: gzip" -I http://yourdomain.com
```

## 📋 维护检查清单

### 每日检查
- [ ] 检查网站是否正常访问
- [ ] 查看错误日志是否有异常
- [ ] 检查磁盘空间使用情况

### 每周检查  
- [ ] 分析访问日志
- [ ] 检查 SSL 证书状态
- [ ] 更新系统包

### 每月检查
- [ ] 备份网站文件和配置
- [ ] 检查 Nginx 和系统更新
- [ ] 优化日志文件大小

## 🎯 最佳实践

1. **定期备份**：自动备份网站文件和 Nginx 配置
2. **监控设置**：使用工具如 Nagios、Zabbix 监控网站状态
3. **安全更新**：定期更新 Nginx 和系统安全补丁
4. **性能测试**：使用 GTmetrix、PageSpeed Insights 测试网站性能
5. **日志轮转**：配置 logrotate 管理日志文件大小

---

**提示**：如果遇到问题，请先检查 Nginx 错误日志 `/var/log/nginx/error.log`，这里通常包含解决问题的关键信息。 