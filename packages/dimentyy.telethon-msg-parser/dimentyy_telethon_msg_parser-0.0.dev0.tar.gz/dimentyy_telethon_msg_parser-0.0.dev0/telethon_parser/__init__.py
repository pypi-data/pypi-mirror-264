from html import parser as html_parser

from telethon.tl.types import TypeMessageEntity, MessageEntityBold, MessageEntityItalic, MessageEntityUnderline, MessageEntityCode, MessageEntityTextUrl, MessageEntityMentionName


class TelethonHTMLParser(html_parser.HTMLParser):
    entity_tags = {
        "b": MessageEntityBold,
        "i": MessageEntityItalic,
        "u": MessageEntityUnderline,
        "m": MessageEntityCode,
        "link": MessageEntityTextUrl,
        "mention": MessageEntityMentionName
    }

    def __init__(self):
        super().__init__()

        self.container = TelethonParser()
        self.entity_attrs: dict[str, dict[str]] = {}

    def handle_starttag(self, tag: str, attrs: dict[str]):
        self.container.open_entity(self.entity_tags[tag])
        self.entity_attrs[tag] = {key: value for key, value in attrs}

    def handle_endtag(self, tag: str):
        self.container.close_entity(self.entity_tags[tag], **self.entity_attrs.pop(tag))

    def handle_data(self, data: str):
        self.container.feed_text(data)


class TelethonParser:
    def __init__(self):
        self.raw_text: str = ""
        self.entities: list[TypeMessageEntity] = []
        self.unclosed_entities: dict[type[TypeMessageEntity], int] = {}
        self.unclosed_entity_args: dict[type[TypeMessageEntity], dict[str, str | int]] = {}

    @staticmethod
    def parse(text: str) -> tuple[str, list[TypeMessageEntity]]:
        parser = TelethonHTMLParser()
        parser.feed(text)
        return parser.container.raw_text, parser.container.entities

    @staticmethod
    def unparse(raw_text: str, entities: list[TypeMessageEntity]):
        # entities = sorted(entities, key=lambda entity: entity.offset)
        raise NotImplemented

    def feed_text(self, text: str):
        self.raw_text += text

    def open_entity(self, entity: type[TypeMessageEntity], **args: str | int):
        self.unclosed_entities[entity] = self.raw_text_tl_len
        self.unclosed_entity_args[entity] = args

    def close_entity(self, entity: type[TypeMessageEntity], **args: str | int):
        offset = self.unclosed_entities.pop(entity, 0)

        self.entities.append(entity(
            offset=offset, length=self.raw_text_tl_len - offset,
            **args or self.unclosed_entity_args.pop(entity, {})
        ))

    @property
    def raw_text_tl_len(self) -> int:
        return len(self.raw_text.encode('utf-16-le')) // 2


__all__ = [
    'TelethonParser'
]
