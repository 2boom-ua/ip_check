#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Copyright (c) 2024 2boom.


import json
import os
import time
import requests
from schedule import every, repeat, run_pending


def getExternalIp() -> str:
	"""Function to get the external IP address from a list of URLs."""
	for url in urls:
		try:
			response = requests.get(url)
			return response.json().get('ip', "")
		except requests.RequestException as e:
			print(f"error {e}")
	return ""


def getHostName() -> str:
	"""Get system hostname"""
	hostname = ""
	hostname_path = '/proc/sys/kernel/hostname'
	if os.path.exists(hostname_path):
		with open(hostname_path, "r") as file:
			hostname = file.read().strip()
	return hostname


def SendMessage(message: str):
	"""Send notifications to various messaging services (Telegram, Discord, Slack, Gotify, Ntfy, Pushbullet, Pushover, Matrix, Mattermost, Rocket.chat)."""
	def SendRequest(url, json_data=None, data=None, headers=None):
		"""Send an HTTP POST request and handle exceptions."""
		try:
			response = requests.post(url, json=json_data, data=data, headers=headers)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			print(f"Error sending message: {e}")
	
	if telegram_on:
		for token, chat_id in zip(telegram_tokens, telegram_chat_ids):
			url = f"https://api.telegram.org/bot{token}/sendMessage"
			json_data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
			SendRequest(url, json_data)
	if discord_on:
		for url in discord_webhook_urls:
			json_data = {"content": message.replace("*", "**")}
			SendRequest(url, json_data)
	if mattermost_on:
		for url in mattermost_webhook_urls:
			json_data = {'text': message.replace("*", "**")}
			SendRequest(url, json_data)
	if slack_on:
		for url in slack_webhook_urls:
			json_data = {"text": message}
			SendRequest(url, json_data)
	if matrix_on:
		for token, server_url, room_id in zip(matrix_tokens, matrix_server_urls, matrix_room_ids):
			url = f"{server_url}/_matrix/client/r0/rooms/{room_id}/send/m.room.message?access_token={token}"
			tmp_message = "<br>".join(string.replace('*', '<b>', 1).replace('*', '</b>', 1) for string in message.split("\n"))
			json_data = {"msgtype": "m.text", "body": tmp_message, "format": "org.matrix.custom.html", "formatted_body": tmp_message}
			SendRequest(url, json_data)
	if rocket_on:
		for token, server_url, user_id, channel in zip(rocket_tokens, rocket_server_urls,rocket_user_ids, rocket_channel_ids):
			url = f"{server_url}/api/v1/chat.postMessage"
			headers_data = {"X-Auth-Token": token, "X-User-Id": user_id, "Content-Type": "application/json"}
			json_data = {"channel": channel, "text": message}
			SendRequest(url, json_data, None, headers_data)
	
	header, message = message.replace("*", "").split("\n", 1)
	message = message.strip()
	
	if gotify_on:
		for token, server_url in zip(gotify_tokens, gotify_server_urls):
			url = f"{server_url}/message?token={token}"
			json_data = {'title': header, 'message': message, 'priority': 0}
			SendRequest(url, json_data)
	if ntfy_on:
		for url in ntfy_webhook_urls:
			encoded_message = message.encode(encoding = 'utf-8')
			headers_data = {"title": header}
			SendRequest(url, None, encoded_message, headers_data)
	if pushbullet_on:
		for token in pushbullet_tokens:
			url = "https://api.pushbullet.com/v2/pushes"
			json_data = {'type': 'note', 'title': header, 'body': message}
			headers_data = {'Access-Token': token, 'Content-Type': 'application/json'}
			SendRequest(url, json_data, None, headers_data)
	if pushover_on:
		for token, user_key in zip(pushover_tokens, pushover_user_keys):
			url = "https://api.pushover.net/1/messages.json"
			json_data = {"token": token, "user": user_key, "message": message, "title": header}
			SendRequest(url, json_data)


if __name__ == "__main__":
	"""Load configuration and initialize monitoring"""
	urls = []
	host_name = getHostName()
	current_path = os.path.dirname(os.path.realpath(__file__))
	dots = {"orange": "\U0001F7E0", "green": "\U0001F7E2", "red": "\U0001F534", "yellow": "\U0001F7E1"}
	square_dots = {"orange": "\U0001F7E7", "green": "\U0001F7E9", "red": "\U0001F7E5", "yellow": "\U0001F7E8"}
	if os.path.exists(f"{current_path}/config.json"):
		with open(f"{current_path}/config.json", "r") as file:
			parsed_json = json.loads(file.read())
		min_repeat = int(parsed_json["MIN_REPEAT"])
		default_dot_style = parsed_json["DEFAULT_DOT_STYLE"]
		urls = parsed_json["SERVICE_URLS"]
		header_message = f"*{host_name}* (ip.check)\n"	
		current_ip = getExternalIp()
		old_ip_address = current_ip
		monitoring_mg = f"- current ip: *{current_ip}*\n"
		if not default_dot_style:
			dots = square_dots
		orange_dot, green_dot, red_dot, yellow_dot = dots["orange"], dots["green"], dots["red"], dots["yellow"]
		messaging_platforms = ["TELEGRAM", "DISCORD", "GOTIFY", "NTFY", "PUSHBULLET", "PUSHOVER", "SLACK", "MATRIX", "MATTERMOST", "ROCKET"]
		telegram_on, discord_on, gotify_on, ntfy_on, pushbullet_on, pushover_on, slack_on, matrix_on, mattermost_on, rocket_on = (parsed_json[key]["ON"] for key in messaging_platforms)
		services = {
			"TELEGRAM": ["TOKENS", "CHAT_IDS"],
			"DISCORD": ["WEBHOOK_URLS"],
			"SLACK": ["WEBHOOK_URLS"],
			"GOTIFY": ["TOKENS", "SERVER_URLS"],
			"NTFY": ["WEBHOOK_URLS"],
			"PUSHBULLET": ["TOKENS"],
			"PUSHOVER": ["TOKENS", "USER_KEYS"],
			"MATRIX": ["TOKENS", "SERVER_URLS", "ROOM_IDS"],
			"MATTERMOST": ["WEBHOOK_URLS"],
			"ROCKET": ["TOKENS", "SERVER_URLS", "USER_IDS", "CHANNEL_IDS"]
		}
		for service, keys in services.items():
			if parsed_json[service]["ON"]:
				globals().update({f"{service.lower()}_{key.lower()}": parsed_json[service][key] for key in keys})
				monitoring_mg += f"- messaging: {service.capitalize()},\n"
		monitoring_mg += f"- polling period: {min_repeat} minute(s),\n- default dot style: {default_dot_style}."
		SendMessage(f"{header_message}{monitoring_mg}")
	else:
		print("config.json not found")
		

@repeat(every(min_repeat).minutes)
def CheckIP():
	"""Function to check the IP periodically."""
	global old_ip_address
	current_ip = getExternalIp()
	if old_ip_address != current_ip:
		old_ip_address = current_ip
		monitoring_mg = f"{orange_dot} new ip is: *{current_ip}*\n"
		SendMessage(f"{header_message}{monitoring_mg}")

while True:
	run_pending()
	time.sleep(1)
