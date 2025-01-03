REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'COERCE_DECIMAL_TO_STRING': True,
    'NON_FIELD_ERRORS_KEY': 'error',
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'STRING_IF_INVALID': '',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
    'NON_FIELD_ERRORS': ['错误'],
    'VALIDATOR_URL': None,
    'LANGUAGE_CODE': 'zh-hans',
}

REST_FRAMEWORK_ERROR_MESSAGES = {
    'not_authenticated': '身份认证信息未提供。',
    'invalid_token': '令牌无效或已过期。',
    'permission_denied': '您没有执行该操作的权限。',
    'not_found': '未找到。',
    'bad_request': '错误的请求。',
    'method_not_allowed': '不允许使用该方法。',
    'unsupported_media_type': '不支持的媒体类型。',
    'validation_error': '数据验证失败。',
    'parse_error': '无法解析请求数据。',
    'authentication_failed': '身份认证失败。',
    'throttled': '请求过于频繁，请稍后再试。'
}

LANGUAGE_CODE = 'zh-hans' 

# OAuth 配置
OAUTH_REDIRECT_URI = '/oauth' 