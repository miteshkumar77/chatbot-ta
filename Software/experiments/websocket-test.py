# Requires environment variable WEBEX_TEAMS_ACCESS_TOKEN to be valid. Get a
# token by creating a new bot (or regenerating one for an existing bot) at
# https://developer.webex.com/my-apps/
#
# To use the bot, run this script, go to the Webex app, search for your bot's
# username (some-name@webex.bot), and send it "help" or "echo".

from webex_bot.webex_bot import WebexBot # pip install webex_bot
import os

bot = WebexBot(
    teams_bot_token=os.getenv('WEBEX_TEAMS_ACCESS_TOKEN'),
    approved_users=[''], # Workaround for bug in webex_bot approval checking: if
                         # approved_users empty, approved_domains is not checked
    approved_domains=['rpi.edu']) # Bot only responds to msg from these domains
bot.run()
