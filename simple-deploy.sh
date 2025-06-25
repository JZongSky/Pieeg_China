#!/bin/bash

# Simple Hugo + Nginx Deployment Script
# This script demonstrates the basic steps to deploy Hugo static files with Nginx

echo "🚀 Starting Hugo + Nginx deployment..."

# Step 1: Generate static files with Hugo
echo "📦 Step 1: Building Hugo static files..."
hugo --minify --cleanDestinationDir

if [ $? -eq 0 ]; then
    echo "✅ Hugo build completed successfully"
    echo "📊 Generated files:"
    ls -la public/ | head -10
    echo "💾 Total size: $(du -sh public/ | cut -f1)"
else
    echo "❌ Hugo build failed"
    exit 1
fi

echo ""
echo "🔧 Step 2: Next steps for Nginx deployment:"
echo ""
echo "For automatic deployment, run:"
echo "  ./deploy-nginx.sh"
echo ""
echo "For manual deployment:"
echo "  1. Install Nginx: sudo apt install nginx"
echo "  2. Copy files: sudo cp -r public/* /var/www/html/"
echo "  3. Set permissions: sudo chown -R www-data:www-data /var/www/html/"
echo "  4. Configure Nginx: sudo nano /etc/nginx/sites-available/default"
echo "  5. Restart Nginx: sudo systemctl restart nginx"
echo ""
echo "📚 For detailed instructions, see: docs/NGINX_DEPLOYMENT_GUIDE.md"
echo ""
echo "🎉 Build completed! Your static files are ready in the 'public/' directory." 