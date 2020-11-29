dex.py(discordex)
==================================

dex.py is discord.py's extension.

Features
--------

- command handler
- args parser

Example
--------

.. code:: python

    from discordex import DexBot
    bot = DexBot(command_prefix = '!')

    @bot.command(r'안녕 <str:name>')
    async def hello(ctx, name: str):
        await ctx.send(f'ㅎㅇ {name}')

    bot.run(token)
    


