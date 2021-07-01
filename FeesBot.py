# bot.py
#Created by Makrron

import discord
import requests
import time
from discord.ext import commands
from discord.ext.commands import Cog, Group, Command, HelpCommand


bot = commands.Bot(command_prefix="-f ", description=" ")

btc_link = "https://mempool.space/api/v1/fees/recommended"
gas_link = "https://www.gasnow.org/api/v3/gas/price"
slow = " "
standar = " "
fast = " "
rapid = " "


class HelpCommand(HelpCommand):
    async def send_bot_help(self, mapping):
        message = ("`-f help =>` this command" + 
            "\n`-f btc =>` show fees of Bitcoin network" + 
            "\n`-f gas =>` show fees of Ethereum network")

        await self.get_destination().send(message)

bot.help_command = HelpCommand()


#COMMANDS
@bot.command()
async def btc(ctx):
    #------------------------------------------
    with requests.Session() as s:
        btc_response = (s.get(btc_link).text)

        rapid = btc_response[btc_response.find('fastestFee')+12:btc_response.find('halfHourFee')-2] 
        fast = btc_response[btc_response.find('halfHourFee')+13:btc_response.find('hourFee')-2]
        standar = btc_response[btc_response.find('hourFee')+9:btc_response.find('minimumFee')-2]
        slow = btc_response[btc_response.find('minimumFee')+12:btc_response.find('}')]
    #------------------------------------------
    res = ("• **Rapid**: " + rapid + " sat/vB\n" + 
           "• **Fast**: " + fast + " sat/vB\n" + 
           "• **Standar**: " + standar + " sat/vB\n" + 
           "• **Slow**: " + slow + " sat/vB")
   
    embed=discord.Embed(title="Bitcoin Fees", description=res, color=0xf77e33)
    embed.set_thumbnail(url="https://mempool.space/es/resources/bitcoin-logo.png")
    await ctx.send(embed=embed)

@bot.command()
async def gas(ctx):
    #------------------------------------------
    with requests.Session() as s:
        fees_response = (s.get(gas_link).text)

        rapid = fees_response[fees_response.find('rapid')+7:fees_response.find('fast')-11]
        fast = fees_response[fees_response.find('fast')+6:fees_response.find('standard')-11]
        standar = fees_response[fees_response.find('standard')+10:fees_response.find('slow')-11] 
        slow = fees_response[fees_response.find('slow')+6:fees_response.find('timestamp')-11]
    #------------------------------------------
    res = ("• **Rapid**: " + rapid + " gwei\n" + 
           "• **Fast**: " + fast + " gwei\n" + 
           "• **Standar**: " + standar + " gwei\n" + 
           "• **Slow**: " + slow + " gwei")

    embed=discord.Embed(title="Ethereum Gas", description=res, color=0x5872a0)
    embed.set_thumbnail(url="https://ethgasstation.info/images/ETHGasStation.png")
    await ctx.send(embed=embed)
    time.sleep(15)

#EVENTS:
@bot.event
async def on_ready():
    print("BOT Ready")

bot.run("BOT_TOKEN")
