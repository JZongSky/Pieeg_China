from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    short_description = db.Column(db.String(255))
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), default=0)
    image_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    features = db.Column(JSON)  # 存储产品特性列表
    specifications = db.Column(JSON)  # 存储产品规格
    applications = db.Column(db.Text)  # 应用场景
    downloads = db.Column(JSON)  # 可下载资料
    purchase_url = db.Column(db.String(255))  # 购买链接
    inquiry_url = db.Column(db.String(255))  # 咨询链接
    gallery_images = db.Column(JSON)  # 产品图库
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    category = db.relationship('ProductCategory', backref='products')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'short_description': self.short_description,
            'description': self.description,
            'price': float(self.price) if self.price else 0,
            'image_url': self.image_url,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'features': self.features,
            'specifications': self.specifications,
            'applications': self.applications,
            'purchase_url': self.purchase_url,
            'inquiry_url': self.inquiry_url,
            'gallery_images': self.gallery_images,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ProductCategory(db.Model):
    __tablename__ = 'product_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductCategory {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
