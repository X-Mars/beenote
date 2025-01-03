from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import NotFound

def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理
    response = exception_handler(exc, context)
    
    # 如果是404错误，自定义错误消息
    if isinstance(exc, (Http404, ObjectDoesNotExist, NotFound)):
        response.data = {'detail': '未找到该笔记'}
    
    return response 