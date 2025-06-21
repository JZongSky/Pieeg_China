# PIEEG 官网快速开始指南

## 🚀 一分钟快速部署

### 前提条件
- 已安装 Docker 和 Docker Compose
- 至少 4GB 可用内存
- 20GB 可用磁盘空间

### 快速部署步骤

1. **获取代码**
```bash
git clone <项目地址>
cd pieeg
```

2. **一键启动**
```bash
chmod +x deploy.sh
./deploy.sh prod
```

3. **验证部署**
```bash
# 等待服务启动（约30秒）
sleep 30

# 运行测试
python3 test_deployment.py
```

4. **访问网站**
- 网站首页: http://localhost
- 管理后台: http://localhost/admin
- 默认管理员: admin / admin123

## 🛠️ 开发环境部署

### 开发环境启动
```bash
./deploy.sh dev
```

### 开发环境访问
- 应用地址: http://localhost:5000
- 直接连接Flask开发服务器

## 📋 部署脚本命令

```bash
# 查看帮助
./deploy.sh help

# 生产环境
./deploy.sh prod

# 开发环境
./deploy.sh dev

# 停止服务
./deploy.sh stop

# 查看日志
./deploy.sh logs

# 备份数据
./deploy.sh backup
```

## 🔧 常见问题

### 端口冲突
如果80端口被占用，修改 `docker-compose.yml`：
```yaml
nginx:
  ports:
    - "8080:80"  # 改为8080端口
```

### 数据库连接失败
```bash
# 查看数据库日志
./deploy.sh logs db

# 重启数据库
docker-compose restart db
```

### 内存不足
确保系统有足够内存：
```bash
free -h
```

## 📊 默认账户

- **管理员账户**: admin / admin123
- **数据库**: pieeg_user / pieeg_password_2024

⚠️ **重要**: 生产环境部署后请立即更改默认密码！

## 🔗 相关链接

- [详细部署指南](deployment_guide.md)
- [项目文档](README.md)
- [API文档](#api文档)

## 📞 获取帮助

如有问题，请：
1. 查看 [故障排除指南](deployment_guide.md#故障排除)
2. 运行测试脚本: `python3 test_deployment.py`
3. 查看服务日志: `./deploy.sh logs` 