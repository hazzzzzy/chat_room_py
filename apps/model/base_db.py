from extensions import db


# 模型基类方法
class base_db:
    # 定义为抽象类
    __abstract__ = True

    # 添加一条数据，对象方法
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
        finally:
            # 关闭连接
            db.session.close()

    # 添加多条数据，静态方法
    @staticmethod
    def save_all(*args):
        try:
            db.session.add_all(args)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            # 关闭连接
            db.session.close()

    # 删除数据
    @staticmethod
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
        finally:
            # 关闭连接
            db.session.close()
