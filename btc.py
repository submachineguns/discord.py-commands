@client.command(aliases=['bitcoin'])
async def btc(ctx):
	r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR')
	r = r.json()
	usd = r['USD']
	eur = r['EUR']
	embed = discord.Embed(color=(0xf2a900))
	embed.description=f'**{str(usd)}$ USD**'
	embed.set_author(name='Bitcoin', icon_url='https://media.discordapp.net/attachments/806971294795956254/808381684012810310/600.png?width=480&height=480')
	embed.set_footer(text='updated bitcoin prices to this hour')
	await ctx.send(embed=embed)
