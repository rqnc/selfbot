import os

os.system('pip uninstall discord.py')
os.system('pip install -U discord.py-self')
import discord
from discord.ext import commands
import colorama
from colorama import Fore
import wavelink
import platform
import psutil
import datetime
import asyncio
import random
import string
from datetime import timedelta
import time

client = commands.Bot(command_prefix=["3"], help_command=None)

afk_users = {}
SUPREME_OWNER_IDS = [1293491746210189384]
allowed_users = {}  
custom_lines = [
 "{user} Bhossdikee madarrchood bhen k lodee",
 "maachar ki jhaaant {user} gandu ...maa ki chut teri tatto ke soudagar ",
 "{user} Kutte ke moot, teri maa ki choot..",
 "Lavde ke bal {user} Lund Chus bsdk",
 "{user} Lund Ke Pasine",
 "{user} Meri Gand Ka Khatmal ",
 "{user} Najayaz paidaish ",
 "{user} Teri maa ke Rundi khana mei 500rs daan dedunga",
 "{user} Sadi hui gaand",
 "{user} Teri gaand main kute ka lund",
 "{user} Teri maa ka bhosda",
 "{user} Teri maa ki chut",
 "{user} Tere gaand mein keede paday",
 "{user} Ullu ke pathe",
 "{user} Phatele Nirodh Ke Natije!",
 "{user} Chut Ka Maindak…",
 "{user} Abla Naari, Tere maa ke Bable Bhaari…",
 "{user} Chut Ke Pasine Mein Talay Hue Bhajiye…",
 "{user} Chullu Bhar Muth Mein Doob Mar!",
 "{user} Kaali Chut Ke Safed Jhaant…",
 "{user} Teri Gaand Mein Kutte Ka Lund…",
 "{user} Teri Jhaatein Kaat Kar Tere Mooh Par Laga Kar Unki French BeardBanaDoonga!",
 "{user} Maderchod-Bhosadike-Bhen-chod-Beti-chodd BhadhavaChoduGaandGaanduGadha",
 "{user} BaklandLauda",
 " Lund Hijra Kuttiya ka Paad Randi Saala kutta Saali kutti Tatti Kamina {user}",
 "{user} Chut ke pasine mein talay huye bhajiye",
 "{user} Teri maa ki chut",
"{user} ke. Lode",
"{user} Teri maa ko chodu",
"{user} Teri maa ki gaand mai mera lund",
"{user} Teri maa ki bhosdi",
"{user} Teri maa ki gaand mai hatthi ka lund",
"{user} Haveli ke piche jhopda teri maa ka bhosda",
"{user} Tu meri andheri raat ki galti hai ",
"{user} Maa ke lode na us raat mai garam hota or na teri maa ko chodta or na tu nikalta",
"{user} Maaa ke lode maa ki chut teri",
"{user} Bhosad chod",
"{user} Andi bandi sandi teri maa randi",
"{user} Ek shyari teri maa ke liye",
"{user} *Shi shi bhari gula ki shi shi bhari gulab ki patthar pr fod du aa beth mere lode pr tuje jhadiyo mai chod du* ",
"{user} Teri maa ne tere baap ko choda",
"{user} Teri maa mai se nhi tere baap mai se nikla tu",
"{user} Teri maa ki bhosdi",
"{user} Teri maa ko chodu sari raat",
"{user} Teri masi ka lund. ",
"{user} Maa ke lode maaa chuda tu",
"{user} Teri esi maa chodunga pura khandan dekhta rahega Yahha se lunnd fek ke marunga bc waha jake girega",
"{user} Madarchod bhosdiwale chacha ke bete teri maa ka lund",
"{user} Teri maa ka lund or tere baap ka bhosda",
"{user} Lawde dalle bhosdeke jhatt ke pille bhikari ek alaulad {user} randwe kutte ke chode madharchod randwe ",
"{user} tere maa  jonny sins se chodwaunga worker ko khodna aur baap ko chodna mat sikha bund me dum nahi hai aur baap se lade aa jata hai lund khada karna sikh pahle sutta hu lund leke aapne aap ko chodeba tohre crush ko japane sadh ak tel laga ke chodbaye"
]

colorama.init(autoreset=True)
loop_status = {}
client.uptime = datetime.datetime.now()

@client.command(name='unban')
async def unban(ctx, user_id: int):
    if not is_allowed(ctx, "unban"):
        return
    try:
        user = await client.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned {user.mention}.")
    except discord.NotFound:
        await ctx.send("User not found in the ban list.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")




@client.command(name='mute')
async def mute(ctx, member: discord.Member, duration: int = 5, *, reason: str = "No reason provided"):
    """
    Mutes (timeouts) a member for a specified duration in minutes.
    Usage: 3mute @member [duration_in_minutes] [reason]
    """
    if not is_allowed(ctx, "mute"):
        return
    try:
        timeout_until = discord.utils.utcnow() + timedelta(minutes=duration)
        await member.timeout(until=timeout_until, reason=reason)
        await ctx.send(f"{member.mention} has been muted for {duration} minutes. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to mute this user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.command(name='unmute')
async def unmute(ctx, member: discord.Member):
    """
    Removes timeout from a muted member.
    Usage: 3unmute @member
    """
    if not is_allowed(ctx, "unmute"):
        return
    try:
        await member.timeout(until=None)  
        await ctx.send(f"{member.mention} has been unmuted.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to unmute this user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.command(name="add_allowed")
async def add_allowed(ctx, user_id: int, command_name: str):
    """Allows a user to use a specific command."""
    if ctx.author.id not in SUPREME_OWNER_IDS:
        return await ctx.send("You are not authorized to use this command.")
    if user_id not in allowed_users:
        allowed_users[user_id] = []
    if command_name not in allowed_users[user_id]:
        allowed_users[user_id].append(command_name)
        await ctx.send(f"User {user_id} has been allowed to use the `{command_name}` command.")


@client.command(name="remove_allowed")
async def remove_allowed(ctx, user_id: int, command_name: str):
    """Revokes a user's permission to use a specific command."""
    if ctx.author.id not in SUPREME_OWNER_IDS:
        return await ctx.send("You are not authorized to use this command.")
    if user_id in allowed_users and command_name in allowed_users[user_id]:
        allowed_users[user_id].remove(command_name)
        await ctx.send(f"User {user_id} is no longer allowed to use the `{command_name}` command.")

def is_allowed(ctx, command_name):
    return ctx.author.id in SUPREME_OWNER_IDS or \
           ctx.author.id in allowed_users and command_name in allowed_users[ctx.author.id]


@client.command(name='ping')
async def ping(ctx):
    if not is_allowed(ctx, "ping"):
        return
    await ctx.send(f"🏓Pong: {round(client.latency * 1000)}ms")


@client.command(name='info')
async def info(ctx):
    """
    Displays bot information, system statistics, and uptime.
    Usage: 3info
    """
    if not is_allowed(ctx, "info"):
        return

    try:
        now = datetime.datetime.now(datetime.timezone.utc)  
        uptime = now - client.uptime

        python_version = platform.python_version()
        discord_version = discord.__version__

        try:
            memory_usage = psutil.Process().memory_info().rss / 1024**2  
        except (PermissionError, AttributeError):
            memory_usage = "Unavailable"

        try:
            cpu_usage = psutil.cpu_percent(interval=1)  
        except (PermissionError, AttributeError):
            cpu_usage = "Unavailable"

        info_text = (
            f"```ini\n[ Bot Information ]\n```\n"
            f"```yaml\n"
            f"Uptime: {str(uptime).split('.')[0]} (hh:mm:ss)\n"
            f"Python Version: {python_version}\n"
            f"Discord.py Version: {discord_version}\n"
            f"Memory Usage: {memory_usage if memory_usage != 'Unavailable' else 'N/A'} MB\n"
            f"CPU Usage: {cpu_usage if cpu_usage != 'Unavailable' else 'N/A'}%\n"
            f"```\n"
            f"```ini\n[ Additional Info ]\n```\n"
            f"Owner: <@{SUPREME_OWNER_IDS[0]}>\n"
            f"Guilds: {len(client.guilds)}\n"
            f"Users: {len(client.users)}\n"
            f"Requested by: {ctx.author}\n"
        )

        await ctx.send(info_text)
    except Exception as e:
        await ctx.send(f"An error occurred while fetching info: {e}")


@client.command(name='servertour')
async def servertour(ctx, member: discord.Member, duration: int = 100):
    """
    Moves a user through all voice channels for a specified duration.
    Usage: 3servertour @user [duration_in_seconds]
    """
    if not is_allowed(ctx, "servertour"):
        return

    if not member.voice:
        await ctx.send(f"• {member.mention} is not in a voice channel!")
        return

    channels = [channel for channel in ctx.guild.channels if isinstance(channel, discord.VoiceChannel)]
    if not channels:
        await ctx.send("• *No voice channels available in this server.*")
        return

    initial_channel = member.voice.channel
    await ctx.send(f"• *Starting server tour for {member.mention}.*")

    end_time = time.time() + duration
    channel_index = 0

    try:
        while time.time() < end_time:
            target_channel = channels[channel_index]
            await member.move_to(target_channel)

            channel_index = (channel_index + 1) % len(channels)

        await member.move_to(initial_channel)
        await ctx.send(f"• *Server tour for {member.mention} is complete.*")
    except discord.Forbidden:
        await ctx.send("• *I don't have permission to move members!*")
    except discord.HTTPException as e:
        await ctx.send(f"• *An error occurred: {e}*")
    except Exception as e:
        await ctx.send(f"• *Unexpected error: {e}*")

vccycle_banned_users = {}

@client.command(name='vccycleban')
async def vccycleban(ctx, member: discord.Member):
    """
    Continuously moves a user through all voice channels whenever they join a channel.
    Usage: 3vccycleban @user
    """
    if not is_allowed(ctx, "vccycleban"):  
        return await ctx.send("You are not authorized to use this command.")
    
    if member.id in vccycle_banned_users:
        return await ctx.send(f"{member.mention} is already under vccycleban.")

    vccycle_banned_users[member.id] = True
    await ctx.send(f"{member.mention} has been placed under vccycleban. They will be cycled through voice channels upon joining.")


@client.command(name='vccycleunban')
async def vccycleunban(ctx, member: discord.Member):
    """
    Stops the vccycleban for a user.
    Usage: 3vccycleunban @user
    """
    if not is_allowed(ctx, "vccycleunban"):  
        return await ctx.send("You are not authorized to use this command.")
    
    if member.id not in vccycle_banned_users:
        return await ctx.send(f"{member.mention} is not under vccycleban.")
    
    del vccycle_banned_users[member.id]
    await ctx.send(f"{member.mention} has been removed from vccycleban.")



@client.event
async def on_voice_state_update(member, before, after):
    """
    Detects when a user joins a voice channel and starts the vccycleban process if they are banned.
    """
    if member.id not in vccycle_banned_users:
       return
    if after.channel:  
        guild = member.guild
        channels = [channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)]

        if not channels:
           return
        async def cycle_user():
            current_channel_index = 0
            while member.id in vccycle_banned_users and member.voice:  
                target_channel = channels[current_channel_index]
                try:
                    await member.move_to(target_channel)
                except discord.Forbidden:
                    return  
                except discord.HTTPException:
                    return  

                current_channel_index = (current_channel_index + 1) % len(channels)

        await cycle_user()


@client.command(name='nick')
async def nick(ctx, member: discord.Member, *, new_nick: str = None):
    if not is_allowed(ctx, "nick"):
        return
    try:
        await member.edit(nick=new_nick)
        await ctx.send(f"Changed nickname for {member.mention} to `{new_nick}`.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change that user's nickname.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.command(name='clearnick')
async def clearnick(ctx, member: discord.Member):
    if not is_allowed(ctx, "clearnick"):
        return
    try:
        await member.edit(nick=None)
        await ctx.send(f"Cleared nickname for {member.mention}.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to clear that user's nickname.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@client.command(name='ban')
async def ban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    if not is_allowed(ctx, "ban"):
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban that user.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='vcban')
async def vcban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """
    Disconnects and bans a user from all voice channels in the server.
    Usage: 3vcban @user [reason]
    """
    if not is_allowed(ctx, "vcban"):
        return
    try:
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(member, connect=False)  
        if member.voice:
            await member.move_to(None)  
        await ctx.send(f"{member.mention} has been voice banned. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to modify voice channel permissions.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='vcunban')
async def vcunban(ctx, member: discord.Member):
    """
    Unbans a user from all voice channels in the server.
    Usage: 3vcunban @user
    """
    if not is_allowed(ctx, "vcunban"):
        return
    try:
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(member, overwrite=None)  
        await ctx.send(f"{member.mention} can now join voice channels again.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to modify voice channel permissions.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

chat_banned_users = {}

@client.command(name='chatban')
async def chatban(ctx, member: discord.Member, *, reason: str = "No reason provided"):
    """
    Adds a user to the internal chat-banned list.
    Usage: 3chatban @user [reason]
    """
    if not is_allowed(ctx, "chatban"):
        return

    chat_banned_users[member.id] = reason
    await ctx.send(f"{member.mention} has been chat banned. Reason: {reason}")

@client.command(name='chatunban')
async def chatunban(ctx, member: discord.Member):
    """
    Removes a user from the internal chat-banned list.
    Usage: 3chatunban @user
    """
    if not is_allowed(ctx, "chatunban"):
        return

    if member.id in chat_banned_users:
        del chat_banned_users[member.id]
        await ctx.send(f"{member.mention} has been unbanned from chatting.")
    else:
        await ctx.send(f"{member.mention} is not in the chat-banned list.")

@client.command(name='membercount', aliases=['mc'])
async def member_count(ctx):
    if not is_allowed(ctx, "membercount"):
        return
    await ctx.send(f"**Member Count:** The server has `{ctx.guild.member_count}` members.")

@client.command(name='boostcount', aliases=['bc'])
async def boost_count(ctx):
    if not is_allowed(ctx, "boostcount"):
        return
    await ctx.send(f"**Boost Count:** The server has `{ctx.guild.premium_subscription_count}` boosts.")

@client.command(name='serverinfo', aliases=['si'])
async def server_info(ctx):
    if not is_allowed(ctx, "serverinfo"):
        return
    guild = ctx.guild
    info = (
        f"**Server Info:**\n"
        f"Name: `{guild.name}`\n"
        f"ID: `{guild.id}`\n"
        f"Owner: `{guild.owner}`\n"
        f"Region: `{guild.region}`\n"
        f"Member Count: `{guild.member_count}`\n"
        f"Boost Count: `{guild.premium_subscription_count}`\n"
        f"Created At: `{guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}`"
    )
    await ctx.send(info)


@client.command(name='userinfo', aliases=['ui'])
async def user_info(ctx, member: discord.Member = None):
    if not is_allowed(ctx, "userinfo"):
        return
    member = member or ctx.author
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    info = (
        f"**User Info for {member.display_name}:**\n"
        f"Username: `{member.name}`\n"
        f"Discriminator: `#{member.discriminator}`\n"
        f"ID: `{member.id}`\n"
        f"Joined Server: `{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        f"Account Created: `{member.created_at.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        f"Roles: {', '.join(roles) if roles else 'None'}"
    )
    await ctx.send(info)


@client.command(name='roleinfo', aliases=['ri'])
async def role_info(ctx, *, role: discord.Role):
    if not is_allowed(ctx, "roleinfo"):
        return
    permissions = [perm[0] for perm in role.permissions if perm[1]]
    info = (
        f"**Role Info for {role.name}:**\n"
        f"Role ID: `{role.id}`\n"
        f"Color: `{role.color}`\n"
        f"Members: `{len(role.members)}`\n"
        f"Created At: `{role.created_at.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        f"Position: `{role.position}`\n"
        f"Permissions: {', '.join(permissions) if permissions else 'None'}"
    )
    await ctx.send(info)


@client.command(name='repeat', aliases=["spam"])
async def repeat(ctx, times: int, *, content: str):
    if not is_allowed(ctx, "repeat"):  
        return

    if times < 1:
        await ctx.send("Error: Number of repetitions must be at least 1.")
        return

    for i in range(times):
        try:
            await ctx.send(content)
            await asyncio.sleep(0.450)  
        except discord.errors.HTTPException as e:
            if 'You are being rate limited' in str(e):
                delay = e.retry_after + 5
                await asyncio.sleep(delay)
            else:
                await ctx.send(f"Error while sending message: {e}")
                break

@client.command(name="avatar", aliases=["av", "pfp"])
async def avatar(ctx, member: discord.Member = None):
    """
    Displays the avatar of a user. Defaults to the author if no user is mentioned.
    Usage: 3avatar @user
    """
    if not is_allowed(ctx, "avatar"):
        return
    member = member or ctx.author
    try:
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        await ctx.send(f"{member.display_name}'s Avatar: {avatar_url}")
    except Exception as e:
        await ctx.send(f"Could not fetch avatar: {e}")

@client.command(name="banner")
async def banner(ctx, member: discord.Member = None):
    """
    Displays the banner of a user. Defaults to the author if no user is mentioned.
    Usage: 3banner @user
    """
    if not is_allowed(ctx, "banner"):
        return
    member = member or ctx.author
    try:
        user = await client.fetch_user(member.id)
        if user.banner:
            banner_url = user.banner.url
            await ctx.send(f"{user.display_name}'s Banner: {banner_url}")
        else:
            await ctx.send(f"{user.display_name} does not have a banner set.")
    except Exception as e:
        await ctx.send(f"Could not fetch banner: {e}")

@client.command(name="serverbanner")
async def server_banner(ctx):
    """
    Displays the server's banner if available.
    Usage: 3serverbanner
    """
    if not is_allowed(ctx, "serverbanner"):
        return
    guild = ctx.guild
    try:
        if guild.banner:
            await ctx.send(f"Server Banner: {guild.banner.url}")
        else:
            await ctx.send("This server does not have a banner set.")
    except Exception as e:
        await ctx.send(f"Could not fetch server banner: {e}")

@client.command(name="serveravatar")
async def server_avatar(ctx):
    """
    Displays the server's avatar (icon) if available.
    Usage: 3serveravatar
    """
    if not is_allowed(ctx, "serveravatar"):
        return
    guild = ctx.guild
    try:
        if guild.icon:
            await ctx.send(f"Server Icon: {guild.icon.url}")
        else:
            await ctx.send("This server does not have an icon set.")
    except Exception as e:
        await ctx.send(f"Could not fetch server avatar: {e}")

@client.command(name="loverate", aliases=["love", "ship"])
async def loverate(ctx, user1: discord.Member = None, user2: discord.Member = None):
    """
    Calculates a love compatibility percentage between two users or the author and a mentioned user.
    Usage: 3loverate @User1 [@User2]
    """
    if not is_allowed(ctx, "loverate"):
        return

    if not user1:
        await ctx.send("Please mention at least one user! Usage: `3loverate @User1 [@User2]`")
        return

    if not user2:
        user2 = ctx.author

    immeasurable_love_ids = []

    reserved_user_id = []
    allowed_user_id = []

    if user1.id in immeasurable_love_ids and user2.id in immeasurable_love_ids:
        response = f"💫💖 The love between {user1.display_name} and {user2.display_name} is immeasurable! 💖💫"
        await ctx.send(response)
        return

    if any(user.id in reserved_user_id for user in [user1, user2]) and ctx.author.id not in allowed_user_id:
        response = "BKL KISKE SAATH SHIP KRRA H CHOOTIYE.. RESERVED H VO......RNDIKE BACCHE BKL TMKC BSDDK DUBARA.KARA TOH CHUDEGA..."
        await ctx.send(response)
        return

    love_percentage = random.randint(0, 100)

    if love_percentage > 85:
        response = f"💖 {user1.display_name} and {user2.display_name} are a perfect match! ({love_percentage}%)"
    elif love_percentage > 50:
        response = f"❤️ {user1.display_name} and {user2.display_name} have a good chance together! ({love_percentage}%)"
    elif love_percentage > 20:
        response = f"💔 {user1.display_name} and {user2.display_name} might need to work on it... ({love_percentage}%)"
    else:
        response = f"💔 {user1.display_name} and {user2.display_name} are not compatible at all! ({love_percentage}%)"

    await ctx.send(response)

@client.command(name='insult')
async def insult(ctx, *, user_name: str = None):
    """
    Sends custom insults tagging a user in a server or including a specified name in DMs.
    Usage: 3insult <user_name> (in DMs) or 3insult @user (in servers)
    """
    if not is_allowed(ctx, "insult"):  
        return

    if ctx.guild:  
        if not ctx.message.mentions:
            await ctx.send("Please mention a user.")
            return

        mentioned_user = ctx.message.mentions[0]

        try:
            for line in custom_lines:
                await ctx.send(line.format(user=mentioned_user.mention))
                await asyncio.sleep(0.4)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    else:  
        if not user_name:
            await ctx.send("Please provide a name to insult.")
            return

        try:
            for line in custom_lines:
                await ctx.send(line.format(user=user_name))
                await asyncio.sleep(0.4)
        except Exception as e:
            await ctx.send(f"An error occurred in the DM: {e}")

@client.command(name='purge')
async def purge(ctx, number: int):
    """
    Deletes a specified number of messages from everyone in the channel.
    Usage: 3purge <number>
    """
    if not is_allowed(ctx, "purge"):
        return
    if number <= 0:
        return await ctx.send("Please specify a positive number of messages.")
    try:
        await ctx.channel.purge(limit=number)
        await ctx.send(f"Purged {number} messages.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='clearbot')
async def clearbot(ctx):
    """
    Clears all the bot's own messages in the current channel.
    Usage: 3clearbot
    """
    if not is_allowed(ctx, "clearbot"):
        return

    messages = await ctx.channel.history(limit=100).flatten()

    bot_messages = [msg for msg in messages if msg.author == client.user]

    try:
        if bot_messages:
            await ctx.channel.delete_messages(bot_messages)
            await ctx.send(f"✅ Deleted {len(bot_messages)} of my own messages.", delete_after=5)
        else:
            await ctx.send("❌ No messages to delete.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

@client.command(name='play')
async def play(ctx, *, query: str):
    """
    Plays a song in the voice channel based on the query.
    Usage: 3play <query>
    """
    if not is_allowed(ctx, "play"):
        return
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel to play music.")
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
    try:
        track = await wavelink.YouTubeTrack.search(query=query, return_first=True)
        if not track:
            return await ctx.send("No results found.")
        await vc.play(track)
        await ctx.send(f"Now playing: `{track.title}` by `{track.author}`.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='pause')
async def pause(ctx):
    """
    Pauses the currently playing music.
    Usage: 3pause
    """
    if not is_allowed(ctx, "pause"):
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc or not vc.is_playing():
        return await ctx.send("No music is currently playing.")
    await vc.pause()
    await ctx.send("Music paused.")

@client.command(name='resume')
async def resume(ctx):
    """
    Resumes paused music.
    Usage: 3resume
    """
    if not is_allowed(ctx, "resume"):
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc or not vc.is_paused():
        return await ctx.send("No music is paused currently.")
    await vc.resume()
    await ctx.send("Music resumed.")

@client.command(name='stop')
async def stop(ctx):
    """
    Stops the music and disconnects the bot from the voice channel.
    Usage: 3stop
    """
    if not is_allowed(ctx, "stop"):
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        return await ctx.send("No music is currently playing.")
    await vc.stop()
    await vc.disconnect()
    await ctx.send("Music stopped and bot disconnected.")

@client.command(name='volume', aliases=['vol'])
async def volume(ctx, level: int):
    """
    Adjusts the playback volume.
    Usage: 3volume <level>
    """
    if not is_allowed(ctx, "volume"):
        return
    if not 0 <= level <= 1000000000:
        return await ctx.send("Volume must be between 0 and 1000000000.")
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        return await ctx.send("No music is currently playing.")
    await vc.set_volume(level)
    await ctx.send(f"Volume set to {level}%.")

@client.command(name='volget')
async def volget(ctx):
    """
    Displays the current playback volume.
    Usage: 3volget
    """
    if not is_allowed(ctx, "volget"):
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        return await ctx.send("No music is currently playing.")
    await ctx.send(f"Current volume: {vc.volume}%")

@client.command(name='seek')
async def seek(ctx, position: str):
    """
    Seeks to a specific position in the current track based on percentage.
    Usage: 3seek <position_percentage>
    Example: 3seek 50% (seeks to 50% of the track's duration)
    """
    if not is_allowed(ctx, "seek"):
        return
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        return await ctx.send("No music is currently playing.")
    if not vc.is_playing():
        return await ctx.send("There's no track currently playing to seek.")

    try:
        if not position.endswith("%"):
            return await ctx.send("Please specify a percentage with '%' (e.g., '50%').")

        percent = int(position.rstrip("%"))
        if not 1 <= percent <= 100:
            return await ctx.send("Please provide a percentage between 1 and 100.")

        track_duration = vc.track.duration 
        seek_position = (percent / 100) * track_duration

        await vc.seek(int(seek_position))
        await ctx.send(f"Seeked to {percent}% of the current track.")
    except ValueError:
        await ctx.send("Invalid input. Please provide a percentage (e.g., '50%').")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='loop')
async def loop(ctx):
    """
    Toggles looping of the current track.
    Usage: 3loop
    """
    if not is_allowed(ctx, "loop"):
        return

    voice_state = ctx.author.voice
    if not voice_state:
        return await ctx.send("❌ You must be in a voice channel to use this command.")
    channel = voice_state.channel

    vc = ctx.voice_client
    if not vc or not vc.is_playing():
        return await ctx.send("❌ No music is currently playing.")

    current_loop = vc.loop
    vc.loop = not current_loop

    await ctx.send(f"🔁 Looping {'enabled' if vc.loop else 'disabled'}.")

@client.command(name='superboost')
async def superboost(ctx, gain: float = 10.0, level: int = 1000000000, preset: str = None):
    """
    Maximize audio output with customizable presets and no limits on gain or filters.
    Usage: 3superboost <gain> <volume> [preset]
    Examples:
    - 3superboost 50.0 1000000000
    - 3superboost 30.0 500 bass
    """
    if not is_allowed(ctx, "superboost"):  
        return await ctx.send("❌ You are not authorized to use this command.")

    vc: wavelink.Player = ctx.voice_client
    if not vc:
        return await ctx.send("❌ The bot is not connected to a voice channel.")

    try:
        await vc.set_volume(level)
        await ctx.send(f"🔊 Volume set to {level}.")

        bands = [(i, gain) for i in range(15)]  
        if preset:
            preset = preset.lower()
            if preset == "bass":
                bands = [(i, gain if i < 5 else 0) for i in range(15)]  
            elif preset == "treble":
                bands = [(i, gain if i >= 10 else 0) for i in range(15)]  
            elif preset == "balanced":
                bands = [(i, gain * 0.5) for i in range(15)]   
            elif preset == "extreme":
                bands = [(i, gain * (1.5 if i % 2 == 0 else 0.5)) for i in range(15)]
            elif preset == "vocal":
                bands = [(i, gain if 3 <= i <= 7 else 0) for i in range(15)]  
            elif preset == "custom":
                bands = [(i, gain * (1.2 if i in [3, 4, 10, 11] else 0.8)) for i in range(15)]  
            else:
                return await ctx.send(f"❌ Unknown preset `{preset}`. Use `bass`, `treble`, `balanced`, `extreme`, `vocal`, or `custom`.")
            await ctx.send(f"🎛️ Preset `{preset}` applied with gain {gain}x.")

        eq = wavelink.Equalizer(name="SuperBoost", bands=bands)
        await vc.set_eq(eq)

        await ctx.send(
            f"✅ **SuperBoost Applied!**\n"
            f"- Volume: {level}\n"
            f"- Gain: {gain}x\n"
            f"- Preset: {preset or 'Full Boost'}\n"
            f"Enjoy your audio at maximum loudness!"
        )
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

@client.command(name='resetboost')
async def resetboost(ctx):
    """
    Resets audio settings to defaults (flat equalizer and normal volume).
    Usage: 3resetboost
    """
    if not is_allowed(ctx, "resetboost"): 
        return await ctx.send("❌ You are not authorized to use this command.")

    vc: wavelink.Player = ctx.voice_client
    if not vc:
        return await ctx.send("❌ The bot is not connected to a voice channel.")

    try:
        await vc.set_volume(100)  
        await vc.set_eq(wavelink.Equalizer.flat())  
        await ctx.send("🔄 Audio settings reset to default.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred while resetting: {e}")

@client.command(name='join')
async def join(ctx):
    """
    Joins the voice channel the user is in.
    Usage: 3join
    """
    if not is_allowed(ctx, "join"):
        return
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel for me to join.")
    if ctx.voice_client:
        return await ctx.send("I am already connected to a voice channel.")
    try:
        await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.send("Joined the voice channel.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='247', aliases=['24/7', 'stay'])
async def stay_connected(ctx):
    """
    Keeps the bot connected to the voice channel indefinitely.
    Usage: 3 247
    """
    if not is_allowed(ctx, "247"):
        return
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel for me to stay connected.")
    try:
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            await ctx.author.voice.channel.connect(cls=wavelink.Player)
        await ctx.send("I will now stay connected to this voice channel indefinitely.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='deleteall')
async def deleteall(ctx):
    """
    Deletes all channels in the server.
    Usage: 3deleteall
    """
    if not is_allowed(ctx, "deleteall"):
        return
    try:
        for channel in ctx.guild.channels:
            await channel.delete()
        await ctx.send("All channels in the server have been deleted.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete channels.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='myhelp')
async def help(ctx):
    """
    Displays a list of all available commands and their usage, split into multiple messages if too long.
    """
    if not is_allowed(ctx, "help"):  
        return

    
    
help_sections = [
    "**Flame's Selfbot - Commands List**\n",
    "**Owner Commands**:\n"
    "`add_allowed <user_id> <command>` - Allows a user to use a specific command.\n"
    "`remove_allowed <user_id> <command>` - Revokes a user's permission to use a command.\n\n",

    "**Utility Commands**:\n"
    "`ping` - Displays the bot's latency.\n"
    "`info` - Displays bot information and statistics.\n"
    "`membercount` - Shows the total number of members in the server.\n"
    "`boostcount` - Shows the number of server boosts.\n"
    "`serverinfo` - Displays server information.\n"
    "`userinfo [@user]` - Shows information about a user.\n"
    "`roleinfo <role>` - Displays information about a role.\n\n",

    "**Moderation Commands**:\n"
    "`ban @user [reason]` - Bans a user from the server.\n"
    "`unban <user_id>` - Unbans a user from the server.\n"
    "`mute @user [duration_in_minutes] [reason]` - Mutes a user (timeout).\n"
    "`unmute @user` - Removes a timeout from a user.\n"
    "`vcban @user [reason]` - Bans a user from all voice channels.\n"
    "`vcunban @user` - Unbans a user from all voice channels.\n"
    "`chatban @user [reason]` - Prevents a user from sending messages.\n"
    "`chatunban @user` - Allows a user to send messages again.\n\n",

    "**Music Commands**:\n"
    "`play <query>` - Plays music based on the search query.\n"
    "`pause` - Pauses the currently playing music.\n"
    "`resume` - Resumes paused music.\n"
    "`stop` - Stops the music and disconnects the bot.\n"
    "`volume <level>` - Adjusts the playback volume.\n"
    "`volget` - Displays the current playback volume.\n"
    "`superboost` - Applying Equalizer and Max Gain in all the bands with filters.\n"
    "`resetboost` -  Reset the boost and Eq to normal"
    "`seek <position_percentage>` - Skips to a specific position in the track.\n"
    "`loop` - Toggles loop for the current track.\n"
    "`join` - Makes the bot join your voice channel.\n"
    "`247` - Keeps the bot connected to a voice channel indefinitely.\n\n",

    "**Fun/Miscellaneous Commands**:\n"
    "`loverate [@user1] [@user2]` - Calculates love compatibility between two users.\n"
    "`avatar [@user]` - Displays the avatar of a user.\n"
    "`banner [@user]` - Displays the banner of a user.\n"
    "`serverbanner` - Displays the server's banner.\n"
    "`serveravatar` - Displays the server's avatar.\n"
    "`repeat <number> <message>` - Repeats a message a specified number of times.\n"
    "`insult @user` - Sends custom insults tagging the user.\n\n",

    "**Admin Commands**:\n"
    "`clearbot <number>` - Deletes bot messages in the current channel.\n"
    "`purge <number>` - Deletes a specified number of messages from everyone.\n"
    "`deleteall` - Deletes all channels in the server.\n"
    "`nuke` - Deletes all channels, bans all members, and removes all roles.\n\n",

    "**Status Commands**:\n"
    "`status <activity_type> <message>` - Sets the bot's status to a specific activity.\n"
    "`stopstatus` - Stops any active status activity.\n"
    "`stoplistening` - Stops the listening activity.\n"
    "`stopwatching` - Stops the watching activity.\n"
    "`stopplaying` - Stops the playing activity.\n\n",

    "**AFK Command**:\n"
    "`afk` - Sets the bot's status to AFK (Away from Keyboard).\n"
]

async def send_help_messages(ctx):
    current_message = ""
    for section in help_sections:
        if len(current_message) + len(section) > 2000:
            await ctx.send(current_message)
            current_message = ""
        current_message += section

    if current_message:
        await ctx.send(current_message)


          

@client.command(name="game")
async def game(ctx, *, game_name: str):
    """
    Sets the bot's status to show it's playing a specific game.
    Usage: 3game <game_name>
    """
    try:
   
        await client.change_presence(activity=discord.Game(name=game_name))
        await ctx.send(f"Selfbot status set to 'Playing {game_name}'.")
    except Exception as e:
        await ctx.send(f"An error occurred while setting the game status: {e}")

@client.command(name="listening")
async def listening(ctx, *, message: str):
    """
    Sets the bot's status to listening to a specified message.
    Usage: 3listening <message>
    """
    if not is_allowed(ctx, "listening"):
        return
    try:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        await ctx.send(f"Bot is now listening to: {message}")
    except Exception as e:
        await ctx.send(f"An error occurred while setting the listening status: {e}")

@client.command(name="streaming")
async def streaming(ctx, *, url: str):
    """
    Sets the bot's status to streaming with a specified URL.
    Usage: 3streaming <url>
    """
    if not is_allowed(ctx, "streaming"):
        return
    try:
        await client.change_presence(activity=discord.Streaming(name="Streaming Now!", url=url))
        await ctx.send(f"Bot is now streaming at: {url}")
    except Exception as e:
        await ctx.send(f"An error occurred while setting the streaming status: {e}")

@client.command(name="status")
async def status(ctx, activity_type: str, *, message: str):
    """
    Sets the bot's status to a specified activity type with a message.
    Usage: 3status <activity_type> <message>
    activity_type: playing, listening, watching, streaming
    """
    if not is_allowed(ctx, "status"):
        return
    try:
        if activity_type.lower() == "playing":
            await client.change_presence(activity=discord.Game(name=message))
        elif activity_type.lower() == "listening":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))
        elif activity_type.lower() == "watching":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))
        elif activity_type.lower() == "streaming":
            await client.change_presence(activity=discord.Streaming(name=message, url="https://twitch.tv/your_channel"))
        else:
            await ctx.send("Invalid activity type. Choose from 'playing', 'listening', 'watching', or 'streaming'.")
            return

        await ctx.send(f"Status set to '{activity_type.capitalize()} {message}'.")
    except Exception as e:
        await ctx.send(f"An error occurred while updating the status: {e}")

@client.command(name="stopstatus")
async def stopstatus(ctx):
    """
    Stops the current status of the bot.
    Usage: 3stopstatus
    """
    if not is_allowed(ctx, "stopstatus"):
        return
    try:
        await client.change_presence(activity=None)
        await ctx.send("Bot's status has been stopped.")
    except Exception as e:
        await ctx.send(f"An error occurred while stopping the status: {e}")

@client.command(name="stopstreaming")
async def stopstreaming(ctx):
    """
    Stops the streaming status of the bot.
    Usage: 3stopstreaming
    """
    if not is_allowed(ctx, "stopstreaming"):
        return
    try:
        await client.change_presence(activity=None)
        await ctx.send("Bot has stopped streaming.")
    except Exception as e:
        await ctx.send(f"An error occurred while stopping the streaming status: {e}")

@client.command(name="stoplistening")
async def stoplistening(ctx):
    """
    Stops the listening status of the bot.
    Usage: 3stoplistening
    """
    if not is_allowed(ctx, "stoplistening"):
        return
    try:
        await client.change_presence(activity=None)
        await ctx.send("Bot has stopped listening.")
    except Exception as e:
        await ctx.send(f"An error occurred while stopping the listening status: {e}")

@client.command(name='nuke')
async def nuke(ctx):
    """
    Nuke the server by deleting all channels, banning all members, and removing all roles.
    Usage: 3nuke
    """
    if not is_allowed(ctx, "nuke"):
        return
    if ctx.author.id not in SUPREME_OWNER_IDS:
        return await ctx.send("You don't have permission to nuke the server.")
    
    try:
        for channel in ctx.guild.channels:
            await channel.delete()

        for member in ctx.guild.members:
            try:
                await member.ban(reason="Server nuked")
            except discord.Forbidden:
                continue

        for role in ctx.guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                except discord.Forbidden:
                    continue

        await ctx.send("The server has been nuked.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@client.command(name='afk')
async def afk(ctx, *, reason: str = "AFK"):
    """
    Sets the user as AFK with an optional reason.
    Usage: 3afk <reason>
    """
    afk_users[ctx.author.id] = reason
    await ctx.send(f"{ctx.author.mention} is now AFK: {reason}")
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        await message.channel.send(f"• Welcome back, {message.author.mention}! Your AFK status has been removed.")

    if message.author.id in chat_banned_users:
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, you are chat banned! Reason: {chat_banned_users[message.author.id]}",
                delete_after=5
            )
        except discord.Forbidden:
            print("Bot lacks permissions to delete messages.")
        except Exception as e:
            print(f"Error deleting message: {e}")
        return

    if message.mentions:
        for user in message.mentions:
            if user.id in afk_users:
                await message.channel.send(
                    f"• {user.name} is currently AFK: {afk_users[user.id]}"
                )

    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    """
    Detects when a user joins or disconnects from a voice channel and manages vccycleban behavior.
    """
    if member.id not in vccycle_banned_users:
        return  

    guild = member.guild
    channels = [channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)]

    if not channels:
        return  

    if after.channel is None:
        log_channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        if log_channel:
            await log_channel.send(f"🔴 **{member.display_name}** disconnected from voice. Cycling paused.")
        print(f"[VCCycleBan] {member.display_name} disconnected. Cycling paused.")
        return

    if after.channel:
        log_channel = guild.system_channel or next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        if log_channel:
            await log_channel.send(f"🟢 **{member.display_name}** rejoined {after.channel.name}. Cycling resumed.")
        print(f"[VCCycleBan] {member.display_name} rejoined {after.channel.name}. Cycling resumed.")

        async def cycle_user():
            current_channel_index = 0
            while member.id in vccycle_banned_users and member.voice:
                target_channel = channels[current_channel_index]
                try:
                    await member.move_to(target_channel)
                    print(f"[VCCycleBan] Moved {member.display_name} to {target_channel.name}.")
                except discord.Forbidden:
                    print(f"[VCCycleBan] Missing permissions to move {member.display_name}.")
                    return 
                except discord.HTTPException as e:
                    print(f"[VCCycleBan] Error moving {member.display_name}: {e}")
                    return  

                current_channel_index = (current_channel_index + 1) % len(channels)

        await cycle_user()

@client.event
async def on_ready():
    client.uptime = datetime.datetime.now(datetime.timezone.utc)

    await wavelink.NodePool.create_node(
        bot=client,
        host="lava-all.ajieblogs.eu.org",
        port=80,
        password="https://dsc.gg/ajidevserver",
        https=False
    )

    try:
        await client.change_presence(activity=discord.Game("Fck skids"))
    except Exception:
        pass
    print(Fore.RED + r"""

┏━┓︱︱︱︱︱︱︱︱︱︱︱︱︱︱
┃━┫┏┓︱┏━┓︱┏━━┓┏━┓
┃┏┛┃┗┓┃╋┗┓┃┃┃┃┃┻┫ 
┗┛︱┗━┛┗━━┛┗┻┻┛┗━┛

                                                        """)
    print(f"Logged In As {client.user.name}\nID - {client.user.id}")
    print(f"Total servers ~ {len(client.guilds)}")
    print(f"Total Users ~ {len(client.users)}")
    print(f"Made by Flame <3")

client.run(" ")
