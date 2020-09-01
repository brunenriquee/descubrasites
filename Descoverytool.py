import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import sys

colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED

internal_urls = set()
external_urls = set()

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    urls = set()

    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(url, max_urls=50):

    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

    total_urls_visited = 0

    print(f"{RED}AVISO !!!!! Requer o uso do http/https {RESET}")
    print("")
    crawl(input('Digite a url: '))

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

def sub_domain(host):

    texto = open("subdomains.txt", "r")
    content = texto.read()
    subdomains = content.splitlines()

    for subdomain in subdomains:

        url = "http://" + subdomain + "." + host
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered subdomain:", url)
    print("")
    print(f"{RED}[+] Sua Busca Terminou{RESET}")


menu = """"
        ------------MENU------------
        1 - External/Internal Link
        2 - Sub Domain
"""

#startprogram
while True:
    print(menu)
    option = input(f"{GREEN}[!] Option: ")

    if option.isnumeric():
        if option == '3':
            print(f"{GREEN}[+] Exiting ... {RESET}")
            break

        elif option == '1':
            url = input(f"\n {GREEN}[$] Target url:{RESET}")
            host = get_all_website_links(url)

        elif option == '2':
            url = input(f"\n {GREEN}[$] Target url:{RESET}")
            host = sub_domain(url)
        else:
            print(f"{RED}\n [-] Option incorrect!{RESET}")

    else:
        print(f"{RED}\n [-] Option incorrect!{RESET}")

sys.exit()