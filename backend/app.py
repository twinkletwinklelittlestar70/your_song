from flask import Flask, render_template, request, jsonify
from .api.RecEngine import rec_engine

# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
# static_url_path 指定访问的路径
app = Flask(
    __name__,
    static_folder="./static",
    static_url_path="/",
    template_folder="./static")

@app.route('/')
def index():
    '''
        当在浏览器访问网址时，通过 render_template 方法渲染 dist 文件夹中的 index.html。
        页面之间的跳转交给前端路由负责，后端不用再写大量的路由
    '''
    return render_template("index.html")

count_index = 0

# Get message from user and return 
@app.route('/api/send_msg', methods=['POST'])
def sned_msg():
    global count_index
    count_index += 1 # 用作测试

# TODO: 提醒：下面处理接口的流程实现的是单个用户的流程。
#       在实际服务中，这里是并发状态。如果有状态需要保存，要留下每个用户的上下文。
#       比如，如果机器人是能够记住用户上一句话的，就需要创建多个机器人实例，不同的用户单独发送聊天请求。否则就变成了所有用户都在跟一个机器人聊天。
#       但推荐引擎的两个接口都是无状态的，目前计划实现为全局单例。

    data = request.json
    # TODO: 从请求接口中获取用户发送的消息
    message = data['message']

    # TODO: 校验请求信息，没有信息或者信息格式不对，返回错误码

    # TODO: 把用户的消息发送给 dialogflow 机器人，拿到机器人回复（这里可能涉及需要多个机器人实例）

    # TODO: 根据返回数据判断是否需要推荐列表

    need_recommend = True # 是否要推荐列表

    # 如果不需要推荐，直接返回机器人的回复给用户
    if not need_recommend:
        return_data = { # 返回给前端的数据
            "response": f"This is normal {count_index} response"
        }
        # TODO: return_data 按API文档，构造成机器人的回复格式
        
        return jsonify(return_data)
    
    # 如果需要推荐，调用rec_engine获取推荐列表
    recommend_list = []
    rec_type = 1 # 1: recommend by genre  # 2: recommend by song
    return_data = { # 返回给前端的数据
        "response": f"This is recommend {count_index} response"
    }

    if rec_type == 1:
        # TODO: 替换成用户指定的风格和歌手
        genre = 'Pop'
        artist_list = ['taylor swift']

        recommend_list = rec_engine.get_list_by_genre(genre, artist_list, 10)
    elif rec_type == 2:
        song_id = 18344
        recommend_list = rec_engine.get_list_by_song(song_id, 10)

    # TODO: return_data 按API文档，构造成回复格式，并在其中拼接上推荐列表。

    return jsonify(return_data)


if __name__ == '__main__':
    app.run()