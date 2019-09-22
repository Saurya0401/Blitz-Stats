#! python 3

import csv
import os
import requests
from datetime import datetime


def get_playerid(acc_id, server_id):
    """
    Function to get the account id of a player by looking up the player's nickname.
    :return: player's account id and server or an error message.
    """

    account_name = acc_id
    server = server_id
    params = {'application_id': '6e556537f926af38c699e6f28d344d13', 'search': account_name}
    try:
        response = requests.api.get(
            url=f'https://api.wotblitz.{server if server != "na" else "com"}/wotb/account/list/', params=params)
    except requests.exceptions.RequestException:
        return None, None, None, 2, "Connection Error."
    else:
        data = response.json()
    if data['status'] == 'ok' and server:
        if len(data['data']) == 0:
            return None, account_name, server, 1, None
        else:
            playerid = data['data'][0]['account_id']
            nickname = data['data'][0]['nickname']
            return str(playerid), nickname, server, 0, None
    elif data['status'] == 'error':
        return None, None, None, 2, data['error']['message']


def get_stats(acc_id, server_id):
    """
    Function that returns the current winrate of a player.
    :return: player's winrate or an error message
    """

    output = None
    player_id, nickname, server, err_code, err_msg = get_playerid(acc_id, server_id)
    if err_code == 0:
        params = {'application_id': '6e556537f926af38c699e6f28d344d13', 'account_id': player_id}
        response = requests.api.get(
            url=f'https://api.wotblitz.{server if server != "na" else "com"}/wotb/account/info/', params=params)
        clan_response = requests.api.get(
            url=f'https://api.wotblitz.{server if server != "na" else "com"}/wotb/clans/accountinfo/',
            params={**params, 'extra': 'clan'})
        player_stats = response.json()['data'][player_id]['statistics']['all']
        try:
            clan_tag = f"[{clan_response.json()['data'][player_id]['clan']['tag']}]"
        except TypeError:
            clan_tag = ""
        winrate = (player_stats['wins']/player_stats['battles']) * 100
        data_update_timestamp = \
            datetime.fromtimestamp(response.json()['data'][player_id]['updated_at']).strftime('%Y-%m-%d %H:%M:%S')
        output = [player_id, f"{nickname} {clan_tag}", float(winrate), str(data_update_timestamp)]
    elif err_code == 1:
        output = [f"ERROR: PLAYER_NOT_FOUND ('{nickname}', {server.upper()})"]
    elif err_code == 2:
        output = [f"ERROR: {err_msg}"]
    return output


def record_stats(player_record):
    if not os.path.isdir("C:\\Users\\saury\\Desktop\\Python Projects\\BlitzStats\\players"):
        os.mkdir("C:\\Users\\saury\\Desktop\\Python Projects\\BlitzStats\\players")
    profile = f"C:\\Users\\saury\\Desktop\\Python Projects\\BlitzStats\\players/{player_record[0]}.csv"
    if not os.path.isfile(profile):
        with open(profile, "w", newline="") as player_file:
            writer = csv.DictWriter(player_file, fieldnames=["acc_id", "player_id", "winrate", "last_updated"])
            writer.writeheader()
            player_file.close()
    with open(profile, "a", newline="") as player_profile:
        recorder = csv.writer(player_profile, delimiter=",")
        recorder.writerow(player_record)


def track_stats(acc_id):
    records = []
    with open(f"players/{acc_id}.csv", "r") as player_record:
        player_records = player_record.readlines()
        player_record.close()
    for record in player_records:
        if player_records.index(record) > 0:
            record = record.split(",")
            record.reverse()
            record[0] = record[0].rstrip("\n")
            records.append(tuple(record[0:2]))
    timestamps = [i[0] for i in records]
    winrates = [float(i[1]) for i in records]
    t = datetime.strptime(timestamps[-1], '%Y-%m-%d %H:%M:%S') - datetime.strptime(timestamps[0], '%Y-%m-%d %H:%M:%S')
    wr = winrates[-1] - winrates[0]
    if t.days >= 2:
        return f"In {t.days} days, your winrate has {'increased' if wr >= 0 else 'decreased'} by {'%.2f' % wr}. " \
            f"In these {t.days} days, your maximum recorded winrate was {'%.2f' % max(winrates)} on " \
            f"{datetime.strptime(timestamps[winrates.index(max(winrates))], '%Y-%m-%d %H:%M:%S')}."
    else:
        return "Time interval too short to track winrate, please check later!"


if __name__ == '__main__':
    record_stats(get_stats("drearydepp", "asia"))
