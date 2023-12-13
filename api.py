# coding: utf-8
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdknlp.v2.region.nlp_region import NlpRegion
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdknlp.v2 import *

if __name__ == "__main__":
    # The AK and SK used for authentication are hard-coded or stored in plaintext, which has great security risks. It is recommended that the AK and SK be stored in ciphertext in configuration files or environment variables and decrypted during use to ensure security.
    # In this example, AK and SK are stored in environment variables for authentication. Before running this example, set environment variables CLOUD_SDK_AK and CLOUD_SDK_SK in the local environment
    ak = "ORAEUEXV4RREC1ZFPEPN"
    sk = "nUVOhC9fBe85rtfpiX3fyODtgRAEBlfpfxCqafiE"

    credentials = BasicCredentials(ak, sk) \

    client = NlpClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(NlpRegion.value_of("cn-north-4")) \
        .build()

    try:
        request = RunSummaryRequest()
        request.body = SummaryReq(
            title="华为“刀片式基站”获2018年度国家科学技术进步奖一等奖",
            length_limit=10000,
            lang="zh",
            content="华为刀片式基站解决方案是华为在深入理解客户诉求基础上,引领业界的创新解决方案。该方案采用统一的模块化设计,实现基站主要元素如射频、基带、电源、电池、微波、传输的刀片化,不同模块间的任意快速拼装组合无缝拼装,能灵活安装在抱杆,铁塔,墙面或者屋顶,“0”站址无需机房机柜,使基站的安装像拼装乐高积木一样简单便捷。刀片式基站同时支持2G/3G/4G等多制式,在多频多模网络发展策略下可以高效利用宝贵的站点资源,大幅降低站点获取难度和减少站点租金,帮助运营商应对移动网络快速增长的容量需求。同时刀片式基站采用自然散热,满足室外55°C高温环境,IP65防护等级,无需机房机柜和空调,其高能效和环境友好的特性,帮助运营商打造绿色移动网络。自2012年推出以来,刀片式基站全球累计已发货超1500万片,在全球超过170个国家310张运营商网络中成功商用部署。全球客户高度肯定了华为创新刀片式基站解决方案,它不但打破了传统机柜站点占地面积大、运维复杂的建站模式,而且还有效地提高了站点的部署效率,特别在密集城区、高铁场景下解决站点空间受限、实现快速部署、降低租赁成本等方面效果显著,同时也为乡村广覆盖场景提供最简单站点方案。在5G时代,华为围绕客户需求持续创新,在2018全球移动宽带论坛上,华为亦推出Super Blade Site——面向5G全室外站解决方案,其中包含最新支持5G容量要求的室外基带单元Blade BBU和有源天线一体化产品Blade AAU,该解决方案进一步匹配5G的最新技术要求和容量要求,极大降低5G引入对天面空间的需求,加速Massive MIMO部署,帮助运营商布局5G网络。华为Super Blade Site在2018全球移动宽带论坛上展出华为无线网络研发总裁郦舟剑表示,“华为一直致力于围绕客户需求持续创新,刀片式基站就是典型的例子。刀片式基站解决客户获取站址难题,帮助运营商快速建站,满足移动业务的迅猛增长的需求,也给客户带来商业成功。同时,面对即将到来的5G时代,华为持续创新,全室外刀片基站解决方案,将助力5G快速规模商用,帮助客户取得更大的商业成功。”国家科学技术进步奖,是国务院设立的国家科学技术奖5大奖项(国家最高科学技术奖、国家自然科学奖、国家技术发明奖、国家科学技术进步奖、国际科学技术合作奖)之一。该奖项授予在技术研究、技术开发、技术创新、推广应用先进科学技术成果、促进高新技术产业化,以及完成重大科学技术工程、计划等过程中做出创造性贡献的中国公民和组织。"
        )
        response = client.run_summary(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)