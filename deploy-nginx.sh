#!/bin/bash

# PIEEG Hugo + Nginx Deployment Script
# This script sets up Nginx to serve Hugo-generated static files

set -e

# Configuration variables
SITE_NAME="pieeg"
DOMAIN="pieeg.cn"
WWW_DOMAIN="www.pieeg.cn"
SITE_ROOT="/var/www/${SITE_NAME}"
NGINX_CONFIG="/etc/nginx/sites-available/${SITE_NAME}"
NGINX_ENABLED="/etc/nginx/sites-enabled/${SITE_NAME}"
BACKUP_DIR="/var/backups/${SITE_NAME}"
LOG_FILE="/var/log/${SITE_NAME}-deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

# Warning message  
warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error_exit "This script should not be run as root. Use sudo for specific commands."
    fi
}

# Install Nginx
install_nginx() {
    log "Installing Nginx..."
    
    if command -v nginx &> /dev/null; then
        success "Nginx is already installed"
        return 0
    fi
    
    # Update package list
    sudo apt update
    
    # Install Nginx
    sudo apt install -y nginx
    
    # Enable and start Nginx
    sudo systemctl enable nginx
    sudo systemctl start nginx
    
    # Configure firewall
    sudo ufw allow 'Nginx Full' 2>/dev/null || true
    
    success "Nginx installed and configured"
}

# Create site directory
create_site_directory() {
    log "Creating site directory..."
    
    # Create backup directory
    sudo mkdir -p "$BACKUP_DIR"
    
    # Backup existing files if they exist
    if [ -d "$SITE_ROOT" ]; then
        BACKUP_NAME="$(date +%Y%m%d-%H%M%S)"
        warning "Backing up existing site to $BACKUP_DIR/$BACKUP_NAME"
        sudo cp -r "$SITE_ROOT" "$BACKUP_DIR/$BACKUP_NAME"
    fi
    
    # Create site directory
    sudo mkdir -p "$SITE_ROOT"
    
    # Set proper ownership
    sudo chown -R "$USER:www-data" "$SITE_ROOT"
    sudo chmod -R 755 "$SITE_ROOT"
    
    success "Site directory created: $SITE_ROOT"
}

# Deploy Hugo files
deploy_hugo_files() {
    log "Deploying Hugo static files..."
    
    # Check if public directory exists
    if [ ! -d "public" ]; then
        error_exit "Public directory not found. Run 'hugo --minify' first."
    fi
    
    # Copy files to site root
    sudo cp -r public/* "$SITE_ROOT/"
    
    # Set proper permissions
    sudo chown -R www-data:www-data "$SITE_ROOT"
    sudo find "$SITE_ROOT" -type d -exec chmod 755 {} \;
    sudo find "$SITE_ROOT" -type f -exec chmod 644 {} \;
    
    success "Hugo files deployed to $SITE_ROOT"
}

# Create Nginx configuration
create_nginx_config() {
    log "Creating Nginx configuration..."
    
    sudo tee "$NGINX_CONFIG" > /dev/null <<EOF
# PIEEG Hugo Site Configuration
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN} ${WWW_DOMAIN};
    
    root ${SITE_ROOT};
    index index.html index.htm;
    
    # Logging
    access_log /var/log/nginx/${SITE_NAME}.access.log;
    error_log /var/log/nginx/${SITE_NAME}.error.log;
    
    # Enable compression
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
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline' 'unsafe-eval'" always;
    
    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot|otf)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary "Accept-Encoding";
        
        # Handle missing files gracefully
        try_files \$uri =404;
    }
    
    # Cache HTML files for shorter period
    location ~* \.(html|htm)$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
        
        try_files \$uri \$uri/ =404;
    }
    
    # Handle JSON and XML files
    location ~* \.(json|xml)$ {
        expires 1h;
        add_header Content-Type "application/json; charset=utf-8";
        
        try_files \$uri =404;
    }
    
    # Main location block
    location / {
        # Try to serve request as file, then as directory, then fall back to 404
        try_files \$uri \$uri/ =404;
        
        # Handle trailing slashes
        if (\$request_uri ~ ^/(.*)/$) {
            return 301 /\$1;
        }
    }
    
    # Handle robots.txt
    location = /robots.txt {
        allow all;
        log_not_found off;
        access_log off;
    }
    
    # Handle favicon
    location = /favicon.ico {
        log_not_found off;
        access_log off;
        expires 1y;
    }
    
    # Deny access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
    
    # Deny access to backup files
    location ~ ~$ {
        deny all;
        access_log off;
        log_not_found off;
    }
}

# Redirect www to non-www (optional)
server {
    listen 80;
    listen [::]:80;
    server_name ${WWW_DOMAIN};
    return 301 http://${DOMAIN}\$request_uri;
}
EOF
    
    success "Nginx configuration created: $NGINX_CONFIG"
}

# Enable site
enable_site() {
    log "Enabling Nginx site..."
    
    # Create symbolic link
    sudo ln -sf "$NGINX_CONFIG" "$NGINX_ENABLED"
    
    # Test Nginx configuration
    sudo nginx -t || error_exit "Nginx configuration test failed"
    
    # Reload Nginx
    sudo systemctl reload nginx
    
    success "Site enabled and Nginx reloaded"
}

# Main deployment function
main() {
    log "Starting PIEEG Hugo + Nginx deployment..."
    
    check_root
    install_nginx
    create_site_directory
    deploy_hugo_files
    create_nginx_config
    enable_site
    
    success "Deployment completed successfully!"
    echo ""
    echo "Your site should now be accessible at:"
    echo "  http://${DOMAIN}"
    echo "  http://${WWW_DOMAIN}"
    echo ""
    echo "Site root: $SITE_ROOT"
    echo "Nginx config: $NGINX_CONFIG"
    echo "Log file: $LOG_FILE"
}

# Script usage
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -d, --domain   Set domain name (default: pieeg.cn)"
    echo "  -r, --root     Set site root directory (default: /var/www/pieeg)"
    echo ""
    echo "Examples:"
    echo "  $0                          # Use default settings"
    echo "  $0 -d example.com           # Use custom domain"
    echo "  $0 -r /var/www/mysite       # Use custom root directory"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--domain)
            DOMAIN="$2"
            WWW_DOMAIN="www.$2"
            shift 2
            ;;
        -r|--root)
            SITE_ROOT="$2"
            shift 2
            ;;
        *)
            error_exit "Unknown option: $1"
            ;;
    esac
done

# Run main function
main "$@" 