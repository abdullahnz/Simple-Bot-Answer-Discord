#!/usr/bin/python

from discord.ext import commands
from bs4 import BeautifulSoup as BS
from dotenv import load_dotenv
import requests, json, random, os
import discord

# load enviroment 
load_dotenv()

_client = commands.Bot(command_prefix='!')
_token = os.getenv('DISCORD_TOKEN')


@_client.event
async def on_ready():
    print('Bot is already running.')


@_client.event
async def on_message(_message):
    # make bot doesnt loop answer message.
    if _message.author == _client.user:
        return

    _hello = [
        "Hmm. Gimana gan %s.",
        "Iya. Halo juga bos %s.",
        "Haloo. Jangan lupa makan ya boss :) %s.",
        "Iya. Yellow yang comel disini. Ada yang bisa dibantu? (%s)",
        "Yellow lucu kan bos %s hehe :)"
    ]

    # convert message from client to lowercase
    client_msg = _message.content.lower()

    if client_msg.startswith('halo'):
        _id_user = "<@{}>".format(_message.author.id)
        _response = random.choice(_hello) % _id_user
        await _message.channel.send(_response)

  
    if client_msg.startswith('hmm'):
        _id_user  = "<@{}>".format(_message.author.id)
        _response = "Gayamu %s hamm hemm hamm hemm. Prok dewe ning kene pie! Hmm, canda bang :)" %_id_user
        await _message.channel.send(_response)
    
    if 'bot' in client_msg or 'yellow' in client_msg:
        _responses = [
            'Manggil gue bos? %s Hmm.',
            'Gimana bos %s tengah - tengah? Otw bos, kita gelut >:)',
            'Gimana. Mau mabar bos? %s.',
            'Gimana sayang %s :smiling_face_with_3_hearts:.'
        ]
        _id_user  = "<@{}>".format(_message.author.id)
        await _message.channel.send(random.choice(_responses) %_id_user)

    if 'mabar' in client_msg or client_msg.startswith('ayo'):
        _responses = [
            'Gk mau. Kau cupu %s, gk maen aku sama orang cupu :)',
            'G LO COPO !!! %s.',
            'Hmm. Jangan deh. Takut menang gw :) %s'
        ]
        _id_user  = "<@{}>".format(_message.author.id)
        await _message.channel.send(random.choice(_responses) %_id_user)

    # make commands works.
    await _client.process_commands(_message)


def search_url(json_data):
    for data in json_data:
        if data[0].startswith('http'):
            return data[0]
            break

def hmm(text):
    result = ''
    for d in text.split():
        d = list(d)
        d[0] = d[0].upper()
        result += ''.join(d) + ' '
    return result

@_client.command()
async def whatis(ctx, *argv):
    # get title argument from client.
    title = ' '.join(argv[0:len(argv)])
    await ctx.channel.send('>>> Searching for: %s ...' %hmm(title))

    # client argument search
    search = ''.join(argv[0:len(argv)])
    base_wiki_url = "https://id.wikipedia.org/w/api.php?action=opensearch&search={}&limit=1&namespace=0&format=json"
   
    # get json data from wiki search api
    content = requests.get(base_wiki_url.format(search)).text

    # parsing json data and get the url target
    url = search_url(json.loads(content))

    # parsing html content to get all info text
    content = requests.get(url).text
    content = BS(content, 'html.parser')
    p = content.find('p')

    # output for client
    output = '\n'.join([
        '>>> %s' %hmm(title),
        '>>> ',
        '>>> %s' %p.text,
        '>>> Continue reading: %s' %url,
    ])

    # send output to client
    await ctx.channel.send(output)

# runing bot
_client.run(_token)
