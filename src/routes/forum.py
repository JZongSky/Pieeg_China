from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import uuid

# 创建论坛蓝图
forum_bp = Blueprint('forum', __name__)

# 模拟数据库 - 实际项目中应使用真实数据库
forum_categories = [
    {"id": "general", "name": "综合讨论", "description": "关于PIEEG的一般性讨论"},
    {"id": "technical", "name": "技术交流", "description": "技术问题和解决方案分享"},
    {"id": "projects", "name": "项目展示", "description": "分享您使用PIEEG设备的项目"},
    {"id": "research", "name": "研究应用", "description": "学术研究和实验讨论"},
    {"id": "hardware", "name": "硬件讨论", "description": "关于PIEEG硬件的讨论"},
    {"id": "software", "name": "软件开发", "description": "软件开发和API使用"}
]

# 模拟话题数据
forum_topics = [
    {
        "id": str(uuid.uuid4()),
        "title": "欢迎来到PIEEG社区论坛",
        "content": "欢迎加入PIEEG社区！这里是分享经验、提问和讨论的地方。",
        "author": "PIEEG团队",
        "category_id": "general",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 120,
        "replies": 5
    },
    {
        "id": str(uuid.uuid4()),
        "title": "如何开始使用PiEEG-8进行基础EEG测量",
        "content": "我刚收到PiEEG-8设备，想了解如何开始进行基础的EEG测量。有没有新手入门指南？",
        "author": "新用户01",
        "category_id": "technical",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 85,
        "replies": 3
    },
    {
        "id": str(uuid.uuid4()),
        "title": "分享：使用PIEEG开发的冥想辅助应用",
        "content": "我使用PiEEG-16开发了一个冥想辅助应用，可以实时监测冥想状态并提供反馈。",
        "author": "冥想爱好者",
        "category_id": "projects",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 210,
        "replies": 12
    },
    {
        "id": str(uuid.uuid4()),
        "title": "ardEEG与Arduino的兼容性问题",
        "content": "我在使用ardEEG与Arduino UNO R4 WiFi连接时遇到了一些问题，有人能帮忙解决吗？",
        "author": "Arduino爱好者",
        "category_id": "hardware",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 65,
        "replies": 2
    },
    {
        "id": str(uuid.uuid4()),
        "title": "Python信号处理课程的学习心得",
        "content": "最近完成了PIEEG提供的Python信号处理课程，分享一下我的学习心得和实践经验。",
        "author": "数据科学家",
        "category_id": "software",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "views": 150,
        "replies": 8
    }
]

# 模拟回复数据
forum_replies = {
    # 话题ID: [回复列表]
}

# 论坛首页
@forum_bp.route('/')
def index():
    return render_template('forum/index.html', 
                          categories=forum_categories, 
                          topics=forum_topics)

# 分类页面
@forum_bp.route('/category/<category_id>')
def category(category_id):
    category = next((c for c in forum_categories if c["id"] == category_id), None)
    if not category:
        flash('分类不存在')
        return redirect(url_for('forum.index'))
    
    # 筛选该分类下的话题
    topics = [t for t in forum_topics if t["category_id"] == category_id]
    
    return render_template('forum/category.html', 
                          category=category, 
                          topics=topics)

# 话题详情页
@forum_bp.route('/topic/<topic_id>')
def topic(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        flash('话题不存在')
        return redirect(url_for('forum.index'))
    
    # 增加浏览量
    topic["views"] += 1
    
    # 获取回复
    replies = forum_replies.get(topic_id, [])
    
    return render_template('forum/topic.html', 
                          topic=topic, 
                          replies=replies)

# 创建新话题页面
@forum_bp.route('/new-topic', methods=['GET', 'POST'])
def new_topic():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        author = request.form.get('author', '匿名用户')  # 实际项目中应从用户会话获取
        
        if not title or not content or not category_id:
            flash('请填写所有必填字段')
            return redirect(url_for('forum.new_topic'))
        
        # 创建新话题
        new_topic = {
            "id": str(uuid.uuid4()),
            "title": title,
            "content": content,
            "author": author,
            "category_id": category_id,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "views": 0,
            "replies": 0
        }
        
        forum_topics.append(new_topic)
        flash('话题创建成功')
        return redirect(url_for('forum.topic', topic_id=new_topic["id"]))
    
    return render_template('forum/new_topic.html', 
                          categories=forum_categories)

# 回复话题
@forum_bp.route('/topic/<topic_id>/reply', methods=['POST'])
def reply(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        flash('话题不存在')
        return redirect(url_for('forum.index'))
    
    content = request.form.get('content')
    author = request.form.get('author', '匿名用户')  # 实际项目中应从用户会话获取
    
    if not content:
        flash('回复内容不能为空')
        return redirect(url_for('forum.topic', topic_id=topic_id))
    
    # 创建新回复
    new_reply = {
        "id": str(uuid.uuid4()),
        "content": content,
        "author": author,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 添加到回复列表
    if topic_id not in forum_replies:
        forum_replies[topic_id] = []
    forum_replies[topic_id].append(new_reply)
    
    # 更新话题回复数
    topic["replies"] += 1
    
    flash('回复成功')
    return redirect(url_for('forum.topic', topic_id=topic_id))

# API: 获取所有分类
@forum_bp.route('/api/categories')
def api_categories():
    return jsonify(forum_categories)

# API: 获取分类下的话题
@forum_bp.route('/api/category/<category_id>/topics')
def api_category_topics(category_id):
    topics = [t for t in forum_topics if t["category_id"] == category_id]
    return jsonify(topics)

# API: 获取话题详情
@forum_bp.route('/api/topic/<topic_id>')
def api_topic(topic_id):
    topic = next((t for t in forum_topics if t["id"] == topic_id), None)
    if not topic:
        return jsonify({"error": "话题不存在"}), 404
    
    # 获取回复
    replies = forum_replies.get(topic_id, [])
    
    return jsonify({
        "topic": topic,
        "replies": replies
    })
