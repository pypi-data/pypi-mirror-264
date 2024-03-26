import asyncio
import logging
from typing import Awaitable

import flet as ft

from hasherino.api import helix
from hasherino.api.chat_history import get_chat_history
from hasherino.api.seven_tv import SevenTV
from hasherino.hasherino_dataclasses import Emote
from hasherino.parse_irc import ParsedMessage
from hasherino.storage import AsyncKeyValueStorage
from hasherino.twitch_websocket import TwitchWebsocket


class HasherinoTab(ft.Tab):
    def __init__(
        self,
        channel: str,
        persistent_storage: AsyncKeyValueStorage,
        memory_storage: AsyncKeyValueStorage,
        message_received: Awaitable[ParsedMessage],
    ):
        super().__init__(tab_content=ft.Row(controls=[ft.Text(channel)]))
        self.persistent_storage = persistent_storage
        self.memory_storage = memory_storage
        self.channel = channel
        self.message_received = message_received

    async def _get_channel_seventv_emotes(self, user: helix.TwitchUser) -> dict:
        try:
            seventv_user = await SevenTV.get_user(user.id)

            if not seventv_user:
                return dict()

            ttv_connection = next(
                connection
                for connection in seventv_user["connections"]
                if connection["platform"] == "TWITCH"
            )
            active_ttv_set = next(
                ttv_set
                for ttv_set in seventv_user["emote_sets"]
                if ttv_set["id"] == ttv_connection["emote_set_id"]
            )
            logging.info(
                f"Loaded {len(active_ttv_set['emotes'])} channel 7tv emotes for {self.channel}"
            )
            return {
                emote["name"]: emote["data"]["id"] for emote in active_ttv_set["emotes"]
            }
        except Exception as e:
            raise Exception(
                f"Failed to load channel 7tv emotes for {self.channel} with error {e}"
            ) from e

    async def _get_global_7tv_emotes(self) -> dict[str, str]:
        try:
            global_emotes = await SevenTV.get_global_emote_set()
            return {emote["name"]: emote["id"] for emote in global_emotes["emotes"]}
        except Exception as e:
            raise Exception("Failed to load global 7tv emotes with error {e}") from e

    async def _get_channel_ttv_emotes(
        self, app_id: str, helix_token: str, user: helix.TwitchUser
    ):
        try:
            return await helix.get_channel_emotes(app_id, helix_token, str(user.id))
        except Exception as e:
            raise Exception(
                f"Failed to load ttv emotes for {self.channel} with error {e}"
            ) from e

    async def load_emotes(self):
        try:
            async with asyncio.TaskGroup() as tg:
                app_id_task = tg.create_task(self.persistent_storage.get("app_id"))
                helix_token_task = tg.create_task(self.persistent_storage.get("token"))

            app_id = await app_id_task
            token = await helix_token_task

            user: helix.TwitchUser = (
                await helix.get_users(
                    app_id,
                    token,
                    [self.channel],
                )
            )[0]

            async with asyncio.TaskGroup() as tg:
                stv_channel_emotes_task = tg.create_task(
                    self._get_channel_seventv_emotes(user)
                )
                stv_global_emotes_task = tg.create_task(self._get_global_7tv_emotes())

            seventv_emotes = await stv_channel_emotes_task
            seventv_emotes.update(await stv_global_emotes_task)

            if not (emotes := await self.memory_storage.get("7tv_emotes")):
                emotes = dict()

            emotes[user.login] = {
                emote_name: Emote(
                    emote_name,
                    emote_id,
                    f"https://cdn.7tv.app/emote/{emote_id}/2x.webp",
                )
                for emote_name, emote_id in seventv_emotes.items()
            }
            await self.memory_storage.set("7tv_emotes", emotes)

        except Exception as e:
            logging.error(f"Error while loading emotes: {e}")

    async def load_history(self):
        if await self.persistent_storage.get("chat_history"):
            limit = int(await self.persistent_storage.get("max_messages_per_chat"))
            for message in await get_chat_history(self.channel, limit):
                await self.message_received(message)


class Tabs(ft.Tabs):
    def __init__(
        self,
        memory_storage: AsyncKeyValueStorage,
        persistent_storage: AsyncKeyValueStorage,
    ):
        super().__init__(
            tabs=[],
            on_change=self.change,
        )
        self.memory_storage = memory_storage
        self.persistent_storage = persistent_storage

    async def add_tab(self, channel: str, message_received: Awaitable[ParsedMessage]):
        tab = HasherinoTab(
            channel, self.persistent_storage, self.memory_storage, message_received
        )
        await tab.load_emotes()
        await tab.load_history()
        close_button = ft.IconButton(icon=ft.icons.CLOSE, on_click=self.close)
        close_button.parent_tab = tab
        tab.tab_content.controls.append(close_button)
        self.tabs = [tab]
        logging.info(f"Added tab {channel}")
        await self.page.add_async()

    async def close(self, button_click: ft.ControlEvent):
        websocket: TwitchWebsocket = await self.memory_storage.get("websocket")
        tab_channel = button_click.control.parent_tab.channel
        await websocket.leave_channel(tab_channel)
        self.tabs.remove(button_click.control.parent_tab)
        await self.persistent_storage.set("channel", None)
        logging.info(f"Closed tab {tab_channel}")
        await self.page.add_async()

    async def change(self, e):
        tab = e.control.tabs[e.control.selected_index]
