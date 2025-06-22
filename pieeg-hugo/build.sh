#!/bin/bash

# PIEEG Hugo 网站构建脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数: 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查Hugo是否安装
check_hugo() {
    if ! command -v hugo &> /dev/null; then
        print_error "Hugo 未安装。请先安装Hugo:"
        echo "  macOS: brew install hugo"
        echo "  Windows: winget install Hugo.Hugo.Extended"
        echo "  Linux: snap install hugo --channel=extended"
        exit 1
    fi
    
    print_message "Hugo 版本: $(hugo version)"
}

# 开发模式
dev() {
    print_step "启动开发服务器..."
    hugo server --buildDrafts --port 1313 --bind 0.0.0.0
}

# 构建生产版本
build() {
    print_step "开始构建生产版本..."
    
    # 清理旧的构建文件
    if [ -d "public" ]; then
        print_message "清理旧的构建文件..."
        rm -rf public/*
    fi
    
    # 构建
    print_message "构建静态网站..."
    hugo --minify
    
    print_message "构建完成! 输出目录: $(pwd)/public"
    print_message "文件大小:"
    du -sh public/
}

# 预览构建结果
preview() {
    if [ ! -d "public" ]; then
        print_warning "未找到构建文件，先进行构建..."
        build
    fi
    
    print_step "启动预览服务器..."
    cd public
    python3 -m http.server 8080 &
    SERVER_PID=$!
    print_message "预览服务器已启动: http://localhost:8080"
    print_message "按 Ctrl+C 停止服务器"
    
    # 等待用户中断
    trap "kill $SERVER_PID; exit" INT
    wait
}

# 部署到目录
deploy() {
    if [ -z "$1" ]; then
        print_error "请指定部署目录"
        echo "用法: $0 deploy /path/to/deploy"
        exit 1
    fi
    
    DEPLOY_DIR="$1"
    
    print_step "部署到 $DEPLOY_DIR"
    
    # 先构建
    build
    
    # 创建部署目录
    mkdir -p "$DEPLOY_DIR"
    
    # 复制文件
    print_message "复制文件到部署目录..."
    cp -r public/* "$DEPLOY_DIR/"
    
    print_message "部署完成!"
}

# 清理
clean() {
    print_step "清理构建文件..."
    rm -rf public/
    rm -rf resources/
    print_message "清理完成!"
}

# 检查配置
check() {
    print_step "检查配置文件..."
    hugo config
    
    print_step "检查内容文件..."
    if [ -f "content/_index.md" ]; then
        print_message "✓ 首页内容文件存在"
    else
        print_warning "✗ 首页内容文件不存在"
    fi
    
    print_step "检查数据文件..."
    for file in data/products.yaml data/applications.yaml data/forum_topics.yaml; do
        if [ -f "$file" ]; then
            print_message "✓ $file 存在"
        else
            print_warning "✗ $file 不存在"
        fi
    done
    
    print_step "检查静态资源..."
    for dir in static/css static/js static/images; do
        if [ -d "$dir" ]; then
            print_message "✓ $dir 目录存在"
        else
            print_warning "✗ $dir 目录不存在"
        fi
    done
}

# 显示帮助
help() {
    echo "PIEEG Hugo 网站构建脚本"
    echo ""
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  dev                启动开发服务器"
    echo "  build              构建生产版本"
    echo "  preview            预览构建结果"
    echo "  deploy <目录>      部署到指定目录"
    echo "  clean              清理构建文件"
    echo "  check              检查配置和文件"
    echo "  help               显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 dev                    # 启动开发服务器"
    echo "  $0 build                  # 构建生产版本"
    echo "  $0 deploy /var/www/html   # 部署到Web服务器目录"
}

# 主函数
main() {
    # 检查是否在正确的目录
    if [ ! -f "hugo.toml" ]; then
        print_error "请在Hugo项目根目录运行此脚本"
        exit 1
    fi
    
    # 检查Hugo
    check_hugo
    
    case "$1" in
        "dev"|"serve")
            dev
            ;;
        "build")
            build
            ;;
        "preview")
            preview
            ;;
        "deploy")
            deploy "$2"
            ;;
        "clean")
            clean
            ;;
        "check")
            check
            ;;
        "help"|"--help"|"-h")
            help
            ;;
        "")
            print_warning "未指定命令，显示帮助信息:"
            help
            ;;
        *)
            print_error "未知命令: $1"
            help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@" 