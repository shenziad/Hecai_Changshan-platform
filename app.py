from flask import Flask, render_template, jsonify
from models import db, Inheritor, Chant, TeachingBook

# 创建 Flask 应用实例
app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# 主页路由
@app.route('/')
def index():
    try:
        inheritors = Inheritor.query.all()
        chants = Chant.query.all()
        return render_template('index.html', 
                             inheritors=inheritors, 
                             chants=chants)
    except Exception as e:
        app.logger.error(f"Error loading index page: {str(e)}")
        return render_template('500.html'), 500

# 详情页路由
@app.route('/inheritor/<int:id>')
def inheritor_detail(id):
    try:
        inheritor = Inheritor.query.get_or_404(id)
        return render_template('inheritor.html', inheritor=inheritor)
    except Exception as e:
        app.logger.error(f"Error loading inheritor {id}: {str(e)}")
        return render_template('404.html'), 404

@app.route('/chant/<int:id>')
def chant_detail(id):
    try:
        chant = Chant.query.get_or_404(id)
        return render_template('chant.html', chant=chant)
    except Exception as e:
        app.logger.error(f"Error loading chant {id}: {str(e)}")
        return render_template('404.html'), 404

# API路由
@app.route('/api/inheritors', methods=['GET'])
def get_inheritors():
    try:
        inheritors = Inheritor.query.all()
        return jsonify([{
            'id': i.id,
            'name': i.name, 
            'description': i.description,
            'image': i.image if i.image else None
        } for i in inheritors])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chants', methods=['GET'])
def get_chants():
    try:
        chants = Chant.query.all()
        return jsonify([{
            'id': c.id,
            'title': c.title,
            'text': c.text,
            'category': c.category
        } for c in chants])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teaching_books', methods=['GET'])
def get_teaching_books():
    try:
        books = TeachingBook.query.all()
        return jsonify([{
            'id': b.id,
            'title': b.title, 
            'description': b.description
        } for b in books])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 数据库初始化函数
def init_db():
    with app.app_context():
        db.create_all()
        
        # 检查是否需要初始化数据
        if not Inheritor.query.first():
            inheritors = [
                Inheritor(
                    name="王培兰",
                    description="出生于嘉庆乙未年，曾为滕王阁重修时主持过喝彩",
                    achievements=["喝彩师爷"],
                    works=["《滕王阁重修喝彩》", "《贺寿喝彩集》"]
                ),
                Inheritor(
                    name="曾令兵",
                    description="""国家级第四批非物质文化遗产"常山喝彩歌谣"第六代传承人，1965年生，衢州常山人。
他出身木匠世家，父亲曾祥泰是常山喝彩歌谣第五代代表性传承人，受家庭熏陶，从小对木工和喝彩歌谣产生浓厚兴趣。
17岁时拜父亲为师学木工手艺，学艺100天便出师，后在招贤街上做木工，木匠技能得心应手。""",
                    image="images/zenglingbing.png",  # 确保这个路径与实际文件名匹配
                    achievements=[
                        "国家级非物质文化遗产传承人",
                        "常山喝彩艺术研究会会长",
                        "浙江省优秀民间文艺人才",
                        "衢州市第八届人大代表",
                        "中国收藏家协会理事",
                        "中国民间文艺家协会会员",
                        "常山县民间文艺家协会主席",
                        "常山县喝彩协会主席",
                        "《上栋梁》获浙江省映山红奖",
                        "《常山喝彩歌谣》纪录片获全国市县电视推优活动一等奖"
                    ],
                    works=[
                        "《常山喝彩艺术》",
                        "《喝彩教学实录》",
                        "《喝彩歌谣代代传》连环画",
                        "《上栋梁》舞台作品",
                        "《常山喝彩歌谣》纪录片"
                    ],
                    contributions=[  # 需要在模型中添加新字段
                        "从各地收集彩词手抄古本",
                        "收藏喝彩仪式道具",
                        "走访民间喝彩师，倡导百业百彩",
                        "推动建成常山喝彩歌谣文化展示馆",
                        "在学校开设特色课程，培养学员超300人",
                        "为非遗项目融入历史街区建言献策",
                        "为非遗工作者提供生活补贴等建议"
                    ]
                ),
                Inheritor(
                    name="刘先宝",
                    description="常山喝彩第二代传承人",
                    image="images/liuxianbao.png",
                    achievements=[
                        "常山喝彩第二代传承人",
                        "浙江省非物质文化遗产传承人",
                        "常山县民间艺术家协会会长"
                    ],
                    works=[
                        "《常山喝彩传统曲目集》",
                        "《喝彩艺术传承与发展》",
                        "《王培兰喝彩艺术研究》"
                    ]
                ),
                Inheritor(
                    name="刘绪兴",
                    description="擅长为喝彩添加韵味，提升了喝彩歌谣的旋律音韵",
                    image="images/liuxuxing.png",
                    achievements=[
                        "常山喝彩艺术创新者",
                        "浙江省民间艺术家",
                        "常山喝彩韵腔流派创始人"
                    ],
                    works=[
                        "《喝彩韵腔集》",
                        "《新编喝彩唱段》",
                        "《韵味喝彩艺术研究》"
                    ]
                ),
                Inheritor(
                    name="刘朝训",
                    description="人称'乌皮师傅'，擅长皮影戏与喝彩结合表演，开创了喝彩艺术的新形式。",
                    image="images/liuchaoxun.png",
                    achievements=[
                        "常山皮影喝彩传承人",
                        "浙江省非物质文化遗产传承人",
                        "常山民间艺术双栖名家"
                    ],
                    works=[
                        "《皮影喝彩艺术》",
                        "《乌皮戏法集》",
                        "《喝彩与皮影的融合》"
                    ]
                ),
                Inheritor(
                    name="曾祥泰",
                    description="以'火中夺籍'闻名，在一次大火中冒险抢救出珍贵的喝彩手稿，为保护非遗作出重要贡献。",
                    image="images/zengxiangtai.png",
                    achievements=[
                        "常山喝彩资深传承人",
                        "非遗保护突出贡献奖获得者",
                        "常山喝彩历史研究专家"
                    ],
                    works=[
                        "《常山喝彩史话》",
                        "《失而复得的喝彩手稿》",
                        "《喝彩艺术档案汇编》"
                    ]
                )
            ]  
            db.session.add_all(inheritors)
            db.session.commit()
        
        if not Chant.query.first():
            chants = [
                Chant(
                    title="东家吓厨仪式",
                    text="""东家办事喜洋洋，手托薄礼拜厨房。
大厨师傅慌几天，提前张罗开菜单。
支支锅，劈劈柴，晚上走了早上来。
各位师傅很劳累，你们确实很受罪：
腰站弯，腿站疼，东家不知咋承情。
东家少茶又缺烟，让您辛苦好几天。
不怕苦，不怕热，骑着摩托和电车。
又做吃，又做喝，东家心里没法说。
几位师傅手艺好，大家有事把您找。
几位师傅您辛苦，忙里忙外为事主。
几位师傅手艺强，东家请俺来帮忙。
几位师傅手艺棒，各种菜式有模样。
几位师傅手艺高，手中不离勺子刀：
生改熟，大破小，凉拌红烧加小炒。
蒸好菜，又烧好汤，各种食材都配上。
又是切菜又是炒，味道弄得还很好。
做饭不离锅和盆，吃饭都靠您几人。
一样一样都做齐，下面准备要开席。
主东表示很满意，特上薄礼表心意：
有酒，有钱，还有烟，咱把礼物往上端。
这些烟酒还有钱，您们师傅都拿完。""",
                    description="这是一首赞美厨师劳动的喝彩词，体现了对厨师工作的尊重和感谢",
                    category="礼仪类"
                ),
                Chant(
                    title="龙门喝彩",
                    text="红日东升照四方，龙门鲤鱼跳龙门，一跳跳在龙门上，二跳跳在龙门上，三跳跳在凤凰堂。",
                    description="这是一首祝贺金榜题名的喝彩词",
                    category="庆贺类"
                ),
                Chant(
                    title="祥瑞颂",
                    text="看那边彩云片片，祥光万道；瑞气千条，环绕四方。",
                    description="这是一首描绘祥瑞景象的喝彩词",
                    category="颂扬类"
                ),
                Chant(
                    title="今日欢歌",
                    text="今日里，龙腾虎跃，今日里，凤舞麟欢。",
                    description="这是一首表达喜庆氛围的喝彩词",
                    category="庆典类"
                )
            ]
            db.session.add_all(chants)
            db.session.commit()

# 启动应用
if __name__ == "__main__":
    init_db()  # 初始化数据库
    app.run(debug=True)