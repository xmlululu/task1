from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdknlp.v2.region.nlp_region import NlpRegion
from huaweicloudsdkcore.exceptions import exceptions
# from huaweicloudsdknlp.v2 import *
from huaweicloudsdknlp.v2.model.summary_req import SummaryReq
from huaweicloudsdknlp.v2.model.run_summary_request import RunSummaryRequest
from huaweicloudsdknlp.v2 import NlpClient


# user specific information
ak = "ORAEUEXV4RREC1ZFPEPN"  # access key
sk = "nUVOhC9fBe85rtfpiX3fyODtgRAEBlfpfxCqafiE"  # secret key
region = "cn-north-4"


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
