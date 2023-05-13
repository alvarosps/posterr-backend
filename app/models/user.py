from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }