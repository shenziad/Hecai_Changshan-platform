from flask_sqlalchemy import SQLAlchemy

# 初始化数据库
db = SQLAlchemy()

# 传承人数据模型
class Inheritor(db.Model):
    __tablename__ = 'inheritors'  # 表名

    # 定义表的字段
    id = db.Column(db.Integer, primary_key=True)  # 自动递增的主键
    name = db.Column(db.String(100), nullable=False)  # 传承人的名字
    description = db.Column(db.Text, nullable=False)  # 传承人的描述
    image = db.Column(db.String(200))  # 添加图片路径字段
    achievements = db.Column(db.JSON)   # 艺术成就列表
    works = db.Column(db.JSON)         # 代表作品列表
    contributions = db.Column(db.JSON)  # 添加贡献字段

    # 返回传承人对象的字符串表示
    def __repr__(self):
        return f'<Inheritor {self.name}>'

# 喝彩词数据模型
class Chant(db.Model):
    __tablename__ = 'chants'  # 表名

    # 定义表的字段
    id = db.Column(db.Integer, primary_key=True)  # 自动递增的主键
    title = db.Column(db.String(100), nullable=False)  # 添加标题字段
    text = db.Column(db.Text, nullable=False)  # 喝彩词的文本内容
    description = db.Column(db.Text)  # 添加描述字段
    category = db.Column(db.String(50))  # 添加分类字段

    # 返回喝彩词对象的字符串表示
    def __repr__(self):
        return f'<Chant {self.text}>'

# 教学书籍数据模型（这里硬编码，实际上可以根据需要扩展）
class TeachingBook(db.Model):
    __tablename__ = 'teaching_books'  # 表名

    # 定义表的字段
    id = db.Column(db.Integer, primary_key=True)  # 自动递增的主键
    title = db.Column(db.String(100), nullable=False)  # 书籍标题
    description = db.Column(db.String(200), nullable=False)  # 书籍描述

    # 返回书籍对象的字符串表示
    def __repr__(self):
        return f'<TeachingBook {self.title}>'
