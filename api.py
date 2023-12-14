from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdknlp.v2.region.nlp_region import NlpRegion
from huaweicloudsdkcore.exceptions import exceptions
# from huaweicloudsdknlp.v2 import *
from huaweicloudsdknlp.v2.model.summary_req import SummaryReq
from huaweicloudsdknlp.v2.model.run_summary_request import RunSummaryRequest
from huaweicloudsdknlp.v2 import NlpClient
from huaweicloud_sis.client.asr_client import AsrCustomizationClient
from huaweicloud_sis.bean.asr_request import AsrCustomLongRequest
from huaweicloud_sis.exception.exceptions import ClientException
from huaweicloud_sis.exception.exceptions import ServerException
from huaweicloud_sis.bean.sis_config import SisConfig
import time
from obs import ObsClient
from obs import PutObjectHeader
import os
import traceback


# user specific information
ak = "ORAEUEXV4RREC1ZFPEPN"  # access key
sk = "nUVOhC9fBe85rtfpiX3fyODtgRAEBlfpfxCqafiE"  # secret key
region = "cn-north-4"
#  server填写Bucket对应的Endpoint, 这里以华北-北京四为例，其他地区请按实际情况填写。
obs_server = "https://obs.cn-north-4.myhuaweicloud.com"
obs_bucket_name = "aeba"


def summarizeText(title, content, length_limit=100, lang='zh'):
    credentials = BasicCredentials(ak, sk) \

    client = NlpClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(NlpRegion.value_of(region)) \
        .build()

    try:
        request = RunSummaryRequest()
        request.body = SummaryReq(
            title=title,
            length_limit=length_limit,
            lang=lang,
            content=content
        )
        response = client.run_summary(request)  # type:ignore
        # print(type(response))
        return response.to_dict().get('summary')
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)
        raise e


def uploadFileToOBS(file_path, content_type):
    # 创建obsClient实例
    obsClient = ObsClient(
        access_key_id=ak,
        secret_access_key=sk,
        server=obs_server
    )

    try:
        # 上传对象的附加头域
        headers = PutObjectHeader()

        # 【可选】待上传对象的MIME类型
        headers.contentType = content_type

        # 对象名，即上传后的文件名
        objectKey = f"{int(time.time())}_{os.path.basename(file_path)}"

        # 上传文件的自定义元数据
        # metadata = {'meta1': 'value1', 'meta2': 'value2'}

        # 文件上传
        resp = obsClient.putFile(
            obs_bucket_name, objectKey, file_path, headers
        )

        # 返回码为2xx时，接口调用成功，否则接口调用失败
        if resp.status < 300:  # type:ignore
            print('Put File Succeeded')
            # print('requestId:', resp.requestId)  # type:ignore
            # print('etag:', resp.body.etag)  # type:ignore
            # print('versionId:', resp.body.versionId)  # type:ignore
            # print('storageClass:', resp.body.storageClass)  # type:ignore
            return objectKey
        else:
            print('Put File Failed')
            # print('requestId:', resp.requestId)  # type:ignore
            # print('errorCode:', resp.errorCode)  # type:ignore
            # print('errorMessage:', resp.errorMessage)  # type:ignore
    except Exception as e:
        print('Put File Failed')
        print(traceback.format_exc())
        raise e


def audio2Text(file_path, audio_format='audio/mpeg'):
    try:
        obj_name = uploadFileToOBS(file_path, audio_format)

        project_id = "65eec9da151845e39b812dbaa59ffa43"
        obs_url = f"https://aeba.obs.cn-north-4.myhuaweicloud.com/{obj_name}"
        obs_audio_format = 'auto'
        # obs_property = 'chinese_8k_general'
        obs_property = 'chinese_8k_common'

        # step1 初始化客户端
        config = SisConfig()

        config.set_connect_timeout(10)       # 设置连接超时
        config.set_read_timeout(10)         # 设置读取超时

        asr_client = AsrCustomizationClient(
            ak, sk, region,
            project_id, sis_config=config
        )

        # step2 构造请求
        asrc_request = AsrCustomLongRequest(
            obs_audio_format, obs_property, obs_url
        )

        # 所有参数均可不设置，使用默认值
        # 设置是否添加标点，yes or no，默认no
        asrc_request.set_add_punc('yes')

        # 设置是否将语音中数字转写为阿拉伯数字，yes or no，默认yes
        asrc_request.set_digit_norm('yes')

        # 设置 是否需要分析信息，True or False, 默认False。
        # 只有need_analysis_info生效，diarization、channel、emotion、speed才会生效
        # 目前仅支持8k模型，详见api文档
        asrc_request.set_need_analysis_info(False)

        # 设置是否需要话者分离，默认True，需要need_analysis_info设置为True才生效。
        asrc_request.set_diarization(False)

        # 设置声道信息, 一般都是单声道，默认为MONO，需要need_analysis_info设置为True才生效
        asrc_request.set_channel('MONO')

        # 设置是否返回感情信息, 默认True，需要need_analysis_info设置为True才生效。
        asrc_request.set_emotion(True)

        # 设置是否需要返回语速信息，默认True，需要need_analysis_info设置为True才生效。
        asrc_request.set_speed(True)

        asrc_request.set_need_word_info('no')

        # step3 发送请求，获取job_id
        job_id = asr_client.submit_job(asrc_request)

        # step4 根据job_id轮询，获取结果。
        status = 'WAITING'
        count = 0   # 每2s查询一次，尝试2000次，即4000s。如果音频很长，可适当考虑加长一些。
        while status != 'FINISHED' and count < 2000:
            print(count, ' query')
            result = asr_client.get_long_response(job_id)  # type:ignore
            status = result.get('status')  # type:ignore
            if status == 'ERROR':
                # print('录音文件识别执行失败, %s' % json.dump(result))
                print(result)  # type:ignore
                break
            time.sleep(2)
            count += 1
        if status != 'FINISHED':
            print('录音文件识别未在 %d 内获取结果，job_id 为%s' % (count, job_id))
        # result为json格式
        # print(type(result))  # type:ignore
        segments = result.get("segments")  # type:ignore
        if len(segments) > 0:
            return segments[0].get("result").get("text")
        # print(json.dumps(result, indent=2, ensure_ascii=False))
    except ClientException as e:
        print(e)
    except ServerException as e:
        print(e)


def summarizeAudio(file_path):
    text = audio2Text(file_path)
    return summarizeText('', text)
