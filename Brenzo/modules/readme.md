## ⇝ Write new modules ⇜ 

```
from Brenzo.app import app
from Brenzo.module.mod import mod
from Brenzo.modules.tr_engine.strings import tld 

@register(cmds="Hi")
@disableable_dec("Hi")
async def _(message):
    j = "Hello there"
    await message.reply(j)
    
__mod_name__ = "Hi"
__help__ = True

dispatcher.add_handler()
dispatcher.add_handler()
"""
```

#### You can add help and mod name string at Locales for your module .
