#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Copyright (c) 2024-25 2boom.


import json
import os
import sys
import time
import socket
import logging
import requests
from schedule import every, repeat, run_pending
from urllib.parse import urlparse


"""Configure logging"""
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


"""Get base url"""
def GetBaseUrl(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}...."


def isIPv6Supported():
    """Get IPv6 support"""
    try:
        socket.create_connection(("ipv6.google.com", 80), timeout=5)
        return True
    except socket.error:
        return False


def getExternalIp():
    """Get external Ips (IPv4/IPv6)"""
    ipv4, ipv6 = None, None
    for url in urls:
        try:
            ipv4_response = requests.get(url, timeout=5)
            ipv4_response.raise_for_status()
            ipv4 = ipv4_response.text.strip()
        except requests.RequestException as e:
            ipv4 = None
    
        if isIPv6Supported():
            try:
                ipv6_response = requests.get(url, timeout=5)
                ipv6_response.raise_for_status()
                ipv6 = ipv6_response.text.strip()
            except requests.RequestException as e:
                ipv6 = None
        else:
            ipv6 = None
        return ipv4, ipv6
    return None, None


def getLocalIp():
    """Get local Ips (IPv4/IPv6)"""
    ipv4, ipv6 = None, None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ipv4 = s.getsockname()[0]
    except Exception as e:
        ipv4 = None
        
    try:
        with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
            s.connect(("2001:4860:4860::8888", 80))
            ipv6 = s.getsockname()[0]
    except Exception as e:
        ipv6 = None

    return ipv4, ipv6


def getHostName() -> str:
    """Get system hostname"""
    hostname = ""
    hostname_path = '/proc/sys/kernel/hostname'
    if os.path.exists(hostname_path):
        with open(hostname_path, "r") as file:
            hostname = file.read().strip()
    return hostname


def SendMessage(message: str):
    """Internal function to send HTTP POST requests with error handling"""
    def SendRequest(url, json_data=None, data=None, headers=None):
        try:
            response = requests.post(url, json=json_data, data=data, headers=headers, timeout=(5, 10))
            response.raise_for_status()
            logger.info(f"Message successfully sent to {GetBaseUrl(url)}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending message to {GetBaseUrl(url)}: {e}")
    
    """"Converts Markdown-like syntax to HTML format."""
    def toHTMLFormat(message: str) -> str:
        message = ''.join(f"<b>{part}</b>" if i % 2 else part for i, part in enumerate(message.split('*')))
        return message.replace("\n", "<br>")

    """Converts the message to the specified format (HTML, Markdown, or plain text)"""
    def toMarkdownFormat(message: str, m_format: str) -> str:
        if m_format == "html":
            return toHTMLFormat(message)
        elif m_format == "markdown":
            return message.replace("*", "**")
        elif m_format == "text":
            return message.replace("*", "")
        elif m_format == "simplified":
            return message
        else:
            logger.error(f"Unknown format '{m_format}' provided. Returning original message.")
            return message

    """Iterate through multiple platform configurations"""
    for url, header, pyload, format_message in zip(platform_webhook_url, platform_header, platform_pyload, platform_format_message):
        data, ntfy = None, False
        formated_message = toMarkdownFormat(message, format_message)
        header_json = header if header else None
        for key in list(pyload.keys()):
            if key == "title":
                delimiter = "<br>" if format_message == "html" else "\n"
                header, formated_message = formated_message.split(delimiter, 1)
                pyload[key] = header.replace("*", "")
            elif key == "extras":
                formated_message = formated_message.replace("\n", "\n\n")
                pyload["message"] = formated_message
            elif key == "data":
                ntfy = True
            pyload[key] = formated_message if key in ["text", "content", "message", "body", "formatted_body", "data"] else pyload[key]
        pyload_json = None if ntfy else pyload
        data = formated_message.encode("utf-8") if ntfy else None
        """Send the request with the appropriate payload and headers"""
        SendRequest(url, pyload_json, data, header_json)


if __name__ == "__main__":
    """Load configuration and initialize monitoring"""
    urls = []
    host_name = getHostName()
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
    dots = {"orange": "\U0001F7E0", "green": "\U0001F7E2", "red": "\U0001F534", "yellow": "\U0001F7E1"}
    square_dots = {"orange": "\U0001F7E7", "green": "\U0001F7E9", "red": "\U0001F7E5", "yellow": "\U0001F7E8"}
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config_json = json.loads(file.read())
        try:
            startup_message = config_json.get("STARTUP_MESSAGE", True)
            default_dot_style = config_json.get("DEFAULT_DOT_STYLE", True)
            min_repeat = max(int(config_json.get("MIN_REPEAT", 1)), 1)
            urls = config_json.get("SERVICE_URLS", [])
        except (json.JSONDecodeError, ValueError, TypeError, KeyError):
            default_dot_style = startup_message = True
            min_repeat = 1
            urls = ["https://ip.me", "https://whatismyip.akamai.com"]
            logger.error("Error or incorrect settings in config.json. Default settings will be used.")
        header_message = f"*{host_name}* (ip.check)\n"    
        external_ipv4, external_ipv6 = getExternalIp()
        local_ipv4, local_ipv6 = getLocalIp()
        old_ip_ipv4 = external_ipv4
        old_ip_ipv6 = external_ipv6
        old_ip_local_ipv4 = local_ipv4
        old_ip_local_ipv6 = local_ipv6
        monitoring_message = monitoring_mg = ""
        if not default_dot_style:
            dots = square_dots
        orange_dot, green_dot, red_dot, yellow_dot = dots["orange"], dots["green"], dots["red"], dots["yellow"]
        no_messaging_keys = ["STARTUP_MESSAGE", "DEFAULT_DOT_STYLE", "MIN_REPEAT", "SERVICE_URLS"]
        messaging_platforms = list(set(config_json) - set(no_messaging_keys))
        for platform in messaging_platforms:
            if config_json[platform].get("ENABLED", False):
                for key, value in config_json[platform].items():
                    platform_key = f"platform_{key.lower()}"
                    if platform_key in globals():
                        globals()[platform_key] = (globals()[platform_key] if isinstance(globals()[platform_key], list) else [globals()[platform_key]])
                        globals()[platform_key].extend(value if isinstance(value, list) else [value])
                    else:
                        globals()[platform_key] = value if isinstance(value, list) else [value]
                monitoring_mg += f"- messaging: {platform.lower().capitalize()},\n"
        if external_ipv4:
            monitoring_message += f"- public IPv4: *{external_ipv4}*,\n"
        if external_ipv6:
            monitoring_message += f"- public IPv6: *{external_ipv6}*,\n"
        if local_ipv4:
            monitoring_message += f"- local IPv4: *{local_ipv4}*,\n"
        if local_ipv6:
            monitoring_message += f"- local IPv6: *{local_ipv6}*,\n"
        monitoring_message += (
            f"{chr(10).join(sorted(monitoring_mg.splitlines()))}\n"
            f"- default dot style: {default_dot_style}.\n"
            f"- polling period: {min_repeat} minute(s)."
        )
        if all(value in globals() for value in ["platform_webhook_url", "platform_header", "platform_pyload", "platform_format_message"]):
            logger.info(f"Started!")
            if startup_message:
                SendMessage(f"{header_message}{monitoring_message}")
        else:
            logger.error("config.json is wrong")
            sys.exit(1)
    else:
        logger.error("config.json not found")
        sys.exit(1)
        

@repeat(every(min_repeat).minutes)
def CheckIP():
    monitoring_message = ""
    global old_ip_ipv4, old_ip_ipv6, old_ip_local_ipv4, old_ip_local_ipv6
    external_ipv4, external_ipv6 = getExternalIp()
    local_ipv4, local_ipv6 = getLocalIp()

    if old_ip_ipv4 != external_ipv4: 
        old_ip_ipv4 = external_ipv4
        monitoring_message += f"{orange_dot} new public IPv4: *{str(external_ipv4)}*\n"

    if old_ip_ipv6 != external_ipv6:
        old_ip_ipv6 = external_ipv6
        monitoring_message += f"{orange_dot} new public IPv6: *{str(external_ipv6)}*\n"

    if old_ip_local_ipv4 != local_ipv4:
        old_ip_local_ipv4 = local_ipv4
        monitoring_message += f"{orange_dot} new local IPv4: *{str(local_ipv4)}*\n"

    if old_ip_local_ipv6 != local_ipv6:
        old_ip_local_ipv6 = local_ipv6
        monitoring_message += f"{orange_dot} new local IPv6: *{str(local_ipv6)}*\n"

    if monitoring_message:
        SendMessage(f"{header_message}{monitoring_message}")

while True:
    run_pending()
    time.sleep(1)
