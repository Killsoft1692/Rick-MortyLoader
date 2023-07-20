def filter_episodes(data):
    return [episode['RawData']['name'] for episode in data if episode['RawData'].get('air_date', '').split(', ')[1] in ['2017', '2018', '2019', '2020', '2021'] and len(episode['RawData']['characters']) > 3]


def filter_odd_episodes_locations(data):
    return [item['RawData']['location']['name'] for item in data if any(int(episode.split('/')[-1]) % 2 != 0 for episode in item['RawData'].get('episode', []))]
