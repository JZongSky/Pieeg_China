"""
数据库迁移脚本 - 添加产品详情页和购买链接相关字段
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import JSON

# 修订ID
revision = '0002_add_product_details'
down_revision = '0001_initial'  # 假设这是前一个迁移版本

def upgrade():
    # 修改产品表，添加新字段
    op.add_column('products', sa.Column('purchase_url', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('inquiry_url', sa.String(255), nullable=True))
    op.add_column('products', sa.Column('features', JSON, nullable=True))
    op.add_column('products', sa.Column('specifications', JSON, nullable=True))
    op.add_column('products', sa.Column('applications', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('downloads', JSON, nullable=True))
    op.add_column('products', sa.Column('gallery_images', JSON, nullable=True))

def downgrade():
    # 回滚操作，删除添加的字段
    op.drop_column('products', 'purchase_url')
    op.drop_column('products', 'inquiry_url')
    op.drop_column('products', 'features')
    op.drop_column('products', 'specifications')
    op.drop_column('products', 'applications')
    op.drop_column('products', 'downloads')
    op.drop_column('products', 'gallery_images')
