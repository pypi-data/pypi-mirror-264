from abc import ABC, abstractmethod

import flet as ft
import validators

from hasherino.hasherino_dataclasses import Emote, Message
from hasherino.pubsub import PubSub


class FontSizeSubscriber(ABC):
    @abstractmethod
    async def on_font_size_changed(self, new_font_size: int):
        ...


class ShowTimestampSubscriber(ABC):
    @abstractmethod
    async def on_show_timestamp_changed(self, show_timestamp: bool):
        ...


class ChatText(ft.Container, FontSizeSubscriber):
    def __init__(self, text: str, color: str, size: int, weight=""):
        try:
            is_url = validators.url(text)
        except validators.ValidationError:
            is_url = False

        color = ft.colors.BLUE if is_url else color
        self.content = ft.Text(
            text, size=size, weight=weight, color=color, selectable=True
        )
        super().__init__(content=self.content, url=text)

    async def on_font_size_changed(self, new_font_size: int):
        self.content.size = new_font_size


class ChatBadge(ft.Image, FontSizeSubscriber):
    def __init__(self, src: str, height: int):
        super().__init__(src=src, height=height)

    async def on_font_size_changed(self, new_font_size: int):
        self.height = new_font_size


class ChatEmote(ft.Container, FontSizeSubscriber):
    def __init__(self, *args, **kwargs):
        self.emote: Emote | None = kwargs.pop("emote", None)
        super().__init__(
            content=ft.Image(
                tooltip=self.emote.name if self.emote else "", *args, **kwargs
            ),
        )

    async def on_font_size_changed(self, new_font_size: int):
        self.height = new_font_size * 2


class ChatTimestamp(ft.Text, ShowTimestampSubscriber, FontSizeSubscriber):
    def __init__(self, text: str, color: str, size: int):
        super().__init__(text, size=size, color=color, selectable=False)

    async def on_show_timestamp_changed(self, show_timestamp: bool):
        self.visible = bool(show_timestamp)

    async def on_font_size_changed(self, new_font_size: int):
        self.size = max(new_font_size - 4, 4)


class ChatMessage(ft.Row):
    def __init__(self, message: Message, page: ft.Page, font_size: int):
        super().__init__()
        self.vertical_alignment = "start"
        self.wrap = True
        self.width = page.width
        self.page = page
        self.font_size = font_size
        self.spacing = 2
        self.run_spacing = 0
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

        self.add_control_elements(message)

    def add_control_elements(self, message):
        if message.timestamp is not None:
            self.controls.append(
                ChatTimestamp(
                    text=f"{message.timestamp.strftime('%H:%M')} ",
                    color=ft.colors.GREY,
                    size=max(self.font_size - 4, 4),
                )
            )

        self.controls.extend(
            [ChatBadge(badge.url, self.font_size) for badge in message.user.badges]
        )

        self.controls.append(
            ChatText(
                f"{message.user.name}: ",
                message.user.chat_color,
                self.font_size,
                weight="bold",
            )
        )

        for element in message.elements:
            if type(element) is str:
                color = message.user.chat_color if message.me else ""
                result = ChatText(element, color, self.font_size)
            elif type(element) is Emote:
                result = ChatEmote(
                    emote=element, src=element.url, height=self.font_size * 2
                )
            else:
                raise TypeError

            self.controls.append(result)

    async def subscribe_to_font_size_change(self, pubsub: PubSub):
        await pubsub.subscribe_all(
            [
                control.on_font_size_changed
                for control in self.controls
                if isinstance(control, FontSizeSubscriber)
            ]
        )

    async def subscribe_to_show_timestamp_change(self, pubsub: PubSub):
        await pubsub.subscribe_all(
            [
                control.on_show_timestamp_changed
                for control in self.controls
                if isinstance(control, ShowTimestampSubscriber)
            ]
        )
