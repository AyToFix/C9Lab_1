import os
from flask import Flask
from dotenv import load_dotenv  # Для .env
from flasgger import Swagger    # Для Swagger
from my_project.auth.dao.db import init_db
from my_project.auth.route.main import register_routes

load_dotenv()  # Читає .env

app = Flask(__name__)

# Дебаг: Виведе пароль з .env (або None)
password = os.getenv('DB_PASSWORD')
print("Пароль з .env:", password)  # Має 'pmlb3goV', не None

# URI з дефолтом (якщо .env None — 'pmlb3goV')
db_password = os.getenv('DB_PASSWORD', 'pmlb3goV')  # Дефолт
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://aytofix:pmlb3goV@dbserverlab1.mysql.database.azure.com/instagram_db1?ssl_ca=DigiCertGlobalRootG2.crt.pem&ssl_verify_cert=true'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Оптимізація

init_db(app)

# Реєструємо роути ПЕРШИМ (щоб Swagger бачив blueprint)
register_routes(app)

# Проста конфігурація Swagger (фікс для blueprint, сканує /users тощо)
app.config['SWAGGER'] = {
    'title': 'Instagram API',
    'uiversion': 2,  # Зміни на 2 (Flasgger базовий, requestBody не парситься в 3)
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,  # Всі роути
            'model_filter': lambda tag: True,  # Docstrings парсинг
        }
    ],
    'specs_route': '/apidocs/',  # UI
    'static_url_path': '/flasgger_static',
    'specification_path': 'apispec',
    'swagger_ui': True,
    'basePath': '/',
    'app': app
}

swagger = Swagger(app)  # Без template

# Print
print("Сервер запущено на http://127.0.0.1:5000")
print("Swagger UI: http://127.0.0.1:5000/apidocs")
print("API endpoints: http://127.0.0.1:5000/users (GET/POST), /media (GET/POST), /saved_stories")

#if __name__ == "__main__":
#    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
