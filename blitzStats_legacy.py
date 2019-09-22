import requests


def get_stats(player_id):
    params = {'application_id': '6e556537f926af38c699e6f28d344d13',
              'account_id': player_id,
              'fields': 'statistics.all'}
    response = requests.api.get(url='https://api.wotblitz.asia/wotb/account/info/', params=params)
    stats_rec = response.json()['data']['2015498511']['statistics']['all']
    stats = {'total_battles': stats_rec['battles'], 'wins': stats_rec['wins'], 'losses': stats_rec['losses']}
    winrate = (stats['wins']/stats['total_battles']) * 100
    return f"Your winrate is {winrate}%."


print(get_stats('2015498511'))
