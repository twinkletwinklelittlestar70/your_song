from flask import Flask, render_template, request, jsonify, send_from_directory

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

# API 接口示例，非功能
@app.route('/accounts', methods=['GET'])
def get_accounts():

    if request.method == "GET":

        username = request.args.get("account")
        password = "aaa" #query_account(username)
        if password == "":
            return "no result"
        else:
            #return render_template("home.html",message=username,password=password)
            return jsonify({"password": password})


if __name__ == '__main__':
    app.run()