from dataclasses import dataclass, field
from html import parser as html_parser

from telethon.tl.types import TypeMessageEntity, MessageEntityBold, MessageEntityItalic, MessageEntityUnderline, MessageEntityCode, MessageEntityTextUrl, MessageEntityMentionName, MessageEntityPre, MessageEntitySpoiler, MessageEntityBlockquote, MessageEntityStrike, MessageEntityCustomEmoji

plain_entities = {MessageEntityBold, MessageEntityItalic, MessageEntityUnderline, MessageEntityStrike, MessageEntityCode, MessageEntitySpoiler, MessageEntityBlockquote}

type Entities = list[TypeMessageEntity]
type Bundle = tuple[str, Entities]


class _HTMLParser(html_parser.HTMLParser):
    entity_tags = {
        "b": MessageEntityBold,
        "i": MessageEntityItalic,
        "u": MessageEntityUnderline,
        "s": MessageEntityStrike,
        "a": MessageEntityTextUrl,
        "link": MessageEntityTextUrl,
        "code": MessageEntityCode,
        "pre": MessageEntityPre,
        "mention": MessageEntityMentionName,
        "spoiler": MessageEntitySpoiler,
        "quote": MessageEntityBlockquote,
        "custom_emoji": MessageEntityCustomEmoji
    }

    entities_tag_attr_args = {
        "a": {"href": ("url", str, None)},
        "link": {"url": ("url", str, None)},
        "pre": {"language": ("language", str, '')},
        "mention": {"user_id": ("user_id", int, None)},
        "custom_emoji": {"document_id": ("document_id", int, None)},
    }

    def __init__(self):
        super().__init__()

        self.container = ParsingContainer()

    def handle_starttag(self, tag: str, raw_attrs: list[tuple[str, any]]):
        if tag not in self.entity_tags:
            return

        if (entity := self.entity_tags[tag]) in plain_entities:
            return self.container.open_entity(entity)

        attrs = dict(raw_attrs)

        return self.container.open_entity(entity, **{
            arg_name: (None if attrs[attr] is None else arg_type(attrs[attr])) if attr in attrs else default

            for attr, (arg_name, arg_type, default) in self.entities_tag_attr_args[tag].items()
        })

    def handle_endtag(self, tag: str):
        self.container.close_entity(self.entity_tags[tag])

    def handle_data(self, data: str):
        self.container.feed_text(data)

    def feed_and_get_bundle(self, text: str) -> Bundle:
        self.feed(text)
        return self.container.bundle

    def feed_and_get_raw_text(self, text: str) -> str:
        self.feed(text)
        return self.container.raw_text

    @classmethod
    def onetime_use(cls, text: str) -> Bundle:
        return cls().feed_and_get_bundle(text)


class ParsingContainer:
    def __init__(self):
        self.raw_text: str = ""
        self.entities: Entities = []

        self.unclosed_entities: dict[type[TypeMessageEntity], int] = {}
        self.unclosed_entities_args: dict[type[TypeMessageEntity], dict[str, str | int]] = {}

    def feed_text(self, text: str):
        self.raw_text += text

    def open_entity(self, entity: type[TypeMessageEntity], **args: str | int):
        self.unclosed_entities[entity] = self.raw_text_tl_len
        self.unclosed_entities_args[entity] = args

    def close_entity(self, entity: type[TypeMessageEntity], **args: str | int):
        if None in (args := args or self.unclosed_entities_args.pop(entity, {...: None})).values(): return

        offset = self.unclosed_entities.pop(entity, 0)

        self.entities.append(entity(
            offset=offset,
            length=self.raw_text_tl_len - offset,
            **args
        ))

    @property
    def raw_text_tl_len(self) -> int:
        return len(self.raw_text.encode('utf-16-le')) // 2

    def __iter__(self):
        return iter(self.bundle)

    @property
    def bundle(self) -> Bundle:
        return self.raw_text, self.entities


class BetterParsing:
    class HTML:
        def parse(self, text: str) -> Bundle:
            return _HTMLParser.onetime_use(text)

        def unparse(self, raw_text: str, entities: Entities):
            # entities = sorted(entities, key=lambda entity: entity.offset)
            raise NotImplemented


__all__ = [
    'BetterParsing'
]
