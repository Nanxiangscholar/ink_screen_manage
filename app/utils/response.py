def success_response(data=None, message='操作成功'):
    """成功响应"""
    return {
        'success': True,
        'data': data,
        'message': message
    }


def error_response(message='操作失败'):
    """错误响应"""
    return {
        'success': False,
        'data': None,
        'message': message
    }, 400
