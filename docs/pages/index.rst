dex.py(discordex)
==================================

dex.py is discord.py's extension.
`This <https://github.com/Team-Kat/dex.py>`_ is the github repository

Features
--------

- many extensions

Examples
--------

.. code:: python

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


Extension example
******************

.. code:: python

    from discordex import Extension

    class IamCuteExtension(Extension):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def on_load(self):
            print('I am cute')

        async def on_message(self, message):
            if message.author.id == self.bot.cute:
                await message.channel.send('You are cute')
    

