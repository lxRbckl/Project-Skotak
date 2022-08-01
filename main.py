# Project Fenaverat by Alex Arbuckle #


# import <
from os import path
from json import loads
from requests import get
from github import Github
from asyncio import sleep
from discord import Intents
from discord.ext import commands
from datetime import datetime as dt
from lxRbckl import jsonLoad, jsonDump, githubSet, githubGet

# >


# global <
gMinute = 120
gBranch = ''
gFile = ''
gRepository = ''
gPath = path.realpath(__file__).split('/')
gDirectory = '/'.join(gPath[:(len(gPath) - 1)])
githubToken = ''
fenaverat = commands.Bot(command_prefix = '', intents = Intents.all())
discordToken = ''

# >


async def setFunction(ctx, pKey: str, pAction: str, pValue: str, pData: dict):
    '''  '''

    # if (new value) then set value <
    if (pValue not in pData[pKey][pAction]):

        await ctx.message.delete()
        pData[pKey][pAction].append(pValue)
        jsonDump(

            pData = pData,
            pFile = f'{gDirectory}/setting.json'

        )

    # >


async def getFunction(ctx, pKey: str, pValue: str, pAction: str, pData: dict):
    '''  '''

    # if (return requested content) <
    if (pAction): r = [f'`{i}`' for i in pData[pKey][pAction]]
    elif (pKey): r = [f'`{i}`' for i in pData[pKey].keys()]
    else: r = [f'`{i}`' for i in pData.keys()]

    # >

    await ctx.message.delete()
    await ctx.channel.send(delete_after = 60, content = '\n'.join(r))


async def delFunction(ctx, pKey: str, pValue: str, pAction: str, pData: dict):
    '''  '''

    # if (existing value) then get value <
    if (pValue in pData[pKey][pAction]):

        await ctx.message.delete()
        pData[pKey][pAction].remove(pValue)
        jsonDump(

            pData = pData,
            pFile = f'{gDirectory}/setting.json'

        )

    # >


@fenaverat.event
async def on_ready(pGithub = Github(githubToken)):
    '''  '''

    aData = {}
    while (True):

        data = jsonLoad(pFile = f'{gDirectory}/setting.json')
        bData = {'topic' : data['topic']['add'], 'language' : data['language']['add']}
        for r in [r for u in data['user']['add'] for r in pGithub.get_user(u).get_repos()]:

            # if (permitted project) <
            if (r not in data['project']['remove']):

                bData[r.full_name] = {

                    'link' : f'https://github.com/{r.full_name}',
                    'description' : r.description if (r.description) else 'null',
                    'topic' : [t for t in r.get_topics() if (t not in data['topic']['remove'])],
                    'language' : [l for l in r.get_languages() if (l not in data['language']['remove'])],
                    'update' : dt.strptime(str(r.pushed_at).split(' ')[0], '%Y-%m-%d').strftime('%B %d %Y'),
                    'feed' : loads(get(f'https://raw.githubusercontent.com/{r.full_name}/main/feed.json')).keys()

                }

            # >

        # if (update) <
        if (aData != bData):

            githubSet(

                pFile = gFile,
                pData = bData,
                pGithub = pGithub,
                pBranch = gBranch,
                pRepository = gRepository,
                pMessage = 'Fenaverat Automated Message'

            )
            aData = bData

        # >

        await sleep(60 * gMinute)


@commands.has_permissions(administrator = True)
@fenaverat.command(aliases = jsonLoad(pFile = f'{gDirectory}/setting.json')['aliases'])
async def commandFunction(ctx, pKey: str = None, pAction: str = None, pValue: str = None):
    '''  '''

    # local <
    isAction = True if (pAction in ['add', 'remove']) else False
    data = jsonLoad(pFile = f'{gDirectory}/setting.json')
    isKey = True if (pKey in data.keys()) else False

    # >

    # if ((existing key) and (existing action)) <
    if ((isKey and isAction) or (ctx.invoked_with.lower() == 'get')):

        # call function <
        await {

            'set' : setFunction,
            'get' : getFunction,
            'del' : delFunction

        }[ctx.invoked_with.lower()](

            ctx = ctx,
            pKey = pKey,
            pValue = pValue,
            pAction = pAction,
            pData = jsonLoad(pFile = f'{gDirectory}/setting.json')

        )

        # >

    # >


# main <
if (__name__ == '__main__'): fenaverat.run(discordToken)

# >
