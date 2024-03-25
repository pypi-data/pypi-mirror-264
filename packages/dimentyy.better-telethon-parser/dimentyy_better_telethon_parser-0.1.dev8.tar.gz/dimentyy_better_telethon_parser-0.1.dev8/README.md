# Better [Telethon](https://pypi.org/project/Telethon/) parser
Standard parsing modes aren't good enought, so I created my own 👍

---
### How to apply the parser?

```python
from telethon import TelegramClient
from dimentyy.btp import BetterParsing

# initialize a client
client = TelegramClient(**...)

# here's everything needed 👇 done.
client.parse_mode = BetterParsing.HTML()
```

### About formatting entities
Telegram: https://core.telegram.org/type/MessageEntity \
Telethon: https://tl.telethon.dev/types/message_entity.html

---
# HTML implementation

### Tags & attributes mapped to formatting entities, 
 &ast; `...` means input text to format

 - `MessageEntityBold` — `<b>...</b>`
 - `MessageEntityItalic` — `<i>...</i>`
 - `MessageEntityUnderline` — `<u>...</u>`
 - `MessageEntityStrike` — `<s>...</s>`
 - `MessageEntityCode` — `<code>...</code>`
 - `MessageEntitySpoiler` — `<spoiler>...</spoiler>`
 - `MessageEntityBlockquote` — `<quote>...</quote>`
 - `MessageEntityTextUrl` where `{URL}` is "The actual URL" [**[???](https://core.telegram.org/constructor/messageEntityTextUrl)**]
   - `<a href="{URL}">...</a>`
   - `<link url="{URL}">...</link>`
 - `MessageEntityPre` where `{LANG}` is "Programming language of the code" [**[???](https://core.telegram.org/constructor/messageEntityPre)**]
   - `<pre language="{LANG}">...</pre>`
   - `<pre>...</pre>` to not specify language 
 - `MessageEntityMentionName` where `{ID}` is "ID of the user that was mentioned" [**[???](https://core.telegram.org/constructor/inputMessageEntityMentionName)**]
   - `<mention user_id={ID}>...</mention>` —
 - `MessageEntityCustomEmoji` where `{ID}` is "Document ID of the custom emoji" [**[???](https://core.telegram.org/constructor/messageEntityCustomEmoji)**] and `{EMOJI}` is "Exactly one regular emoji"
   - `<custom_emoji document_id={ID}>{EMOJI}</custom_emoji>` 

&ast; offset & length are filled automatically!

### Examples
 - `<b>Bold text</b>`
   - Raw text: `"Bold text"`
   - Entities: `[MessageEntityBold(offset=0, length=9)]`


 - `<mention user_id=490288812>t.me/dimentyy</mention>`
   - Raw text: `"t.me/dimentyy"`
   - Entities: `[MessageEntityMentionName(offset=0, length=13, user_id=490288812)]`

---
### Quick description
```python
from telethon.tl.types import TypeMessageEntity

type Entities = list[TypeMessageEntity]
type Bundle = tuple[str, Entities]

class BetterParsing:
    class HTML:
        def __init__(self): ...
        def parse(self, text: str) -> Bundle: ...
        def unparse(self, raw_text: str, entities: Entities) -> str: ...
```
---

### Current state
- [x] First filled checkbox
- [ ] Implementation for all formatting entities
- [ ] Better naming
- [ ] Options?
- [ ] Error handling
- [ ] Unparsing
- [ ] Documenting
---

### Please don't look at source code
Thank you 🥺
