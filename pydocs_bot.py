import discord
import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


class MyClient(discord.Client):
    def driver(self, lang: str, mes: str):
        url = 'https://devdocs.io/#q='
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get(url + lang + " " + mes)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, features="lxml")
        driver.quit()
        if (mes[-2:] == "()"):
            mes = mes[:len(mes)-2]
        target = soup.find(id=mes)
        return target.find_previous("dl").text
        

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        args = message.content.split(' ')
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello {0.author.mention}'.format(message))
        
        if message.content.startswith('!python'):
            await message.channel.send(self.driver('py', args[1]))

        

        
client = MyClient()
client.run(os.environ['DISCORD_BOT'])
