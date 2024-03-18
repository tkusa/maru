import html
from common import config, log, text
from scan.dynamic.recon.scanner import Scanner
from protocols.http import interface as HttpInterface

class XssScanner(Scanner):

    def checkReflection(self, key, response):
        if key not in response.body:
            return False
        return True

    def checkEscape(self, key, response):
        escaped = html.escape(key)
        if escaped not in response.body:
            return False
        return True

    def checkRemoval(self, key, response):
        pass

    def checkReflectedXss(self, url, target, params={}):
        log.info(f"Reflected XSS Check : {url} {target}")
        key = text.randomAscii()
        symbols = ['"', "'", "<", ">"]
        params[target] = key 
        r = HttpInterface.get(url, params)
        reflected = self.checkReflection(key, r)
        
        if not reflected:
            log.info(f"No reflection")
            return False
        not_escaped = []
        for symbol in symbols:
            key = text.randomAscii()
            params[target] = key + symbol
            r = HttpInterface.get(url, params)
            escaped = self.checkEscape(key + symbol, r)
            if not escaped:
                not_escaped.append(symbol)
        if len(not_escaped) == 0:
            return False
        
        log.success(f"Reflected XSS detected!")
        log.success(f"Not escaped: {' '.join(not_escaped)}")
        return True