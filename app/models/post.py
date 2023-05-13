from app import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(777), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    repost_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    reposts = db.relationship('Post', backref=db.backref('repost', remote_side=[id]), lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "username": self.author.username,
            "repost_id": self.repost_id,
            "repost_count": len(self.reposts)
        }