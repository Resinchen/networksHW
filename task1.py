import argparse
import re
import socket
import time
from subprocess import Popen, PIPE


def parser_args():
    parser = argparse.ArgumentParser(description="traceAS")
    parser.add_argument('host', type=str, help='Хост')
    return parser.parse_args()


def whois(whois_server, ip_addr):
    sock = socket.socket()
    sock.connect((whois_server, 43))
    sock.send("{}\r\n".format(ip_addr).encode())
    time.sleep(2)
    data = sock.recv(4096).decode()
    sock.close()
    return data


def get_whois_server(ip_addr):
    info = whois('whois.arin.net', ip_addr)
    if info.find("ReferralServer:") != -1:
        whois_serv = info.split("ReferralServer:")[1].split("\n")[0].replace(" ", "")

        if whois_serv.find("ripe") != -1:
            return 'whois.ripe.net'
        elif whois_serv.find("apnic") != -1:
            return 'whois.apnic.net'
        elif whois_serv.find("lacnic") != -1:
            return 'whois.lacnic.net'
    else:
        return 'whois.arin.net'


def work_whois(ip_addr):
    whois_server = get_whois_server(ip_addr)
    info = whois(whois_server, ip_addr).lower()
    autosys = info.split("origin")[1].split("\n")[0].replace(" ", "").replace(":", "") if info.find(
        "origin") != -1 else None
    country = info.split("country")[1].split("\n")[0].replace(" ", "").replace(":", "") if info.find(
        "country") != -1 else None
    provider = info.split("mnt-by:")[1].split("\n")[0].replace(" ", "").replace(":", "") if info.find(
        "mnt-by:") != -1 else None

    return autosys, country, provider


def tracert(ip_addr):
    list_routers = []
    p = Popen(['tracert', ip_addr], stdout=PIPE)
    while True:
        line = p.stdout.readline()
        list_routers.append(line.decode('utf-8', 'replace'))
        if not line:
            break
    return list_routers


def is_White_IP(ip):
    if ip.find('192.168.') == 0:
        return False
    if ip.find('10.') == 0:
        return False
    ip_list = ip.split('.')
    if ip_list[0] == '172' and 16 <= int(ip_list[1]) <= 31:
        return False
    return True


def work_traced(ip_addr):
    list_routing = tracert(ip_addr)
    g = ""
    for i in list_routing:
        g += i

    x = re.findall(r"\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}", g)[1:]
    x = [e for e in x if is_White_IP(e)]
    return x


def presented(list_with_info):
    for i in list_with_info:
        print(i)


class InfoNote:
    def __init__(self, num, ip, autosys, country, provider):
        self.provider = provider
        self.country = country
        self.autosys = autosys
        self.ip = ip
        self.num = num

    def __str__(self):
        return "{} | {} | {} | {} | {}".format(self.num, self.ip, self.autosys, self.country, self.provider)


def main_work():
    args = parser_args()
    ip_addr = args.host
    list_info = []
    routing_list = work_traced(ip_addr)
    for i in range(len(routing_list)):
        info = work_whois(routing_list[i])
        if info is (None, None, None):
            list_info.append("Info not found")
        else:
            list_info.append(InfoNote(i, routing_list[i], info[0], info[1], info[2]))
    return list_info


if __name__ == '__main__':
    list_infos = main_work()
    presented(list_infos)
