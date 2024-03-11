from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor, as_completed
from common import log, text
from models.endpoint import Endpoint
from protocols.http.method import HttpMethod
from protocols.http import interface as HttpInterface
from scan.dynamic.recon.scanner import Scanner

class HttpScanner(Scanner):

    def __init__(self, thread_cnt, blacklist=[404]):
        super().__init__(thread_cnt=thread_cnt)
        self.blacklist = blacklist

    def bruteforceDir(self, url, wordlist, methods=[HttpMethod.GET], headers=[]):
        log.info(f"Directory Brutoforce : {url}")
        self.init_result()
        url = text.stripUrl(url)
        total = len(wordlist) * len(methods)
        executor = ThreadPoolExecutor(max_workers=self.thread_cnt)
        threads = []
        for word in wordlist:
            self.result[word] = {}
            for method in methods:
                future = executor.submit(self.thread_request, url, word, method)
                threads.append(future)
        for t in as_completed(threads):
            print(f"{self.request_cnt} / {total}", end="\r")

        return self.result

    def thread_request(self, url, word, method, headers=[]):
        target = url + word
        r = HttpInterface.request(method, target, headers=headers)
        self.request_cnt += 1
        if r.status not in self.blacklist:
            self.result[word][method] = r
            self.success_cnt += 1
            log.success(f"{method.value} /{word} {r.status}")
            

    def enumerateEndpoint(self, url, headers=[]):
        log.info(f"Endpoint Enumeration : {url}")
        self.init_result()
        origin = text.getOrigin(url)
        r = HttpInterface.get(url, headers=headers)
        soup = bs(r.body, features='html.parser')
        # a
        links = soup.find_all("a")
        for link in links:
            href = link["href"]
            target_origin = text.getOrigin(href)
            if target_origin is not None and origin != target_origin:
                continue

            target = text.getPath(href)
            params = text.getParams(href)
            endpoint = Endpoint(target, HttpMethod.GET, params)
            if target not in self.result:
                self.result[target] = []
            self.result[target].append(endpoint)
            params_str = params if len(params) > 0 else ""
            log.success(f"{HttpMethod.GET.value} {target} {params_str}")
        # form
        forms = soup.find_all("form")
        for form in forms:
            target = text.getPath(url)
            method = "GET"
            action = form.get('action')
            if action is not None:    
                target = text.getPath(action)
            form_method = form.get('method')
            if form_method is not None:
                method = form_method.upper()
            inputs = form.find_all('input')
            params = {}
            for i in inputs:
                name = i.get("name")
                if name is not None:
                    params[name] = ""
            selects = form.find_all('select')
            for i in selects:
                name = i.get("name")
                if name is not None:
                    params[name] = ""
            params_str = params if len(params) > 0 else ""
            log.success(f"{method} {target} {params_str}")
        # iframe
        # script
        # style
        return self.result




        




