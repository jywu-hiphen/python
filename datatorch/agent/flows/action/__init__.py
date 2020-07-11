from .action import Action

import os
import logging

from typing import Awaitable
from datatorch.api import ApiClient
from datatorch.agent.directory import agent_directory


__all__ = ["Action", "get_action"]


logger = logging.getLogger("datatorch.agent.action")


def _download_action(name, version, uri):
    pass


async def get_action(action: str, agent=None) -> Awaitable[Action]:
    name, version = action.split("@", 1)
    uri = "https://github.com/"

    # Get actions directory
    action_dir = agent_directory.action_dir(name, version)
    folder_exists = os.path.exists(action_dir)

    if folder_exists:
        logger.debug("Action found locally ({}@{}).".format(name, version))
    else:
        logger.debug("Downloading action {}@{}.".format(name, version))
        _download_action(name, version, uri)

    return Action(action, action_dir, agent=agent)


def get_inputs() -> dict:

    return {}