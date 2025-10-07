from flask import Blueprint, request, jsonify
from my_project.auth.service.service import (
    get_users, get_media, get_users_by_saved_story_id, add_user, delete_user, update_user, 
    get_user_media, get_user_saved_stories, add_media, update_media, delete_media, 
    add_saved_story, update_saved_story, delete_saved_story, get_saved_stories, 
    add_comment, add_tag, get_column_stat, insert_noname_comments, add_saved_story_raw
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/users', methods=['GET'])
def users():
    """
    Отримай всіх користувачів з Instagram БД
    ---
    tags:
      - Users
    responses:
      200:
        description: Список користувачів з дампу
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: integer
              username:
                type: string
              email:
                type: string
              password_hash:
                type: string
              created_at:
                type: string
    """
    return jsonify(get_users())

@main_bp.route('/media', methods=['GET'])
def media():
    """
    Отримай всі медіа (пости/фото)
    ---
    tags:
      - Media
    responses:
      200:
        description: Список медіа
        schema:
          type: array
          items:
            type: object
            properties:
              media_id:
                type: integer
              media_type:
                type: string
              media_url:
                type: string
              uploaded_at:
                type: string
              user_id:
                type: integer
    """
    return jsonify(get_media())

@main_bp.route('/users', methods=['POST'])
def create_user():
    """
    Створи нового користувача (CRUD POST)
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        description: Дані нового користувача (JSON)
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: new_user
              description: Ім'я користувача (унікальне, 3-20 символів)
            email:
              type: string
              example: new@example.com
              description: Email (унікальний, валідний формат)
            password_hash:
              type: string
              example: hashed_password_123
              description: Захешований пароль (мінімум 8 символів)
          required: [username, email, password_hash]
    responses:
      201:
        description: Новий користувач створено
        schema:
          type: object
          properties:
            user_id:
              type: integer
            username:
              type: string
            email:
              type: string
            password_hash:
              type: string
            created_at:
              type: string
      400:
        description: Email або username існує
    """
    data = request.json
    user, status = add_user(data)
    return jsonify(user), status

@main_bp.route('/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    """
    Видали користувача (CRUD DELETE)
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID користувача для видалення
    responses:
      204:
        description: Користувача видалено
      404:
        description: Користувача не знайдено
    """
    delete_user(user_id)
    return '', 204

@main_bp.route('/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    """
    Онови користувача (CRUD PUT)
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID користувача для оновлення
      - name: body
        in: body
        description: Нові дані користувача (JSON)
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              example: updated_user
              description: Нове ім'я (унікальне)
            email:
              type: string
              example: updated@example.com
              description: Новий email (унікальний)
            password_hash:
              type: string
              example: new_hashed_password
              description: Новий пароль
          required: [username, email, password_hash]
    responses:
      200:
        description: Користувача оновлено
        schema:
          type: object
        properties:
          user_id:
            type: integer
          username:
            type: string
          email:
            type: string
          password_hash:
            type: string
          created_at:
            type: string
      404:
        description: Користувача не знайдено
    """
    data = request.json
    user = update_user(user_id, data)
    return jsonify(user)

@main_bp.route('/media', methods=['POST'])
def create_media():
    """
    Створи медіа (CRUD POST)
    ---
    tags:
      - Media
    parameters:
      - name: body
        in: body
        description: Дані нового медіа (JSON)
        required: true
        schema:
          type: object
          properties:
            media_type:
              type: string
              example: photo
              description: Тип медіа (photo/video)
            media_url:
              type: string
              example: https://example.com/img.jpg
              description: URL медіа
            user_id:
              type: integer
              example: 1
              description: ID користувача-власника
          required: [media_type, media_url, user_id]
    responses:
      201:
        description: Медіа створено
        schema:
          type: object
          properties:
            media_id:
              type: integer
            media_type:
              type: string
            media_url:
              type: string
            uploaded_at:
              type: string
            user_id:
              type: integer
      400:
        description: Невалідні дані
    """
    data = request.json
    media, status = add_media(data)
    return jsonify(media), status

@main_bp.route('/media/<int:media_id>', methods=['DELETE'])
def remove_media(media_id):
    """
    Видали медіа (CRUD DELETE)
    ---
    tags:
      - Media
    parameters:
      - name: media_id
        in: path
        type: integer
        required: true
        description: ID медіа для видалення
    responses:
      204:
        description: Медіа видалено
      404:
        description: Медіа не знайдено
    """
    delete_media(media_id)
    return '', 204

@main_bp.route('/media/<int:media_id>', methods=['PUT'])
def modify_media(media_id):
    """
    Онови медіа (CRUD PUT)
    ---
    tags:
      - Media
    parameters:
      - name: media_id
        in: path
        type: integer
        required: true
        description: ID медіа для оновлення
      - name: body
        in: body
        description: Нові дані медіа (JSON)
        required: true
        schema:
          type: object
          properties:
            media_type:
              type: string
              example: video
              description: Новий тип медіа
            media_url:
              type: string
              example: https://example.com/new_video.mp4
              description: Новий URL
            user_id:
              type: integer
              example: 2
              description: Новий власник (ID користувача)
          required: [media_type, media_url, user_id]
    responses:
      200:
        description: Медіа оновлено
        schema:
          type: object
          properties:
            media_id:
              type: integer
            media_type:
              type: string
            media_url:
              type: string
            uploaded_at:
              type: string
            user_id:
              type: integer
      404:
        description: Медіа не знайдено
    """
    data = request.json
    media = update_media(media_id, data)
    return jsonify(media)

@main_bp.route('/users/<int:user_id>/media', methods=['GET'])
def get_user_media_route(user_id):
    """
    Отримай медіа користувача
    ---
    tags:
      - Users Media
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID користувача
    responses:
      200:
        description: Медіа користувача
        schema:
          type: array
          items:
            type: object
            properties:
              media_id:
                type: integer
              media_type:
                type: string
              media_url:
                type: string
              uploaded_at:
                type: string
              user_id:
                type: integer
    """
    media_list = get_user_media(user_id)
    return jsonify(media_list)

@main_bp.route('/users/<int:user_id>/saved_stories', methods=['GET'])
def get_user_saved_stories_route(user_id):
    """
    Отримай збережені сторіз користувача
    ---
    tags:
      - Users Stories
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID користувача
    responses:
      200:
        description: Збережені сторіз
        schema:
          type: array
          items:
            type: object
            properties:
              saved_story_id:
                type: integer
              user_id:
                type: integer
              story_id:
                type: integer
              saved_at:
                type: string
    """
    saved_stories = get_user_saved_stories(user_id)
    return jsonify(saved_stories)

@main_bp.route('/saved_stories', methods=['GET'])
def saved_stories():
    """
    Отримай всі збережені сторіз
    ---
    tags:
      - SavedStories
    responses:
      200:
        description: Список збереженних сторіз
        schema:
          type: array
          items:
            type: object
            properties:
              saved_story_id:
                type: integer
              user_id:
                type: integer
              story_id:
                type: integer
              saved_at:
                type: string
    """
    return jsonify(get_saved_stories())

@main_bp.route('/saved_stories', methods=['POST'])
def create_saved_story():
    """
    Створи збережену сторіз (CRUD POST)
    ---
    tags:
      - SavedStories
    parameters:
      - name: body
        in: body
        description: Дані збереженої сторіз (JSON)
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 1
              description: ID користувача, що зберігає
            story_id:
              type: integer
              example: 1
              description: ID сторіз для збереження
          required: [user_id, story_id]
    responses:
      201:
        description: Сторіз збережено
        schema:
          type: object
          properties:
            saved_story_id:
              type: integer
            user_id:
              type: integer
            story_id:
              type: integer
            saved_at:
              type: string
      400:
        description: Невалідні дані
    """
    data = request.json
    saved_story, status = add_saved_story(data)
    return jsonify(saved_story), status

@main_bp.route('/saved_stories/<int:saved_story_id>', methods=['DELETE'])
def remove_saved_story(saved_story_id):
    """
    Видали збережену сторіз (CRUD DELETE)
    ---
    tags:
      - SavedStories
    parameters:
      - name: saved_story_id
        in: path
        type: integer
        required: true
        description: ID збереженої сторіз для видалення
    responses:
      204:
        description: Сторіз видалено
      404:
        description: Сторіз не знайдено
    """
    delete_saved_story(saved_story_id)
    return '', 204

@main_bp.route('/saved_stories/<int:saved_story_id>', methods=['PUT'])
def modify_saved_story(saved_story_id):
    """
    Онови збережену сторіз (CRUD PUT)
    ---
    tags:
      - SavedStories
    parameters:
      - name: saved_story_id
        in: path
        type: integer
        required: true
        description: ID збереженої сторіз для оновлення
      - name: body
        in: body
        description: Нові дані сторіз (JSON)
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 2
              description: Новий ID користувача
            story_id:
              type: integer
              example: 2
              description: Новий ID сторіз
          required: [user_id, story_id]
    responses:
      200:
        description: Сторіз оновлено
        schema:
          type: object
          properties:
            saved_story_id:
              type: integer
            user_id:
              type: integer
            story_id:
              type: integer
            saved_at:
              type: string
      404:
        description: Сторіз не знайдено
    """
    data = request.json
    saved_story = update_saved_story(saved_story_id, data)
    return jsonify(saved_story)

@main_bp.route('/saved_stories/<int:saved_story_id>/users', methods=['GET'])
def get_users_by_saved_story_id_route(saved_story_id):
    """
    Отримай користувачів по ID збереженої сторіз
    ---
    tags:
      - SavedStories Users
    parameters:
      - name: saved_story_id
        in: path
        type: integer
        required: true
        description: ID збереженої сторіз
    responses:
      200:
        description: Користувачі, що зберегли сторіз
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: integer
              username:
                type: string
              email:
                type: string
              password_hash:
                type: string
              created_at:
                type: string
    """
    users = get_users_by_saved_story_id(saved_story_id)
    return jsonify(users)

@main_bp.route('/add_comment', methods=['POST'])
def add_comment_route():
    """
    Додай коментар (процедура add_comment)
    ---
    tags:
      - Comments
    parameters:
      - name: body
        in: body
        description: Дані коментаря (JSON)
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 1
              description: ID користувача
            story_id:
              type: integer
              example: 1
              description: ID сторіз
            comment_text:
              type: string
              example: Test comment from Swagger
              description: Текст коментаря
            tag_id:
              type: integer
              example: 1
              description: ID тегу
          required: [user_id, story_id, comment_text, tag_id]
    responses:
      200:
        description: Коментар додано
        schema:
          type: object
          properties:
            user_id:
              type: integer
            story_id:
              type: integer
            comment_text:
              type: string
            tag_id:
              type: integer
      500:
        description: Помилка БД
    """
    try:
        data = request.json
        user_id = data['user_id']
        story_id = data['story_id']
        comment_text = data['comment_text']
        tag_id = data['tag_id']
        add_comment(user_id, story_id, comment_text, tag_id)
        return jsonify({
            "user_id": user_id,
            "story_id": story_id,
            "comment_text": comment_text,
            "tag_id": tag_id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/add_tag', methods=['POST'])
def add_tag_route():
    """
    Додай тег (процедура add_tag)
    ---
    tags:
      - Tags
    parameters:
      - name: body
        in: body
        description: Назва тегу (JSON)
        required: true
        schema:
          type: object
          properties:
            tag_name:
              type: string
              example: new_tag
              description: Назва тегу (унікальна)
          required: [tag_name]
    responses:
      200:
        description: Тег додано
        schema:
          type: object
          properties:
            tag_name:
              type: string
    """
    data = request.json
    tag_name = data['tag_name']
    add_tag(tag_name)
    return jsonify({"tag_name": tag_name})

@main_bp.route('/add_saved_story', methods=['POST'])
def add_saved_story_route():
    """
    Додай збережену сторіз (процедура add_saved_story)
    ---
    tags:
      - SavedStories Raw
    parameters:
      - name: body
        in: body
        description: Дані сторіз (JSON)
        required: true
        schema:
          type: object
          properties:
            user_id:
              type: integer
              example: 1
              description: ID користувача
            story_id:
              type: integer
              example: 1
              description: ID сторіз
          required: [user_id, story_id]
    responses:
      200:
        description: Сторіз збережено (raw)
        schema:
          type: object
          properties:
            user_id:
              type: integer
            story_id:
              type: integer
            created_at:
              type: string
    """
    data = request.json
    user_id = data['user_id']
    story_id = data['story_id']
    created_at = add_saved_story_raw(user_id, story_id)
    return jsonify({
        "user_id": user_id,
        "story_id": story_id,
        "created_at": created_at
    })

@main_bp.route('/insert_noname_comments', methods=['POST'])
def insert_noname_comments_route():
    """
    Встав 10 анонімних коментів (процедура)
    ---
    tags:
      - Comments
    parameters: []
    responses:
      200:
        description: 10 коментів вставлено
        schema:
          type: object
          properties:
            message:
              type: string
              example: 10 comments inserted successfully
    """
    insert_noname_comments()
    return jsonify({"message": "10 comments inserted successfully"})

@main_bp.route('/get_column_stat', methods=['GET'])
def get_column_stat_route():
    """
    Отримай статистику колонки (процедура get_column_stat)
    ---
    tags:
      - Stats
    parameters:
      - name: stat_type
        in: query
        type: string
        required: true
        example: AVG
        description: Тип статистики (AVG, SUM, COUNT)
      - name: column_name
        in: query
        type: string
        required: true
        example: age
        description: Назва колонки
      - name: table_name
        in: query
        type: string
        required: true
        example: Users
        description: Назва таблиці
    responses:
      200:
        description: Статистика
        schema:
          type: object
          properties:
            result:
              type: number
              example: 25.5
      404:
        description: Немає результату
    """
    stat_type = request.args.get('stat_type')  
    column_name = request.args.get('column_name')  
    table_name = request.args.get('table_name')  

    result = get_column_stat(stat_type, column_name, table_name)

    if result is not None:  
        return jsonify({"result": result}), 200
    else:
        return jsonify({"error": "No result found"}), 404

def register_routes(app):
    app.register_blueprint(main_bp)
