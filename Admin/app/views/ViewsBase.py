import json
import os
from app.utils.ZLMediaKit import ZLMediaKit
from app.utils.Analyzer import Analyzer
from app.utils.DjangoSql import DjangoSql
from django.http import HttpResponse
import time
from datetime import datetime

from framework.settings import ConfigObj

base_media = ZLMediaKit(mediaApiHost=ConfigObj.get("mediaApiHost"),
                        mediaHttpHost=ConfigObj.get("mediaHttpHost"),
                        mediaRtmpHost=ConfigObj.get("mediaRtmpHost"))
base_analyzer = Analyzer(ConfigObj.get("analyzerApiHost"))

base_djangoSql = DjangoSql()
base_behaviors = base_djangoSql.select("select * from av_behavior")

base_session_key_user = "user"

def getUser(request):
    user = request.session.get(base_session_key_user)
    # request.session.get("user") = {'id': 1, 'username': 'admin', 'email': '786251107@qq.com', 'last_login': '2022-06-03 22:33:21'}

    return user

def parse_get_params(request):

    params = {}
    for k in request.GET:
        params.__setitem__(k, request.GET.get(k))

    return params


def parse_post_params(request):

    params = {}
    for k in request.POST:
        params.__setitem__(k, request.POST.get(k))

    return params

def HttpResponseJson(res):

    def json_dumps_default(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError

    return HttpResponse(json.dumps(res, default=json_dumps_default), content_type="application/json")
