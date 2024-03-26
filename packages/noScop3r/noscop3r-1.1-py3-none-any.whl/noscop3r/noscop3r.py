#! /usr/bin/env python3

import re
import socket
import sys
from netaddr import IPNetwork
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize Colorama

def resolve_domain(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return {"IP":ip_address, "URL":domain_name2}
    except:
        try:
            domain_name2 = "www." + domain_name
            ip_address = socket.gethostbyname(domain_name2)
            return {"IP":ip_address, "URL":domain_name}
        except Exception as e:
            return None


def sanitise_url(url):
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    url = url.split(':')[0].split('/')[0].split('#')[0].split('?')[0]
    return url



def process_ip(ip):
    try:
        return [{"IP": str(ip_address)} for ip_address in IPNetwork(ip)]
    except Exception as e:
        print(f"Error with line -> {ip}")
        return []



def generate_table(data_list, red_ips):
    from tabulate import tabulate

    table_data = []
    for count, entry in enumerate(data_list, start=1):
        ip = entry.get('IP', '')
        url = entry.get('URL', '')

        # Color the IP red if it's in the red_ips set
        if ip in red_ips:
            ip = f"{Fore.RED}{ip}{Style.RESET_ALL}"

        table_data.append([count, ip, url])

    return tabulate(table_data, headers=['Count', 'IP', 'URL(s)'], tablefmt="grid")



def process_file(file_path):
    ip_pattern = re.compile(r'^(\d{1,3}\.){1,3}\d{1,3}$')
    ip_pattern2 = re.compile(r'^(\d{1,3}\.){1,3}\d{1,3}/\d{1,2}$')
    ip_dict = {}  # Dictionary to hold IPs and their URLs
    seen_IPs = set()  # Set to track seen IPs
    red_ips = set()  # Set to track IPs to be colored red
    numOfDupes = 0

    try:
        with open(file_path, "r") as file:
            lines = file.read().split('\n')
            for line in lines:
                line = line.strip()
                if re.match(ip_pattern2, line):
                    items = process_ip(line)
                    for item in items:
                        ip = item["IP"]
                        print (ip)
                        if ip not in seen_IPs:
                            ip_dict[ip] = {"IP": ip, "URL": ""}
                            seen_IPs.add(ip)
                elif re.match(ip_pattern, line):
                    if line in seen_IPs:
                        numOfDupes += 1
                        print("Duplicate IP", numOfDupes, ": ", line)
                    else:
                        ip_dict[line] = {"IP": line, "URL": ""}
                        seen_IPs.add(line)
                else:
                    address = sanitise_url(line)
                    sanitise_address = resolve_domain(address)
                    if sanitise_address is None:
                        print("\n\nInvalid URL -", f"{Fore.RED}{address}{Style.RESET_ALL}\n\n")
                    else:
                        ip = sanitise_address["IP"]
                        if ip not in seen_IPs:
                            red_ips.add(ip)
                        ip_dict.setdefault(ip, {"IP": ip, "URL": ""})
                        ip_dict[ip]["URL"] += sanitise_address["URL"] + '\n'

            IP_list = list(ip_dict.values())
            print(generate_table(IP_list, red_ips), "\n")
    except FileNotFoundError:
        print(f"File {file_path} not found. Please check the file path.")
    except Exception as e:
        print("An error occurred:", e)

            
    except FileNotFoundError:
        print(f"File {file_path} not found. Please check the file path.")

if __name__ == "__main__":
    print(r"""


        _   __     _____                     
       / | / /___ / ___/_________  ____  ___ 
      /  |/ / __ \\__ \/ ___/ __ \/ __ \/ _ \
     / /|  / /_/ /__/ / /__/ /_/ / /_/ /  __/
    /_/ |_/\____/____/\___/\____/ .___/\___/ 
                               /_/           

- by Jack Mason


""")
    if '-h' in sys.argv or len(sys.argv) != 2:
        print("\nUsage: python script.py [filename.txt]\n\nFunctions:\n- Expands IPs\n- Matches URLs to IPs\n- Displays Out-of-Scope URLs\n- Counts Total IPs\n\n")
    else:
        process_file(sys.argv[1])