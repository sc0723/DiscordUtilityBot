import discord
from discord.ext import commands
import json

from discord.ext.commands import TextChannelConverter

class TaskManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="add_task", description="Adds a task", guild_ids=["741731955434848407"])
    async def add_task(self, ctx, *, task: str):
        '''
        :param ctx:
        :param task:
        :return: Send message saying task was successfully added or there was an error thrown
        '''
        file_name = "user_tasks.json"
        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
        except Exception as e:
            data = {}
        user_id = str(ctx.author.id)
        if user_id not in data:
            data[user_id] = {"last_id": 0, "tasks": {}}
        new_task_id = data[user_id]["last_id"] + 1
        data[user_id]["last_id"] = new_task_id

        data[user_id]["tasks"][str(new_task_id)] = task
        display_task_number = len(data[user_id]["tasks"])


        try:
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error writing to JSON: {e}")

        await ctx.respond(f"✅ Task #{display_task_number} added: `{task}`", ephemeral=True)

    @commands.slash_command(name="finish_task", description="Removes a task", guild_ids=["741731955434848407"])
    async def finish_task(self, ctx, *, task_number: int):
        '''
        :param ctx:
        :param task_number:
        :return: Sends message that task has been removed or there was a certain error
        '''
        file_name = "user_tasks.json"
        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
        except Exception as e:
            await ctx.respond(f"Error getting data to remove task", ephemeral=True)
            return

        user_id = str(ctx.author.id)
        if user_id not in data or not data[user_id]["tasks"]:
            await ctx.respond(f"{user_id} does not have any tasks", ephemeral=True)
            return
        task_list = data[user_id]["tasks"]

        sorted_task_list = sorted(task_list.keys(), key=int)

        if 1 <= task_number <= len(sorted_task_list):
            task_to_delete = sorted_task_list[task_number - 1]
        else:
            await ctx.respond(f"❌ Invalid task number. Please enter a number between 1 and {len(sorted_task_list)}.",
                              ephemeral=True)
            return

        removed_task_description = task_list.pop(task_to_delete)

        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.respond(f"✔️ Great job! Completed: `{removed_task_description}`", ephemeral=True)

    @commands.slash_command(name="show_tasks", desciption="Displays all current tasks", guild_ids=["741731955434848407"])
    async def show_tasks(self, ctx):
        file_name = "user_tasks.json"
        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
        except Exception as e:
            await ctx.respond(f"Error getting data to remove task", ephemeral=True)
            return

        user_id = str(ctx.author.id)
        if user_id not in data or not data[user_id]["tasks"]:
            await ctx.respond("🎉 You have no tasks! Enjoy your free time.", ephemeral=True)
            return

        tasks_dict = data[user_id]["tasks"]

        sorted_tasks = sorted(tasks_dict.keys(), key=int)
        description_string = ""
        display_num = 1

        for task in sorted_tasks:
            task_description = tasks_dict[task]
            description_string += f"**{display_num}.** {task_description}\n"
            display_num += 1

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s To-Do List",
            description=description_string,
            color=discord.Color.blurple()
        )

        embed.set_footer(text="Use /finish_task <number> to complete a task.")
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(TaskManager(bot))