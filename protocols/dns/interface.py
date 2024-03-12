import dns.resolver
import dns.rdatatype
import dns.reversename
import dns.zone
import dns.query
import time
from common import config

def requestRecord(domain, type):
    result = []
    try:
        answer = dns.resolver.resolve(domain, type)
    except dns.resolver.NoAnswer:
        return result
    except dns.resolver.NXDOMAIN:
        return result
    except dns.resolver.NoNameservers:
        return result
    except dns.resolver.LifetimeTimeout:
        return result
    for rdata in answer:
        result.append(rdata.to_text())
    time.sleep(config.MIN_WAIT)
    return result


def requestA(domain):
    result = requestRecord(domain, dns.rdatatype.A)
    return result


def requestAAAA(domain):
    result = requestRecord(domain, dns.rdatatype.AAAA)
    return result


def requestCNAME(domain):
    result = requestRecord(domain, dns.rdatatype.CNAME)
    return result


def requestMX(domain):
    result = requestRecord(domain, dns.rdatatype.MX)
    return result


def requestNS(domain):
    result = requestRecord(domain, dns.rdatatype.NS)
    return result


def requestTXT(domain):
    result = requestRecord(domain, dns.rdatatype.TXT)
    return result


def requestPTR(ip):
    query = dns.reversename.from_address(ip)
    result = requestRecord(query, dns.rdatatype.PTR)
    return result


def requestSOA(domain):
    result = requestRecord(domain, dns.rdatatype.SOA)
    return result


def requestAXFR(domain, ns):
    result = []
    ns_ip = requestA(ns)
    try:
        for ip in ns_ip:
            query = dns.query.xfr(ip, domain, lifetime=15)
            zone = dns.zone.from_xfr(query)
            result.append(zone.to_text())
    except dns.zone.NoNS:
        return result
    return result