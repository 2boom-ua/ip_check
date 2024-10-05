# ip_check
<div align="center">  
    <img src="https://github.com/2boom-ua/ip_check/blob/main/ip_check.jpg?raw=true" alt="" width="260" height="62">
</div>
### Overview

This script monitors the system's external IP address and sends notifications to various messaging platforms (e.g., Telegram, Discord, Gotify, Ntfy, Slack, Pushbullet, Pushover, Rocket.chat, Matrix, Mattermost) when the external IP changes. It reads configuration settings from a config.json file, including polling intervals and service tokens. The IP is checked periodically, and if a change is detected, an alert is sent via the configured messaging services.


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

### Edit config.json:
A **config.json** file in the same directory as the script, and include your API tokens and configuration settings.
```
{
    "TELEGRAM": {
        "ON": false,
        "TOKENS": [
            "first tocken",
            "second tocken",
            "...."
        ],
        "CHAT_IDS": [
            "first chat_id",
            "second chat_id",
            "...."
        ]
    },
    "DISCORD": {
        "ON": false,
        "WEBHOOK_URLS": [
            "first url",
            "second url",
            "...."
        ]
    },
    "SLACK": {
        "ON": false,
        "WEBHOOK_URLS": [
            "first url",
            "second url",
            "...."
        ]
    },
    "GOTIFY": {
        "ON": false,
        "TOKENS": [
            "first tocken",
            "second tocken",
            "...."
        ],
        "CHAT_URLS": [
            "first server_url",
            "second server_url",
            "...."
        ]
    },
    "NTFY": {
        "ON": false,
        "WEBHOOK_URLS": [
            "first url",
            "second url",
            "...."
		]
    },
    "PUSHBULLET": {
        "ON": false,
        "TOKENS": [
            "first tocken",
            "second tocken",
            "...."
        ]
    },
    "PUSHOVER": {
        "ON": false,
        "TOKENS": [
            "first tocken",
            "second tocken",
            "...."
        ],
        "USER_KEYS": [
            "first user_key",
            "second user_key",
            "...."
        ]
    },
    "MATRIX": {
        "ON": false,
        "TOKENS": [
            "first tocken",
            "second tocken",
            "...."
        ],
        "SERVER_URLS": [
            "first server_url",
            "second server_url",
            "...."
        ],
        "ROOM_IDS": [
            "!first room_id",
            "!second room_id",
            "...."
        ]
    },
    "MATTERMOST": {
        "ON": false,
        "WEBHOOK_URLS": [
            "first url",
            "second url",
            "...."
        ]
    },
    "ROCKET": {
        "ON": false,
        "TOKENS": [
            "first tocken",
            "second tocken",
            "...."
        ],
		"USER_IDS": [
            "first user_id",
            "second user_id",
            "...."
        ],
        "SERVER_URLS": [
           "first server_url",
            "second server_url",
            "...."
        ],
		"CHANNEL_IDS": [
            "#first channel",
            "#second channel",
            "...."
        ]
    },
    "DEFAULT_DOT_STYLE": true,
    "MIN_REPEAT": 15
}
```
| Item   | Required   | Description   |
|------------|------------|------------|
| DEFAULT_DOT_STYLE | true/false | Round/Square dots. |
| MIN_REPEAT | 15 | Set the poll period in minutes. Minimum is 1 minute. | 

## Running as a Linux Service
You can set this script to run as a Linux service for continuous monitoring.

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

## License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.

## Author

- **2boom** - [GitHub](https://github.com/2boom-ua)

