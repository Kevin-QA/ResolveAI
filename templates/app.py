from flask import Flask, render_template

# 初始化 Flask 应用
app = Flask(__name__)


# 定义主页路由
@app.route('/')
def home():
    """
    当用户访问根路径时，渲染 index.html 模板。
    """
    page_title = "欢迎来到主页 - 我的第一个Flask网站"

    # render_template 会自动在 'templates' 文件夹中查找 index.html
    return render_template('index.html', title=page_title)


# 定义关于页面路由
@app.route('/about')
def about():
    """
    当用户访问 /about 路径时，渲染 about.html 模板。
    """
    page_title = "关于我们"
    content = "这是一个关于页面，用于介绍本网站和开发者。"

    # 联调提示：您可以在这里设置断点，检查 page_title 和 content 的值。
    return render_template('about.html', title=page_title, content=content)


# 运行应用
if __name__ == '__main__':
    # 在 PyCharm 中运行或调试时，请确保配置正确，通常 PyCharm 会自动处理。
    app.run(debug=True)