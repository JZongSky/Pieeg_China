from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from src.models.product import Product, ProductCategory
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # 获取推荐产品
    featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(4).all()
    return render_template('index.html', featured_products=featured_products)

@main_bp.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    per_page = 12  # 每页显示的产品数量
    category_slug = request.args.get('category')
    
    # 获取所有产品分类
    categories = ProductCategory.query.order_by(ProductCategory.order).all()
    
    # 根据分类筛选产品
    query = Product.query.filter_by(is_active=True)
    if category_slug:
        category = ProductCategory.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=category.id)
    else:
        category = None
    
    # 分页
    pagination = query.order_by(desc(Product.is_featured), Product.name).paginate(page=page, per_page=per_page)
    products = pagination.items
    
    return render_template('products/index.html', 
                          products=products, 
                          categories=categories, 
                          category=category_slug,
                          pagination=pagination)

@main_bp.route('/products/<slug>')
def product_detail(slug):
    # 获取产品详情
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    # 获取相关产品（同类别的其他产品）
    if product.category_id:
        related_products = Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id,
            Product.is_active == True
        ).limit(4).all()
    else:
        related_products = []
    
    return render_template('products/detail.html', 
                          product=product, 
                          related_products=related_products)
