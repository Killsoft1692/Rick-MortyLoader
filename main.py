import asyncio
import json
import uuid
from typing import List

import aiohttp

import settings
from models import Info
from loggers import DefaultLogger
from encoders import DataClassJSONEncoder
from helpers import filter_episodes, filter_odd_episodes_locations


async def fetch_data(session: aiohttp.ClientSession, data_type: str, endpoint: str) -> (str, List[Info]):
    async with session.get(endpoint) as response:
        if response.status == 200:
            data = await response.json()
            fetched_data = data['results']
            return data_type, [Info(str(uuid.uuid4()), item['name'], item) for item in fetched_data]
        else:
            pass


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        # Fetch and save all data from available endpoints
        tasks = []
        for data_type in settings.AVAILABLE_TYPES:
            # Let's assume that we have endpoint that gives for us only count,
            # and we know that for each entity we'll have around 50 pages
            for page in range(1, settings.COUNT_OF_PAGES + 1):
                tasks.append(
                    fetch_data(
                        session, data_type, f"{settings.API_BASE_URL}{data_type}/?page={page}"
                    )
                )
        # Filtering results
        results = await asyncio.gather(*tasks)
        for position,  data_type in enumerate(settings.AVAILABLE_TYPES):
            raw_data = filter(lambda x: x[0] == settings.AVAILABLE_TYPES[position], filter(bool, results))
            filtered_objects = [item for _, inner_list in raw_data for item in inner_list]
            with open(f"{data_type}s.json", 'w') as file:
                json.dump(
                   filtered_objects, file, indent=2, cls=DataClassJSONEncoder
                )

if __name__ == "__main__":
    asyncio.run(main())

    # Task 1: Print episodes aired between 2017 and 2021 with more than three characters
    with open("episodes.json") as file:
        episodes_data = json.load(file)
    filtered_episodes = filter_episodes(episodes_data)
    DefaultLogger.info("Episodes aired between 2017 and 2021 with more than three characters:")
    DefaultLogger.info(list(set(filtered_episodes)))

    # Task 2: Print locations that appear on odd episode numbers
    with open("characters.json") as file:
        characters_data = json.load(file)
    filtered_locations = filter_odd_episodes_locations(characters_data)
    DefaultLogger.info("Locations that appear on odd episode numbers:")
    DefaultLogger.info(list(set(filtered_locations)))
