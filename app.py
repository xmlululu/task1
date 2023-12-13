from flask import Flask, request, jsonify, render_template
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdknlp.v2.region.nlp_region import NlpRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdknlp.v2 import *
import os

app = Flask(__name__)

# 初始化华为云NLP客户端
def create_nlp_client():
    ak = "ORAEUEXV4RREC1ZFPEPN"
    sk = "nUVOhC9fBe85rtfpiX3fyODtgRAEBlfpfxCqafiE"
    credentials = BasicCredentials(ak, sk)
    client = NlpClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(NlpRegion.value_of("cn-north-4")) \
        .build()
    return client

nlp_client = create_nlp_client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    global content
    text_data = request.form.get('text')
    file_data = request.files.get('file')
    summary_length = request.form.get('summary_length', type=int)

    if file_data:
        content = file_data.read().decode('utf-8')
    elif text_data:
        content = text_data
    else:
        return jsonify({'summary': '没有提供内容。'})


    content = content.replace('\n', '').replace('\r', '')
    original_length = len(content)
    length_limit = float(summary_length / original_length if original_length > 0 else 0)
    print(content)
    print(length_limit)

    # 使用华为云NLP服务生成总结
    try:
        summary_request = RunSummaryDomainRequest()
        summary_request.body = SummaryDomainReq(
            content=content,
            length_limit=length_limit,  # 或者根据需求调整
            lang="zh"  # 或根据实际情况调整
        )
        response = nlp_client.run_summary_domain(summary_request)
        summary = response.summary
    except exceptions.ClientRequestException as e:
        return jsonify({'error': e.error_msg}), e.status_code

    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
