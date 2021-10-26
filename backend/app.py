from flask import Flask, render_template, request, jsonify
from .api.RecEngine import rec_engine
from .utils import gen_uuid
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'E://project-code//your_song//iss-project-agent-yvrh-8508c4e851cb.json'

DIALOGFLOW_PROJECT_ID = 'iss-project-agent-yvrh'
DIALOGFLOW_LANGUAGE_CODE = 'en'
Session123 = {}
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
    message = data['message']

    # TODO: 校验请求信息，没有信息或者信息格式不对，返回错误码

    # TODO: 把用户的消息发送给 dialogflow 机器人，拿到机器人回复（这里可能涉及需要多个机器人实例）

    # SESSION_ID = gen_uuid()
    SESSION_ID = 'me'
    if  SESSION_ID not in Session123:
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        Session123[SESSION_ID]={}
        Session123[SESSION_ID]["session"]=  session
        Session123[SESSION_ID]["session_client"]=  session_client
    else:
        session=Session123[SESSION_ID]["session"]
        session_client=Session123[SESSION_ID]["session_client"] 


    text_to_be_analyzed = message
    
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise


    # TODO: 根据返回数据判断是否需要推荐列表

    # 是否要推荐列表
    # print ("this is response")
    # print(response)# 检查response


    value = response.query_result.parameters.fields     #拿到response里识别部分

    # 如果不需要推荐，直接返回机器人的回复给用户
    # 识别"Default Welcome Intent"意图
    if response.query_result.intent.display_name == "Default Welcome Intent":
        # response的结构
        return_data = { # 返回给前端的数据
            "response": response.query_result.fulfillment_text
        }
        # TODO: return_data 按API文档，构造成机器人的回复格式
        
        return jsonify(return_data)
    
    # 如果需要推荐，调用rec_engine获取推荐列表

    # 需要推荐genre相关，识别"Genre_english"意图
    elif response.query_result.intent.display_name == "Genre_english":
        recommend_list = []
        if not value['genre'].list_value.values:    # 如果没有任何类型genre输入，继续询问用户
            return_data = {  # 返回给前端的数据
                "response": response.query_result.fulfillment_text
            }
        else:  # 如果获取到输入的genre,返回该风格类型的歌曲list
            rec_type=value['genre'].list_value.values[0].string_value
            recommend_list = rec_engine.get_list_by_genre(rec_type, artist_list=[], number=10)
            return_data = {  # 返回给前端的数据
                 "response": f"These songs which you may like",
                 "recommend_list": recommend_list
            }
    # 需要根据歌名推荐，识别"song_name"意图
    elif response.query_result.intent.display_name == "song_name":
        song_name = value['music_name'].list_value.values[0].string_value  # 获取歌名
        recommend_list = rec_engine.get_list_by_song(song_name=song_name, number=10)
        return_data = {  # 返回给前端的数据
            "response": f"These songs which you may like",
            "recommend_list": recommend_list
        }
    else:  # 当需要推荐，但是没有识别到任何意图时
        return_data = {
            "response": f"What genre like do you want?"
        }

    # TODO: return_data 按API文档，构造成回复格式，并在其中拼接上推荐列表。

    return jsonify(return_data)


if __name__ == '__main__':
    app.run()


#     artist: "Pinkie Pie"
# genre: "rock"
# id: 9209
# mode: 1
# name: "The Smile Song"
# uri: "spotify:track:78gubWpj4JIxFeMixvdNsi"
# url: "https://open.spotify.com/track/78gubWpj4JIxFeMixvdNsi"