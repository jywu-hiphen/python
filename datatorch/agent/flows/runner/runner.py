import os
import asyncio

from typing import Awaitable
from ..template import render


class Runner(object):
    def __init__(self, config, action):
        self.config = config
        self.action = action
        self.original_wd = os.getcwd()

    async def run(self, inputs: dict = {}):
        self.inputs = inputs
        return await self.execute()

    async def execute(self) -> Awaitable[dict]:
        raise NotImplementedError("This method must be implemented.")

    def action_dir(self):
        """ Changes the current work directory to the actions directory. """
        os.chdir(self.action.dir)

    def original_dir(self):
        """ Changes the current work directory back to the original. """
        os.chdir(self.original_wd)

    async def run_cmd(self, command: str, wait=True):
        process = await asyncio.create_subprocess_shell(
            command, shell=True, stdout=asyncio.subprocess.PIPE
        )
        if wait:
            await process.wait()
        return process

    def get(self, key, default=None):
        """ Gets a string from config and renders templating. """
        return self.template(self.config.get(key, default), {"input": self.inputs})

    def template(self, string, variables={}) -> str:
        return render(string, variables or {})
