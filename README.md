# What?

Plaworld does not have a method to manage players with a whitelist. This tool automatically rejects unnecessary players.

# Spec

python: 3.10.x

# Run


```
RCON_PASSWORD=$RCON_PASSWORD RCON_ADDRESS=$RCON_ADDRESS ALLOWED_STEAMIDS=$YOUR_FIRENDS1,$YOUR_FIRENDS2 python app.py
```

ALLOWED_STEAMIDS: When you want to write multiple IDs, separate them with commas.

or https://hub.docker.com/r/mocchi/palworld-rejector

## How to check SteamID
FYI: https://help.steampowered.com/en/faqs/view/2816-BE67-5B69-0FEC

