#!/bin/bash

# PIEEG 官网一键部署脚本
# 支持本地开发和生产环境部署

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    echo "PIEEG 官网一键部署脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  dev         启动开发环境"
    echo "  prod        启动生产环境"
    echo "  stop        停止所有服务"
    echo "  restart     重启所有服务"
    echo "  logs        查看日志"
    echo "  clean       清理Docker资源"
    echo "  backup      备份数据库"
    echo "  restore     恢复数据库"
    echo "  update      更新应用"
    echo "  help        显示此帮助信息"
    echo ""
}

# 检查Docker和Docker Compose
check_requirements() {
    print_info "检查系统要求..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    
    print_success "系统要求检查通过"
}

# 创建必要的目录和文件
setup_environment() {
    print_info "设置环境..."
    
    # 创建必要的目录
    mkdir -p logs
    mkdir -p ssl
    mkdir -p mysql-init
    mkdir -p src/static/uploads/products
    mkdir -p src/static/uploads/temp
    
    # 复制环境配置文件
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_info "已创建.env文件，请根据需要修改配置"
        else
            print_warning ".env.example文件不存在，跳过环境配置"
        fi
    fi
    
    # 创建MySQL初始化脚本
    cat > mysql-init/01-init.sql << 'EOF'
-- 创建数据库
CREATE DATABASE IF NOT EXISTS pieeg_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户并授权
CREATE USER IF NOT EXISTS 'pieeg_user'@'%' IDENTIFIED BY 'pieeg_password_2024';
GRANT ALL PRIVILEGES ON pieeg_db.* TO 'pieeg_user'@'%';
FLUSH PRIVILEGES;
EOF
    
    print_success "环境设置完成"
}

# 启动开发环境
start_dev() {
    print_info "启动开发环境..."
    
    # 使用开发环境配置
    export FLASK_ENV=development
    export SECRET_KEY=dev-secret-key
    
    # 启动服务（只启动数据库和Redis）
    docker-compose up -d db redis
    
    print_info "等待数据库启动..."
    sleep 15
    
    # 初始化数据库
    print_info "初始化数据库..."
    python3 init_db.py
    
    # 启动Flask开发服务器
    print_info "启动Flask开发服务器..."
    export FLASK_APP=src.main
    export FLASK_ENV=development
    flask run --host=0.0.0.0 --port=5000
}

# 启动生产环境
start_prod() {
    print_info "启动生产环境..."
    
    # 构建并启动所有服务
    docker-compose up -d --build
    
    print_info "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    if curl -f http://localhost/health &> /dev/null; then
        print_success "生产环境启动成功！"
        print_info "访问地址: http://localhost"
        print_info "管理员登录: admin / admin123"
    else
        print_error "服务启动失败，请检查日志"
        docker-compose logs
    fi
}

# 停止服务
stop_services() {
    print_info "停止所有服务..."
    docker-compose down
    print_success "服务已停止"
}

# 重启服务
restart_services() {
    print_info "重启服务..."
    docker-compose restart
    print_success "服务已重启"
}

# 查看日志
show_logs() {
    if [ -n "$2" ]; then
        # 查看指定服务的日志
        docker-compose logs -f "$2"
    else
        # 查看所有服务的日志
        docker-compose logs -f
    fi
}

# 清理Docker资源
clean_docker() {
    print_warning "这将删除所有停止的容器、未使用的网络和镜像"
    read -p "确定要继续吗？[y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "清理Docker资源..."
        docker system prune -f
        print_success "清理完成"
    else
        print_info "取消清理操作"
    fi
}

# 备份数据库
backup_database() {
    print_info "备份数据库..."
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="backup_${timestamp}.sql"
    
    docker-compose exec db mysqldump -u root -proot_password_2024 pieeg_db > "$backup_file"
    
    if [ -f "$backup_file" ]; then
        print_success "数据库备份完成: $backup_file"
    else
        print_error "数据库备份失败"
    fi
}

# 恢复数据库
restore_database() {
    if [ -z "$2" ]; then
        print_error "请指定备份文件"
        echo "用法: $0 restore <backup_file>"
        exit 1
    fi
    
    backup_file="$2"
    if [ ! -f "$backup_file" ]; then
        print_error "备份文件不存在: $backup_file"
        exit 1
    fi
    
    print_warning "这将覆盖现有数据库"
    read -p "确定要继续吗？[y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "恢复数据库..."
        docker-compose exec -T db mysql -u root -proot_password_2024 pieeg_db < "$backup_file"
        print_success "数据库恢复完成"
    else
        print_info "取消恢复操作"
    fi
}

# 更新应用
update_app() {
    print_info "更新应用..."
    
    # 拉取最新代码
    if [ -d .git ]; then
        git pull
    fi
    
    # 重新构建并启动
    docker-compose up -d --build
    
    print_success "应用更新完成"
}

# 主逻辑
case "$1" in
    "dev")
        check_requirements
        setup_environment
        start_dev
        ;;
    "prod")
        check_requirements
        setup_environment
        start_prod
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "logs")
        show_logs "$@"
        ;;
    "clean")
        clean_docker
        ;;
    "backup")
        backup_database
        ;;
    "restore")
        restore_database "$@"
        ;;
    "update")
        update_app
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_error "未知选项: $1"
        show_help
        exit 1
        ;;
esac 