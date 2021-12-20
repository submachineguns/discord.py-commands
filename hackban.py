#hackban #not a cog command

@client.command(aliases=['hban'])
@commands.has_permissions(ban_members=True)
async def hackban(ctx, user: discord.User):
    if user in ctx.guild.members:
        emb = discord.Embed(description=f"<:error:867509993884614666> This user is already in the guild", color = 0xec6a6a) #{emoji name} {emoji id}
        await ctx.send(embed=emb, mention_author=False)

    else:
        await ctx.guild.ban(user)
        await ctx.send(f":thumbsup:")
        
#error handling

@hackban.error
async def hackban_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            
            em = discord.Embed(color = 0xd65c27)
            
            em.add_field(name = ";hackban", value = "```Syntax: ;hackban (user)\nExample: ;hackban 852669175580958780```")

            await ctx.send(embed = em)
