import argparse
from json import loads
from os import name, system
from requests import get
from time import sleep, time
from socket import *
from time import sleep
from colorama import Fore
from nmap3 import Nmap

startTime = time()

parser = argparse.ArgumentParser(description='A Tool For Find & Scan SubDomains')
parser.add_argument("--domain", help="Domain to scan")
parser.add_argument("--top_ports", help="Scan Top ports", action='store_true')

args = parser.parse_args()

res_check_subdomain = []


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def baner():
    clear()
    print("""                                                                        
  _____       _     ______ _           _           
 / ____|     | |   |  ____(_)         | |          
| (___  _   _| |__ | |__   _ _ __   __| | ___ _ __ 
 \___ \| | | | '_ \|  __| | | '_ \ / _` |/ _ \ '__|
 ____) | |_| | |_) | |    | | | | | (_| |  __/ |   
|_____/ \__,_|_.__/|_|    |_|_| |_|\__,_|\___|_|   

                                    | @Mr_Hax0r |  
                                    

""")
    sleep(2)


def fiend_ip(domain):
    sleep(2)
    try:
        return gethostbyname(domain)
    except:
        return 'Unknown !'



def finder_subdomain(domain):
    request = get("https://crt.sh/?q={}&output=json".format(domain))
    res_json = loads(request.text)

    list_res = []

    for num in range(0, len(res_json)):
        res_res = res_json[num]['name_value'].splitlines()

        for number in range(0, len(res_res)):
            if '*' not in res_res[number]:

                list_res.append(res_res[number])
                res = []
                for i in list_res:
                    if i not in res:
                        res.append(i)
                response_crt = []
                for i in res:
                    if i[:4] == 'www.':
                        pass
                    else:
                        response_crt.append(i)

    return response_crt


def check_subdomain(subdomains: list):
    print(Fore.WHITE + "\n====================================================")
    print(Fore.WHITE + "     Check Subdomains                                |")
    print(Fore.WHITE + "====================================================\n")
    print(Fore.WHITE + 'It is working, wait ....\n')
    for subdomain in subdomains:
        try:
            re = get('http://{}'.format(subdomain), timeout=4)

            if re.status_code == 200:

                print(Fore.GREEN + '[+]  [ {} ] --->  [ {} ] ---> [ {} ]'.format(subdomain, re.status_code,
                                                                                 fiend_ip(subdomain)))
                res_check_subdomain.append(subdomain)

            else:

                print(Fore.RED + '[-]  [ {} ] --->  [ {} ] ---> [ {} ]'.format(subdomain, re.status_code,
                                                                               fiend_ip(subdomain)))
        except:
            print(Fore.RED + '[-] [ {} ]  --->  [ Unknown ! ] ---> [ {} ]'.format(subdomain, fiend_ip(subdomain)))

    return res_check_subdomain


def scan_top_ports(domains):
    nmap = Nmap()
    print(Fore.WHITE + "\n====================================================")
    print(Fore.WHITE + "     Scna top ports                                 |")
    print(Fore.WHITE + "====================================================\n")
    print(Fore.WHITE + 'It is working, wait ....\n')
    print('-' * 47)
    try:
        for domain in domains:
            results = nmap.scan_top_ports(domain)
            for res in results[list(results)[0]]['ports']:
                print(Fore.WHITE + "[*] [ {} ]  {}-{} --- >  {} ".format(domain, res['portid'], res['protocol'], res['state']))
            print('-' * 47)
    except:
        print('eroor')



def main():
    baner()
    if args.domain:
        check_subdomain(finder_subdomain(args.domain))
        if args.top_ports:

            scan_top_ports(domains=finder_subdomain(args.domain))
    else:
        parser.print_help()

    print(Fore.WHITE + "\n====================================================")
    print(Fore.WHITE + "        Time taken  : {}            ".format(time() - startTime))
    print(Fore.WHITE + "====================================================\n")


if __name__ == "__main__":
    main()
