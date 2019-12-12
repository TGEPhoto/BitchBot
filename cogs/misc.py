import aiohttp
import asyncio
import discord
import random
import re
import string
from discord.ext import commands

from keys import logWebhook
from util import funs  # pylint: disable=no-name-in-module

RES_PATH = 'res/'


def c_to_f(c: float) -> float:
    return (c * 9 / 5) + 32


def f_to_c(f: float) -> float:
    return (f - 32) * (5 / 9)


# noinspection SpellCheckingInspection,PyPep8Naming,PyIncorrectDocstring
class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_chars = {
            'a': '🇦',
            'b': '🇧',
            'c': '🇨',
            'd': '🇩',
            'e': '🇪',
            'f': '🇫',
            'g': '🇬',
            'h': '🇭',
            'i': '🇮',
            'j': '🇯',
            'k': '🇰',
            'l': '🇱',
            'm': '🇲',
            'n': '🇳',
            'o': '🇴',
            'p': '🇵',
            'q': '🇶',
            'r': '🇷',
            's': '🇸',
            't': '🇹',
            'u': '🇺',
            'v': '🇻',
            'w': '🇼',
            'x': '🇽',
            'y': '🇾',
            'z': '🇿'
        }

        self.emoji_chars_alts = {
            'k': "🎋",
            'l': "👢",
            'o': "⭕",
            'q': "🎯",
            's': "💲",
            'u': "⛎",
            'x': "❌"
        }

    @commands.command(aliases=["send"])
    async def say(self, ctx, *, message):
        """Have the bot say something. Have fun!

        Args:
            message: The message you want to say
        """

        await ctx.channel.trigger_typing()
        sentMessage = await ctx.send(message)
        await funs.log(ctx, 'Say', message, sentMessage)
        await ctx.message.delete(delay=5)

    @commands.command(aliases=["sendembed", "embed"])
    async def sayembed(self, ctx, *, message):
        """
        Have the bot say something in embeds. Have fun!
        """
        await ctx.channel.trigger_typing()

        embed = discord.Embed()
        splitedMessage = message.split('\n')
        for i in splitedMessage:
            if i.startswith('t'):
                embed.title = i[2:]
            elif i.startswith('d'):
                embed.description = i[2:]
            elif i.startswith('f'):
                embed.set_footer(text=i[2:])
            elif i.startswith('c'):
                embed.colour = discord.Colour(int(f'0x{i[2:].strip()}', 16))

        fields = [j.strip('?').split(',') for j in splitedMessage if j.startswith("?")]
        for f in fields:
            embed.add_field(name=f[0], value=f[1], inline=f[2].strip() != 'false')
        sentMessage = await ctx.send(embed=embed)

        embed.timestamp = ctx.message.created_at
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.add_field(name='Message', value=f'[Jump To Message]({sentMessage.jump_url})', inline=False)

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(logWebhook, adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(embed=embed, username='sayembed')

    @commands.command(aliases=["kayliesman"])
    @funs.cause_check()
    async def rabbitman(self, ctx):
        """
        Sends a rabbitman picture
        """

        files = []
        for i in range(1, 11):
            files.append(f'{RES_PATH}rabbitman{i}.jpg')

        await ctx.channel.send(file=discord.File(files[random.randint(0, len(files) - 1)]))

    @commands.command()
    @funs.cause_check()
    async def baby(self, ctx):
        """
        Sends a Baby picture
        """
        files = []
        for i in range(1, 9):
            files.append(f'{RES_PATH}baby{i}.jpg')

        await ctx.channel.send(file=discord.File(files[random.randint(0, len(files) - 1)]))

    @commands.command(aliases=["addreaction"])
    async def react(self, ctx, msg: discord.Message, text):
        """
        Add the given reactions to a message
        """

        sent = []
        for i in text:
            if re.fullmatch(r'[a-z]', i, re.IGNORECASE):
                emoji = str(i).lower()
                if (i in sent) and (emoji in self.emoji_chars_alts.keys()):
                    await msg.add_reaction(self.emoji_chars_alts[emoji])
                else:
                    await msg.add_reaction(self.emoji_chars[emoji])
                sent.append(i)

        await funs.log(ctx, 'react', text, ctx.message, ''.join(sent))

    @commands.command()
    async def totogglecase(self, ctx, *, msg):
        """
        Convert string to toggle case
        """
        out = ""
        message = str(msg)
        for i in range(0, len(message)):
            out += message[i].lower() if (i % 2 == 0) else message[i].upper()

        sentMessage = await ctx.send(out)
        await funs.log(ctx, 'toggle case', msg, sentMessage, out)
        await ctx.message.delete(delay=5)

    @commands.command(aliases=["yell"])
    async def touppercase(self, ctx, *, msg):
        """
        Convert string to toggle case
        """
        out = str(msg).upper()
        sentMessage = await ctx.send(out)
        await funs.log(ctx, 'touppercase', msg, sentMessage, out)
        await ctx.message.delete()

    @commands.command(aliases=["wide"])
    async def addspaces(self, ctx, msg: str, spaces: int = 3):
        """
        Adds 3 spaces in between every character.
        If the first arg is a number, it will use that for the number of spaces instead.
        """

        between = spaces * ' '
        out = between.join(list(str(msg)))
        sentMessage = await ctx.send(out)
        await funs.log(ctx, 'addspaces', msg, sentMessage, out)
        await ctx.message.delete(delay=5)

    @commands.command()
    async def flip(self, ctx, *, msg):
        """
        Converts given text to flipped unicode characters
        """
        FLIP_RANGES = [
            (string.ascii_lowercase, "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎz"),
            (string.ascii_uppercase, "ⱯᗺƆᗡƎᖵ⅁HIᒋ⋊ꞀWNOԀꝹᴚS⊥ႶɅMX⅄Z"),
            (string.digits, "0ІᘔƐᔭ59Ɫ86"),
            (string.punctuation, "¡„#$%⅋,)(*+'-˙/:؛>=<¿@]\\[ᵥ‾`}|{~"),
        ]

        msgBack = ""
        for c in list(msg):
            for r in range(len(FLIP_RANGES)):
                try:
                    p = FLIP_RANGES[r][0].index(c)
                    if not p == -1:
                        newC = FLIP_RANGES[r][1][p]
                        msgBack += newC
                        break
                except ValueError:
                    msgBack += ' '
                    continue

        out = ' '.join(msgBack.split())
        sentMessage = await ctx.send(out)
        await funs.log(ctx, 'flip', msg, sentMessage, out)
        await ctx.message.delete(delay=5)

    @commands.command(aliases=["rick", "rickroll"])
    async def rickroulette(self, ctx):
        """
        Rickroll bot. Lose/win
        """
        await ctx.channel.trigger_typing()
        rick = "https://tenor.com/view/never-gonna-give-you-up-dont-give-never-give-up-gif-14414705"
        await asyncio.sleep(3)
        await ctx.send(f"Get rick rolled\n {rick}")

    @commands.command(aliases=["to_c"])
    async def toc(self, ctx, message):
        """
        Convert fahrenheit to celsius.
        Format: '>toc <temp in f>'. 
        Example: '>toc 69'.
        """

        try:
            await ctx.send(f'{int(f_to_c(float(message)))}°C')
        except Exception as identifier:
            await ctx.send(f"Bruh...\nDon't you know how to follow instructions\nError: {identifier}")

    @commands.command(aliases=["to_f"])
    async def tof(self, ctx, message):
        """
        Convert celsius to fahrenheit.
        Format: '>tof <temp in c'.
        Example: '>tof 20.5'.
        """

        try:
            await ctx.send(f'{int(c_to_f(float(message)))}°F')
        except Exception as identifier:
            await ctx.send(f"Bruh...\nDon't you know how to follow instructions\nError: {identifier}")

    @commands.command()
    async def poll(self, ctx, question, *answers):
        """
        Start a poll.
        If answers/questions contain spaces put it in quotes
        Example:
            >poll "Do you like bacon" yes

        Args:
            question: The question you want to ask. This will be title of embed
            answers: The answers for the poll. If no answers are provided, it will default to yes/no.
             Max of 10 answers are allowed
        """

        if answers == ():
            msg = await ctx.send(f"**📊 {question}**")
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")

        elif len(answers) < 10:
            letter_emote = list(self.emoji_chars.values())
            inner = ""
            for i in range(len(answers)):
                inner += f"{letter_emote[i]} {answers[i]}\n"
            embed = discord.Embed(title=f"**📊 {question}**", description=inner, color=funs.random_discord_color())
            msg = await ctx.send(embed=embed)
            for i in range(len(answers)):
                await msg.add_reaction(letter_emote[i])
        else:
            pass


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
