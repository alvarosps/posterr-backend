from flask import Blueprint, request, jsonify
from app import app, db
from app.models import Post, User
from sqlalchemy import func
from datetime import datetime, timedelta

post_routes = Blueprint('post_routes', __name__)

def can_create_post(user_id):
    day_ago = datetime.utcnow() - timedelta(days=1)
    post_count = Post.query.filter(Post.user_id == user_id, Post.created_at > day_ago).count()
    return post_count < 5

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
