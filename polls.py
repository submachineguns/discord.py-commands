import asyncio
import colorama
import random
import discord
import discord.ext.commands as commands


def setup(bot):
    bot.add_cog(Polls(bot))


class Polls(commands.Cog):
    """Polls commands"""
    def __init__(self, bot):
        self.bot = bot
        self.keycaps_emojis = [f'{i}\u20e3' for i in range(1, 10)]
        self.keycaps_emojis.append('\N{KEYCAP TEN}')

    @commands.command(name='instantpoll', aliases=['ip'])
    @commands.guild_only()
    async def instant_poll(self, ctx, title, *options):
        if len(options) > 10:
            raise commands.BadArgument('Too many options, max is 10')

        
        poll = discord.Embed(title=title, color = 0x000000)
        poll.description = '\n'.join(f'{self.keycaps_emojis[i]} {o}' for i, o in enumerate(options))
        poll.set_author(name=f'{ctx.author.display_name} ({ctx.author})', icon_url=ctx.author.avatar_url)

        message = await ctx.send(embed=poll)
        for i in range(len(options)):
            await message.add_reaction(self.keycaps_emojis[i])

    @commands.command()
    @commands.guild_only()
    async def poll(self, ctx):
        to_delete = [ctx.message]

        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        # Start with the poll's title
        emb = discord.Embed(description=f"{ctx.author.mention}: What do you want to name the title?", color=0x242526)
        await ctx.send(embed=emb)
        try:
            title = await ctx.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            raise commands.UserInputError(f'{ctx.author.mention} You took too long')
        to_delete.append(title)

        # Loop and register the poll's options until the user says we're done
        options = []
        while True:
            emb = discord.Embed(description=f"Type **No more options** if none\n\n{ctx.author.mention}: What will be entry #{len(options) + 1}?", color=0x242526)
            await ctx.send(embed=emb)
            try:
                entry = await ctx.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                raise commands.UserInputError(f'{ctx.author.mention} You took too long')
            to_delete.append(entry)

            if entry.content.lower() == 'no more options':
                break
            options.append(entry.content)

        # Create the poll
        await ctx.invoke(self.instant_poll, title.content, *options)

        # Cleanup
        try:
            await ctx.channel.delete_messages(to_delete, reason='Poll command cleanup.')
        except:
            pass