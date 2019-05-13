""" run_bot """
import sys
from datetime import datetime, date
import asyncio
import discord

from lib import atcoder

class AtCoderClient(discord.Client):
    """ AtCoderClient """
    def __init__(self, channel_id):
        super().__init__()
        self._channel_id = channel_id
        self._last_get_minute = datetime.now().strftime("%M")
        self._last_get_day = date.today()

    async def _send_contest_plan(self, channel):
        """ _send_contest_plan """
        today = date.today().strftime("%Y-%m-%d")
        today_contests = []
        contest_plan = atcoder.get_contest_plan()
        # Format message of future contests
        msg = '予定されたコンテストは以下です\n'
        for contest in contest_plan:
            msg += f"> {contest['time']}  {contest['name']}  Rate対象: {contest['rate']}\n"
            if today in contest['time']:
                today_contests.append(contest)
        # Format massage of today contests
        if today_contests:
            msg = f"本日開催のコンテストがあります！！\n\n" + msg
        else:
            msg = f"本日開催のコンテストはありません\n\n" + msg
        # Send message to channel
        await channel.send(msg)

    async def _schedule_send_everyday(self, channel):
        """ _schedule_send_everyday """
        while True:
            today = date.today()
            if today != self._last_get_day:
                await self._send_contest_plan(channel)
                self._last_get_day = today
            await asyncio.sleep(1)

    async def on_ready(self):
        """ on_ready """
        print('on ready')
        channel = self.get_channel(self._channel_id)
        asyncio.ensure_future(self._schedule_send_everyday(channel))

    async def on_message(self, message):
        """ on_message """
        # API 'get contest'
        if message.content.startswith("get contest"):
            await self._send_contest_plan(message.channel)

def main():
    """ main """
    # Check argument
    args = sys.argv
    if len(args) != 3:
        print(f'[ERROR] Usage: python {__file__} <token> <channel id>', file=sys.stderr)
        sys.exit(1)

    token = args[1]
    channel_id = int(args[2])
    # Run bot
    ac_cli = AtCoderClient(channel_id)
    ac_cli.run(token)

if __name__ == '__main__':
    main()
