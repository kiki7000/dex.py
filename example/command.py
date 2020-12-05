# 모듈화
from discordex import Command, CommandGroup


class Sans(Command):
    async def before_run(self, ctx):
        pass

    async def run(self, ctx, name):
        await ctx.send(f'hi {ctx.args.name} I\'m {self.bot.user.name}!')

    async def after_run(self, ctx):
        pass

    async def errorhandler(self, ctx, error):
        pass


def setup(bot):
    async def asdf(ctx):
        await ctx.send('extension!')

    cmd = Sans(bot)
    cmd.use(asdf, check=True)  # bot.use(cmd, asdf, check = True)
    bot.add_command(r'hello <str:name>', cmd, aliases=[r'sans <str:name>'], bot_permission=['kick_members'])

r'hello <longstr:desc>'
# or
@bot.command(r'hello <str:name>', aliases=[r'sans <str:name>'], bot_permission=['kick_members'])
@bot.use_ext()
class Sans(Command):
    async def before_execute(self, ctx):
        pass

    async def execute(self, ctx, name):
        await ctx.send(f'hi {ctx.args.name} I\'m {self.bot.user.name}!')

    async def after_execute(self, ctx):
        pass

    async def error_handler(self, ctx, error):
        print_exc()
