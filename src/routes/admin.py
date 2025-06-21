from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from src.models.product import Product, ProductCategory
from src.models.admin import db
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import uuid

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 产品管理路由
@admin_bp.route('/products')
def products():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/products/index.html', products=products)

@admin_bp.route('/products/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        # 获取基本信息
        name = request.form.get('name')
        slug = request.form.get('slug')
        short_description = request.form.get('short_description')
        description = request.form.get('description')
        price = request.form.get('price') or 0
        category_id = request.form.get('category_id')
        purchase_url = request.form.get('purchase_url')
        inquiry_url = request.form.get('inquiry_url')
        applications = request.form.get('applications')
        is_featured = 'is_featured' in request.form
        is_active = 'is_active' in request.form
        
        # 处理产品特性
        features = request.form.getlist('features[]')
        features = [f for f in features if f.strip()]
        
        # 处理产品规格
        spec_names = request.form.getlist('spec_names[]')
        spec_values = request.form.getlist('spec_values[]')
        specifications = []
        for i in range(min(len(spec_names), len(spec_values))):
            if spec_names[i].strip() and spec_values[i].strip():
                specifications.append({
                    'name': spec_names[i].strip(),
                    'value': spec_values[i].strip()
                })
        
        # 处理主图片上传
        image_url = None
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            filename = secure_filename(file.filename)
            # 生成唯一文件名
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', unique_filename)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file.save(file_path)
            image_url = f"/static/uploads/products/{unique_filename}"
        
        # 处理图库图片
        gallery_images = []
        gallery_urls = request.form.getlist('gallery_images[]')
        for url in gallery_urls:
            if url.strip():
                gallery_images.append({'url': url.strip()})
        
        # 创建新产品
        product = Product(
            name=name,
            slug=slug,
            short_description=short_description,
            description=description,
            price=price,
            category_id=category_id if category_id else None,
            image_url=image_url,
            features=features,
            specifications=specifications,
            applications=applications,
            purchase_url=purchase_url,
            inquiry_url=inquiry_url,
            gallery_images=gallery_images,
            is_featured=is_featured,
            is_active=is_active
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('产品创建成功', 'success')
        return redirect(url_for('admin.products'))
    
    # GET请求，显示创建表单
    categories = ProductCategory.query.order_by(ProductCategory.order).all()
    return render_template('admin/products/create.html', categories=categories)

@admin_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        # 获取基本信息
        product.name = request.form.get('name')
        product.slug = request.form.get('slug')
        product.short_description = request.form.get('short_description')
        product.description = request.form.get('description')
        product.price = request.form.get('price') or 0
        product.category_id = request.form.get('category_id') or None
        product.purchase_url = request.form.get('purchase_url')
        product.inquiry_url = request.form.get('inquiry_url')
        product.applications = request.form.get('applications')
        product.is_featured = 'is_featured' in request.form
        product.is_active = 'is_active' in request.form
        
        # 处理产品特性
        features = request.form.getlist('features[]')
        product.features = [f for f in features if f.strip()]
        
        # 处理产品规格
        spec_names = request.form.getlist('spec_names[]')
        spec_values = request.form.getlist('spec_values[]')
        specifications = []
        for i in range(min(len(spec_names), len(spec_values))):
            if spec_names[i].strip() and spec_values[i].strip():
                specifications.append({
                    'name': spec_names[i].strip(),
                    'value': spec_values[i].strip()
                })
        product.specifications = specifications
        
        # 处理主图片上传
        if 'image' in request.files and request.files['image'].filename:
            file = request.files['image']
            filename = secure_filename(file.filename)
            # 生成唯一文件名
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', unique_filename)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            file.save(file_path)
            product.image_url = f"/static/uploads/products/{unique_filename}"
        
        # 处理图库图片
        gallery_images = []
        gallery_urls = request.form.getlist('gallery_images[]')
        for url in gallery_urls:
            if url.strip():
                gallery_images.append({'url': url.strip()})
        product.gallery_images = gallery_images
        
        # 更新时间
        product.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('产品更新成功', 'success')
        return redirect(url_for('admin.products'))
    
    # GET请求，显示编辑表单
    categories = ProductCategory.query.order_by(ProductCategory.order).all()
    return render_template('admin/products/edit.html', product=product, categories=categories)

@admin_bp.route('/products/<int:id>/delete', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    
    flash('产品已删除', 'success')
    return redirect(url_for('admin.products'))

# 产品分类管理路由
@admin_bp.route('/product-categories')
def product_categories():
    categories = ProductCategory.query.order_by(ProductCategory.order).all()
    return render_template('admin/products/categories.html', categories=categories)

@admin_bp.route('/product-categories/create', methods=['GET', 'POST'])
def create_product_category():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        description = request.form.get('description')
        order = request.form.get('order', 0, type=int)
        
        category = ProductCategory(
            name=name,
            slug=slug,
            description=description,
            order=order
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('产品分类创建成功', 'success')
        return redirect(url_for('admin.product_categories'))
    
    return render_template('admin/products/create_category.html')

@admin_bp.route('/product-categories/<int:id>/edit', methods=['GET', 'POST'])
def edit_product_category(id):
    category = ProductCategory.query.get_or_404(id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.slug = request.form.get('slug')
        category.description = request.form.get('description')
        category.order = request.form.get('order', 0, type=int)
        category.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('产品分类更新成功', 'success')
        return redirect(url_for('admin.product_categories'))
    
    return render_template('admin/products/edit_category.html', category=category)

@admin_bp.route('/product-categories/<int:id>/delete', methods=['POST'])
def delete_product_category(id):
    category = ProductCategory.query.get_or_404(id)
    
    # 检查是否有产品使用此分类
    products_count = Product.query.filter_by(category_id=id).count()
    if products_count > 0:
        flash(f'无法删除此分类，有 {products_count} 个产品正在使用它', 'danger')
        return redirect(url_for('admin.product_categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('产品分类已删除', 'success')
    return redirect(url_for('admin.product_categories'))

# 图片上传API
@admin_bp.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'uploads', unique_filename)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        file.save(file_path)
        url = f"/static/uploads/uploads/{unique_filename}"
        
        return jsonify({'url': url})
    
    return jsonify({'error': '上传失败'}), 500
