import discord
from discord.ext import tasks, commands
import json
from datetime import time
from zoneinfo import ZoneInfo

DATA_FILE = "user_tasks.json"

USER_ID = 409121437786308621

class DailySummary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_daily_summary.start()

    def cog_unload(self):
        self.send_daily_summary.cancel()

    @tasks.loop(time=time(hour=8, minute=0, tzinfo=ZoneInfo("America/New_York")))
    async def send_daily_summary(self):
        await self.bot.wait_until_ready()

        user = self.bot.fetch_user(USER_ID)

        if not user:
            print("Could not find the specified user.")
            return

        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        except Exception as e:
            return

        user_id = str(USER_ID)

        if user_id not in data or not data[user_id]["tasks"]:
            return

        tasks_dict = data[user_id]["tasks"]
        sorted_task_ids = sorted(tasks_dict.keys(), key=int)

        description_string = ""
        for i, task_id in enumerate(sorted_task_ids, 1):
            description_string += f"**{i}.** {tasks_dict[task_id]}\n"

        embed = discord.Embed(
            title="Your Daily Task Summary",
            description=description_string,
            color=discord.Color.gold()
        )

        # Send the embed as a Direct Message (DM)
        await user.send(embed=embed)
        print("Daily task summary sent successfully.")

def setup(bot):
    bot.add_cog(DailySummary(bot))


