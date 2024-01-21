from mcrcon import MCRcon

import os
import io
import time
import csv
import json
import logging


logging.basicConfig(level=logging.INFO)

# e.g.: 00001,000002,00003
ALLOWED_LIST = os.environ.get("ALLOWED_STEAMIDS", "").split(",")

# KickPlayer or BanPlayer
# FYI: https://tech.palworldgame.com/server-commands
REJECT_COMMAND = os.environ.get("REJECT_COMMAND", "KickPlayer")


def fetch_login_players(mcr):
    players = []
    for _ in range(3):
        try:
            response = mcr.command("ShowPlayers")
            reader = csv.reader(io.StringIO(response))
            next(reader)  # skip header
            for row in reader:
                players.append(
                    {
                        "name": row[0],
                        "steamid": row[2],
                    }
                )
            break
        except:
            mcr.connect()

    return players


def reject_player(mcr, player):
    for _ in range(5):
        try:
            mcr.command("{} {}".format(REJECT_COMMAND, player["steamid"]))
            logging.info(
                json.dumps(
                    {
                        "message": "rejected player",
                        "reject_command": REJECT_COMMAND,
                        "player": player,
                    }
                )
            )
            break
        except:
            mcr.connect()


def auto_reject_players(mcr, players):
    for player in players:
        if player["steamid"] not in ALLOWED_LIST:
            reject_player(mcr, player)


if __name__ == "__main__":
    rcon_address = os.environ.get("RCON_ADDRESS", "127.0.0.1")
    rcon_port = int(os.environ.get("RCON_PORT", "25575"))
    rcon_password = os.environ["RCON_PASSWORD"]

    time_window = int(os.environ.get("TIME_WINDOW", "15"))

    with MCRcon(rcon_address, rcon_password, rcon_port) as mcr:
        logging.info(
            json.dumps(
                {
                    "message": "start rejector",
                    "allowed_list": ALLOWED_LIST,
                }
            )
        )
        while True:
            players = fetch_login_players(mcr)
            auto_reject_players(mcr, players)
            time.sleep(time_window)
