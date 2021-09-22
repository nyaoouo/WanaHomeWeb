from django.http import JsonResponse


def client_error(msg="client error occurred", code=499, status=400, **other_args):
    data = {'code': code, "msg": msg, **other_args}
    return JsonResponse(data, status=status)


def server_error(msg="server error occurred", code=599, status=500, **other_args):
    data = {'code': code, "msg": msg, **other_args}
    return JsonResponse(data, status=status)


def success(msg='success', **other_args):
    data = {'code': 200, "msg": msg, **other_args}
    return JsonResponse(data)


def request_method_error(required_method: str = None):
    return client_error(f'Invalid request method, {required_method} is required' if required_method is not None else 'Invalid request method')


def api_not_exists(request):
    return client_error(
        f"api {request.get_full_path()} is not exist",
        code=404, status=404
    )


def param_input_error(msg='parameter given is invalid'):
    return client_error(msg)


def require_captcha(captcha_type: str, captcha_public_key: str):
    return client_error("require captcha", code=403, status=403, type=captcha_type, key=captcha_public_key)
