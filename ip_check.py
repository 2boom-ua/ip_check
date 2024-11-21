#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Copyright (c) 2024 2boom.


import json
import os
import sys
import time
import socket
import requests
from schedule import every, repeat, run_pending

def getExternalIp() -> str:
	for url in urls:
		try:
			response = requests.get(url)
			external_ip = response.json()
			return external_ip['ip']
		except requests.RequestException as e:
			print(f"error {e}")
	return None

def getLocalIp() -> str:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		local_ip = s.getsockname()[0]
	finally:
		s.close()
	return local_ip

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
			response = requests.post(url, json=json_data, data=data, headers=headers)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			print(f"Error sending message: {e}")
	
	"""Converts the message to HTML format by replacing Markdown-like syntax"""
	def toHTMLFormat(message: str) -> str:
		formatted_message = ""
		for i, string in enumerate(message.split('*')):
			formatted_message += f"<b>{string}</b>" if i % 2 else string
		formatted_message = formatted_message.replace("\n", "<br>")
		return formatted_message

	"""Converts the message to the specified format (HTML, Markdown, or plain text)"""
	def toMarkdownFormat(message: str, m_format: str) -> str:
		if m_format == "html":
			return toHTMLFormat(message)
		elif m_format == "markdown":
			return message.replace("*", "**")
		elif m_format == "text":
			return message.replace("*", "")
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
	current_path = os.path.dirname(os.path.realpath(__file__))
	dots = {"orange": "\U0001F7E0", "green": "\U0001F7E2", "red": "\U0001F534", "yellow": "\U0001F7E1"}
	square_dots = {"orange": "\U0001F7E7", "green": "\U0001F7E9", "red": "\U0001F7E5", "yellow": "\U0001F7E8"}
	if os.path.exists(f"{current_path}/config.json"):
		with open(f"{current_path}/config.json", "r") as file:
			config_json = json.loads(file.read())
		try:
			default_dot_style = config_json.get("DEFAULT_DOT_STYLE", True)
			min_repeat = max(int(config_json.get("MIN_REPEAT", 1)), 1)
			urls = config_json.get("SERVICE_URLS", [])
		except (json.JSONDecodeError, ValueError, TypeError, KeyError):
			default_dot_style = True
			min_repeat = 1
			urls = ["https://ifconfig.co/json", "https://ipinfo.io/json"]
		header_message = f"*{host_name}* (ip.check)\n"	
		external_ip = getExternalIp()
		local_ip = getLocalIp()
		old_ip_address = external_ip
		old_ip_local = local_ip
		monitoring_message = monitoring_mg = ""
		if not default_dot_style:
			dots = square_dots
		orange_dot, green_dot, red_dot, yellow_dot = dots["orange"], dots["green"], dots["red"], dots["yellow"]
		no_messaging_keys = ["DEFAULT_DOT_STYLE", "MIN_REPEAT", "SERVICE_URLS"]
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
		monitoring_message = f"- public ip: *{external_ip}*\n- local  ip: *{local_ip}*\n"
		monitoring_message += "\n".join([*sorted(monitoring_mg.splitlines()), ""])
		monitoring_message += (
			f"- default dot style: {default_dot_style}.\n"
			f"- polling period: {min_repeat} minute(s)."
		)
		if all(value in globals() for value in ["platform_webhook_url", "platform_header", "platform_pyload", "platform_format_message"]):
			SendMessage(f"{header_message}{monitoring_message}")
		else:
			print("config.json is wrong")
			sys.exit(1)
	else:
		print("config.json not found")
		sys.exit(1)
		

@repeat(every(min_repeat).minutes)
def CheckIP():
	monitoring_message = ""
	global old_ip_address, old_ip_local
	external_ip = getExternalIp()
	local_ip = getLocalIp()
	if old_ip_address != external_ip: # !=
		old_ip_address = external_ip
		monitoring_message += f"{orange_dot} new public ip: *{str(external_ip)}*\n"
	if old_ip_local != local_ip:
		old_ip_local = local_ip
		monitoring_message += f"{orange_dot} new local ip: *{str(external_ip)}*\n"
	if monitoring_message:
		SendMessage(f"{header_message}{monitoring_message}")

while True:
	run_pending()
	time.sleep(1)
