## ip_check
<div align="center">  
    <img src="https://github.com/2boom-ua/ip_check/blob/main/ip_check.jpg?raw=true" alt="" width="260" height="62">
</div>

### Overview
This script monitors the system's external IP (IPv4/IPv6) and internal IP addresses and sends notifications to various messaging platforms (e.g., Telegram, Discord, Gotify, Ntfy, Slack, Pushbullet, Pushover, Rocket.chat, Matrix, Mattermost, Pumble, Flock, Zulip, Apprise, Custom webhook) when the external IP changes. It reads configuration settings from a config.json file, including polling intervals and service tokens. The IP is checked periodically, and if a change is detected, an alert shall be sent via the configured messaging services.


### Features

- **Service Status Monitoring:** Regularly checks if specified services are active or inactive.
- **Real-time notifications with support for multiple accounts** via:
  - Telegram
  - Discord
  - Slack
  - Gotify
  - Ntfy
  - Pushbullet
  - Pushover
  - Rocket.chat
  - Matrix
  - Mattermost
  - Zulip
  - Pumble
  - Flock
  - Apprise
  - Webntfy
  - Custom webhook
- **Configuration:** Easily configurable through JSON files for notification settings and excluded services.
- **Polling Period:** Adjustable polling interval to check service status.


### Requirements
- Python 3.x
- Docker installed and running
- Dependencies: `requests`, `schedule`

### Clone the repository:
```
git clone https://github.com/2boom-ua/ip_check.git
cd check_services
```
### Install required Python packages:
```
pip install -r requirements.txt
```

## Edit config.json:
You can use any name and any number of records for each messaging platform configuration, and you can also mix platforms as needed. The number of message platform configurations is unlimited.

[Configuration examples for Telegram, Matrix, Apprise, Pumble, Mattermost, Discord, Ntfy, Gotify, Zulip, Flock, Slack, Rocket.Chat, Pushover, Pushbullet](docs/json_message_config.md)
```
    "CUSTOM_NAME": {
        "ENABLED": false,
        "WEBHOOK_URL": [
            "first url",
            "second url",
            "...."
        ],
        "HEADER": [
            {first JSON structure},
            {second JSON structure},
            {....}
        ],
        "PYLOAD": [
            {first JSON structure},
            {second JSON structure},
            {....}
        ],
        "FORMAT_MESSAGE": [
            "markdown",
            "html",
            "...."
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Custom notifications |
| WEBHOOK_URL | url | The URL of your Custom webhook |
| HEADER | JSON structure | HTTP headers for each webhook request. This varies per service and may include fields like {"Content-Type": "application/json"}. |
| PAYLOAD | JSON structure | The JSON payload structure for each service, which usually includes message content and format. Like as  {"body": "message", "type": "info", "format": "markdown"}|
| FORMAT_MESSAGE | markdown,<br>html,<br>text,<br>simplified | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

- **markdown** - a text-based format with lightweight syntax for basic styling (Pumble, Mattermost, Discord, Ntfy, Gotify),
- **simplified** - simplified standard Markdown (Telegram, Zulip, Flock, Slack, RocketChat).
- **html** - a web-based format using tags for advanced text styling,
- **text** - raw text without any styling or formatting.
```
 "SERVICE_URLS": [
      "https://ip.me",
      "https://whatismyip.akamai.com",
      "https://checkip.amazonaws.com",
      "https://api.my-ip.io/ip"
],
```

| Item | Required | Description |
|------------|------------|------------|
| SERVICE_URLS | url | The URL of ifconfig services 

```
"STARTUP_MESSAGE": true,
 "DEFAULT_DOT_STYLE": true,
 "MIN_REPEAT": 15
```

| Item   | Required   | Description   |
|------------|------------|------------|
| STARTUP_MESSAGE | true/false | On/Off startup message. |
| DEFAULT_DOT_STYLE | true/false | Round/Square dots. |
| MIN_REPEAT | 15 | Set the poll period in minutes. Minimum is 1 minute. | 


## Docker
```bash
  docker build -t ip_check .
```
or
```bash
  docker pull ghcr.io/2boom-ua/ip_check:latest
```
### Dowload and edit config.json
```bash
curl -L -o ./config.json  https://raw.githubusercontent.com/2boom-ua/ip_check/main/config.json
```
### docker-cli
```bash
docker run -v ./config.json:/ip_check/config.json --name ip_check -e TZ=UTC ghcr.io/2boom-ua/ip_check:latest 
```
### docker-compose
```
version: "3.8"
services:
  ip_check:
    container_name: ip_check
    image: ghcr.io/2boom-ua/ip_check:latest
    network_mode: "host"
    volumes:
      - ./config.json:/ip_check/config.json
    environment:
      - TZ=UTC
    restart: always
```

```bash
docker-compose up -d
```
---
### Running as a Linux Service
You can set this script to run as a Linux service for continuous monitoring.

### Clone the repository:
```
git clone https://github.com/2boom-ua/ip_check.git
cd ip_services
```
### Install required Python packages:
```
pip install -r requirements.txt
```

Create a systemd service file:
```
nano /etc/systemd/system/ip_check.service
```
Add the following content:
```
[Unit]
Description=check external ip changes
After=multi-user.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /opt/ip_check/ip_check.py

[Install]
WantedBy=multi-user.target
```
```
systemctl daemon-reload
```
```
systemctl enable ip_check.service
```
```
systemctl start ip_check.service
```

### License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.

### Author

- **2boom** - [GitHub](https://github.com/2boom-ua)

