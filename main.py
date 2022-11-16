# Project Skotak by Alex Arbuckle #


# import <
from github import Github
from discord import Intents
from discord.ext import commands
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


# main <
if (__name__ == '__main__'): skotak.run(discordToken)

# >
