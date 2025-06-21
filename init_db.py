#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表和初始数据
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

from src.main import create_app
from src.models.admin import db, User, Product, ProductCategory

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        print("正在创建数据库表...")
        
        # 删除所有表（仅在开发环境）
        if os.getenv('FLASK_ENV') == 'development':
            db.drop_all()
            print("已删除现有表")
        
        # 创建所有表
        db.create_all()
        print("数据库表创建成功")
        
        # 创建初始数据
        create_initial_data()
        
        print("数据库初始化完成!")

def create_initial_data():
    """创建初始数据"""
    
    # 创建管理员用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@pieeg.cn',
            role='admin'
        )
        admin.set_password('admin123')  # 请在生产环境中更改密码
        db.session.add(admin)
        print("已创建管理员用户: admin / admin123")
    
    # 创建产品分类
    categories_data = [
        {'name': 'EEG设备', 'slug': 'eeg-devices', 'description': '脑电波测量设备', 'order': 1},
        {'name': '扩展板', 'slug': 'extension-boards', 'description': '各种平台的扩展板', 'order': 2},
        {'name': '配件', 'slug': 'accessories', 'description': '电极和其他配件', 'order': 3},
    ]
    
    for cat_data in categories_data:
        category = ProductCategory.query.filter_by(slug=cat_data['slug']).first()
        if not category:
            category = ProductCategory(**cat_data)
            db.session.add(category)
            print(f"已创建产品分类: {cat_data['name']}")
    
    db.session.commit()
    
    # 获取分类ID
    eeg_category = ProductCategory.query.filter_by(slug='eeg-devices').first()
    board_category = ProductCategory.query.filter_by(slug='extension-boards').first()
    
    # 创建示例产品
    products_data = [
        {
            'name': 'PiEEG-8',
            'slug': 'pieeg-8',
            'short_description': '8通道脑机接口设备，兼容Raspberry Pi',
            'description': '''PiEEG-8是一款低成本的8通道脑机接口设备，专为Raspberry Pi设计。该设备可以测量EEG（脑电波）、EMG（肌电图）和ECG（心电图）生物信号。

主要特性：
- 兼容Raspberry Pi 3, 4和5
- 8个通道连接湿电极或干电极
- 24位分辨率，250 SPS至16 kSPS采样率
- 可编程信号增益：1, 2, 4, 6, 8, 12, 24
- 低噪音设计，适合研究和教育用途''',
            'price': 299.00,
            'image_url': '/static/images/pieeg-8.png',
            'is_featured': True,
            'is_active': True,
            'category_id': eeg_category.id if eeg_category else None,
            'features': [
                '8通道高精度采样',
                '24位ADC分辨率',
                '可调采样率',
                '低功耗设计',
                '开源软件支持'
            ],
            'specifications': [
                {'name': '通道数', 'value': '8'},
                {'name': 'ADC分辨率', 'value': '24位'},
                {'name': '采样率', 'value': '250 SPS - 16 kSPS'},
                {'name': '信号增益', 'value': '1, 2, 4, 6, 8, 12, 24'},
                {'name': '兼容平台', 'value': 'Raspberry Pi 3/4/5'},
            ],
            'applications': '适用于神经科学研究、BCI开发、教育培训等',
            'purchase_url': 'https://shop.pieeg.cn/pieeg-8',
            'inquiry_url': 'mailto:info@pieeg.cn'
        },
        {
            'name': 'PiEEG-16',
            'slug': 'pieeg-16',
            'short_description': '16通道脑机接口设备，兼容Raspberry Pi',
            'description': '''PiEEG-16是一款高性能的16通道脑机接口设备，专为需要更多通道的专业应用设计。

主要特性：
- 兼容Raspberry Pi 5
- 16个通道连接湿电极或干电极
- 24位分辨率，250 SPS至16 kSPS采样率
- 可编程信号增益：1, 2, 4, 6, 8, 12, 24
- 专业级信号质量''',
            'price': 599.00,
            'image_url': '/static/images/pieeg-16.png',
            'is_featured': True,
            'is_active': True,
            'category_id': eeg_category.id if eeg_category else None,
            'features': [
                '16通道同步采样',
                '24位ADC分辨率',
                '专业级信号质量',
                '可调采样率',
                '完整的软件工具链'
            ],
            'specifications': [
                {'name': '通道数', 'value': '16'},
                {'name': 'ADC分辨率', 'value': '24位'},
                {'name': '采样率', 'value': '250 SPS - 16 kSPS'},
                {'name': '信号增益', 'value': '1, 2, 4, 6, 8, 12, 24'},
                {'name': '兼容平台', 'value': 'Raspberry Pi 5'},
            ],
            'applications': '适用于专业神经科学研究、临床试验、高级BCI应用',
            'purchase_url': 'https://shop.pieeg.cn/pieeg-16',
            'inquiry_url': 'mailto:info@pieeg.cn'
        },
        {
            'name': 'ardEEG',
            'slug': 'ardeeg',
            'short_description': 'Arduino扩展板，8通道脑机接口设备',
            'description': '''ardEEG是专为Arduino设计的8通道脑机接口扩展板，让Arduino爱好者也能轻松进入脑机接口领域。

主要特性：
- 兼容Arduino UNO R4 WiFi
- 8个通道连接湿电极或干电极
- 24位分辨率，250 SPS至16 kSPS采样率
- 低功耗，适合可穿戴设备应用''',
            'price': 199.00,
            'image_url': '/static/images/ardeeg.png',
            'is_featured': True,
            'is_active': True,
            'category_id': board_category.id if board_category else None,
            'features': [
                'Arduino兼容设计',
                '8通道生物信号采集',
                '低功耗运行',
                '易于集成',
                '开源代码库'
            ],
            'specifications': [
                {'name': '通道数', 'value': '8'},
                {'name': 'ADC分辨率', 'value': '24位'},
                {'name': '采样率', 'value': '250 SPS - 16 kSPS'},
                {'name': '工作电压', 'value': '3.3V/5V'},
                {'name': '兼容平台', 'value': 'Arduino UNO R4 WiFi'},
            ],
            'applications': '适用于创客项目、可穿戴设备、IoT应用',
            'purchase_url': 'https://shop.pieeg.cn/ardeeg',
            'inquiry_url': 'mailto:info@pieeg.cn'
        }
    ]
    
    for prod_data in products_data:
        product = Product.query.filter_by(slug=prod_data['slug']).first()
        if not product:
            product = Product(**prod_data)
            db.session.add(product)
            print(f"已创建产品: {prod_data['name']}")
    
    db.session.commit()
    print("初始数据创建完成")

if __name__ == '__main__':
    init_database() 