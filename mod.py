from asyncio import sleep
from datetime import datetime, timedelta
from re import search
from typing import Optional

from discord import Embed, Member, NotFound, Object
from discord.utils import find
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions

class Mod(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_message(self, message):
		def _check(m):
			return (m.author == message.author
					and len(m.mentions)
					and (datetime.utcnow()-m.created_at).seconds < 60)

		if not message.author.bot:
			if len(list(filter(lambda m: _check(m), self.bot.cached_messages))) >= 3:
				await message.channel.send("Stop Pinging", delete_after=10)
				await self.kick_members(message, [message.author], 5, reason="Spam Pinging")
            

			self.bot.cogs_ready.ready_up("mod")

def setup(bot):
	bot.add_cog(Mod(bot))