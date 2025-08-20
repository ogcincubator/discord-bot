import discord, os, csv

BOT_TOKEN = os.getenv("BOT")

GUILD_ID = 874597684873400331

ROLE_NAME = "Attendee"

# USERNAMES_TO_ASSIGN_ROLE = [
#     "username1",
#     "another_user",
#     "ExampleUser",
# ]

CSV_FILENAME = "usernames.csv"

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """
    This function is called when the bot has successfully connected to Discord.
    """
    print(f'Logged in as {client.user}')

    USERNAMES_TO_ASSIGN_ROLE = []
    try:
        with open(CSV_FILENAME, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            # Read the first item from each row, ignoring empty rows.
            USERNAMES_TO_ASSIGN_ROLE = [rows[0] for rows in reader if rows]
        if not USERNAMES_TO_ASSIGN_ROLE:
            print(f"Warning: The CSV file '{CSV_FILENAME}' is empty or improperly formatted.")
            await client.close()
            return
        print(f"Successfully loaded {len(USERNAMES_TO_ASSIGN_ROLE)} usernames from '{CSV_FILENAME}'.")
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILENAME}' was not found. Please create it in the same directory as the script.")
        await client.close()
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        await client.close()
        return

    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(f"Error: Guild with ID {GUILD_ID} not found. Make sure the bot is in the server.")
        await client.close()
        return

    # Find the role to be assigned on the server.
    role_to_assign = discord.utils.get(guild.roles, name=ROLE_NAME)
    if not role_to_assign:
        print(f"Error: Role named '{ROLE_NAME}' not found on the server.")
        await client.close()
        return

    print(f"Successfully found guild: '{guild.name}' and role: '{role_to_assign.name}'")

    # Iterate through the list of usernames.
    for username in USERNAMES_TO_ASSIGN_ROLE:
        member = guild.get_member_named(username)

        # If get_member_named doesn't find the user (as it requires the discriminator),
        # we can iterate through all members to find a match for the username part.
        if not member:
            print(f"'{username}' not found with exact match. Searching through all members...")
            found_member = None
            for m in guild.members:
                if m.name.lower() == username.lower():
                    found_member = m
                    break
            member = found_member

        if member:
            # If the member is found, check if they already have the role.
            if role_to_assign in member.roles:
                print(f"'{member.name}' already has the '{role_to_assign.name}' role.")
            else:
                try:
                    # If they don't have the role, add it.
                    await member.add_roles(role_to_assign)
                    print(f"Successfully assigned the '{role_to_assign.name}' role to '{member.name}'.")
                    dm_message = f"Hello! You were checked-in in the **{guild}** server. Enjoy the code sprint!"
                    await member.send(dm_message)
                except discord.Forbidden:
                    print(f"Error: The bot does not have permissions to assign the '{role_to_assign.name}' role to '{member.name}'. Check the bot's role hierarchy.")
                except discord.HTTPException as e:
                    print(f"An error occurred while assigning the role to '{member.name}': {e}")
        else:
            # If the member is not found on the server.
            print(f"User '{username}' not found on the server.")

    # After processing all usernames, close the bot's connection.
    await client.close()

# Run the bot with your token.
try:
    client.run(BOT_TOKEN)
except discord.LoginFailure:
    print("Error: Invalid bot token provided. Please check your BOT_TOKEN.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")