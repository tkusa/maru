from enum import Enum

class HttpMethod(Enum):
    GET = 'GET'
    HEAD = 'HEAD'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    PATCH = 'PATCH'

    def fromStr(self, method: str):
        method = method.upper()
        if method == HttpMethod.GET.value:
            return HttpMethod.GET
        elif method == HttpMethod.POST.value:
            return HttpMethod.POST
        elif method == HttpMethod.PUT.value:
            return HttpMethod.PUT
        elif method == HttpMethod.DELETE.value:
            return HttpMethod.DELETE
        elif method == HttpMethod.CONNECT.value:
            return HttpMethod.CONNECT
        elif method == HttpMethod.OPTIONS.value:
            return HttpMethod.OPTIONS
        elif method == HttpMethod.TRACE.value:
            return HttpMethod.TRACE
        elif method == HttpMethod.PATCH.value:
            return HttpMethod.PATCH
        else:
            return None

