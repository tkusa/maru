from concurrent.futures import ThreadPoolExecutor, as_completed
from common import log
from protocols.dns import interface as DnsInterface
from protocols.dns.domain import Domain
from scan.dynamic.recon.scanner import Scanner

class DnsScanner(Scanner):

    def bruteforceSubdomain(self, domain, wordlist):
        log.info(f"Subdomain Butoforce : {domain}")
        self.init_result()
        total = len(wordlist)
        executor = ThreadPoolExecutor(max_workers=self.thread_cnt)
        threads = []
        for word in wordlist:
            future = executor.submit(self.thread_request, domain, word)
            threads.append(future)
        for t in as_completed(threads):
            print(f"{self.request_cnt} / {total}", end="\r")
        return self.result
    
    def thread_request(self, domain, word):
        query = word + "." + domain
        answer = DnsInterface.requestA(query)
        self.request_cnt += 1
        if len(answer) != 0:
            response = Domain(query)
            response.ip = answer
            self.result[word] = response
            self.success_cnt += 1
            log.success(f"{query}")
    
    