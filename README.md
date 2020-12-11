<div align = "center">
    <img src = ".github/dex.png" style = "margin-top: 50px;" width = "350px" height = "100px"><br /><br />
    <a href = "https://travis-ci.com/github/kiki7000/dex.py"><img src = "https://travis-ci.com/kiki7000/dex.py.svg?token=DkyrrJTQxucGFxZuyzo5&branch=master"></a>
    <a href = "https://pypi.org/project/dex.py/"><img src = "https://badge.fury.io/py/dex.py.svg" /></a>
    <a href = "https://dexpy.readthedocs.io/en/latest/?badge=latest"><img src = "https://readthedocs.org/projects/dexpy/badge/?version=latest" /></a><br />
    <i style = "font-size: 18px"><b>d</b>iscord.py <b>ex</b>tension</i><br />
</div>

Dex.py is a module that allows you to use various extensions in discord.py. There are many built-in extensions so you could develop dex.py more easily

## Install
Install and update using pip:
```
pip install dex.py
```

## Example
```py
from discordex import DexBot
bot = DexBot('!')

@bot.command('myname <str:name>')
def myname(ctx):
    await ctx.send(f'hello {ctx.nargs.name}')

bot.run('Very Very secret token')
```