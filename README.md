# ***D**iscordpy **Ex**tension*

<a href = "https://travis-ci.com/github/Team-Kat/dex.py"><img src = "https://travis-ci.com/Team-Kat/dex.py.svg?token=DkyrrJTQxucGFxZuyzo5&branch=master"></a>
<a href = "https://pypi.org/project/dex.py/"><img src = "https://badge.fury.io/py/dex.py.svg" /></a>
<a href="https://www.codacy.com/gh/Team-Kat/dex.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Team-Kat/dex.py&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/30cfe9c820b64a4a9b7a40163ed1bffd"/></a>
<a href = "https://dexpy.readthedocs.io/en/latest/?badge=latest"><img src = "https://readthedocs.org/projects/dexpy/badge/?version=latest" /></a><br />

Dex.py is a module that allows you to use various extensions in discord.py. There are many built-in extensions so you could develop dex.py more easily

## Install
Install and update using pip:
```
pip install dex.py
```

## Example
```py
from discord import Client
from discordex import Dex
from discordex.extensions.handler import Handler

bot = Client()
dex = Dex(bot)

dex.add(Handler(
    use_cmd = True,
    use_events = False,
    sub_routes = True
))

bot.run(token)
```