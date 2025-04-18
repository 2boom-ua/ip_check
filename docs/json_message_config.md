### Telegram

```
    "TELEGRAM": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "https://api.telegram.org/bot{TOKEN}/sendMessage"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"chat_id": "{CHAT_ID}", "text": "message", "parse_mode": "Markdown"}
        ],
        "FORMAT_MESSAGE": [
            "simplified"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Telegram notifications |
| TOKEN | String | The token of your Telegram bot |
| CHAT_ID | String | The ID of the Telegram chat where notifications will be sent |
| FORMAT_MESSAGE | simplified | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Matrix
```
    "MATRIX": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{SERVER_URL}/_matrix/client/r0/rooms/{ROOM_ID}/send/m.room.message?access_token={TOKEN}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"msgtype": "m.text", "body": "message", "format": "org.matrix.custom.html", "formatted_body": "message"}
        ],
        "FORMAT_MESSAGE": [
            "html"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Matrix notifications |
| SERVER_URL | url | The URL of your Matrix server or https://matrix.org |
| ROOM_ID | String | The room_id |
| TOKEN | String | The token for your Matrix application. For get token you can use /tools/get_matrix_token.py |
| FORMAT_MESSAGE | html | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Apprise
```
    "APPRISE": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{SERVER_URL}/notify/{CONFIG_ID}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"body": "message", "type": "info", "format": "markdown"}
        ],
        "FORMAT_MESSAGE": [
            "markdown"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Apprise notifications |
| SERVER_URL | url | The URL of your Apprise server |
| CONFIG_ID | String | The your config_id or name of config |
| FORMAT_MESSAGE | markdown | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

### Ntfy
```
    "NTFY": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{SERVER_URL}/{SUBSCRIBE}"
        ],
        "HEADER": [
            {"Content-Type": "text/markdown"}
        ],
        "PAYLOAD": [
            {"data": "message"}
        ],
        "FORMAT_MESSAGE": [
            "markdown"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Ntfy notifications |
| SERVER_URL | url | The URL of your Ntfy server |
| SUBSCRIBE | String | The code of your subscribe |
| FORMAT_MESSAGE | markdown | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Pumble
```
    "PUMBLE": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{INCOMING_WEBHOOK_URL}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"text": "message"}
        ],
        "FORMAT_MESSAGE": [
            "markdown"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Pumble notifications |
| INCOMING_WEBHOOK_URL | url | The URL is generated by the service  |
| FORMAT_MESSAGE | markdown | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Mattermost
```
    "MATTERMOST": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{INCOMING_WEBHOOK_URL}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"text": "message"}
        ],
        "FORMAT_MESSAGE": [
            "markdown"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Mattermost notifications |
| INCOMING_WEBHOOK_URL | url | The URL is generated by the service  |
| FORMAT_MESSAGE | markdown | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Zulip
```
    "ZULIP": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{URL_ORGANIZATION}.zulipchat.com/api/v1/external/slack_incoming?api_key={API_KEY}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"text": "message"}
        ],
        "FORMAT_MESSAGE": [
            "simplified"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Zulip notifications |
| URL_ORGANIZATION | url | The URL of your Zulip organization |
| API_KEY| String | The code of your api_key |
| FORMAT_MESSAGE | simplified | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Flock
```
    "FLOCK": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "https://api.flock.com/hooks/sendMessage/{TOKEN}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"text": "message"}
        ],
        "FORMAT_MESSAGE": [
            "simplified"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Flock notifications |
| TOKEN | String | The your webhook token |
| FORMAT_MESSAGE | simplified | Specifies the message format used by each service, such as markdown, html, or other text formatting.|


### Slack
```
    "SLACK": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{INCOMING_WEBHOOK_URL}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"text": "message", "mrkdwn": "True"}
        ],
        "FORMAT_MESSAGE": [
            "simplified"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Slack notifications |
| INCOMING_WEBHOOK_URL | url | The URL is generated by the service |
| FORMAT_MESSAGE | simplified | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

### Rocket.chat
```
    "ROCKET.CHAT": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{INCOMING_WEBHOOK_URL}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"text": "message"}
        ],
        "FORMAT_MESSAGE": [
            "simplified"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Rocket.chat notifications |
| INCOMING_WEBHOOK_URL | url | The URL is generated by the service |
| FORMAT_MESSAGE | simplified | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

### Gotify
```
    "GOTIFY": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{SERVER_URL}/message?token={TOKEN}"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"title": "title", "message": "message", "priority": 0, "extras": {"client::display": {"contentType": "text/markdown"}}}
        ],
        "FORMAT_MESSAGE": [
            "markdown"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Gotify notifications |
| SERVER_URL | url | The URL of your Gotify server |
| TOKEN | String | The token for your Gotify app |
| FORMAT_MESSAGE | markdown | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

### Pushover
```
    "PUSHOVER": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "https://api.pushover.net/1/messages.json"
        ],
        "HEADER": [
            {"Content-type": "application/json"}
        ],
        "PAYLOAD": [
            {"token": "{TOKEN}", "user": "{USER_KEY}", "title": "header", "message": "message", "html": "1"}
        ],
        "FORMAT_MESSAGE": [
            "html"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Pushover notifications |
| TOKEN | String | The token from your Pushover account |
| USER_KEY | String | The user_key from your Pushover account |
| FORMAT_MESSAGE | html | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

### Pushbullet
```
    "PUSHBULLET": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "https://api.pushbullet.com/v2/pushes"
        ],
        "HEADER": [
            {"Content-Type": "application/json", "Access-Token": "{TOKEN}"}
        ],
        "PAYLOAD": [
            {"type": "note", "title": "header", "body": "message"}
        ],
        "FORMAT_MESSAGE": [
            "text"
        ]
    },
```

| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Pushbullet notifications |
| TOKEN | String | The token from your Pushbullet account |
| FORMAT_MESSAGE | text | Specifies the message format used by each service, such as markdown, html, or other text formatting.|

### Webntfy
```
    "WEBNTFY": {
        "ENABLED": true,
        "WEBHOOK_URL": [
            "{SERVER_URL}/messages"
        ],
        "HEADER": [
            {"Content-Type": "application/json"}
        ],
        "PAYLOAD": [
            {"message": "message"}
        ],
        "FORMAT_MESSAGE": [
            "markdown"
        ]
    },
```
| Item | Required | Description |
|------------|------------|------------|
| ENABLED | true/false | Enable or disable Webntfy notifications |
| SERVER_URL | url | The URL of your Webntfy server |
| FORMAT_MESSAGE | markdown | Specifies the message format used by each service, such as markdown, html, or other text formatting.|
