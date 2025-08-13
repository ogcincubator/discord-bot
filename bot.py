import os
import discord
from discord.ext import commands

# --- Configuration ---
BOT_TOKEN = os.getenv("BOT")
print (BOT_TOKEN)
GUILD_ID = 874597684873400331 
COMMAND_PREFIX = "!"
# ---------------------

# Define the intents your bot needs
intents = discord.Intents.default()
intents.members = True  # Enable the members intent
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
@bot.event
async def on_ready():
    """Event that runs when the bot has connected to Discord."""
    print(f'Logged in as {bot.user}')
    print('Bot is ready to receive commands.')

@bot.command(name='assignrole')
@commands.has_permissions(manage_roles=True) # Checks if the command author has "Manage Roles" permission
async def assign_role(ctx, member_name: str, role_name: str):
    """
    Assigns a role to a user and notifies them via DM.

    Usage: !assignrole "Username#1234" "Role Name"
    """
    try:
        # Find the member in the guild. This is more robust than searching by name alone.
        member = await commands.MemberConverter().convert(ctx, member_name)

        # Find the role in the guild by its name.
        # Note: Role names are case-sensitive.
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if not role:
            await ctx.send(f"The role '{role_name}' was not found on this server.")
            return

        # Add the role to the member
        await member.add_roles(role)

        # --- New DM Functionality ---
        dm_message = f"Hello! You were checked-in in the **{ctx.guild.name}** server. Enjoy the code sprint!"
        
        try:
            # Attempt to send a DM to the user
            await member.send(dm_message)
            # Send confirmation to the channel that the role was added and DM was sent
            await ctx.send(f"Successfully assigned the '{role.name}' role to {member.mention}. I have also notified them via DM.")
        except discord.Forbidden:
            # This happens if the user has DMs disabled or blocked the bot.
            await ctx.send(f"Successfully assigned the '{role.name}' role to {member.mention}, but I could not send them a DM as their DMs are private.")
        # --- End of DM Functionality ---

    except commands.MemberNotFound:
        await ctx.send(f"Could not find a member named '{member_name}'. Please make sure you provide their full username and discriminator (e.g., 'Username#1234').")
    except discord.Forbidden:
        await ctx.send("I don't have the necessary permissions to assign roles. Please check my role hierarchy and permissions in the server settings.")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")

# Run the bot with the token from the environment variable
bot.run(BOT_TOKEN)