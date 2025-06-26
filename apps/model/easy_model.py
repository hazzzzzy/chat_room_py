from datetime import datetime

from flask_sqlalchemy.query import Query

from extensions import db


# 基类模型
class EasyModel(db.Model):
    # 定义为抽象类
    __abstract__ = True
    # 默认字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键ID")
    create_at = db.Column(db.DATETIME, default=datetime.now, comment="创建时间")
    query: Query

    # 自定义将返回实例对象转化为json
    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item
