from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from website import models
from website.datebase import API


class Authtication(BaseAuthentication):
    def authenticate(self, request):  # 如果执行到最后一个还是没有给user赋值，则会返回一个匿名用户
        method = request._request.method
        token = request.data['token']
        obj = models.WebsiteUserinfo.objects.filter(token=token).first()
        if not token or not obj:
            raise exceptions.AuthenticationFailed({'code': 1, 'message': '用户认证失败！', 'data': {}})
        # auth = {}.fromkeys([n.url for n in models.WebsiteAuth.objects.all()], False)
        # 获取用户权限
        auth = []
        for i in API().get_user_url(obj.username):
            auth.append('/oa/'+i)
            # auth[i] = True

        auth.append('/oa/customerstatistics')
        auth.append('/oa/tranrecord')
        auth.append('/oa/tranrecord1')
        auth.append('/oa/tranmonery')
        now_request_path = "/".join(request._request.path.split('/')[:3])
        if now_request_path not in auth:
            raise exceptions.AuthenticationFailed({'code': 1, 'message': '无权访问！', 'data': {}})
        return obj.username, auth

