import json
from typing import Dict, Any

import aiohttp

from bot_station_client.bot_station_client.model.config import BotStationClientConfig


class BotStationClient:
    config: BotStationClientConfig = ""

    def __init__(self, config: BotStationClientConfig):
        self.config = config

    async def create(self,
                     name: str,
                     description: str,
                     prompt_intro: str,
                     add_external_context_to_prompt: bool = False,
                     add_messages_history_to_prompt: bool = False,
                     temperature: float = 0.6
                     ):
        await self.__post(
            method="create",
            content={
                "name": name,
                "description": description,
                "prompt_intro": prompt_intro,
                "add_external_context_to_prompt": str(add_external_context_to_prompt).lower(),
                "add_messages_history_to_prompt": str(add_messages_history_to_prompt).lower(),
                "temperature": temperature,
            }
        )

    async def train(self,
                    bot_id: str,
                    text: str
                    ):
        await self.__post(
            method="create",
            content={
                "id": bot_id,
                "data": text,
            }
        )

    async def call(self,
                   bot_id: str,
                   chat_id: int | str,
                   text: str
                   ):
        await self.__post(
            method="call",
            content={
                "bot_id": bot_id,
                "chat_id": chat_id,
                "data": text
            }
        )

    async def __post(self,
                     method: str,
                     content: Dict[str, str | int],
                     ) -> Any:
        """
        Returns response json body
        """
        headers: Dict[str, str] = {}
        content_str: str = json.dumps(content)
        async with aiohttp.ClientSession(headers=headers) as session:
            url = f'{self.config.base_uri}/{method}'
            async with session.post(url=url, data=content_str) as response:
                data = await response.json()
                return data
