from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

# Import models first to ensure they are registered with SQLAlchemy
from src.models.admin import db, User, Product as AdminProduct, ProductCategory as AdminProductCategory
from src.models.product import Product, ProductCategory

# Import routes
from src.routes.main import main_bp
from src.routes.admin import admin_bp
from src.routes.forum import forum_bp

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pieeg-dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'pieeg_db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(app.root_path), 'src', 'static', 'uploads')
    
    # 初始化扩展
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # 注册蓝图
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(forum_bp)
    
    # 错误处理
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # 创建上传目录
    with app.app_context():
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'temp'), exist_ok=True)
        
        # 创建数据库表
        try:
            db.create_all()
            print("数据库表创建成功")
        except Exception as e:
            print(f"数据库表创建失败: {e}")
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
