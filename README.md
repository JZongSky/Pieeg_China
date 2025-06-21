# PIEEG 官网项目

## 项目概述

PIEEG官网是一个展示低成本脑机接口设备的现代化网站，包含产品展示、交互式数据可视化、社区论坛和管理系统。网站采用Flask框架开发，具有响应式设计，支持容器化部署。

## 主要功能

### 前台功能
- **首页展示**：品牌介绍、产品概览、数据可视化
- **产品中心**：详细的产品信息、规格参数、购买链接
- **数据可视化**：交互式图表展示EEG、EMG、ECG数据
- **社区论坛**：用户交流、技术讨论、项目分享
- **关于我们**：公司介绍、联系方式

### 后台管理
- **用户管理**：用户账户、权限管理
- **产品管理**：产品信息、分类、图片管理
- **内容管理**：新闻、页面内容管理
- **论坛管理**：话题、回复、分类管理
- **系统设置**：网站配置、参数设置

## 技术栈

### 后端
- **框架**：Flask 3.0.3
- **数据库**：MySQL 8.0
- **ORM**：SQLAlchemy
- **缓存**：Redis（可选）
- **服务器**：Gunicorn + Nginx

### 前端
- **模板引擎**：Jinja2
- **样式**：CSS3 + 响应式设计
- **交互**：JavaScript + Plotly.js
- **图标**：Font Awesome

### 部署
- **容器化**：Docker + Docker Compose
- **反向代理**：Nginx
- **进程管理**：Gunicorn
- **数据持久化**：Docker Volumes

## 快速开始

### 环境要求

- Docker 20.0+
- Docker Compose 2.0+
- Python 3.12+（开发环境）
- MySQL 8.0+（开发环境）

### 一键部署

#### 1. 克隆项目
```bash
git clone <repository-url>
cd pieeg
```

#### 2. 生产环境部署
```bash
# 设置执行权限
chmod +x deploy.sh

# 启动生产环境
./deploy.sh prod
```

#### 3. 开发环境启动
```bash
# 启动开发环境
./deploy.sh dev
```

### 部署脚本说明

部署脚本 `deploy.sh` 提供了完整的部署和管理功能：

```bash
# 查看帮助
./deploy.sh help

# 启动生产环境
./deploy.sh prod

# 启动开发环境  
./deploy.sh dev

# 停止服务
./deploy.sh stop

# 重启服务
./deploy.sh restart

# 查看日志
./deploy.sh logs
./deploy.sh logs web  # 查看特定服务日志

# 备份数据库
./deploy.sh backup

# 恢复数据库
./deploy.sh restore backup_20240101_120000.sql

# 更新应用
./deploy.sh update

# 清理Docker资源
./deploy.sh clean
```

## 手动部署

### 1. 环境配置

复制环境配置文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，修改相应配置：
```bash
# Flask配置
FLASK_APP=src.main
FLASK_ENV=production
SECRET_KEY=your-production-secret-key

# 数据库配置
DB_USERNAME=pieeg_user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pieeg_db
```

### 2. Docker部署

#### 构建和启动服务
```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 初始化数据库
```bash
# 进入Web容器
docker-compose exec web bash

# 运行初始化脚本
python init_db.py
```

### 3. 传统部署

#### 安装依赖
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

#### 配置数据库
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE pieeg_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pieeg_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON pieeg_db.* TO 'pieeg_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 初始化应用
```bash
# 初始化数据库
python init_db.py

# 启动应用
gunicorn --bind 0.0.0.0:5000 --workers 4 src.main:app
```

## 开发指南

### 目录结构
```
pieeg/
├── src/                    # 源代码目录
│   ├── models/            # 数据模型
│   ├── routes/            # 路由处理
│   ├── templates/         # 模板文件
│   ├── static/            # 静态资源
│   └── main.py           # 应用入口
├── migrations/            # 数据库迁移
├── logs/                 # 日志文件
├── ssl/                  # SSL证书
├── docker-compose.yml    # Docker编排
├── Dockerfile           # Docker构建
├── nginx.conf           # Nginx配置
├── deploy.sh            # 部署脚本
├── init_db.py          # 数据库初始化
└── requirements.txt    # Python依赖
```

### 开发环境搭建

1. **克隆项目**
```bash
git clone <repository-url>
cd pieeg
```

2. **创建虚拟环境**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，设置开发环境配置
```

5. **启动数据库**
```bash
# 使用Docker启动MySQL
docker run -d --name pieeg_mysql \
  -e MYSQL_DATABASE=pieeg_db \
  -e MYSQL_USER=pieeg_user \
  -e MYSQL_PASSWORD=pieeg_password \
  -e MYSQL_ROOT_PASSWORD=root_password \
  -p 3306:3306 mysql:8.0
```

6. **初始化数据库**
```bash
python init_db.py
```

7. **启动应用**
```bash
export FLASK_APP=src.main
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### 数据库管理

#### 创建迁移
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### 数据库操作
```bash
# 备份数据库
mysqldump -u root -p pieeg_db > backup.sql

# 恢复数据库
mysql -u root -p pieeg_db < backup.sql
```

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FLASK_APP` | Flask应用模块 | `src.main` |
| `FLASK_ENV` | 运行环境 | `development` |
| `SECRET_KEY` | 密钥 | `pieeg-dev-key` |
| `DB_USERNAME` | 数据库用户名 | `root` |
| `DB_PASSWORD` | 数据库密码 | `password` |
| `DB_HOST` | 数据库主机 | `localhost` |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_NAME` | 数据库名称 | `pieeg_db` |

### 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Web应用 | 5000 | Flask应用端口 |
| Nginx | 80/443 | HTTP/HTTPS端口 |
| MySQL | 3306 | 数据库端口 |
| Redis | 6379 | 缓存端口 |

## 部署到生产环境

### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 域名和SSL配置

#### 域名解析
```bash
# 添加A记录指向服务器IP
pieeg.cn        A    your.server.ip
www.pieeg.cn    A    your.server.ip
```

#### SSL证书（Let's Encrypt）
```bash
# 安装certbot
sudo apt install certbot

# 申请证书
sudo certbot certonly --standalone -d pieeg.cn -d www.pieeg.cn

# 复制证书到项目目录
sudo cp /etc/letsencrypt/live/pieeg.cn/fullchain.pem ssl/pieeg.cn.pem
sudo cp /etc/letsencrypt/live/pieeg.cn/privkey.pem ssl/pieeg.cn.key
```

#### 启用HTTPS
编辑 `nginx.conf`，取消HTTPS配置注释，然后重启服务：
```bash
docker-compose restart nginx
```

### 3. 生产环境优化

#### 性能优化
- 启用Nginx gzip压缩
- 配置静态文件缓存
- 使用CDN加速静态资源
- 优化数据库查询

#### 安全加固
- 更改默认密码
- 限制管理员IP访问
- 启用防火墙
- 定期备份数据

#### 监控和日志
```bash
# 查看服务状态
docker-compose ps

# 实时日志
docker-compose logs -f

# 系统资源监控
docker stats

# 磁盘使用情况
df -h
```

## 故障排除

### 常见问题

#### 1. 数据库连接失败
```bash
# 检查数据库服务
docker-compose ps db

# 查看数据库日志
docker-compose logs db

# 测试数据库连接
docker-compose exec web python -c "
from src.main import create_app
app = create_app()
with app.app_context():
    from src.models.admin import db
    print('Database connection:', db.engine.execute('SELECT 1').scalar())
"
```

#### 2. 静态文件404
```bash
# 检查静态文件目录权限
ls -la src/static/

# 重启Nginx
docker-compose restart nginx

# 检查Nginx配置
docker-compose exec nginx nginx -t
```

#### 3. 应用启动失败
```bash
# 查看应用日志
docker-compose logs web

# 进入容器调试
docker-compose exec web bash

# 检查Python环境
docker-compose exec web python --version
docker-compose exec web pip list
```

### 日志位置

- **应用日志**: `logs/` 目录
- **Nginx日志**: 容器内 `/var/log/nginx/`
- **MySQL日志**: 容器内 `/var/log/mysql/`
- **Docker日志**: `docker-compose logs`

## API文档

### 论坛API

#### 获取分类列表
```
GET /api/categories
```

#### 获取分类话题
```
GET /api/category/<category_id>/topics
```

#### 获取话题详情
```
GET /api/topic/<topic_id>
```

### 产品API

#### 获取产品列表
```
GET /api/products
```

#### 获取产品详情
```
GET /api/products/<slug>
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 官网：https://pieeg.cn
- 邮箱：info@pieeg.cn
- 技术支持：support@pieeg.cn

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 完整的产品展示系统
- 社区论坛功能
- 管理后台
- 容器化部署支持
