import ssl

import certifi
from aiohttp import ClientSession, TCPConnector


class SevenTV:
    _EMOTES = {}

    @staticmethod
    def _get_client_session() -> ClientSession:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = TCPConnector(ssl=ssl_context)
        return ClientSession(connector=conn)

    @staticmethod
    async def _gql_request(query: dict):
        async with SevenTV._get_client_session() as session:
            async with session.post(
                "https://7tv.io/v3/gql",
                headers={
                    "Content-Type": "application/json",
                },
                json=query,
            ) as response:
                return (await response.json())["data"]

    @staticmethod
    async def get_user(ttv_user_id: str):
        return (
            await SevenTV._gql_request(
                {
                    "operationName": "GetUserByConnection",
                    "query": """
                        query GetUserByConnection($platform: ConnectionPlatform! $id: String!) {
                            userByConnection (platform: $platform id: $id) {
                                id
                                type
                                username
                                roles
                                created_at
                                connections {
                                    id
                                    platform
                                    emote_set_id
                                }
                                editors {
                                  user {
                                    id
                                    username
                                  }
                                }
                                emote_sets {
                                    id
                                    emotes {
                                        id
                                        name
                                        data {
                                          id
                                          name
                                        }
                                    }
                                    capacity
                                }
                            }
                        }""",
                    "variables": {
                        "platform": "TWITCH",
                        "id": ttv_user_id,
                    },
                }
            )
        )["userByConnection"]

    @staticmethod
    async def get_global_emote_set() -> dict:
        if SevenTV._EMOTES:
            return SevenTV._EMOTES

        return (
            await SevenTV._gql_request(
                {
                    "operationName": "AppState",
                    "query": """
                        query AppState {
                          globalEmoteSet: namedEmoteSet(name: GLOBAL) {
                            id
                            name
                            emotes {
                              id
                              name
                              flags
                              __typename
                            }
                            capacity
                            __typename
                          }
                          roles: roles {
                            id
                            name
                            allowed
                            denied
                            position
                            color
                            invisible
                            __typename
                          }
                        }""",
                    "variables": {},
                }
            )
        )["globalEmoteSet"]
