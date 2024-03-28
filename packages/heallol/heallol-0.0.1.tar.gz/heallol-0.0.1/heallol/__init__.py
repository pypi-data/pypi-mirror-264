"""
heal.lol
~~~~~~
API wrapper for the Heal API.

Copyright (c) 2024, aiokev

Licensed under GPL-3.0
"""

__version__ = "0.0.1"
__title__ = "heallol"
__author__ = "aiokev"
__license__ = "GPL-3.0"
__copyright__ = "Copyright (c) 2024, aiokev"

from heallol.tiktok import TikTok


class New:
    """
    This class represents a Heal object.
    """

    def __init__(self, token: str):
        self.token = token
        self.tiktok = TikTok(self.token)
