import requests
from common import log
from protocols.http.method import HttpMethod
from protocols.http.response import HttpResponse


def request(method, url, params=None, data=None, headers=None) -> HttpResponse:
    try:
        if method == HttpMethod.GET:
            r = requests.get(url, params=params, data=data, headers=headers)
        elif method == HttpMethod.HEAD:
            r = requests.head(url, params=params, data=data, headers=headers)
        elif method == HttpMethod.POST:
            r = requests.post(url, params=params, data=data, headers=headers)
        elif method == HttpMethod.PUT:
            r = requests.put(url, params=params, data=data, headers=headers)
        elif method == HttpMethod.DELETE:
            r = requests.delete(url, params=params, data=data, headers=headers)
        elif method == HttpMethod.OPTIONS:
            r = requests.options(url, params=params, data=data, headers=headers)
        elif method == HttpMethod.PATCH:
            r = requests.patch(url, params=params, data=data, headers=headers)
        else:
            return None
    except requests.ConnectionError:
        return None
    except requests.ConnectTimeout:
        return None
    except requests.HTTPError:
        return None
    except requests.ReadTimeout:
        return None
    except requests.RequestException:
        return None
    
    result = HttpResponse(response=r)
    return result


def get(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.GET, url, params=params, data=data, headers=headers)
    return response

def head(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.HEAD, url, params=params, data=data, headers=headers)
    return response

def post(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.POST, url, params=params, data=data, headers=headers)
    return response

def put(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.PUT, url, params=params, data=data, headers=headers)
    return response

def delete(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.DELETE, url, params=params, data=data, headers=headers)
    return response

def options(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.OPTIONS, url, params=params, data=data, headers=headers)
    return response

def TRACE(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.TRACE, url, params=params, data=data, headers=headers)
    return response

def patch(url, params=[], data=[], headers=[]) -> HttpResponse:
    response = request(HttpMethod.PATCH, url, params=params, data=data, headers=headers)
    return response