from flask_sqlalchemy import SQLAlchemy

# Ініціалізація SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        # db.create_all()  # Закоментовано: Таблиці з дампу, не створювати дубль
        pass  # Просто підключаємо БД
