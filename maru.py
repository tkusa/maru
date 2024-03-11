import argparse
from common import config, io, text
from protocols.http.method import HttpMethod
from scan.dynamic.recon.dns_scanner import DnsScanner 
from scan.dynamic.recon.http_scanner import HttpScanner 

def main():
    parser = argparse.ArgumentParser(
        prog="Maru",
        description="Auto recon"
    )
    parser.add_argument('action')
    parser.add_argument('target')
    parser.add_argument('-t', '--thread', default=3)
    args = parser.parse_args()

    action = args.action
    target = args.target
    thread = args.thread
    
    if action == "all" or action == "subdomain":
        domain = text.getDomain(target)
        subdomain_list = config.DIR_WORDLIST + "/subdomain.txt"
        subdomain(domain, subdomain_list, thread_cnt=thread)
    if action == "all" or action == "dir":
        directory_list = config.DIR_WORDLIST + "/directory.txt"
        dir(target, directory_list, thread_cnt=thread)
    if action == "all" or action == "endpoint":
        endpoint(target)

    
def subdomain(domain, file=None, thread_cnt=config.MAX_THREADS):
    dns = DnsScanner(thread_cnt=thread_cnt)
    wordlist = io.readLines(file)
    result = dns.bruteforceSubdomain(domain, wordlist)
    return result

def dir(url, file=None, methods=config.HTTP_METHODS, blacklist=config.HTTP_BLACKLIST, thread_cnt=config.MAX_THREADS):
    http = HttpScanner(thread_cnt=thread_cnt, blacklist=blacklist)
    wordlist = io.readLines(file)
    result = http.bruteforceDir(url, wordlist, methods)
    return result

def endpoint(url, blacklist=config.HTTP_BLACKLIST, thread_cnt=config.MAX_THREADS):
    http = HttpScanner(thread_cnt=thread_cnt, blacklist=blacklist)
    result = http.enumerateEndpoint(url)
    return result

if __name__ == "__main__":
    main()