import json
import logging
import http.client
import requests

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

logger = logging.getLogger('log')


def index(request, _):
    """
    路由请求
     `` request `` 请求对象
    """

    if request.method == 'GET' or request.method == 'get':
        return index_page(request)
    elif request.method == 'POST' or request.method == 'post':
        return send_wxmsg(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                           json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return render(request, 'index.html')


def send_wxmsg(request):
    """
    发送微信消息
     `` request `` 请求对象
    """

    # 1 检查x-wx-openid参数
    if 'HTTP_X_WX_OPENID' not in request.META:
        return 'error'

    # 2 检查req body参数
    if request.body is None:
        return 'error'

    # 3 组装请求微信参数
    wx_openid = request.META['HTTP_X_WX_OPENID']
    req_body = json.loads(request.body.decode('utf-8'))
    data = {
        'touser': wx_openid,
        'msgtype': 'text',
        'text': {
            'content': '云托管接收消息推送成功，内容如下：{}'.format(req_body)
        }
    }
    json_data = json.dumps(data, ensure_ascii=False).encode('UTF-8')
    wx_api_url = 'http://api.weixin.qq.com/cgi-bin/message/custom/send'
    response = requests.post(url=wx_api_url, data=json_data)
    print(response)
    logger.info(response)

    return HttpResponse("success", content_type="text/plain")


def index_page(request):
    """
    获取主页
    `` request `` 请求对象
    """
    return render(request, 'index.html')
