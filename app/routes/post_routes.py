from flask import Blueprint, request, jsonify
from app import app, db
from app.models import Post, User

post_routes = Blueprint('post_routes', __name__)

@post_routes.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        if keyword:
            posts = Post.query.filter(Post.content.like(f'${keyword}%'), Post.repost_id.is_(None)).all()
        else:
            posts = Post.query.all()
        return jsonify([post.to_dict() for post in posts])
    
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        content = request.json.get('content')
        repost_id = request.json.get('repost_id')

        if not user_id or not content:
            return jsonify({"error": "Invalid request"}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        new_post = Post(content=content, author=user, repost_id=repost_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify(new_post.to_dict()), 201