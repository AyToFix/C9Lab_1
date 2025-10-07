from my_project.auth.dao.db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Media(db.Model):
    __tablename__ = 'Media'
    media_id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.String(50), nullable=False)
    media_url = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)

    def to_dict(self):
        return {
            "media_id": self.media_id,
            "media_type": self.media_type,
            "media_url": self.media_url,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
            "user_id": self.user_id
        }

class SavedStories(db.Model):
    __tablename__ = 'SavedStories'
    saved_story_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    story_id = db.Column(db.Integer, db.ForeignKey('Stories.story_id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "saved_story_id": self.saved_story_id,
            "user_id": self.user_id,
            "story_id": self.story_id,
            "saved_at": self.saved_at.isoformat() if self.saved_at else None
        }

class Story(db.Model):
    __tablename__ = 'Stories'
    story_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey('Media.media_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    expiration_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "story_id": self.story_id,
            "user_id": self.user_id,
            "media_id": self.media_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expiration_at": self.expiration_at.isoformat() if self.expiration_at else None
        }

# Решта моделей (Reaction, Comment тощо) аналогічно, з to_dict
class Reaction(db.Model):
    __tablename__ = 'Reactions'
    reaction_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('Stories.story_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    reaction_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "reaction_id": self.reaction_id,
            "story_id": self.story_id,
            "user_id": self.user_id,
            "reaction_type": self.reaction_type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Comment(db.Model):
    __tablename__ = 'Comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('Stories.story_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "story_id": self.story_id,
            "user_id": self.user_id,
            "comment_text": self.comment_text,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Follower(db.Model):
    __tablename__ = 'Followers'
    follower_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    follower_user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    followed_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "follower_id": self.follower_id,
            "user_id": self.user_id,
            "follower_user_id": self.follower_user_id,
            "followed_at": self.followed_at.isoformat() if self.followed_at else None
        }

class Notification(db.Model):
    __tablename__ = 'Notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Hashtag(db.Model):
    __tablename__ = 'Hashtags'
    hashtag_id = db.Column(db.Integer, primary_key=True)
    hashtag_name = db.Column(db.String(255), nullable=False, unique=True)

    def to_dict(self):
        return {
            "hashtag_id": self.hashtag_id,
            "hashtag_name": self.hashtag_name
        }

class StoryHashtag(db.Model):
    __tablename__ = 'StoryHashtags'
    story_id = db.Column(db.Integer, db.ForeignKey('Stories.story_id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('Hashtags.hashtag_id'), primary_key=True)

    def to_dict(self):
        return {
            "story_id": self.story_id,
            "hashtag_id": self.hashtag_id
        }
