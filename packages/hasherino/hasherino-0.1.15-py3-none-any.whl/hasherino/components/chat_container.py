import asyncio
import logging
from enum import Enum, auto
from math import isclose

import flet as ft

from hasherino.components.chat_message import ChatMessage
from hasherino.hasherino_dataclasses import Message
from hasherino.pubsub import PubSub
from hasherino.storage import AsyncKeyValueStorage


class ChatContainer(ft.Container):
    class _UiUpdateType(Enum):
        NO_UPDATE = (auto(),)
        SCROLL = (auto(),)
        PAGE = (auto(),)

    def __init__(
        self,
        persistent_storage: AsyncKeyValueStorage,
        memory_storage: AsyncKeyValueStorage,
        font_size_pubsub: PubSub,
        ts_pubsub: PubSub,
    ):
        self.persistent_storage = persistent_storage
        self.memory_storage = memory_storage
        self.font_size_pubsub = font_size_pubsub
        self.ts_pubsub = ts_pubsub
        self.is_chat_scrolled_down = False
        self.chat = ft.ListView(
            expand=True,
            spacing=0,
            auto_scroll=False,
            on_scroll=self.on_scroll,
        )
        self.scroll_down_btn = ft.FloatingActionButton(
            icon=ft.icons.ARROW_DOWNWARD_ROUNDED,
            on_click=self.scroll_to_bottom,
            shape=ft.CircleBorder(),
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.GREY_200),
        )
        super().__init__(
            content=self.chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        )
        self.scheduled_ui_update: self._UiUpdateType = self._UiUpdateType.NO_UPDATE
        asyncio.ensure_future(self.update_ui())

    async def scroll_to_bottom(self, _):
        await self.chat.scroll_to_async(offset=-1, duration=10)

    async def update_ui(self):
        while True:
            match self.scheduled_ui_update:
                case self._UiUpdateType.SCROLL:
                    await self.chat.scroll_to_async(offset=-1, duration=10)
                case self._UiUpdateType.PAGE:
                    await self.page.update_async()
                case self._UiUpdateType.NO_UPDATE | _:
                    pass

            self.scheduled_ui_update = self._UiUpdateType.NO_UPDATE

            await asyncio.sleep(
                float(await self.persistent_storage.get("chat_update_rate"))
            )

    async def on_scroll(self, event: ft.OnScrollEvent):
        self.is_chat_scrolled_down = isclose(
            event.pixels, event.max_scroll_extent, rel_tol=0.01
        )
        self.scroll_down_btn.visible = not self.is_chat_scrolled_down
        await self.scroll_down_btn.update_async()

    async def add_author_to_user_set(self, author: str):
        tab_name = await self.persistent_storage.get("channel")

        # Get existing list from memory or initialize a new one
        if user_set := await self.memory_storage.get("channel_user_list"):
            if tab_name in user_set:
                user_set[tab_name].add(author)
            else:
                user_set[tab_name] = {author}
        else:
            user_set = {tab_name: {author}}

        logging.debug(f"User {author} added to {tab_name}'s user list")

        await self.memory_storage.set("channel_user_list", user_set)

    async def on_message(self, message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(
                message, self.page, await self.persistent_storage.get("chat_font_size")
            )
            await self.add_author_to_user_set(message.user.name)
            await m.subscribe_to_font_size_change(self.font_size_pubsub)
            await m.subscribe_to_show_timestamp_change(self.ts_pubsub)

        elif message.message_type == "login_message":
            m = ft.Text(
                message.elements[0],
                italic=True,
                size=await self.persistent_storage.get("chat_font_size"),
            )

        self.chat.controls.append(m)

        n_messages_to_remove = len(
            self.chat.controls
        ) - await self.persistent_storage.get("max_messages_per_chat")
        if n_messages_to_remove > 0:
            del self.chat.controls[:n_messages_to_remove]
            logging.debug(
                f"Chat has {len(self.chat.controls)} lines in it, removed {n_messages_to_remove}"
            )

        if self.is_chat_scrolled_down:
            self.scheduled_ui_update = self._UiUpdateType.SCROLL
        elif (
            self.scheduled_ui_update != self._UiUpdateType.SCROLL
        ):  # Scroll already updates
            self.scheduled_ui_update = self._UiUpdateType.PAGE
