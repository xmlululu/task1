from flask import Flask, request, jsonify, render_template
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdknlp.v2.region.nlp_region import NlpRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdknlp.v2 import *
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.webdriver.support.wait import WebDriverWait

import api

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

#首页面
@app.route('/')
def index():
    return render_template('index.html')
#处理文本的页面
@app.route('/txt')
def txt():
    return render_template('text_summarizer.html')

#处理音频的页面
@app.route('/audio', methods=['GET'])
def audioPage():
    return render_template('audio_summarizer.html')

#进行文本处理的代码
@app.route('/summarize', methods=['POST'])
def summarize():
    global content
    url_data = request.form.get('url')
    text_data = request.form.get('text')
    file_data = request.files.get('file')
    summary_length = request.form.get('summary_length', type=int)

    content=""

    if url_data:
        # 使用爬虫获取网页内容
        edge_options = Options()
        edge_options.add_argument('--headless')
        edge_options.add_argument('--disable-gpu')
        driver = webdriver.Edge(options=edge_options)
        driver.get(url_data)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            content = driver.find_element(By.XPATH, '//*[@class="article"]').text
        except TimeoutException:
            return jsonify({'error': '加载页面元素超时'})
        finally:
            driver.quit()
    elif file_data:
        content = file_data.read().decode('utf-8')
    elif text_data:
        content = text_data

    print(url_data)
    print(content)

    if not content:
        return jsonify({'summary': '没有提供内容。'})


    content = content.replace('\n', '').replace('\r', '').replace('\t', '').replace('\s+', '').replace('\s', '')
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

@app.route('/summarize_audio', methods=['POST'])
def summarizeAudioRoute():
    # 获取表单数据
    file = request.files.get('file')

    summary_length = request.form.get('summary_length', type=int) or 10

    if file:
        # 处理上传的文件
        file.save(file.filename)
    else:
        return jsonify({'summary': '没有提供内容。'})

    # 在这里添加你的文本总结逻辑
    content = api.audio2Text('./' + file.filename)
    print(content)
    content = content.replace('\n', '').replace('\r', '').replace('\t', '').replace('\s+', '').replace('\s', '')
    original_length = len(content)

    length_limit = float(summary_length / original_length if original_length > 0 else 0)

    summary = api.summarizeText('', content, length_limit=length_limit)

    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run(debug=True)
