dex.py(discordex)
==================================

dex.py is discord.py's extension.
`This <https://github.com/kiki7000/dex.py>`_ is the github repository

Features
--------

- command handler
- args parser

Example
--------

.. code:: python

    from discordex import DexBot
    bot = DexBot(command_prefix = '!')

    @bot.command(r'hello <str:name>')
    async def hello(ctx):
        await ctx.send(f'hi {ctx.args.name}')

    bot.run(token)
    


