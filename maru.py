import argparse
from common import config, io, text
from protocols.http.method import HttpMethod
from scan.dynamic.recon.dns_scanner import DnsScanner 
from scan.dynamic.recon.http_scanner import HttpScanner 
from scan.dynamic.recon.xss_scanner import XssScanner 
from report import markdown

def main():
    parser = argparse.ArgumentParser(
        prog="Maru",
        description="Auto recon"
    )
    parser.add_argument('action')
    parser.add_argument('target')
    parser.add_argument('-p', '--param')
    parser.add_argument('-t', '--thread', default=3)
    args = parser.parse_args()

    action = args.action
    target = args.target
    param = args.param
    thread = args.thread

    headers = {
        "User-Agent": "maru",
        # "X-HackerOne-Research": "<hackerone>"
    }

    domain = text.getDomain(target)
    domains = [domain]
    report_dir = config.DIR_REPORT + "/" + domain
    io.mkdir(report_dir)
    if action == "all" or action == "subdomain":
        subdomain_list = config.DIR_WORDLIST + "/subdomain.txt"
        subdomain_result = subdomain(domain, subdomain_list, thread_cnt=thread)
        for sub in subdomain_result:
            response = subdomain_result[sub]
            domains.append(response.domain)
        markdown.subdomain_report(report_dir + "/subdomain.md", subdomain_result)
    
    sites = []
    if action == "all" or action == "dir":
        directory_list = config.DIR_WORDLIST + "/directory.txt"
        for domain in domains:
            subdomain_dir = report_dir + "/" + domain
            io.mkdir(subdomain_dir)
            url = "https://" + domain
            dir_result = dir(url, directory_list, thread_cnt=thread, headers=headers)
            for word in dir_result:
                if HttpMethod.GET.value not in dir_result[word]:
                    continue
                if dir_result[word]["GET"].status == 200:
                    dir_url = url + "/" + word
                    r = { 
                        "url" : dir_url,
                        "domain": domain,
                        "path": word,
                        "result": dir_result[word]
                    }
                    sites.append(r)
            markdown.dir_report(subdomain_dir + "/dir.md", dir_result)

    pages = []
    if action == "all" or action == "endpoint":
        cnt = 0
        for site in sites:
            endpoint_dir = report_dir + "/" + site["domain"] + "/endpoints"
            io.mkdir(endpoint_dir)
            endpoint_result = endpoint(site["url"], headers=headers)
            markdown.endpoint_report(endpoint_dir + f"/{cnt}.md", endpoint_result)
            cnt += 1
    if action == "all" or action == "xss":
        rxss(target, param)
            
            

    
def subdomain(domain, file=None, thread_cnt=config.MAX_THREADS):
    dns = DnsScanner(thread_cnt=thread_cnt)
    wordlist = io.readLines(file)
    result = dns.bruteforceSubdomain(domain, wordlist)
    return result

def dir(url, file=None, methods=config.HTTP_METHODS, blacklist=config.HTTP_BLACKLIST, thread_cnt=config.MAX_THREADS, headers={}):
    http = HttpScanner(thread_cnt=thread_cnt, blacklist=blacklist)
    wordlist = io.readLines(file)
    result = http.bruteforceDir(url, wordlist, methods, headers)
    return result

def endpoint(url, blacklist=config.HTTP_BLACKLIST, thread_cnt=config.MAX_THREADS, headers={}):
    http = HttpScanner(thread_cnt=thread_cnt, blacklist=blacklist)
    result = http.enumerateEndpoint(url, headers)
    return result

def rxss(url, target, params={}, thread_cnt=config.MAX_THREADS):
    xss = XssScanner(thread_cnt=thread_cnt)
    result = xss.checkReflectedXss(url, target, params)


if __name__ == "__main__":
    main()