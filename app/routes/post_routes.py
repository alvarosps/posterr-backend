from flask import Blueprint, request, jsonify
from app import app, db
from app.models import Post, User
from sqlalchemy import func, or_
from datetime import datetime, timedelta

post_routes = Blueprint('post_routes', __name__)

def can_create_post(user_id):
    day_ago = datetime.utcnow() - timedelta(days=1)
    post_count = Post.query.filter(Post.user_id == user_id, Post.created_at > day_ago).count()
    return post_count < 100

@post_routes.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        sort_by = request.args.get('sort_by', 'latest')
        
        query = Post.query.filter(Post.repost_id.is_(None))

        if keyword:
            query = query.filter(Post.content.like(f'%{keyword}%'))

        if sort_by == 'trending':
            query = query.order_by(func.count(Post.reposts).desc())
        else:
            query = query.order_by(Post.created_at.desc())

        posts = query.all()
        return jsonify([post.to_dict() for post in posts])
    
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        content = request.json.get('content')
        repost_id = request.json.get('repost_id')

        if not user_id or not content:
            return jsonify({"error": "Invalid request"}), 400

        if not can_create_post(user_id):
            return jsonify({"error": "Rate limit exceeded"}), 429
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        if repost_id and Post.query.filter_by(user_id=user_id, repost_id=repost_id).count() > 0:
            return jsonify({"error": "Duplicate repost"}), 400

        new_post = Post(content=content, author=user, repost_id=repost_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify(new_post.to_dict()), 201

@post_routes.route('/api/posts/<int:post_id>', methods=['GET'])
def handle_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post.to_dict())

@post_routes.route('/api/posts/<int:post_id>/repost', methods=['POST'])
def handle_repost(post_id):
    user_id = request.json.get('user_id')

    if not user_id:
        return jsonify({"error": "Invalid request"}), 400

    if not can_create_post(user_id):
        return jsonify({"error": "Rate limit exceeded"}), 429

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    original_post = Post.query.get(post_id)
    if not original_post:
        return jsonify({"error": "Post not found"}), 404

    if Post.query.filter_by(user_id=user_id, repost_id=post_id).count() > 0:
        return jsonify({"error": "Duplicate repost"}), 400

    repost = Post(content=original_post.content, author=user, repost_id=post_id)
    db.session.add(repost)
    db.session.commit()

    return jsonify(repost.to_dict()), 201

@post_routes.route('/api/posts/search', methods=['GET'])
def search_posts():
    keyword = request.args.get('keyword', '')

    if keyword:
        posts = Post.query.filter(
            or_(
                Post.content.ilike(f'%{keyword}%'),
                User.username.ilike(f'%{keyword}%')
            )
        ).join(User).all()
    else:
        posts = []

    return jsonify([post.to_dict() for post in posts])
