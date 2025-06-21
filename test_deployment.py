#!/usr/bin/env python3
"""
PIEEG官网部署测试脚本
用于验证部署后所有功能是否正常工作
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

class DeploymentTester:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.session = requests.Session()
        self.passed = 0
        self.failed = 0
        
    def test(self, description, test_func):
        """执行测试并报告结果"""
        print(f"Testing: {description}...", end=" ")
        try:
            result = test_func()
            if result:
                print("✓ PASS")
                self.passed += 1
            else:
                print("✗ FAIL")
                self.failed += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            self.failed += 1
    
    def test_homepage(self):
        """测试首页是否可访问"""
        response = self.session.get(self.base_url)
        return response.status_code == 200 and "PIEEG" in response.text
    
    def test_health_check(self):
        """测试健康检查端点"""
        try:
            response = self.session.get(urljoin(self.base_url, "/health"))
            return response.status_code == 200 and "healthy" in response.text
        except:
            return False
    
    def test_products_page(self):
        """测试产品页面"""
        response = self.session.get(urljoin(self.base_url, "/products"))
        return response.status_code == 200
    
    def test_forum_page(self):
        """测试论坛页面"""
        response = self.session.get(urljoin(self.base_url, "/forum"))
        return response.status_code == 200
    
    def test_admin_page(self):
        """测试管理页面（应该重定向到登录）"""
        response = self.session.get(urljoin(self.base_url, "/admin"))
        return response.status_code in [200, 302, 401, 403]
    
    def test_static_files(self):
        """测试静态文件是否可访问"""
        static_files = [
            "/static/css/style.css",
            "/static/js/charts.js",
            "/static/images/pieeg-hero.png"
        ]
        
        for file_path in static_files:
            try:
                response = self.session.get(urljoin(self.base_url, file_path))
                if response.status_code != 200:
                    return False
            except:
                return False
        return True
    
    def test_forum_api(self):
        """测试论坛API"""
        try:
            response = self.session.get(urljoin(self.base_url, "/forum/api/categories"))
            return response.status_code == 200 and response.headers.get('content-type', '').startswith('application/json')
        except:
            return False
    
    def test_responsive_design(self):
        """测试响应式设计（检查viewport meta标签）"""
        response = self.session.get(self.base_url)
        return 'viewport' in response.text
    
    def test_security_headers(self):
        """测试安全头（如果配置了）"""
        response = self.session.get(self.base_url)
        # 至少应该有基本的安全头
        headers = response.headers
        return 'X-Content-Type-Options' in headers or 'X-Frame-Options' in headers
    
    def test_database_connection(self):
        """通过页面内容测试数据库连接"""
        # 如果产品页面能正常显示，说明数据库连接正常
        response = self.session.get(urljoin(self.base_url, "/products"))
        return response.status_code == 200 and len(response.content) > 1000
    
    def run_all_tests(self):
        """运行所有测试"""
        print(f"Starting deployment tests for {self.base_url}")
        print("=" * 60)
        
        # 等待服务启动
        print("Waiting for services to start...")
        time.sleep(5)
        
        # 运行测试
        self.test("Homepage accessibility", self.test_homepage)
        self.test("Health check endpoint", self.test_health_check)
        self.test("Products page", self.test_products_page)
        self.test("Forum page", self.test_forum_page)
        self.test("Admin page", self.test_admin_page)
        self.test("Static files serving", self.test_static_files)
        self.test("Forum API", self.test_forum_api)
        self.test("Responsive design", self.test_responsive_design)
        self.test("Database connection", self.test_database_connection)
        
        # 可选的高级测试
        print("\nAdvanced tests:")
        self.test("Security headers", self.test_security_headers)
        
        # 报告结果
        print("\n" + "=" * 60)
        print(f"Test Results: {self.passed} passed, {self.failed} failed")
        
        if self.failed == 0:
            print("🎉 All tests passed! Deployment is successful.")
            return True
        else:
            print("❌ Some tests failed. Please check the issues.")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test PIEEG website deployment")
    parser.add_argument("--url", default="http://localhost", 
                       help="Base URL to test (default: http://localhost)")
    parser.add_argument("--wait", type=int, default=30,
                       help="Wait time for services to start (default: 30 seconds)")
    
    args = parser.parse_args()
    
    print(f"Waiting {args.wait} seconds for services to start...")
    time.sleep(args.wait)
    
    tester = DeploymentTester(args.url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 