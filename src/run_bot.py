""" run_bot """
import sys
import datetime
import schedule
import discord

from lib import atcoder


class AtCoderClient(discord.Client):
    """ AtCoderClient """
    @staticmethod
    async def _send_contest_plan(channel):
        """ _send_contest_plan """
        today = datetime.date.today().strftime("%Y-%m-%d")
        today_contests = []
        contest_plan = atcoder.get_contest_plan()
        # Format message of future contests
        msg = '予定されたコンテストは以下です'
        for contest in contest_plan:
            msg += f"\n> {contest['time']}  {contest['name']}  Rate対象: {contest['rate']}"
            if today in contest['time']:
                today_contests.append(contest)
        # Format massage of today contests
        if today_contests:
            msg += f"\n\n本日開催のコンテストがあります！！"
            for contest in today_contests:
                msg += f"\n> {contest['time']}  {contest['name']}  Rate対象: {contest['rate']}"
        else:
            msg += f"\n\n本日開催のコンテストはありません"
        # Send message to channel
        await channel.send(msg)

    @staticmethod
    def _schedule_contest():
        """ _schedule_contest """
        schedule.every().day.at("00:00").do(AtCoderClient._send_contest_plan)

    async def on_ready(self):
        """ on_ready """
        print('on ready')
        self._schedule_contest()

    async def on_message(self, message):
        """ on_message """
        # API 'get contest'
        if message.content.startswith("get contest"):
            await self._send_contest_plan(message.channel)

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
