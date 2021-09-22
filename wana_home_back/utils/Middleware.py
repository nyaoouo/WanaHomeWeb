import json
import zlib

from django.http import QueryDict

from utils import Returns


class AjajPostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and 'application/json' in request.headers['Content-Type']:
            data = request.body
            if 'zlib' in request.headers:
                try:
                    data = zlib.decompress(data)
                except Exception as e:
                    pass
            request.POST = QueryDict('', mutable=True)
            try:
                request.POST.update(json.loads(data))
            except Exception:
                return Returns.param_input_error("json load failed")
        return self.get_response(request)
