from my_project.auth.dao.db import db
from my_project.auth.domain.models import User, Media, SavedStories, Story

def get_users():
    users = User.query.all()
    return [u.to_dict() for u in users]

def get_media():
    media = Media.query.all()
    return [m.to_dict() for m in media]

def add_user(data):
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return {"error": "Email already exists"}, 400
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=data['password_hash']
    )
    db.session.add(user)
    db.session.commit()
    return user.to_dict(), 201

def delete_user(user_id):
    saved_stories = SavedStories.query.filter_by(user_id=user_id).all()
    for saved_story in saved_stories:
        db.session.delete(saved_story)
    db.session.commit()

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

def update_user(user_id, data):
    user = User.query.get_or_404(user_id)
    user.username = data['username']
    user.email = data['email']
    user.password_hash = data['password_hash']
    db.session.commit()
    return user.to_dict()

def get_user_media(user_id):
    media_list = Media.query.filter_by(user_id=user_id).all()
    return [m.to_dict() for m in media_list]

def get_user_saved_stories(user_id):
    saved_stories = SavedStories.query.filter_by(user_id=user_id).all()
    return [ss.to_dict() for ss in saved_stories]

def get_users_by_saved_story_id(saved_story_id):
    saved_stories = SavedStories.query.filter_by(saved_story_id=saved_story_id).all()
    return [{
        "user_id": ss.user_id,
        "username": User.query.get(ss.user_id).username,
        "saved_at": ss.saved_at
    } for ss in saved_stories]

def add_media(data):
    media = Media(
        media_type=data['media_type'],
        media_url=data['media_url'],
        user_id=data['user_id']
    )
    db.session.add(media)
    db.session.commit()
    return media.to_dict(), 201

def update_media(media_id, data):
    media = Media.query.get_or_404(media_id)
    media.media_type = data['media_type']
    media.media_url = data['media_url']
    media.user_id = data['user_id']
    db.session.commit()
    return media.to_dict()

def delete_media(media_id):
    media = Media.query.get_or_404(media_id)
    db.session.delete(media)
    db.session.commit()
    return '', 204

def add_saved_story(data):
    saved_story = SavedStories(
        user_id=data['user_id'],
        story_id=data['story_id']
    )
    db.session.add(saved_story)
    db.session.commit()
    return saved_story.to_dict(), 201

def delete_saved_story(saved_story_id):
    saved_story = SavedStories.query.get_or_404(saved_story_id)
    db.session.delete(saved_story)
    db.session.commit()
    return '', 204

def update_saved_story(saved_story_id, data):
    saved_story = SavedStories.query.get_or_404(saved_story_id)
    saved_story.user_id = data['user_id']
    saved_story.story_id = data['story_id']
    db.session.commit()
    return saved_story.to_dict()

def get_users_by_story_id(story_id):
    saved_stories = SavedStories.query.filter_by(story_id=story_id).all()
    return [{
        "user_id": ss.user_id,
        "username": User.query.get(ss.user_id).username,
        "saved_at": ss.saved_at
    } for ss in saved_stories]

def get_saved_stories():
    saved_stories = SavedStories.query.all()
    return [ss.to_dict() for ss in saved_stories]

# Решта функцій (add_comment тощо) без змін — вони OK, бо raw SQL
def add_comment(user_id, story_id, comment_text, tag_id):
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc('add_comment', [user_id, story_id, comment_text, tag_id])
        connection.commit()
        cursor.close()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def add_saved_story_raw(user_id, story_id):  # Перейменував, бо add_saved_story вище ORM
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        created_at = cursor.callproc('add_saved_story', [user_id, story_id, 0])
        cursor.close()
        connection.commit()
        return created_at[2]  
    finally:
        connection.close()

def insert_noname_comments():
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc('insert_noname_comments')
        cursor.close()
        connection.commit()
    finally:
        connection.close()

def add_tag(tag_name):
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc('add_tag', [tag_name])
        cursor.close()
        connection.commit()
    finally:
        connection.close()

def get_column_stat(stat_type, column_name, table_name):
    connection = db.engine.raw_connection()
    try:
        cursor = connection.cursor()
        out_result = 0.0  
        cursor.callproc('get_column_stat', [stat_type, column_name, table_name, out_result])
        cursor.execute("SELECT @result;")  
        output = cursor.fetchone() 
        cursor.close()
        connection.commit()
        return float(output[0]) if output and output[0] is not None else None
    finally:
        connection.close()
