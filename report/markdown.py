from common import config, io

def subdomain_report(path, result):
    report = "# Subdomains" + config.LF + config.LF
    for word in result:
        domain = result[word]
        report += domain.domain + config.LF
    io.write(path, report.encode())

def dir_report(path, result):
    report = "# Directories" + config.LF + config.LF
    for word in result:
        dir = result[word]
        for method in dir:
            response = dir[method]
            report += f"{method} /{word} {response.status}" + config.LF
    io.write(path, report.encode())

def endpoint_report(path, result):
    report = "# Endpoints" + config.LF + config.LF
    for word in result:
        endpoint = result[word]
        params_str = endpoint.params if len(endpoint.params) > 0 else ""
        report += f"{endpoint.method} {endpoint.uri} {params_str}"
    io.write(path, report.encode())
