# Project Skotak by Alex Arbuckle #


# import <
from github import Github
from asyncio import sleep
from discord import Intents
from discord.ext import commands
from datetime import datetime as dt
from lxRbckl import githubSet, githubGet, requestsGet

# >


# token <
# global <
githubToken = ''
discordToken = ''

gFile = 'setting.json'
gGithub = Github(githubToken)
gRepository = 'lxRbckl/Project-Skotak'
skotak = commands.Bot(command_prefix = '', intents = Intents.all())
gSettingLink = 'https://github.com/lxRbckl/Project-Skotak/raw/main/setting.json'

# >


async def setFunction(

        ctx,
        pKey: str = None,
        pValue: str = None,
        pElement: str = None,
        pSetting: dict = None

):
    '''  '''

    # set <
    if (isinstance(pSetting[pKey], int)): pSetting[pKey] = int(pValue); return True
    elif (isinstance(pSetting[pKey], list)): pSetting[pKey].append(pValue); return True
    elif (isinstance(pSetting[pKey], dict)): pSetting[pKey][pValue].append(pElement); return True

    # >


async def getFunction(

        ctx,
        pKey: str = None,
        pValue: str = None,
        pElement: str = None,
        pSetting: dict = None

):
    '''  '''

    # get <
    # send <
    if (not pKey): content = '\n'.join(pSetting.keys())
    elif (isinstance(pSetting[pKey], int)): content = pSetting[pKey]
    elif (isinstance(pSetting[pKey], list)): content = '\n'.join(pSetting[pKey])
    elif (isinstance(pSetting[pKey], dict)): content = '\n'.join(pSetting[pKey][pValue])

    await ctx.channel.send(

        delete_after = 60,
        content = f'`{content}`'

    ) if (content) else None

    # >

    return False


async def delFunction(

        ctx,
        pKey: str = None,
        pValue: str = None,
        pElement: str = None,
        pSetting: dict = None

):
    '''  '''

    # delete <
    if (isinstance(pSetting[pKey], list)): pSetting[pKey].remove(pValue); return True
    elif (isinstance(pSetting[pKey], dict)): pSetting[pKey][pValue].remove(pElement); return True

    # >


@commands.has_permissions(administrator = True)
@skotak.command(aliases = requestsGet(pLink = gSettingLink)['aliases'])
async def functionCommand(

        ctx,
        pKey: str = None,
        pValue: str = None,
        pElement: str = None

):
    '''  '''

    # set (setting)
    # get (bSetting) <
    setting = githubGet(

        pFile = gFile,
        pGithub = gGithub,
        pRepository = gRepository

    )
    bSetting = await {

        'set' : setFunction,
        'get' : getFunction,
        'del' : delFunction

    }[ctx.invoked_with.lower()](

        ctx = ctx,
        pKey = pKey,
        pValue = pValue,
        pSetting = setting,
        pElement = pElement

    )

    # >

    # if (update) <
    if (bSetting):

        githubSet(

            pFile = gFile,
            pData = setting,
            pGithub = gGithub,
            pRepository = gRepository

        )

    # >


@skotak.event
async def on_ready():
    '''  '''

    # set (aData) <
    # while (running) <
    aData = {}
    while (True):

        # set (data, setting) <
        # iterate (repository) <
        setting = requestsGet(pLink = gSettingLink)
        bData = {'topic' : setting['topic']['add'], 'language' : setting['language']['add']}
        for r in [r for u in setting['user']['add'] for r in gGithub.get_user(u).get_repos()]:

            # if (included project) <
            if (r.full_name.split('/')[1] not in setting['project']['remove']):

                # get feed <
                # add repository <
                try:

                    feed = githubGet(

                        pGithub = gGithub,
                        pFile = 'feed.json',
                        pRepository = r.full_name

                    )['feed']

                except: feed = None

                bData[r.full_name.split('/')[1]] = {

                    'projectLink' : f'https://github.com/{r.full_name}',
                    'description' : r.description if (r.description) else 'None',
                    'feedSubject' : list(feed['content'].keys()) if (feed) else [],
                    'topic' : [t for t in r.get_topics() if (t not in setting['topic']['remove'])],
                    'update' : dt.strptime(str(r.pushed_at).split(' ')[0], '%Y-%m-%d').strftime('%B %d %Y'),
                    'language' : [l for l in r.get_languages().keys() if (l not in setting['language']['remove'])],
                    'feedLink' : f'https://raw.githubusercontent.com/{r.full_name}/main/feed.json' if (feed) else 'None'

                }

                # >

            # >

        # >

        # if (change) <
        # sleep <
        if (aData != bData):

            githubSet(

                pData = bData,
                pGithub = gGithub,
                pFile = 'data.json',
                pRepository = gRepository,

            )
            aData = bData

        await sleep(60 * setting['interval'])

        # >

    # >


# main <
if (__name__ == '__main__'): skotak.run(discordToken)

# >
