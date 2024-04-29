import requests
import re
import subprocess

from os import environ, path
from dotenv import load_dotenv
load_dotenv()

config_path = environ.get('DNSCONFIG_PATH', './dnsconfig.js')  # cSpell:ignore DNSCONFIG dnsconfig
if not path.exists(config_path):
    raise FileNotFoundError(f"Config file '{config_path}' does not exist. Quitting.")

import logging
log_level = environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=log_level
)
logger = logging.getLogger(__name__)

def get_public_ip():
    response = requests.get('https://icanhazip.com')
    return response.text.strip()

def read_dnsconfig():
    with open(config_path, 'r') as file:
        return file.read()

def get_configured_ip(subdomain):
    pattern = rf"A\('{subdomain}', '(\d+\.\d+\.\d+\.\d+)'\)"
    match = re.search(pattern, read_dnsconfig())
    if match:
        return match.group(1)
    return None

def update_dns_config(subdomain, old_ip, new_ip):
    # Replace only the specific subdomain's IP
    new_content = re.sub(rf"A\('{subdomain}', '{old_ip}'\)", f"A('{subdomain}', '{new_ip}')", read_dnsconfig())
    with open(config_path, 'w') as file:
        file.write(new_content)

def check_ip():
    subdomain = environ.get('SUBDOMAIN') or input("Enter the subdomain to check against: ")
    current_ip = get_public_ip()
    last_ip = get_configured_ip(subdomain)

    if current_ip != last_ip:
        logging.info(f"IP has changed from {last_ip} to {current_ip}")
        update_dns_config(subdomain, last_ip, current_ip)
        if not environ.get('UNATTENDED'):
            input("Press Enter to push the new DNS configuration, or Ctrl+C to cancel.")
        subprocess.run(["dnscontrol", "push"])
    else:
        logging.debug("IP has not changed")