This is a Telegram bot based on the project [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

# Features

 - Daemon process
 - Authorization

# Supported commands

 - `/start`: Nothing. Just return a string.
 - `/user_id`: Return current user's ID. This command doesn't need admin privilege
 - `/kancolle_avatar`: Return current avatar for [@KanColle_STAFF](https://twitter.com/KanColle_STAFF)
 - `/db_status`: Return database file status
 - `/imgur_upload`: Upload a image pointed by a URL to your Imgur account

# Dependencies

 - beautifulsoup4
 - python-telegram-bot
 - tinydb
 - importlib

 # Config file example

 ```
{
	"bot_token": "123456:xxxxxxxxxxxxxxxxx", // Your bot token
	"admin": ["12345678"],                   // Admin user id
	"db_name": "db.json"                     // Database name
	// For next three values, please refer to Imgur API documents.
    "imgur_client_id": "xxxxxxxxxxxx",       
    "imgur_client_secret": "xxxxxxxxxxxxx",
    "imgur_client_refresh_token": "xxxxxx"
}
 ```