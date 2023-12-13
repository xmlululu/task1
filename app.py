# app.py
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # 渲染HTML页面
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    # 获取表单数据
    text = request.form['text']
    file = request.files['file']

    # 判断是处理文件还是文本
    if file:
        # 处理上传的文件
        content = file.read().decode('utf-8')
    elif text:
        # 处理输入的文本
        content = text
    else:
        # 如果没有内容，返回错误信息
        return jsonify({'summary': '没有提供内容。'})

    # 在这里添加你的文本总结逻辑
    summary = '这里将显示文本的总结。'

    # 返回JSON响应
    return jsonify({'summary': summary})


# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True)
