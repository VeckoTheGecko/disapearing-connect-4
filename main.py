"""
A spin on connect 4 where the only tokens you can see are the last 2 placed, all other tokens are grey.
A game of simple strategy just got a new challenge: memory!

This code was originally written by me a couple years ago, however I wanted to refactor it using MVC architecture.
"""

import pygame
import os

from model import Model
from view import View
from controller import Controller

if __name__ == "__main__":
    view = View(200, 400)
    controller = Controller(model=Model(), view=View())
    input()
