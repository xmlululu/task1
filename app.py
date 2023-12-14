from flask import Flask, request, jsonify, render_template
import api
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text', methods=['GET'])
def textPage():
    return render_template('text_summarizer.html')


@app.route('/audio', methods=['GET'])
def audioPage():
    return render_template('audio_summarizer.html')


@app.route('/summarize_text', methods=['POST'])
def summarizeTextRoute():
    # 获取表单数据
    text = request.form.get('text')
    file = request.files.get('file')

    # 判断是处理文件还是文本
    if file:
        # 处理上传的文件
        content = file.read().decode('utf-8')
    elif text:
        # 处理输入的文本
        content = text
    else:
        return jsonify({'summary': '没有提供内容。'})

    # 在这里添加你的文本总结逻辑
    summary = api.summarizeText(title='', content=content)

    return jsonify({'summary': summary})


@app.route('/summarize_audio', methods=['POST'])
def summarizeAudioRoute():
    # 获取表单数据
    file = request.files.get('file')

    # 判断是处理文件还是文本
    if file:
        # 处理上传的文件
        file.save(file.filename)
    else:
        return jsonify({'summary': '没有提供内容。'})

    # 在这里添加你的文本总结逻辑
    summary = api.summarizeAudio('./' + file.filename)

    return jsonify({'summary': summary})


# 启动Flask应用
if __name__ == '__main__':
    app.run(debug=True)
