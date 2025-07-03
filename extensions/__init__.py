from flask_sqlalchemy import SQLAlchemy

# redisClient = FlaskRedis()
db = SQLAlchemy()


def initExtensions(app):
    db.init_app(app)
    # redisClient.init_app(app)
