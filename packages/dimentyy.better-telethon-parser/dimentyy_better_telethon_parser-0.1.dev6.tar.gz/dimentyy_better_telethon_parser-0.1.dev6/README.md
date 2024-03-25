# Better [Telethon](https://pypi.org/project/Telethon/) parser
Standard parsing modes aren't good enought, so I created my own :like: 

---
### How to apply parser?

```python
from telethon import TelegramClient
from dimentyy.btp import BetterParsing

# initialize client
client = TelegramClient(**...)
client.parse_mode = BetterParsing.HTML()
```
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
- [x] One filled checkbox
- [ ] Implementation of all formatting entities
- [ ] Better naming
- [ ] Options?
- [ ] Error handling
- [ ] Unparsing
- [ ] Documenting
