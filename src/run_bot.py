""" run_bot """
import sys
import discord

from lib import atcoder

class AtCoderClient(discord.Client):
    """ AtCoderClient """

    async def on_ready(self):
        """ on_ready """

        print('on ready')

    async def on_message(self, message):
        """ on_message """
        # API 'get contest'
        if message.content.startswith("get contest"):
            contest_plan = atcoder.get_contest_plan()
            # Send message to channel
            msg = '予定されたコンテストは以下です'
            for contest in contest_plan:
                msg += f"\n> {contest['time']}  {contest['name']}  Rate対象: {contest['rate']}"
            await message.channel.send(msg)

def main():
    """ main """
    # Check argument
    args = sys.argv
    if len(args) != 2:
        print(f'[ERROR] Usage: python {__file__} <bot token>', file=sys.stderr)
        sys.exit(1)

    token = args[1]
    # Run bot
    ac_cli = AtCoderClient()
    ac_cli.run(token)

if __name__ == '__main__':
    main()
