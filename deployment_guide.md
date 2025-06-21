# PIEEG 官网容器化部署指南

## 概述

本指南详细介绍了如何使用Docker容器化技术部署PIEEG官网。支持开发环境和生产环境的一键部署，包含完整的服务栈：Web应用、数据库、缓存、反向代理。

## 系统要求

### 硬件要求
- **CPU**: 2核心或以上
- **内存**: 4GB RAM 或以上  
- **存储**: 20GB 可用空间
- **网络**: 稳定的互联网连接

### 软件要求
- **操作系统**: Linux (推荐Ubuntu 20.04+)、macOS 或 Windows 10+
- **Docker**: 20.0+ 
- **Docker Compose**: 2.0+
- **Git**: 用于代码管理

## 快速部署

### 1. 准备工作

#### 安装Docker（Ubuntu/Debian）
```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 将当前用户添加到docker组
sudo usermod -aG docker $USER

# 重新登录或执行以下命令使组变更生效
newgrp docker
```

#### 安装Docker Compose
```bash
# 下载Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 设置执行权限
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker-compose --version
```

### 2. 获取项目代码

```bash
# 克隆项目（替换为实际的仓库地址）
git clone https://github.com/your-org/pieeg-website.git
cd pieeg-website

# 或者如果你已经有代码包
tar -xzf pieeg-website.tar.gz
cd pieeg-website
```

### 3. 一键部署

#### 生产环境部署
```bash
# 设置脚本执行权限
chmod +x deploy.sh

# 启动生产环境
./deploy.sh prod
```

#### 开发环境部署
```bash
# 启动开发环境
./deploy.sh dev
```

部署脚本会自动：
- 检查系统依赖
- 创建必要目录
- 生成配置文件
- 启动服务容器
- 初始化数据库
- 创建默认管理员账户

## 详细部署步骤

### 1. 环境配置

#### 创建环境配置文件
```bash
# 复制环境配置模板
cp .env.example .env

# 编辑配置文件
nano .env
```

#### 关键配置项说明
```bash
# Flask应用配置
FLASK_APP=src.main                    # 应用入口
FLASK_ENV=production                  # 运行环境: development/production
SECRET_KEY=your-secret-key-here       # 密钥（生产环境必须更改）

# 数据库配置
DB_USERNAME=pieeg_user                # 数据库用户名
DB_PASSWORD=secure-password-here      # 数据库密码（生产环境必须更改）
DB_HOST=db                           # 数据库主机（容器名）
DB_PORT=3306                         # 数据库端口
DB_NAME=pieeg_db                     # 数据库名称

# 文件上传配置
UPLOAD_FOLDER=src/static/uploads      # 上传文件目录
```

### 2. 生产环境部署

#### 配置生产环境变量
```bash
# 生成安全的密钥
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 更新.env文件中的生产环境配置
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key
DB_PASSWORD=your-secure-database-password
```

#### 启动生产服务
```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

#### 验证部署
```bash
# 检查Web服务
curl -I http://localhost

# 检查健康状态
curl http://localhost/health

# 检查数据库连接
docker-compose exec web python -c "
from src.main import create_app
app = create_app()
with app.app_context():
    from src.models.admin import db
    print('Database connection successful')
"
```

### 3. 域名和SSL配置

#### 域名解析设置
```bash
# 在域名注册商处添加DNS记录
# A记录: pieeg.cn -> 你的服务器IP
# A记录: www.pieeg.cn -> 你的服务器IP
```

#### SSL证书申请（Let's Encrypt）
```bash
# 安装certbot
sudo apt install certbot

# 临时停止nginx容器
docker-compose stop nginx

# 申请SSL证书
sudo certbot certonly --standalone -d pieeg.cn -d www.pieeg.cn

# 复制证书到项目目录
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/pieeg.cn/fullchain.pem ssl/pieeg.cn.pem
sudo cp /etc/letsencrypt/live/pieeg.cn/privkey.pem ssl/pieeg.cn.key
sudo chown -R $USER:$USER ssl/
```

#### 启用HTTPS
```bash
# 编辑nginx.conf，取消HTTPS配置的注释
nano nginx.conf

# 重启nginx服务
docker-compose restart nginx
```

## 服务管理

### 常用命令

```bash
# 查看所有服务状态
docker-compose ps

# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f [service_name]

# 进入容器
docker-compose exec web bash
docker-compose exec db mysql -u root -p

# 更新服务
docker-compose pull
docker-compose up -d --build
```

### 使用部署脚本

```bash
# 查看帮助
./deploy.sh help

# 启动生产环境
./deploy.sh prod

# 启动开发环境
./deploy.sh dev

# 停止所有服务
./deploy.sh stop

# 重启服务
./deploy.sh restart

# 查看实时日志
./deploy.sh logs

# 查看特定服务日志
./deploy.sh logs web
./deploy.sh logs db

# 备份数据库
./deploy.sh backup

# 恢复数据库
./deploy.sh restore backup_20240101_120000.sql

# 清理Docker资源
./deploy.sh clean

# 更新应用
./deploy.sh update
```

## 数据库管理

### 数据库备份

#### 自动备份
```bash
# 使用部署脚本备份
./deploy.sh backup

# 手动备份
docker-compose exec db mysqldump -u root -proot_password_2024 pieeg_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### 定时备份（可选）
```bash
# 添加cron任务
crontab -e

# 每天凌晨2点自动备份
0 2 * * * cd /path/to/pieeg && ./deploy.sh backup
```

### 数据库恢复

```bash
# 使用部署脚本恢复
./deploy.sh restore backup_20240101_120000.sql

# 手动恢复
docker-compose exec -T db mysql -u root -proot_password_2024 pieeg_db < backup_20240101_120000.sql
```

### 数据库维护

```bash
# 连接数据库
docker-compose exec db mysql -u root -p

# 查看数据库状态
docker-compose exec db mysql -u root -p -e "SHOW DATABASES; SHOW TABLES FROM pieeg_db;"

# 优化数据库
docker-compose exec db mysql -u root -p -e "OPTIMIZE TABLE pieeg_db.*;"
```

## 监控和维护

### 日志管理

#### 查看应用日志
```bash
# 实时查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# 查看最近的日志
docker-compose logs --tail=100 web
```

#### 日志轮转
```bash
# 创建logrotate配置
sudo nano /etc/logrotate.d/pieeg

# 添加以下内容
/path/to/pieeg/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
}
```

### 性能监控

#### 系统资源监控
```bash
# 查看容器资源使用情况
docker stats

# 查看磁盘使用情况
df -h

# 查看内存使用情况
free -h

# 查看CPU使用情况
top
```

#### 应用性能监控
```bash
# 查看应用响应时间
curl -w "@curl-format.txt" -o /dev/null -s http://localhost/

# 创建curl格式文件
cat > curl-format.txt << 'EOF'
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
EOF
```

### 故障排除

#### 常见问题及解决方案

**1. 容器启动失败**
```bash
# 查看详细错误日志
docker-compose logs [service_name]

# 检查配置文件语法
docker-compose config

# 重新构建镜像
docker-compose build --no-cache
```

**2. 数据库连接失败**
```bash
# 检查数据库容器状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 测试数据库连接
docker-compose exec db mysql -u pieeg_user -p
```

**3. 静态文件无法访问**
```bash
# 检查Nginx配置
docker-compose exec nginx nginx -t

# 查看静态文件权限
ls -la src/static/

# 重启Nginx
docker-compose restart nginx
```

**4. 端口冲突**
```bash
# 查看端口占用
netstat -tulpn | grep :80
netstat -tulpn | grep :3306

# 修改docker-compose.yml中的端口映射
# 然后重启服务
docker-compose down
docker-compose up -d
```

## 安全加固

### 基本安全措施

1. **更改默认密码**
```bash
# 更改数据库root密码
docker-compose exec db mysql -u root -p -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_strong_password';"

# 更改应用管理员密码
# 登录管理后台: http://your-domain/admin
# 使用默认账户: admin / admin123
# 立即更改密码
```

2. **限制网络访问**
```bash
# 配置防火墙（Ubuntu）
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

3. **定期更新**
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 更新Docker镜像
docker-compose pull
docker-compose up -d --build
```

### SSL/TLS配置

1. **强化SSL配置**
编辑nginx.conf文件：
```nginx
# 添加安全头
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
add_header X-XSS-Protection "1; mode=block" always;

# 配置SSL协议和加密套件
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
```

2. **自动续期SSL证书**
```bash
# 创建续期脚本
sudo nano /etc/cron.monthly/renew-ssl

# 添加以下内容
#!/bin/bash
certbot renew --quiet
cd /path/to/pieeg
sudo cp /etc/letsencrypt/live/pieeg.cn/fullchain.pem ssl/pieeg.cn.pem
sudo cp /etc/letsencrypt/live/pieeg.cn/privkey.pem ssl/pieeg.cn.key
docker-compose restart nginx

# 设置执行权限
sudo chmod +x /etc/cron.monthly/renew-ssl
```

## 扩展和优化

### 性能优化

1. **启用Redis缓存**
```bash
# Redis服务已在docker-compose.yml中配置
# 修改应用代码以使用Redis缓存
```

2. **配置CDN**
```bash
# 将静态文件上传到CDN
# 修改模板中的静态文件URL
```

3. **数据库优化**
```sql
-- 连接到数据库
-- 添加索引
CREATE INDEX idx_products_slug ON products(slug);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_topics_category ON topics(category_id);
```

### 集群部署

对于高可用性部署，可以考虑：

1. **多节点部署**
2. **负载均衡**
3. **数据库主从复制**
4. **容器编排（Kubernetes）**

## 迁移指南

### 从传统部署迁移到容器化

1. **数据备份**
```bash
# 备份现有数据库
mysqldump -u root -p pieeg_db > migration_backup.sql

# 备份上传文件
tar -czf uploads_backup.tar.gz /path/to/uploads/
```

2. **导入数据**
```bash
# 启动新的容器化环境
./deploy.sh prod

# 导入数据库
./deploy.sh restore migration_backup.sql

# 恢复上传文件
tar -xzf uploads_backup.tar.gz -C src/static/uploads/
```

### 环境迁移

1. **配置导出**
```bash
# 导出环境配置
cp .env production.env

# 导出数据库
./deploy.sh backup
```

2. **新环境导入**
```bash
# 复制配置
cp production.env .env

# 导入数据
./deploy.sh restore backup_file.sql
```

## 支持与维护

### 技术支持

- **文档**: 查看项目README.md
- **问题反馈**: 创建GitHub Issue
- **社区讨论**: 参与论坛讨论

### 维护计划

建议定期进行以下维护：

1. **每日检查**
   - 服务状态检查
   - 日志审查
   - 性能监控

2. **每周维护**
   - 数据库备份验证
   - 系统更新检查
   - 安全扫描

3. **每月维护**
   - SSL证书检查
   - 性能优化
   - 容量规划

---

## 附录

### 常用端口列表

| 服务 | 端口 | 说明 |
|------|------|------|
| Nginx | 80 | HTTP |
| Nginx | 443 | HTTPS |
| Flask | 5000 | Web应用 |
| MySQL | 3306 | 数据库 |
| Redis | 6379 | 缓存 |

### 目录结构说明

```
pieeg/
├── src/                        # 应用源码
│   ├── models/                # 数据模型
│   ├── routes/                # 路由控制器
│   ├── templates/             # 模板文件
│   ├── static/                # 静态资源
│   └── main.py               # 应用入口
├── migrations/                # 数据库迁移
├── logs/                     # 应用日志
├── ssl/                      # SSL证书
├── mysql-init/               # MySQL初始化脚本
├── docker-compose.yml        # Docker编排文件
├── Dockerfile               # Docker构建文件
├── nginx.conf               # Nginx配置
├── deploy.sh               # 部署脚本
├── init_db.py             # 数据库初始化
├── .env                   # 环境配置
├── .env.example          # 环境配置模板
└── requirements.txt      # Python依赖
```

### 环境变量完整列表

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| FLASK_APP | src.main | Flask应用入口 |
| FLASK_ENV | development | 运行环境 |
| SECRET_KEY | pieeg-dev-key | 应用密钥 |
| DB_USERNAME | root | 数据库用户名 |
| DB_PASSWORD | password | 数据库密码 |
| DB_HOST | localhost | 数据库主机 |
| DB_PORT | 3306 | 数据库端口 |
| DB_NAME | pieeg_db | 数据库名称 |
| UPLOAD_FOLDER | src/static/uploads | 上传目录 |

---

本指南提供了PIEEG官网容器化部署的完整流程。如有疑问，请查看项目文档或联系技术支持。
